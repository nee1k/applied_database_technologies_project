# demographics.py
from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db

demographics = Blueprint('demographics', __name__)


@demographics.route("/show_demographics")
def show_demographics():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Demographics;")
    demographics = cursor.fetchall()
    cursor.close()
    return render_template("demographics_dashboard.html", demographics=demographics)


@demographics.route("/create_demographic", methods=['GET', 'POST'])
def create_demographic():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO Demographics (
                strata_race_label,
                strata_sex_label,
                strata_race_sex_label
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
        return redirect(url_for("demographics.show_demographics"))  # Note the Blueprint prefix
    else:
        return render_template("create_demographic.html")  # Ensure this template exists


@demographics.route("/delete_demographic/<int:demographic_id>")
def delete_demographic(demographic_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM Demographics WHERE demographic_id = %s", (demographic_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("demographics.show_demographics"))  # Note the Blueprint prefix
