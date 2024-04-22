from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db

geographiclocations = Blueprint('geographiclocations', __name__)


@geographiclocations.route("/show_geographiclocations")
def show_geographiclocations():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM GeographicLocations;")
    locations = cursor.fetchall()
    cursor.close()
    return render_template("geographiclocations_dashboard.html", locations=locations)


@geographiclocations.route("/create_geographiclocation", methods=['GET', 'POST'])
def create_geographiclocation():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO GeographicLocations (
                geo_label_city,
                geo_label_state,
                geo_label_citystate,
                geo_fips_code
            ) VALUES (%s, %s, %s, %s);
            """,
            [
                request.form["geo_label_city"],
                request.form["geo_label_state"],
                request.form["geo_label_citystate"],
                request.form["geo_fips_code"]
            ]
        )
        db.commit()
        cursor.close()
        return redirect(url_for("geographiclocations.show_geographiclocations"))  # Note the Blueprint prefix
    else:
        return render_template("create_geographiclocation.html")  # Ensure this template exists


@geographiclocations.route("/delete_geographiclocation/<int:geo_id>")
def delete_geographiclocation(geo_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM GeographicLocations WHERE geo_id = %s", (geo_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("geographiclocations.show_geographiclocations"))  # Note the Blueprint prefix
