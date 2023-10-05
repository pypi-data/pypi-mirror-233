import datetime
import glob
import hashlib
import os
import pickle
import random
import re
import shutil
import string
import subprocess
import time
from collections import defaultdict
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formatdate
from html import unescape
from itertools import groupby
from pathlib import Path
from smtplib import SMTP_SSL
from tempfile import TemporaryFile

import PyPDF2
import redis
import yaml
from flask import render_template, request, session
from pdfformfiller import PdfFormFiller
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from . import app


class FloatObject(PyPDF2.generic.FloatObject):
    def __add__(self, other):
        return self.as_numeric() + other

    def __radd__(self, other):
        return self.as_numeric() + other

    def __sub__(self, other):
        return self.as_numeric() - other

    def __rsub__(self, other):
        return -self.as_numeric() + other


PyPDF2.generic.FloatObject = FloatObject


class Setting(dict):
    def __init__(self, d):
        self.__dict__.update(d)


class User:
    def __init__(self, name, email, hash):
        self.name = name
        self.email = email.lower()
        self.hash = hash
        self.articles = dict()

    @staticmethod
    def row_cols():
        return (
            "name,email,title,presentation,presenter,"
            "author1_last,author1_first,author1_type,author1_id,author1_dep,"
            "author2_last,author2_first,author2_type,author2_id,author2_dep,"
            "author3_last,author3_first,author3_type,author3_id,author3_dep,"
            "author4_last,author4_first,author4_type,author4_id,author4_dep,"
            "author5_last,author5_first,author5_type,author5_id,author5_dep,"
            "session,keyword1,keyword2,file,renamed,assign,page,refuse_abst,"
            "comment\r\n"
        )

    @staticmethod
    def row_data(dc_):
        dc = {k: unescape(v) for k, v in dc_.items()}
        ip = int(dc["presentation"])
        pp = {"p%d" % i: ("※" if i == ip else "") for i in range(1, 6)}
        fnam = dc["file"] or ""
        renamed = dc["key"] if fnam else ""
        page = str(get_page(get_abst(dc["key"]))) if fnam else ""
        refuse_abst = 1 if dc["refuse_abst"] else 0
        com = dc["comment"].replace("\r\n", " ")
        dc.update(
            dict(
                fnam=fnam, renamed=renamed, page=page, refuse_abst=refuse_abst, com=com
            )
        )
        return (
            '"{name}",{email},"{title}",{presentation},{presenter},'
            '{p1}{author1_last},{author1_first},{author1_type},{author1_id},"{author1_dep}",'
            '{p2}{author2_last},{author2_first},{author2_type},{author2_id},"{author2_dep}",'
            '{p3}{author3_last},{author3_first},{author3_type},{author3_id},"{author3_dep}",'
            '{p4}{author4_last},{author4_first},{author4_type},{author4_id},"{author4_dep}",'
            '{p5}{author5_last},{author5_first},{author5_type},{author5_id},"{author5_dep}",'
            '"{session}","{keyword1}","{keyword2}",{fnam},{renamed},{assign},{page},'
            '{refuse_abst},"{com}"'
        ).format(**dc, **pp)

    @staticmethod
    def bytedata():
        """article list"""
        return (
            User.row_cols()
            + "\r\n".join(
                User.row_data(ar) for us in load_users() for ar in us.articles.values()
            )
        ).encode("utf_8_sig")

    @staticmethod
    def summary():
        """summary"""
        dc1, dc2 = defaultdict(int), defaultdict(int)
        for us in load_users():
            for ar in us.articles.values():
                dc1[ar["session"]] += 1
                dc2[ar["keyword1"]] += 1
                if ar["keyword2"]:
                    dc2[ar["keyword2"]] += 1
        mes = "All users = %d All Articles = %d" % (
            len(list_users()) - 1,
            len_articles(),
        )
        return mes, dc1, dc2


def logurl():
    u = request.base_url[len(request.url_root) :]
    if not u:
        return
    nam = "-"
    us = load_user(session.get("user", ""))
    if us:
        nam = us.name
    t = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    add_log("%s %s %s %s" % (t, nam, request.method, u))


def cmpfnc(x):
    xx = (x if isinstance(x, str) else x[0]).split("-")
    return "-".join(xx[:-1] + [str(int(xx[-1]) + 100)])


def make_allpdf():
    lst = []
    for us in load_users():
        for k, ar in us.articles.items():
            ag = ar["assign"]
            if ag:
                lst.append((ag, k))
    lst = sorted(lst, key=cmpfnc)
    # make_lstpdf('../all.pdf', lst)  # 1ファイルで作成
    if os.path.isdir("all"):
        shutil.rmtree("all")
    pfx = app.setting.prefix
    for ag, k in lst:
        dr = "all/" + ag[:3]
        os.makedirs(dr, exist_ok=True)
        make_lstpdf(f"{dr}/{pfx}-{ag}.pdf", [(ag, k)])
    time.sleep(0.1)
    subprocess.run(["tar", "czf", "all.tgz", "all"])


