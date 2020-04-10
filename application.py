import os
import requests

from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
from flask_socketio import SocketIO, emit
from time import time, localtime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
app.config["SECRET_KEY"] = "HakomonA"


class Post():

    def __init__(self, content):
        self.content = content
        self.username = session["username"]
        realtime = time()
        result = localtime(realtime)
        min = result.tm_min
        if result.tm_min < 10:
            min = f"0{result.tm_min}"
        self.time = f"{result.tm_mday}/{result.tm_mon} {result.tm_hour}:{min}"
        self.str = f"{self.content}        {self.username} {self.time}"


class Channel():

    def __init__(self, channelname):
        self.channelname = channelname
        self.posts = []

    def addPost(self, post):
        self.posts.append(post)

test = Channel("test")
test1 = Channel("test1")
channels = [test,test1]
channelselected = {"channel": None}



@app.route("/logout")
def addchannel():
    session["username"] = None
    return render_template("homepage.html")


@app.route("/", methods=["GET","POST"])
def index():
    if(request.method == "GET"):
        return render_template("homepage.html")
    username = request.form.get("username")
    session["username"] = username
    return render_template("homepage.html")


@socketio.on("add post")
def newpost(data):
    content = data["content"]
    post = Post(content)
    if channelselected["channel"] != None:
        channelselected["channel"].addPost(post)
    emit("conversation", {"post_content":post.str}, broadcast=True)


@app.route("/creatChannel", methods=["POST", "GET"])
def channelcreate():
    if request.method == "GET":
        return render_template("creatChannel.html")
    newchannelname = request.form.get("newname")
    newchannel = Channel(newchannelname)
    channels.append(newchannel)
    return render_template("chat.html", channel = newchannel)

@app.route("/posts", methods=["POST"])
def posts():
    return jsonify(channelSelected)

@app.route("/selectchannel", methods=["POST", "GET"])
def selected():
    if request.method == "GET":
        return render_template("selectchannel.html", channels = channels)
    selected = request.form.get("selectchannel")
    for channel in channels:
        if selected == channel.channelname:
            channelselected["channel"] = channel
            return render_template("chat.html", channel = channel)
