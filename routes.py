from flask import abort, Blueprint, redirect, request, render_template, url_for
from .db import get_db
import random
import string

main = Blueprint("main", __name__)


@main.get("/")
def home():
    return render_template("home.html")


@main.get("/show_metrics")
def show_metrics():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Metrics;")
    metrics = cursor.fetchall()
    cursor.close()
    return render_template("metrics_dashboard.html", metrics=metrics)


@main.post("/create_metric")
def create_metric():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        INSERT INTO Metrics (
            metric_item_label,
            metric_cat_label,
            metric_subcat_label,
            metric_item_label_subtitle,
            metric_cat_item_yaxis_label
        ) VALUES (%s, %s, %s, %s, %s);
        """,
        [
            request.form["metric_item_label"],
            request.form["metric_cat_label"],
            request.form["metric_subcat_label"],
            request.form["metric_item_label_subtitle"],
            request.form["metric_cat_item_yaxis_label"]
        ]
    )
    db.commit()
    cursor.close()
    return redirect(url_for("main.index"))


@main.get("/delete_metric/<int:metric_id>")
def delete_metric(metric_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT 1 FROM Metrics WHERE metric_id = %s;",
        [metric_id]
    )
    metric = cursor.fetchone()

    if not metric:
        cursor.close()
        abort(404)

    cursor.execute(
        "DELETE FROM metrics WHERE metric_id = %s",
        [metric_id]
    )
    db.commit()
    cursor.close()
    return redirect(url_for("main.index"))


@main.get("/show_demographics")
def show_demographics():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Demographics;")
    demographics = cursor.fetchall()
    cursor.close()
    return render_template("demographics_dashboard.html", demographics=demographics)


@main.post("/create_demographics")
def create_demographics():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        INSERT INTO Demographics (
            strata_race_label, strata_sex_label, strata_race_sex_label
        ) VALUES (%s, %s, %s);
        """,
        [
            request.form["strata_race_label"],
            request.form["strata_sex_label"],
            request.form["strata_race_sex_label"]
        ]
    )
    db.commit()
    cursor.close()
    return redirect(url_for("main.index"))


@main.get("/delete_demographics/<int:demographic_id>")
def delete_demographic(demographic_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT 1 FROM demographics WHERE demographic_id = %s;",
        [demographic_id]
    )
    metric = cursor.fetchone()

    if not metric:
        cursor.close()
        abort(404)

    cursor.execute(
        "DELETE FROM demographics WHERE demographic_id = %s",
        [demographic_id]
    )
    db.commit()
    cursor.close()
    return redirect(url_for("main.index"))


@main.get("/show_geographiclocations")
def show_geographiclocations():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM GeographicLocations;")
    locations = cursor.fetchall()
    cursor.close()
    return render_template("geographiclocations_dashboard.html", locations=locations)


@main.get("/show_sources")
def show_sources():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Sources;")
    sources = cursor.fetchall()
    cursor.close()
    return render_template("sources_dashboard.html", sources=sources)