def make_lstpdf(pnam, lst):
    pdfmetrics.registerFont(TTFont("IPAexGothic", "/usr/share/fonts/ipaexg.ttf"))
    sty1 = ParagraphStyle("sty1", fontName="IPAexGothic", fontSize=16)
    sty2 = ParagraphStyle(
        "sty2", alignment=TA_RIGHT, fontName="IPAexGothic", fontSize=9
    )
    pdf = PyPDF2.PdfFileMerger()
    for ag, k in lst:
        ff = PdfFormFiller(get_abst(k))
        p = ff.pdf.getPage(0)
        ff.add_text(ag, 0, (40, 14), (100, 40), sty1)
        ff.add_text(app.setting.orsj, 0, (0, 14), (p.mediaBox[2] - 40, 40), sty2)
        ff.add_text(
            app.setting.year + " " + app.setting.ncon,
            0,
            (0, 24),
            (p.mediaBox[2] - 40, 40),
            sty2,
        )
        n = min(2, ff.pdf.getNumPages())
        with TemporaryFile() as fp:
            ff.write(fp)
            fp.seek(0)
            fr = PyPDF2.PdfFileReader(fp)
            pdf.append(fr, pages=(0, n))
        if n < 2:
            with open(get_abst("empty"), "rb") as fp:
                pdf.append(fp)
    if os.path.exists(pnam):
        os.remove(pnam)
        time.sleep(0.05)
    try:
        pdf.write(pnam)
    except:
        pass


def get_page(f):
    try:
        with open(f, "rb") as fp:
            p = PyPDF2.PdfFileReader(fp)
            return p.getNumPages()
    except:
        return -1


def get_abst(f):
    return str(Path(__file__).parent / "static" / "pdf" / f"{f}.pdf")


def article_data(dc):
    return {
        s: dc[s]
        for s in (
            "name email key file title presentation presenter "
            "author1_last author1_first author1_type author1_id author1_dep "
            "author2_last author2_first author2_type author2_id author2_dep "
            "author3_last author3_first author3_type author3_id author3_dep "
            "author4_last author4_first author4_type author4_id author4_dep "
            "author5_last author5_first author5_type author5_id author5_dep "
            "session keyword1 keyword2 assign refuse_abst comment"
        ).split()
    }


def get_account(pr=None, nocheck=False):
    msg = []
    name = request.form["name"]
    email = request.form["email"].lower()
    opw = ""
    if pr is not None:
        if name != "admin" or pr:
            opw = request.form.get("opw")
            if get_hash(opw) != pr:
                msg.append("Illegal password")
    else:
        if not name or (name == "admin" and app.rds.exists("admin")):
            msg.append("Set name")
        email_ptn = r"[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)+"
        if email == "admin" or not re.match(email_ptn, email):
            msg.append("Set E-mail")
        if not nocheck and exist_user(email):
            msg.append("Already registered")
    pw = request.form["pw"]
    pw2 = request.form["pw2"]
    if pw != pw2:
        msg.append("Password not match")
    if not pw:
        msg.append("Set Password")
    return "\n".join(msg), name, email, opw, pw


def unique_key():
    s = {k for us in load_users() for k in us.articles}
    while True:
        key = rand_str(6)
        if key not in s:
            return key


def send_mail(to, sub, body):
    charset = "ISO-2022-JP"
    msg = MIMEText(body, "plain", charset)
    msg["Subject"] = Header(sub, charset)
    msg["From"] = fr = os.environ.get("MAIL_USER")
    rt = os.environ.get("REPLY_TO")
    if rt:
        msg["Reply-To"] = rt
    msg["To"] = to
    msg["Date"] = formatdate()
    with SMTP_SSL(os.environ.get("SMTP_HOST", "smtp.gmail.com")) as smtp:
        smtp.login(fr, os.environ.get("MAIL_PASSWD"))
        smtp.sendmail(fr, [to], msg.as_string())


def render_ex(file, *args, **kwargs):
    user = session.get("user")
    dc = dict()
    if user:
        us = load_user(user)
        if us:
            dc = {"name": us.name, "email": us.email}
    return render_template(file, *args, setting=app.setting, user=dc, **kwargs)


