import shutil
import sys
from os import environ
from pathlib import Path
from subprocess import Popen


def show_help():
    print(
        """\
Step 1) $ orsj-submit setting
Step 2) $ edit setting.yml
Step 3) $ orsj-submit redis
Step 4) $ export MAIL_USER=XXX
        $ export MAIL_PASSWD=XXX
        $ export SECRET_KEY=XXX
Step 5) $ orsj-submit run
"""
    )


def main():
    if len(sys.argv) <= 1:
        show_help()
        return
    com = sys.argv[1]
    if com == "setting":
        shutil.copyfile(Path(__file__).parent / "setting.yml", "setting.yml")
        print("Edit setting.yml")
    elif com == "redis":
        p = Popen(["redis-server"])
        p.wait()
    elif com == "run":
        from .orsj import app
        from .orsj.views import setting  # noqa

        HOST = environ.get("SERVER_HOST", "0.0.0.0")
        try:
            PORT = int(environ.get("SERVER_PORT", "5000"))
        except ValueError:
            PORT = 5000
        app.config["MAX_CONTENT_LENGTH"] = int(
            environ.get("MAX_CONTENT_LENGTH", "2100200")
        )
        # app.debug = True
        app.run(HOST, PORT)
    else:
        show_help()
