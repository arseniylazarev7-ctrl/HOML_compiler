from text_funces import del_garbage
import cpp

class Application:
    def __init__(self, file_path):
        self.Width = ""
        self.Height = ""
        self.CodeClassH = ""
        self.CodeClassCpp = ""
        self.Includes = ""
        self.ID = ""
        self.Dirs = []
        self.Files = []
        self.Vars = []
        self.Pages = []
        self.Libs = {}
        self.Types = {}

        self.path = file_path

    def gen_class_app(self):
        self.gen_class_appH()
        self.gen_class_appCpp()

    def gen_class_appH(self):
        self.CodeClassH = (f"// This is class for your application!\n" + del_garbage(cpp.ClassAppAppH)).replace("/*ClassName*/", f"ClassApp{self.ID}")

        vars = ""
        for var in self.Vars:
            if not var.is_out:
                if var.value == "":
                    print(f"\t{var.type} {var.name};\n")
                    vars += f"\t{var.type} {var.name};\n"
                else:
                    vars += f"\t{var.type} {var.name} = {var.value};\n"
            else:
                vars += f"\t{var.type} {var.name} = __{var.name};\n"
                self.Includes += f"\n#include \"__{var.name}.h\"\n"
            
        self.CodeClassH = self.CodeClassH.replace("/*vars*/", del_garbage(vars))

        pages = ""
        for page in self.Pages:
            pages += f"\tClassPage{page.ID} {page.ID};\n"
        self.CodeClassH = self.CodeClassH.replace("/*pages*/", del_garbage(pages))

    def gen_class_appCpp(self):
        self.CodeClassCpp = del_garbage(cpp.ClassAppAppCpp)
        self.CodeClassCpp = self.CodeClassCpp.replace("/*Name*/", self.ID)
        self.CodeClassCpp = self.CodeClassCpp.replace("/*ClassName*/", f"ClassApp{self.ID}")
        self.CodeClassCpp = self.CodeClassCpp.replace("/*Width*/", self.Width)
        self.CodeClassCpp = self.CodeClassCpp.replace("/*Height*/", self.Height)

        init = ""
        for page in self.Pages:
            init += f"\t{page.ID}.init({page.is_main}, {page.bg_path}, {page.bg_color});\n"
        self.CodeClassCpp = self.CodeClassCpp.replace("/*Init()*/", "\t" + del_garbage(init))

        loop = ""
        for page in self.Pages:
            loop += "\n"

            for string in page.code_loop.split("\n"):
                loop += "\t" + string + "\n"

        self.CodeClassCpp = self.CodeClassCpp.replace("/*Loop()*/", "\t" + del_garbage(loop))