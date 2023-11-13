import os
from statistics import mean

FOLDER = "swimdata/"
path = "/Users/Leon/Year3SETU/CloudDev/swimdata"

# function 1
def convert2hundreths(timestring):
    mins, rest = timestring.split(":")
    secs, hundreths = rest.split(".")
    return int(hundreths) + (int(secs) * 100) + ((int(mins) * 60) * 100)

# function 2
def build_time_string(num_time):
    secs, hundredths = f"{num_time/100:.2f}".split(".")
    mins = int(secs) // 60
    seconds = int(secs) - mins*60
    return f"{mins}:{seconds}.{hundredths}"

# function 3
def get_swimmers_data(filename):
    name, age, distance, stroke = filename.removesuffix(".txt").split("-")
    with open(FOLDER + filename) as fn:
        data = fn.read()
    times = data.strip().split(",")
    converts = []
    for t in times:
        converts.append(convert2hundreths(t))
    average = build_time_string(mean(converts))

    return name, age, distance, stroke, times, converts, average

# function 4
def get_swimmers_names(): 
    swim_list = []
    dir_list = os.listdir(path)
    for file in dir_list:
        if file.endswith(".txt"):
           swim_list.append(file)

    names = [filename.removesuffix(".txt").split("-")[0] for filename in swim_list]
    unique_names = list(set(names))
    sorted_names = sorted(unique_names)

    return sorted_names

# function 5
def get_swimmers_list():
    swim_list = []
    dir_list = os.listdir(path)
    for file in dir_list:
        if file.endswith(".txt"):
            swim_list.append(file)
           
    return swim_list

# function 6
def get_events(name: str, files: list) -> list:
    swims = []
    for file in files:
        if file.startswith(name+'-'):
            names, age, distance, stroke = file.removesuffix(".txt").split("-")
            race = f"{distance} {stroke}"
            swims.append((race, file))

    return swims


    return name, age, distance, stroke, times, converts, average

# function 7
def produce_bar_chart(fn):
    """Given the name of a swimmer's file, produce a HTML/SVG-based bar chart.

    Save the chart to the CHARTS folder. Return the path to the bar chart file.
    """
    swimmer, age, distance, stroke, times, converts, average = get_swimmers_data(fn)
    from_max = max(converts) + 50
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    header = f"""<!DOCTYPE html>
                    <html>
                        <head>
                            <title>{title}</title>
                        </head>
                        <body>
                            <h3>{title}</h3>"""
    body = ""
    for n, t in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 350)
        body = (
            body
            + f"""
                            <svg height="30" width="400">
                                <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
                            </svg>{t}<br />"""
        )
    footer = f"""
                            <p>Average time: {average}</p>
                        </body>
                    </html>"""
    page = header + body + footer
    save_to = f"{fn.removesuffix('.txt')}.html"
    with open(save_to, "w") as sf:
        print(page, file=sf)

    return save_to
