class Var:
    def __init__(self, var_text, var_type, var_name, var_value, includes, is_out):
        self.text = var_text
        self.type = var_type
        self.name = var_name
        self.value = var_value
        self.includes = includes
        self.is_out = is_out