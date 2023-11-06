import os
import webbrowser

from statistics import mean

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Select, Button

import swim_utils 

FOLDER = "/swimdata"
path = "/Users/Leon/Year3SETU/CloudDev/swimdata"
sorted_names = swim_utils.get_swimmers_names()
new_list = swim_utils.get_swimmers_list()
second_list = []

class swimmer_main(App):
    def compose(self) -> ComposeResult:
        yield Header()
        s1 = Select((name, name) for name in sorted_names)
        yield s1
        self.s2 = Select(options=second_list, id="second_menu")
        yield self.s2
        yield Button("Generate")

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        name = str(event.value)
        values = swim_utils.get_events(name, new_list)

        self.s2.set_options(values)

    @on (Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        url = "file:///Users/Leon/Year3SETU/CloudDev/calvin.html"
        webbrowser.open(url)
        self.exit(str(event.button))    

if __name__ == "__main__":
    app = swimmer_main()
    app.run()

