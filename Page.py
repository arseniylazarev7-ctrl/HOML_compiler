class Page:
    def __init__(self):
        self.ID = ""
        self.els = []
        self.vars = []
        self.code_classH = ""
        self.code_classCpp = ""
        self.code_loop = ""
        self.is_main = ""
        self.bg_path = ""
        self.bg_color = ""
        self.includes = ""
        self.includes_items = ""
        self.path = None
        self.types = []

    def gen_class_page(self, els, vars, init, update):
        self.els = els
        self.vars = vars
        
        self.gen_class_pageH(els, vars, init, update)
        self.gen_class_pageCpp(els, vars, init, update)

    def gen_class_pageH(self, els, vars, init, update):
        self.code_classH = f"class ClassPage{self.ID} : public ClassPage " + "{\npublic:\n"
        for var in vars:
            if not var.is_out:
                if var.value == "":
                    self.code_classH += f"\t{var.type} {var.name};\n"
                else:
                    self.code_classH += f"\t{var.type} {var.name} = {var.value};\n"
            else:
                self.code_classH += f"\t{var.type} {var.name} = __{var.name};\n"
                self.includes_items += f"\n#include \"__{var.name}.h\"\n"

        self.code_classH += "\n"

        for el in els:
            if not el.is_out:
                self.code_classH += f"\t{el.type} {el.id};\n"
            else:
                self.code_classH += f"\t{el.type} {el.id} = __{el.id};\n"
                self.includes_items += f"\n#include \"__{el.id}.h\"\n"

        self.code_classH += "\n\tvoid init(bool isMain, string bg_path, vector<int> bg_color);\n\tvoid update();\n\tvoid draw();\n};"

    def gen_class_pageCpp(self, els, vars, init, update):
        self.code_classCpp = f"\nvoid ClassPage{self.ID}::init(bool isMain, string bg_path, vector<int> bg_color)" + " {\n\n\t// Code for set main properties:\n\tthis->isOpen = isMain;\n\tthis->bg_img = -1;\n\tthis->bg_color = bg_color;\n\n\t// Code from tag <init>, on page:\n"
        for string in init.split("\n"):
            self.code_classCpp += "\t" + string + "\n"
        self.code_classCpp += "\n"
        for el in els:
            self.code_classCpp += f"\t{el.id}.init{el.args};\n"
        self.code_classCpp += "\t}\n\n"

        self.code_classCpp += f"void ClassPage{self.ID}::update()" + " {\n"
        for el in els:
            self.code_classCpp += f"\t{el.id}.update();\n"
        self.code_classCpp += "\n\t// Code from tag <update>, on page:\n"
        for string in update.split("\n"):
            self.code_classCpp += "\t" + string + "\n"
        self.code_classCpp += "}\n\n"

        self.code_classCpp += f"void ClassPage{self.ID}::draw()" + " {\n"
        for el in els:
            self.code_classCpp += f"\t{el.id}.draw();\n"
        self.code_classCpp += "}"