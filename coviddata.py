from flask import Blueprint, render_template, request, redirect, url_for, flash

import db
from db import get_db

coviddata = Blueprint('coviddata', __name__)


@coviddata.route("/show_coviddata/", defaults={'page': 1})
@coviddata.route("/show_coviddata/<int:page>")
def show_coviddata(page):
    per_page = 20
    offset = (page - 1) * per_page
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CovidData LIMIT %s OFFSET %s;", (per_page, offset))
    covid_data = cursor.fetchall()
    cursor.close()
    return render_template("coviddata_dashboard.html", covid_data=covid_data)


@coviddata.route("/create_coviddata", methods=['GET', 'POST'])
def create_coviddata():
    if request.method == 'POST':
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                """
                INSERT INTO CovidData (
                    metric_id, source_id, geo_id, strata_id, demographic_id,
                    value, date_label, geo_label_proxy_or_real, value_ci_flag,
                    value_95_ci_low, value_95_ci_high, value_90_ci_low, value_90_ci_high
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                [
                    request.form["metric_id"],
                    request.form["source_id"],
                    request.form["geo_id"],
                    request.form["strata_id"],
                    request.form["demographic_id"],
                    request.form["value"],
                    request.form["date_label"],
                    request.form["geo_label_proxy_or_real"],
                    request.form["value_ci_flag"],
                    request.form["value_95_ci_low"],
                    request.form["value_95_ci_high"],
                    request.form["value_90_ci_low"],
                    request.form["value_90_ci_high"]
                ]
            )
            db.commit()
            return render_template("success_template.html", message="Covid data added successfully!")
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}")  # Display error message via flash
            return render_template("error_template.html", error_message=str(e))
        finally:
            cursor.close()
    else:
        return render_template("create_coviddata.html")


@coviddata.route("/delete_coviddata/<int:covid_data_id>")
def delete_coviddata(covid_data_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM CovidData WHERE covid_data_id = %s", (covid_data_id,))
    db.commit()
    cursor.close()
    return redirect(url_for("coviddata.show_coviddata"))  # Note the Blueprint prefix


@coviddata.route('/query_coviddata', methods=['GET', 'POST'])
def query_coviddata():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor(dictionary=True)
        # Prepare and execute the query
        cursor.execute("SELECT * FROM CovidData WHERE demographic_id = %s LIMIT 20;", (request.form["demographic_id"],))
        results = cursor.fetchall()
        cursor.close()
        db.close()  # Closing the database connection
        # Render the results in 'query_results.html'
        return render_template('query_results.html', results=results)
    # Show the form for a GET request
    return render_template('query_coviddata.html')
