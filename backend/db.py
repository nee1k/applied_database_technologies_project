import mysql.connector

from flask import g


def get_db():
    if "db" not in g or not g.db.is_connected():
        # connect to the database
        g.db = mysql.connector.connect(
            host="ryvdxs57afyjk41z.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
            user="fgn6003omv8blkav",
            passwd="d1i4jrvuc1mazbyz",
            db="s7kc8cqsfabbmu4f",
            port=3306
            # ssl_verify_identity=True,
            # ssl_ca="C:\ssl\certs\cacert.pem"
        )

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        # close the database
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
