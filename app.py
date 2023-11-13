from flask import Flask, render_template, request, session # from module import Class.
import os 

import hfpy_utils
import swim_utils


app = Flask(__name__)
app.secret_key = "session"


@app.get("/")
@app.get("/hello")
def hello():
    return render_template(
        "base.html"
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
    ) = swim_utils.get_swimmers_data("Abi-10-100m-Breast.txt")

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

def get_swimmers_names():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    unique_names = set()
    for swimmer in files:
        unique_names.add(swim_utils.get_swimmers_data(swimmer)[0])
    return sorted(list(unique_names))

@app.get("/swimmers")
def display_swimmers():
    names = get_swimmers_names()
    return render_template (
        "select.html",
        title="Select a swimmer to chart",
        url="/displayevents",
        select_id="swimmer",
        data=names,
    )

@app.post("/displayevents")
def get_swimmer_events():
    return request.form["swimmer"]


if __name__ == "__main__":
    app.run(debug=True)
