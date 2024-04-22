# strata.py
from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db

strata = Blueprint('strata', __name__)


@strata.route("/show_strata")
def show_strata():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Strata;")
    strata = cursor.fetchall()
    cursor.close()
    return render_template("strata_dashboard.html", strata=strata)


@strata.route("/create_strata", methods=['GET', 'POST'])
def create_strata():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO Strata (
                geo_strata_region,
                geo_strata_poverty,
                geo_strata_Population,
                geo_strata_PopDensity,
                geo_strata_Segregation
            ) VALUES (%s, %s, %s, %s, %s);
            """,
            [
                request.form["geo_strata_region"],
                request.form["geo_strata_poverty"],
                request.form["geo_strata_Population"],
                request.form["geo_strata_PopDensity"],
                request.form["geo_strata_Segregation"]
            ]
        )
        db.commit()
        cursor.close()
        return redirect(url_for("strata.show_strata"))  # Note the Blueprint prefix
    else:
        return render_template("create_strata.html")  # Ensure this template exists


@strata.route("/delete_strata/<int:strata_id>")
def delete_strata(strata_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM Strata WHERE strata_id = %s", (strata_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("strata.show_strata"))  # Note the Blueprint prefix
