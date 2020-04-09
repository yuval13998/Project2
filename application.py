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
        self.time = f"{result.tm_mday}/{result.tm_mon} {result.tm_hour}:{result.tm_min}"
        self.str = f"{self.content}        {self.username} {self.time}"


class Channel():
    posts = []

    def __init__(self, channelname):
        self.channelname = channelname

    def addPost(self, post):
        self.posts.append(post)

channels = []
channelSelected = ""



@app.route("/addChannel")
def addchannel():
    test = Channel("test")

    channels.append(test)
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
    for channel in channels:
        if channelSelected == channel.channelname:
            channel.addPost(post)
    emit("conversation", {"post_content":post.str, "postlen": len(channel.posts)}, broadcast=True)




@app.route("/chat/<string:channelname>")
def chat(channelname):
    for channel in channels:
        if channelname == channel.channelname:
            channelSelected = channelname
            return render_template("chat.html", channel = channel)

@app.route("/posts", methods=["POST"])
def posts():
    return jsonify(channelSelected)
