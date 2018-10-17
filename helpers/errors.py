class PrettyErrors:
    errors = None
    error_type = 'list'

    def __init__(self, **kwargs):
        try:
            self.errors = kwargs['errors'].as_data()
            self.error_type = 'internal'
        except AttributeError:
            self.errors = kwargs['errors']
            if type(kwargs['errors']) == dict:
                self.error_type = 'dict'
            else:
                self.error_type = 'list'

    def as_html(self):
        html = "<ul>"
        if self.error_type == 'dict' or self.error_type == 'internal':
            for key, value in self.errors.items():
                if type(value) == str:
                    html += "<li><{}</li>".format(
                        value
                    )
                elif type(value) == list:
                    for item in value:
                        html += "<li>{}</li>".format(", ".join(item))
                else:
                    html += "<li><strong>{}</strong>: {}</li>".format(key, value)
        else:
            for value in self.errors:
                if type(value) == list:
                    for item in value:
                        html += "<li>{}</li>".format(", ".join(item))
                elif type(value) == dict:
                    for item, msg in value.items():
                        html += "<li><strong>{}</strong>: {}</li>".format(item, msg)
                else:
                    html += "<li><{}</li>".format(
                        value
                    )

        html += "</ul>"

        return html

    def as_list(self):
        return list(self.errors)
