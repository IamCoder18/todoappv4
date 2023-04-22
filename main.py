from flask import Flask, render_template, request, redirect
from firebase import firebase
from random import randrange

app = Flask(__name__, static_url_path='', static_folder='static')
firebase = firebase.FirebaseApplication("https://to-do-app-v4-default-rtdb.firebaseio.com/", None)

class user:
    curr_user = 000000

    def user(self):
        return self.curr_user

    def setUser(self, user):
        self.curr_user = user

    def getUsername(self):
        try:
            fbitems = firebase.get(f"Users", "")
            val = list(fbitems.values())
            for key in fbitems.keys():
                if list(fbitems[key].values())[0] == self.curr_user:
                    return list(fbitems[key].values())[3]
        except Exception as e:
            pass

    def getStatus(self):
        try:
            fbitems = firebase.get(f"Users", "")
            val = list(fbitems.values())
            for key in fbitems.keys():
                if list(fbitems[key].values())[0] == self.curr_user:
                    return list(fbitems[key].values())[2]
        except Exception as e:
            pass

user = user()

def removeItem(item):
    try:
        fbitems = firebase.get(f"{user.user()}/Todo", "")
        val = list(fbitems.values())
        lst = []
        for key in fbitems.keys():
            if list(fbitems[key].values())[0] == item:
                firebase.delete(f"{user.user()}/Todo", key)
    except Exception as e:
        pass
def addItem(item):
    try:
        if item != "" or item != " ":
            firebase.post(f'{user.user()}/Todo', {"item": item})
    except Exception as e:
        pass
def getItems():
    try:
        fbitems = firebase.get(f"{user.user()}/Todo", "")
        val = list(fbitems.values())
        lst = []
        for key in fbitems.keys():
            lst.append(list(fbitems[key].values())[0])
        return lst
    except AttributeError:
        return ["Add A Task"]
def rename(item, newitem):
    try:
        fbitems = firebase.get(f"{user.user()}/Todo", "")
        val = list(fbitems.values())
        lst = []
        for key in fbitems.keys():
            if list(fbitems[key].values())[0] == item:
                firebase.put(f"{user.user()}/Todo/{key}", "item", newitem)
    except Exception as e:
        pass

def checkLogin(usr, pwd):
    fbitems = firebase.get(f"Users", "")
    val = list(fbitems.values())
    lst = []
    for key in fbitems.keys():
        try:
            if list(fbitems[key].values())[3] == usr:
                if list(fbitems[key].values())[1] == pwd:
                    user.setUser(list(fbitems[key].values())[0])
                    return ["loged in", user.user()]
        except Exception as e:
            return "wrong user or pwd"
def signUp(usr, pwd):
    try:
        user.setUser(randrange(100000, 999999))
        fbitems = firebase.get(f"Users", "")
        val = list(fbitems.values())
        lst = []
        for key in fbitems.keys():
            if user.user() == list(fbitems[key].values())[0]:
                if list(fbitems[key].values())[3] == usr:
                    if list(fbitems[key].values())[1] == pwd:
                        return "login"
                return "duplicate"
            else:
                firebase.post('Users', {"status": "free", "username": usr, "password": pwd, "id": user.user()})
                return "done"
    except Exception as e:
        pass

@app.route("/", methods=["GET", "POST"])
def home():
    if user.user() == 000000:
        return redirect("/login")
    if request.method == "POST":
        req = request.form
        task = req.get("task")
        renameTask = req.get("rename-task")
        if req.get("hid") == "remove":
            removeItem(task)
        if req.get("hid") == "logout":
            user.setUser(000000)
        if req.get("hid") == "add":
            addItem(task)
        if req.get("hid") == "rename":
            rename(task, renameTask)
        if req.get("hid") == "avatar":
            return render_template("home.html", items=len(getItems()), todo=getItems(), username=user.getUsername(), status=user.getStatus(), avatar="yes")
        return redirect(location="/success")
    return render_template("home.html", items=len(getItems()), todo=getItems(), username=user.getUsername(), status=user.getStatus(), avatar="no")

@app.route("/success", methods=["GET", "POST"])
def success():
    return redirect(location="/")

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            req = request.form
            username = req.get("username")
            pwd = req.get("pwd")
            if checkLogin(username, pwd)[0] == "loged in":
                user.setUser(checkLogin(username, pwd)[1])
                return redirect(location="/")
            else:
                return render_template("login.html", incorrect="yes")
        return render_template("login.html", incorrect="no")
    except Exception as e:
        return render_template("login.html", incorrect="yes")

@app.route("/signUp", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        req = request.form
        username = req.get("username")
        pwd = req.get("pwd")
        status = signUp(username, pwd)
        if status == "done":
            return redirect(location="/")
        if status == "login":
            return render_template("signUp.html", status="login")
        if status == "duplicate":
            signUp(usr, pwd)
    return render_template("signUp.html", status="")


if __name__ == "__main__":
    app.run(debug=True)