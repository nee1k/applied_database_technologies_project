from flask import Flask
from flask import render_template

from demographics import demographics
from metrics import metrics
from sources import sources
from strata import strata
from geographiclocations import geographiclocations

app = Flask(__name__)
app.register_blueprint(metrics, url_prefix='/metrics')
app.register_blueprint(sources, url_prefix='/sources')
app.register_blueprint(demographics, url_prefix='/demographics')
app.register_blueprint(strata, url_prefix='/strata')
app.register_blueprint(geographiclocations, url_prefix='/geographiclocations')  # Optional URL prefix


@app.route('/')
def hello_world():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
