from flask import Flask, render_template, request, session # from module import Class.
import os 

import hfpy_utils
import swim_utils


app = Flask(__name__)


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
        "select_name.html",
        title="Select a swimmer to chart",
        url="/displayevents",
        selected_swimmer="swimmer",
        data=names,
    )

def get_swimmer_events(selected_swimmer):
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    swims = []
    for file in files:
        if selected_swimmer and file.startswith(selected_swimmer + '-'):
            swimmer_data = swim_utils.get_swimmers_data(file)
            if swimmer_data:
                distance,stroke = swimmer_data[2],swimmer_data[3]
                race = f"{distance} {stroke}"
                swims.append((race))
    return swims


@app.post("/displayevents")
def display_events():
    selected_swimmer = request.form.get("swimmer")
    events = get_swimmer_events(selected_swimmer)

    return render_template (
        "select_event.html",
        title="Select an event to chart",
        url="/chart",
        select_event="event",
        data=events,
        selected_swimmer=selected_swimmer, 
    )

if __name__ == "__main__":
    app.run(debug=True)
