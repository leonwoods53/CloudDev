from flask import Flask, render_template, request # from module import Class.


import os 

import hfpy_utils
import swim_utils


app = Flask(__name__)

FOLDER = "swimdata"

@app.get("/")
@app.get("/hello")
def hello():
    return render_template(
                "select.html",
                title= "Swimmer Events"
    )


@app.get("/chart")
def display_chart():
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data("Darius-13-100m-Fly.txt")

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [ hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts ]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )


@app.get("/getswimmers")
def get_swimmers_names():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    names = set()
    for swimmer in files:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])
    return render_template(
        "select.html",
        title="Select a swimmer to chart",
        data=sorted(names),
    )


@app.post("/displayevents", methods=["POST"])
def get_swimmer_events():
    selected_swimmer = request.form["swimmer"]
    return request.form["swimmer"]


if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.
