import json
import random
from typing import List

from pyecharts.charts import Bar

from django_silica.EventManager import test_event
from django_silica.SilicaComponent import SilicaComponent


class TestComponent(SilicaComponent):
    first_name: str = "Simon"
    last_name: str = "Smith"

    query_params: List = ["last_name"]

    count: int = 0

    todo: str = ""
    todos: list = []

    chart_data: dict = []
    factory_name: str = "ABC Ltd"
    original_factory_name: str
    is_editing_factory: bool = False

    alert_text: str = "Alert!"

    def mount(self):
        self.original_factory_name = self.factory_name

    def set_name(self, name: str):
        self.first_name = name

    def add_todo(self):
        if self.todo != "":
            self.todos.append(self.todo)
        # self.emit(event_name="newtodo", payload=todo)
        # self.emit_to(components=["..."], payload=todo)
        # self.emit_to_component_name(payload=todo)

    def show_chart(self):
        bar = Bar()
        bar.add_xaxis(["shirts", "cardigans", "chiffons", "trousers", "heels", "socks"])
        values = random.sample(range(10, 30), 6)
        bar.add_yaxis("Merchant A", values)
        # render will generate a local HTML file, by default render.html will be generated in the current directory
        # You can also pass in a path parameter, e.g. bar.render("mycharts.html")

        bar.render()
        self.chart_data = json.loads(bar.dump_options())
        self.js_call("createChart")

    def destroy_chart(self):
        self.js_call("destroyChart")

    def remove_todos(self):
        self.todos = []

    def increment(self):
        self.count = int(self.count) + 1

    def decrement(self):
        self.count = int(self.count) - 1

    def callAlert(self):
        self.js_call("alert", self.alert_text)

    def start_editing(self):
        self.original_factory_name = self.factory_name
        self.is_editing_factory = True

    def cancel_editing(self):
        self.factory_name = self.original_factory_name
        self.is_editing_factory = False

    def save_factory(self):
        self.is_editing_factory = False
        self.original_factory_name = self.factory_name
        # self.emit("custom_event", {"key": "value"})

        test_event.send(sender=self, component=self, data={"key": "value"})
        # signal = EventManager.get_signal(test)
        # signal.send(sender=self, component=self, data=payload)

    def redirect_me(self):
        self.redirect("/reporting/cpk")
        pass