def authenticated(nouser=False, onlyadmin=False):
    def useronly(func):
        class Func:
            def __init__(self, func, nouser, onlyadmin):
                self.func = func
                self.nouser = nouser
                self.onlyadmin = onlyadmin
                self.__name__ = func.__name__

            def __call__(self, *args, **kwargs):
                if not load_user("admin").hash:
                    us = "admin"
                else:
                    us = session.get("user", "")
                if not us or (onlyadmin and us != "admin"):
                    return render_ex(
                        "login.jade", _title="Login", message="Please login"
                    )
                logurl()
                if nouser:
                    return func(*args, **kwargs)
                return func(load_user(us), *args, **kwargs)

        return Func(func, nouser, onlyadmin)

    return useronly


def del_abst():
    dc = {get_abst(k) for us in load_users() for k in us.articles}
    for f in glob.glob(get_abst("*")):
        if f not in dc:
            os.remove(f)


def len_articles():
    return sum(len(us.articles) for us in load_users())


def getfilename(f):
    if not f:
        return None
    from werkzeug.utils import secure_filename

    fn = secure_filename(f.filename)
    if fn.lower() == "pdf":
        fn = "_.pdf"
    return fn if fn.lower().endswith(".pdf") else None


def getname(dc, i):
    la = dc["author%s_last" % i]
    fr = dc["author%s_first" % i]
    return " ".join(s for s in [la, fr] if s)


def is_member_id(s):
    if not str.isdigit(s):
        return False
    n = int(s)
    return 1000000 <= n <= 10000000


def get_hash(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def rand_str(n):
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    )


def load_data():
    with open("setting.yml", encoding="utf8") as fp:
        app.setting = Setting(yaml.safe_load(fp))
        app.rds = redis.StrictRedis()
    load_users()


def load_users():
    if not app.rds.exists("admin"):
        save_user(User("admin", "admin", ""))
        app.rds.save()
    return [pickle.loads(app.rds.get(k)) for k in list_users()]


def load_user(s):
    b = app.rds.get(s.lower())
    return pickle.loads(b) if b else None


def save_to_file():
    app.rds.save()


def save_user(u):
    app.rds.set(u.email, pickle.dumps(u))


def del_users(ss):
    for s in ss:
        app.rds.delete(s)


def exist_user(s):
    return app.rds.exists(s)


def list_users():
    return [k for k in app.rds.keys() if not k.startswith(b"$")]


def get_signup_request(k):
    b = app.rds.get("$signup_" + k)
    return pickle.loads(b) if b else None


def set_signup_request(k, v):
    app.rds.setex("$signup_" + k, 1800, pickle.dumps(v))


def add_log(s):
    app.rds.rpush("$log", s)


def get_logs():
    return [s.decode() for s in app.rds.lrange("$log", 0, -1)]


def move_article(fr, ky, to):
    ufr = pickle.loads(app.rds.get(fr) or b"\x80\x03N.")
    ar = ufr.articles.get(ky, None) if ufr else None
    uto = pickle.loads(app.rds.get(to) or b"\x80\x03N.")
    if not ufr or not ar or not uto or ky not in ufr.articles or ky in uto.articles:
        return False
    ar["email"] = to
    uto.articles[ky] = ar
    del ufr.articles[ky]
    app.rds.set(fr, pickle.dumps(ufr))
    app.rds.set(to, pickle.dumps(uto))
    return True


def isseq(ll):
    return all(isseq2(list(v)) for k, v in groupby(ll, lambda l: l[0]))


def isseq2(ll):
    return all(l[2] == ll[0][2] for l in ll)


def check():
    dc1, dc2, dc3, dc4, ss, sa = {}, defaultdict(list), set(), set(), [], []
    for us in load_users():
        for ar in us.articles.values():
            tt, ag = ar["title"], ar["assign"]
            if ag:
                pr = int(ar["presentation"])
                for i in range(1, 6):
                    s = getname(ar, i)
                    if i == pr:
                        t = ar["author%d_dep" % i]
                        dc1[ag] = "%s<br><strong>%s</strong> %s" % (ar["title"], s, t)
                    if s:
                        dc2[s].append(("%s%s" % ("*" if i == pr else "", ag),))
            if tt in dc3:
                ss.append(tt)
            dc3.add(tt)
            if ag and ag in dc4:
                sa.append(ag)
            dc4.add(ag)
    i, lst = 0, []
    for k, v in dc2.items():
        v = [s[0] for s in sorted(v, key=cmpfnc)]
        if len(v) > 1 and not isseq(s.lstrip("*") for s in v):
            lst.append((i, k, ", ".join(v)))
            i += 1
    rms, tms = set(), set()
    for k, _ in dc1.items():
        rms.add(k[2])
        tms.add(k[:2] + k[4:])
    rms = sorted(rms)
    tbl = [[""] + rms]
    for tm in sorted(tms, key=cmpfnc):
        tbl.append([tm] + [dc1.get(tm[:2] + rm + tm[1:], "") for rm in rms])
    return lst, tbl, ss, sa
