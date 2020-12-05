import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

@app.route("/", methods=['GET'])
def main_view():
    print(os.getcwd())
    return render_template("main_page.html")

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
