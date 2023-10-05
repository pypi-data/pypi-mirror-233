class DocGen:
    
    def __init__(self, attrs: dict):
        self.attrs = attrs
        self.doc = {
            'docstring': attrs.get('__doc__'),
            'attributes': {},
            'methods': {}
        }
        self._generate_doc_dict()

    def _generate_doc_dict(self):
        for attr_name, attr_value in self.attrs.items():
            if callable(attr_value):
                self.doc['methods'][attr_name] = attr_value.__doc__
            else:
                if not attr_name.startswith('_'):
                    self.doc['attributes'][attr_name] = \
                        type(attr_value).__name__
