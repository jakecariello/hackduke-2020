from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main_view():
    return render_template("main_page.html")