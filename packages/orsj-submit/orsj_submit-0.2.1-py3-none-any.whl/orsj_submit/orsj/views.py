"""
Routes and views for the flask application.
"""
import datetime
import os
import re
import time
from collections import defaultdict
from html import escape
from subprocess import call
from unicodedata import normalize

import PyPDF2
from flask import make_response, redirect, request

from . import app
from .util import (
    User,
    article_data,
    authenticated,
    check,
    del_abst,
    del_users,
    exist_user,
    get_abst,
    get_account,
    get_hash,
    get_logs,
    get_signup_request,
    getfilename,
    getname,
    is_member_id,
    load_data,
    load_user,
    load_users,
    logurl,
    make_allpdf,
    move_article,
    rand_str,
    render_ex,
    save_to_file,
    save_user,
    send_mail,
    session,
    set_signup_request,
    unique_key,
)

load_data()
setting = app.setting


@app.route("/robots.txt")
def robots():
    response = make_response()
    response.data = "User-agent: *\nDisallow: /\n"
    response.headers["Content-Type"] = "text/plain"
    return response


@app.route("/")
def home():
    """home page."""
    return render_ex("index.jade", _title=setting.ncon + setting.header)


@app.route("/desc")
def desc():
    """description page."""
    return render_ex("desc.jade", _title="発表申込の流れ")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """signup page."""
    logurl()
    if request.method == "POST":
        key = rand_str(16)
        msg, name, email, _, pw = get_account()
        if msg:
            return render_ex("signup.jade", _title="新規アカウント作成", message=msg)
        hsh = get_hash(pw)
        set_signup_request(key, (name, email, hsh, True))
        url = request.base_url[: request.base_url.rindex("/")] + "/confirm/" + key
        if session.get("user", "") == "admin":
            return redirect(url)
        else:
            body = (
                "次のURLを開いてください\n"
                + request.base_url[: request.base_url.rindex("/")]
                + "/confirm/"
                + key
            )
            send_mail(email, f"Sign upの確認 - {setting.ncon}", body)
            return render_ex("message.jade", _title="メッセージ", message="確認メールを送信しました")
    return render_ex("signup.jade", _title="新規アカウント作成", message="項目を入力してください")


