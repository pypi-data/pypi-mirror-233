from silica.SilicaComponent import SilicaComponent


class InlineTemplate(SilicaComponent):
    msg = "Hello World!"

    def inline_template(self):
        return """<div>{{ msg }}</div>"""
