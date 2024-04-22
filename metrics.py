# metrics.py
from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db

metrics = Blueprint('metrics', __name__)


@metrics.route("/show_metrics")
def show_metrics():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Metrics;")
    metrics = cursor.fetchall()
    cursor.close()
    return render_template("metrics_dashboard.html", metrics=metrics)


@metrics.route("/create_metric", methods=['GET', 'POST'])
def create_metric():
    if request.method == 'POST':
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
        return redirect(url_for("metrics.show_metrics"))  # Prefix with 'metrics.'
    else:
        return render_template("create_metric.html")


@metrics.route("/delete_metric/<int:metric_id>")
def delete_metric(metric_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM Metrics WHERE metric_id = %s", (metric_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("metrics.show_metrics"))  # Prefix with 'metrics.'
