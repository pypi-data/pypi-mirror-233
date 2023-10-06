from django_silica.SilicaComponent import SilicaComponent


class QueryParams(SilicaComponent):
    property_1 = "foo"

    query_params = ["property_1"]

    def inline_template(self):
        return """
            <div>{{ property_1 }}</div>
        """