@app.route("/confirm/<string:key>")
def confirm(key):
    """confirm page."""
    logurl()
    signup_request = get_signup_request(key)
    if not signup_request:
        return render_ex("message.jade", _title="メッセージ", message="有効期限切れです．再作成してください")
    name, email, hsh, issignup = signup_request
    if issignup and exist_user(email):
        return render_ex("message.jade", _title="メッセージ", message="すでに登録されています")
    us = load_user(email) or User(None, email, None)
    us.name = name
    us.hash = hsh
    save_user(us)
    save_to_file()
    return render_ex(
        "message.jade",
        _title="メッセージ",
        message=("登録完了しました。ログインしてください。" if issignup else "パスワードを再設定しました"),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """login page."""
    if not load_user("admin").hash:  # adminのパスワードが未設定
        return redirect("/account")
    msg = ""
    if request.method == "POST":
        us = load_user(request.form["email"])
        if us and us.hash == get_hash(request.form["pw"]):
            session["user"] = us.email
            logurl()
            return redirect("/")
        msg = "E-mailまたはパスワードが正しくありません"
    logurl()
    return render_ex("login.jade", _title="ログイン", message=msg)


@app.route("/forget", methods=["GET", "POST"])
def forget():
    """forget page."""
    logurl()
    msg = ""
    if request.method == "POST":
        msg, _, email, _, pw = get_account(None, True)
        if not msg:
            us = load_user(request.form["email"])
            if us:
                hsh = get_hash(pw)
                key = rand_str(16)
                set_signup_request(key, (us.name, email, hsh, False))
                url = request.base_url[: request.base_url.rindex("/")]
                body = "次のURLを開いてください\n" + url + "/confirm/" + key
                send_mail(email, f"Forget passwordの確認 - {setting.ncon}", body)
                return render_ex("message.jade", _title="メッセージ", message="確認メールを送信しました")
            msg = "E-mailが正しくありません"
    return render_ex("forget.jade", _title="パスワードを忘れた場合", message=msg)


@app.route("/logout")
def logout():
    """logout page"""
    logurl()
    session.pop("user")
    return redirect("/")


@app.route("/account", methods=["GET", "POST"])
@authenticated(nouser=True)
def account():
    """account page"""
    msg = ""
    first = False
    us = load_user("admin")
    if not us.hash:
        first = True
        msg = "Set NEW password"
    else:
        us = load_user(session.get("user", ""))
    if not us:
        return redirect("/login")
    if request.method == "POST":
        msg, _, _, opw, pw = get_account(us.hash)
        if not msg:
            us.hash = get_hash(pw)
            save_user(us)
            if first:
                return redirect("/account")
            else:
                return render_ex("message.jade", _title="メッセージ", message="パスワードを変更しました")
    return render_ex(
        "account.jade",
        _title="アカウント",
        name=us.name,
        email=us.email,
        first=first,
        message=msg,
    )


@app.route("/articles", methods=["GET", "POST"])
@authenticated()
def articles(us):
    """articles page"""
    isadmin = us.name == "admin"
    msg = frem = toem = ""
    if isadmin:
        if request.method == "POST":
            ismove = request.form["btn"] == "発表申込オーナー変更"
            users = load_users()
            if ismove:
                frem, toem = request.form["fremail"], request.form["toemail"]
                if not frem or not toem:
                    msg = "Set information"
                    users = []
            for usr in users:
                if not ismove:
                    usr.articles = {
                        k: v for k, v in usr.articles.items() if k not in request.form
                    }
                    save_user(usr)
                else:
                    for k in usr.articles:
                        if k in request.form:
                            move_article(frem, k, toem)
            del_abst()
        articles = [ar for usr in load_users() for ar in usr.articles.values()]
    else:
        if request.method == "POST":
            res = check_expired(us)
            if res[0]:
                return res[1]
            us.articles = {
                k: v for k, v in us.articles.items() if k not in request.form
            }
            save_user(us)
            del_abst()
        articles = us.articles.values()
    return render_ex(
        "articles.jade",
        _title="発表申込一覧",
        message=msg,
        admin=isadmin,
        articles=articles,
        fremail=frem,
        toemail=toem,
    )


def check_expired(us):
    if us.name != "admin" and datetime.datetime.now() > datetime.datetime.strptime(
        setting.expired, "%Y/%m/%d %H:%M"
    ):
        return True, render_ex("message.jade", _title="メッセージ", message="発表申込期限を過ぎています")
    return False, None


@app.route("/submit", methods=["GET", "POST"])
@app.route("/submit/<string:key>", methods=["GET", "POST"])
@authenticated()
def submit(us, key=None):
    """submit page"""
    dc = defaultdict(str)
    if key is not None:
        ar = us.articles.get(key)
        if not ar:
            return redirect("/")
        dc.update(ar)
        dc["change"] = "1"
        dc["_key"] = "/" + key
    else:
        dc["presentation"] = "1"  # 初期設定
        dc["change"] = "0"  # 初期設定
        dc["key"] = unique_key()
    msg = []
    if request.method == "POST":
        res = check_expired(us)
        if res[0]:
            return res[1]
        dc["social_gathering"] = dc["refuse_abst"] = ""
        for k, v in request.form.items():
            dc[k] = escape(v.strip())
        dc["title"] = normalize("NFKC", dc["title"])
        pr = dc["presentation"]
        dc["presenter"] = getname(dc, pr)
        if not dc["presenter"]:
            msg.append("発表者の氏名を設定してください")
        if dc["change"] == "0":  # 差替え
            f = request.files["abstract"]
            dc["file"] = getfilename(f)
        else:
            f = None  # 差替えない場合は、アップロードさせない
        for i in range(1, 6):
            nam = getname(dc, i)
            if (
                nam
                and dc["author%s_type" % i] in ["正会員", "学生会員"]
                and not is_member_id(dc["author%s_id" % i])
            ):
                msg.append("著者%sの会員番号を設定してください" % i)
        if not dc["file"]:
            msg.append("アブストラクト原稿(PDF)を設定してください")
        elif not msg:
            if f and dc["file"]:
                fn = get_abst(dc["key"])
                f.save(fn)
                a = PyPDF2.PdfFileReader(fn)
                if a.isEncrypted:
                    os.remove(fn)
                    msg.append("アブストラクト原稿(PDF)は暗号化しないでください")
                elif not (1 <= a.getNumPages() <= 2):
                    os.remove(fn)
                    msg.append("アブストラクト原稿(PDF)は1または2ページにしてください")
            if not msg:
                dc.update({"name": us.name, "email": us.email})
                us.articles[dc["key"]] = article_data(dc)
                save_user(us)
                save_to_file()
                msg = (
                    f'"{dc["title"]}"を{"更新しました" if key else "申し込みました"}。\n'
                    f"発表申込一覧をご確認ください。\n"
                    f"別途、{setting.ncon}から参加の申込みが必要です。\n"
                    f"{setting.nconurl}"
                )
                if us.name != "admin":
                    send_mail(us.email, f"発表申込受付 - {setting.ncon}", msg)
                    msg = "メールをご確認ください。\n" + msg
                return render_ex("message.jade", _title="発表申込受付", message=msg)
    return render_ex(
        "submit.jade",
        _title="更新" if key else "発表申込",
        dc=dc,
        sessions=setting.sessions,
        keywords=setting.keywords,
        message="\n".join(msg),
    )


@app.route("/summary")
@authenticated(nouser=True, onlyadmin=True)
def summary():
    s, dc1, dc2 = User.summary()
    return render_ex("summary.jade", _title="サマリ", os=os, dc1=dc1, dc2=dc2, message=s)


@app.route("/del_user", methods=["GET", "POST"])
@authenticated(nouser=True, onlyadmin=True)
def del_user():
    users = load_users()
    if request.method == "POST":
        del_users([us.email for us in users if us.email in request.form])
        del_abst()
        save_to_file()
        users = load_users()
    return render_ex(
        "del_user.jade",
        _title="アカウント削除",
        nar={us.email: len(us.articles) for us in users},
        users=[us for us in users if us.name != "admin"],
    )


@app.route("/assign", methods=["GET", "POST"])
@authenticated(nouser=True, onlyadmin=True)
def assign():
    ptn = re.compile(r"\d-[A-Z]-\d")
    msg = ""
    if request.method == "POST":
        dc = dict((s.split() + [""])[:2] for s in request.form["val"].splitlines())
        for us in load_users():
            for k, v in us.articles.items():
                if k in dc and ptn.match(dc[k]):
                    v["assign"] = dc[k]
                us.articles[k] = v
            save_user(us)
        save_to_file()
        msg = "Assigned"
    return render_ex("assign.jade", _title="割付", message=msg)


@app.route("/check")
@authenticated(nouser=True, onlyadmin=True)
def check_():
    msg = ""
    names, tables, ss, sa = check()
    return render_ex(
        "check.jade",
        _title="チェック",
        message=msg,
        names=names,
        tables=tables,
        ss=ss,
        sa=sa,
    )


@app.route("/dl_list")
@authenticated(nouser=True, onlyadmin=True)
def dl_list():
    response = make_response()
    response.data = User.bytedata()
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = "attachment; filename=articles.csv"
    return response


@app.route("/dl_all/")
@authenticated(nouser=True, onlyadmin=True)
def dl_all():
    del_abst()
    save_to_file()
    with open("articles.csv", "wb") as fp:
        fp.write(User.bytedata())
    s, dc1, dc2 = User.summary()
    with open("summary.txt", "w") as fp:
        fp.write(s + "\r\n")
    time.sleep(1)
    response = make_response()
    fn = datetime.datetime.today().strftime("../orsj%y%m%d-%H%M.tgz")
    if os.path.exists(fn):
        os.remove(fn)
        time.sleep(1)
    call(
        [
            "tar",
            "zcf",
            fn,
            "-C",
            "..",
            os.path.basename(os.getcwd()),
            "--exclude",
            "__pycache__",
        ]
    )
    time.sleep(1)
    with open(fn, "rb") as fp:
        response.data = fp.read()
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = "attachment; filename=%s" % fn.lstrip(
        "../"
    )
    return response


@app.route("/dl_allpdf")
@authenticated(nouser=True, onlyadmin=True)
def dl_allpdf():
    fnam = "all.tgz"
    pnam = "../" + fnam
    make_allpdf()
    if not os.path.exists(pnam):
        return render_ex("message.jade", _title="メッセージ", message="エラー")
    response = make_response()
    with open(pnam, "rb") as fp:
        response.data = fp.read()
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = "attachment; filename=" + fnam
    return response


@app.route("/dl_pdf/<string:key>")
def dl_pdf(key):
    logurl()
    us = load_user(session.get("user", ""))
    if not us:
        return redirect("/login")
    if us.name != "admin" and key not in us.articles:
        return render_ex("message.jade", _title="メッセージ", message="見つかりませんでした")
    fn = get_abst(key)
    if not fn or not os.path.exists(fn):
        return redirect("/articles")
    response = make_response()
    with open(fn, "rb") as fp:
        response.data = fp.read()
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = "attachment; filename=%s.pdf" % key
    return response


@app.route("/dl_log/")
@authenticated(nouser=True, onlyadmin=True)
def dl_log():
    response = make_response()
    response.data = "\n".join(get_logs())
    response.headers["Content-Type"] = "text/plain"
    response.headers["Content-Disposition"] = "attachment; filename=orsj.log"
    return response
