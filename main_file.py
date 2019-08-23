import os
import pandas
from flask import Flask, render_template, request
from geopy.geocoders import ArcGIS

app = Flask(__name__)


def load_file(df, file_detail):
    geolocator = ArcGIS()
    df["Longitude"] = None
    df["Latitude"] = None
    i = 0
    for Address, City, State, Country in zip(df["Address"], df["City"], df["State"], df["Country"]):
        loc = geolocator.geocode(Address + City + State + Country)
        df["Longitude"][i] = "{0:.3f}".format(loc.longitude)
        df["Latitude"][i] = "{0:.3f}".format(loc.latitude)
        i += 1

    df.to_csv(file_detail.filename)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/progress/", methods=["post"])
def success():
    file_detail = request.files['file_name']
    file_ext = file_detail.filename.split(".")
    if file_ext[1] == 'csv':
        file_path = os.path.abspath(file_detail.filename)
        file_detail.save(file_path)
        dataframe = pandas.read_csv(file_path)
        if "Address" in dataframe:
            load_file(dataframe, file_detail)
            return render_template("index.html",  tables=[dataframe.to_html(classes='data', header="true")])
        else:
            return render_template("Fail.html")


if __name__ == "__main__":
    app.run(debug=True)
