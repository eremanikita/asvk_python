C = type("C", (), {"var": 100500, "__init__": (lambda self, var: setattr(self, "var", var))})

