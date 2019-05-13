from check50 import *
from functools import wraps
import subprocess
import os

def helper(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "app"):
            self.app = self.flask(Survey.APP)
        return f(self, *args, **kwargs)
    return wrapper


def unpack(filename):
    p = subprocess.call(["unzip", filename])


def goto(filename):
    contents = os.listdir(".")

    # Traverse through dir until  is found
    while "filename.py" not in contents:
        dirs = [c for c in contents if not c.startswith(".") and os.path.isdir(c)]
        if len(dirs) == 1:
            os.chdir(dirs[0])
            contents = os.listdir(".")
        else:
            return False

    return True

ZIPNAME = "survey.zip"

REQUIRED = ["application.py",
            "templates/layout.html",
            "templates/form.html",
            "templates/error.html",
            "static/styles.css"]


class Survey(Checks):

    APP = "application.py"


    @helper
    def get_content(self, route, tag="input"):
        content = self.app.get(route).content()
        return content.find_all(tag)


    @check()
    def exists(self):
        """application.py exists"""
        if ZIPNAME in os.listdir("."):
            unpack(ZIPNAME)
            goto(REQUIRED[0])

        self.require(*required)


    @check("exists")
    def startup(self):
        """application starts up"""
        self.flask(Survey.APP).get("/").status(200)


    @check("startup")
    def has_form(self):
        """has form"""

        if len(self.get_content("/", "form")) < 1:
            raise Error("expected form element")


    @check("has_form")
    def has_text_fields(self):
        """has one or more text fields"""

        form = self.get_content("/", "form")[0]
        if len(form.find_all("textarea")):
            return

        inputs = form.find_all("input")
        types = [
            "date", "datetime-local", "email", "month", "number", "password",
            "search", "tel", "text", "time", "url", "week"
        ]

        if any((e.attrs["type"] in types for e in inputs)):
            return

        raise Error("expected at least one text input")


    @check("has_form")
    def has_checkbox_or_radio_buttons(self):
        """has one or more checkboxes or two or more radio buttons"""

        inputs = self.get_content("/", "form")[0].find_all("input")
        if len(tuple(filter(lambda e: e.attrs["type"] == "checkbox", inputs))) < 1 and \
            len(tuple(filter(lambda e: e.attrs["type"] == "radio", inputs))) < 2:
            raise Error("expected at least one checkbox or two radio buttons")


    @check("has_form")
    def has_select_and_options(self):
        """has one or more select menus, each with two or more options"""

        selects = self.get_content("/", "form")[0].find_all("select")
        if len(selects) < 1 or \
            any((len(select.find_all("option")) < 2 for select in selects)):
            raise Error("expected one or more select menus, each with two or more options")
