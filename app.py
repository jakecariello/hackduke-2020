import os
from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sys import platform

app = Flask(__name__)

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')


try:
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]
    # db_host = os.environ["INSTANCE_CONNECTION_NAME"]

    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    cloud_sql_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    # items = [db_user, db_pass, db_name, db_socket_dir, cloud_sql_connection_name]
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock={db_socket_dir}>/{cloud_sql_connection_name}/.s.PGSQL.5432'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}?host=/cloudsql/{cloud_sql_connection_name}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+pg8000://{db_user}:{db_pass}@{db_host}/{db_name}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock=cloudsql/{cloud_sql_connection_name}/.s.PGSQL.5432'
    print(app.config['SQLALCHEMY_DATABASE_URI'])

    # assert all([item is not None for item in items])
    # for item in items:
    #     print(item, flush=True)


except Exception:

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////tmp/test.db'

# This must be set, determine which is best for you
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/", methods=['GET'])
def main_view():
    print(db, flush=True)
    print(db.session.query("T").from_statement(text("SELECT 1")).all(), flush=True)
    return render_template("main_page.html")

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
