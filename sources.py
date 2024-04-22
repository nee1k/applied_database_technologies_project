# sources.py
from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db

sources = Blueprint('sources', __name__)


@sources.route("/show_sources")
def show_sources():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Sources;")
    sources = cursor.fetchall()
    cursor.close()
    return render_template("sources_dashboard.html", sources=sources)


@sources.route("/create_source", methods=['GET', 'POST'])
def create_source():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO Sources (
                metric_source_desc_label_fn,
                metric_source_desc_label_url_fn
            ) VALUES (%s, %s);
            """,
            [
                request.form["metric_source_desc_label_fn"],
                request.form["metric_source_desc_label_url_fn"]
            ]
        )
        db.commit()
        cursor.close()
        return redirect(url_for("sources.show_sources"))  # Note the Blueprint prefix
    else:
        return render_template("create_source.html")  # Ensure this template exists


@sources.route("/delete_source/<int:source_id>")
def delete_source(source_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM Sources WHERE source_id = %s", (source_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("sources.show_sources"))  # Note the Blueprint prefix
