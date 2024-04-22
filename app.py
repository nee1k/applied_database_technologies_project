from flask import Flask, render_template, request, redirect, url_for

from db import get_db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("home.html")


@app.route("/show_metrics")
def show_metrics():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Metrics;")
    metrics = cursor.fetchall()
    cursor.close()
    return render_template("metrics_dashboard.html", metrics=metrics)


@app.route("/show_demographics")
def show_demographics():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Demographics;")
    demographics = cursor.fetchall()
    cursor.close()
    return render_template("demographics_dashboard.html", demographics=demographics)


@app.route("/show_geographiclocations")
def show_geographiclocations():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM GeographicLocations;")
    locations = cursor.fetchall()
    cursor.close()
    return render_template("geographiclocations_dashboard.html", locations=locations)


@app.route("/show_sources")
def show_sources():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Sources;")
    sources = cursor.fetchall()
    cursor.close()
    return render_template("sources_dashboard.html", sources=sources)


@app.route("/create_metric")
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


if __name__ == '__main__':
    app.run(debug=True)
