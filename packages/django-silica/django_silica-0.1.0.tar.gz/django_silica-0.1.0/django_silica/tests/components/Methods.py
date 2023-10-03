from silica.SilicaComponent import SilicaComponent


class Methods(SilicaComponent):
    template_name = "methods.html"

    test_value = 1

    fruit = "banana"

    def set_apple(self):
        self.fruit = "apple"

    def set_fruit(self, fruit=""):
        self.fruit = fruit
