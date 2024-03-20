from flask import Blueprint

UI = Blueprint(__name__ ,"home")


@UI.route("/")
def home():
    return "home page" 