from Application import Application
from Page import Page
from Var import Var
from El import El

from text_funces import del_garbage, get_homl_type, split_first_char, split_last_char, get_staples, tokenize, correct_path, del_marks, staples_to_dict, find_comments

from XML import XML

App = None

def add_type(text, file_path, file_id):
    global App

    index = 0

    tokens = tokenize(text)

    for token in tokens:
        if token != file_id:
            index += len(token)
        else:
            index += len(token)
            break

    class_text, index = get_staples(text, index, "{}")

    comments = find_comments(class_text)
    if len(comments) > 0:
        for comment in comments:
            comment = del_garbage(comment)

            if comment[0:6] == "<args>":
                App.Types[file_id] = {
                    "args": del_garbage(comment[6:-7]),
                    "file_path": file_path,
                    "file_name": file_id
                }

    else:
        App.Types[file_id] = {
            "args": "",
            "file_path": file_path,
            "file_name": file_id
        }

def parse_args(get_string, default_string):
    get_dict = staples_to_dict(get_string)
    default_dict = staples_to_dict(default_string)

    out_dict = {}
    out_string = "("

    default_list = list(default_dict.keys())

    for arg in default_list:
        try:
            out_dict[arg] = get_dict[arg]
        except KeyError:
            out_dict[arg] = default_dict[arg]

    for arg in out_dict:
        if out_dict[arg] in default_list:
            out_dict[arg] = out_dict[out_dict[arg]]

        if arg == "id":
            el_id = out_dict[arg][1:-1]

        out_string += out_dict[arg] + ", "
    out_string = out_string[:-2] + ")"

    return out_string, el_id

def parse_els(els, includes, page):
    global App

    el_list = []

    for el in els:
        if del_marks(el.text)[-5:] == ".homl":
            is_out = True

            with open(f"{App.path}\\{page.path}\\{del_marks(el.text)}", "r") as f:
                el_text = del_marks(XML(f.read()).find("homl/content").text)

        elif del_marks(el.text[0:4]) == "<homl":
            is_out = False
            el_text = del_marks(XML(del_marks(el.text)).find("homl/content").text)

        else:
            is_out = False
            el_text = del_marks(el.text)

        el_type = el.attributes["type"]
        
        if App.Types[el_type]["args"] != "":
            el_args, el_id = parse_args(el_text, App.Types[el_type]["args"])

        try:
            if App.Types[el_type]["args"] != "":
                includes = f"\n#include \"{f"{App.Types[el_type]["file_path"][len(f"{App.path}\\dist\\{App.ID}") + 1:]}\\{App.Types[el_type]["file_name"]}"}.h\"\n"
        except KeyError:
            pass

        el_list.append(El(el_text, el_type, el_id, el_args, includes, is_out))

    return el_list

def parse_vars(vars, includes, page=None):
    var_list = []
    
    for var in vars:
        if del_marks(var.text)[-5:] == ".homl":
            is_out = True
            
            if page == None:
                with open(f"{App.path}\\{del_marks(var.text)}", "r") as f:
                    var_text = del_marks(XML(f.read()).find("homl/content").text)

            else:
                with open(f"{App.path}\\{page.path}\\{del_marks(var.text)}", "r") as f:
                    var_text = del_marks(XML(f.read()).find("homl/content").text)

        elif del_marks(var.text[0:4]) == "<homl":
            is_out = False
            var_text = del_marks(XML(var.text).find("homl/content").text)

        else:
            is_out = False
            var_text = var.text

        var_type = var.attributes["type"]
        var_name, var_value = split_first_char(var_text, "=")
        var_name, var_value = del_garbage(var_name), del_garbage(var_value)
        
        var_list.append(Var(var_text, var_type, var_name, var_value, includes, is_out))

    return var_list

def parse_pages(pages):
    global App

    out = []

    for page in pages:

        page_out = Page()
        if del_marks(page.text)[-5:] == ".homl":
            with open(App.path + "\\" + del_marks(correct_path(page.text)), "r") as f:
                page_text = f.read()
                if "\\" in page_text or "/" in page_text:
                    page_out.path = del_marks(split_last_char(correct_path(page.text), ["\\", "/"])[0])
                else:
                    page_out.path = ""
        else:
            page_text = del_marks(page.text)
            page_out.path = ""

        page_ = XML(page_text)

        page_out.ID = del_marks(page_.find("homl/inf/id").text)
        page_out.includes = del_marks(page_.find("homl/inf/includes").text)
        
        if del_marks(page_.find("homl/content/loop").text)[-5:] == ".homl":
            if page_out.path == "":
                with open(f"{App.path}\\{del_marks(page_.find("homl/content/loop").text)}", "r") as f:
                    page_out.code_loop = del_marks(XML(f.read()).find("homl/content").text)
            else:
                with open(f"{App.path}\\{page_out.path}\\{del_marks(page_.find("homl/content/loop").text)}", "r") as f:
                    page_out.code_loop = del_marks(XML(f.read()).find("homl/content").text)
        elif del_marks(page_.find("homl/content/loop").text)[0:4] == "<homl":
            page_out.code_loop = XML(del_marks(page_.find("homl/content/loop").text)).find("homl/content").text
        else:
            page_out.code_loop = del_marks(page_.find("homl/content/loop").text)

        page_els = page_.findall("homl/content/el")
        for el in page_els:
            page_out.types.append(App.Types[el.attributes["type"]])
        page_vars = page_.findall("homl/content/var")

        els = parse_els(page_els, page_out.includes, page_out)
        vars = parse_vars(page_vars, page_out.includes, page_out)
        
        if del_marks(page_.find("homl/content/init").text)[-5:] == ".homl":
            if page_out.path == "":
                with open(f"{App.path}\\{del_marks(page_.find("homl/content/init").text)}", "r") as f:
                    init = del_marks(XML(f.read()).find("homl/content").text)
            else:
                with open(f"{App.path}\\{page_out.path}\\{del_marks(page_.find("homl/content/init").text)}", "r") as f:
                    init = del_marks(XML(f.read()).find("homl/content").text)
        elif del_marks(page_.find("homl/content/init").text)[0:4] == "<homl":
            init = XML(del_marks(page_.find("homl/content/init").text)).find("homl/content").text  
        else:
            init = del_marks(page_.find("homl/content/init").text)

        if del_marks(page_.find("homl/content/update").text)[-5:] == ".homl":
            if page_out.path == "":
                with open(f"{App.path}\\{del_marks(page_.find("homl/content/update").text)}", "r") as f:
                    update = del_marks(XML(f.read()).find("homl/content").text)
            else:
                with open(f"{App.path}\\{page_out.path}\\{del_marks(page_.find("homl/content/update").text)}", "r") as f:
                    update = del_marks(XML(f.read()).find("homl/content").text)
        elif del_marks(page_.find("homl/content/update").text)[0:4] == "<homl":
            update = XML(del_marks(page_.find("homl/content/update").text)).find("homl/content").text  
        else:
            update = del_marks(page_.find("homl/content/update").text)
        
        bg = del_marks(page_.find("homl/inf/bg").text)
        if bg[0] == "{":
            page_out.bg_color = bg
            page_out.bg_path = "\"\""
        else:
            page_out.bg_color = "{0, 0, 0, 0}"
            page_out.bg_path = bg

        page_out.is_main = page.attributes["ismain"]

        page_out.gen_class_page(els, vars, init, update)

        out.append(page_out)

    return out

def parse_files(files, lib_name, lib_path, lib_text_tag):
    global App

    lib = {}

    for file in files:
        if del_marks(file.text)[-5:] == ".homl":

            if del_marks(lib_text_tag)[-5:] != ".homl":
                with open(App.path + f"\\lib\\{lib_name}\\" + correct_path(file.text), "r") as f:
                    file_text = f.read()
                    file_path = split_last_char(App.path + f"\\dist\\{App.ID}\\lib\\{lib_name}\\" + del_marks(correct_path(file.text)), ["\\", "/"])[0]
            else:
                with open(lib_path + "\\" + correct_path(file.text), "r") as f:
                    file_text = f.read()
                    file_path = split_last_char(App.path + f"\\dist\\{App.ID}\\lib\\{lib_name}\\" + del_marks(correct_path(file.text)), ["\\", "/"])[0]

        else:
            file_text = del_marks(file.text)
            file_path = lib_path

        if file_path[-1] == "\\":
            file_path = file_path[:-1]

        file_ = XML(file_text)
        file_id = del_marks(file_.find("homl/inf/id").text)
        file_code = del_marks(file_.find("homl/content").text)
        file_include = del_marks(file_.find("homl/inf/includes").text)

        add_type(file_code, file_path, file_id)

        lib[file_id] = {
            "file_code": file_code,
            "file_type": get_homl_type(file_text),
            "file_path": file_path,
            "file_include": file_include
        }

    return lib

def parse_libs(libs):
    global App

    out = {}

    for lib in libs:
        if del_marks(lib.text)[-5:] == ".homl":
            with open(App.path + "\\" + del_marks(correct_path(lib.text)), "r") as f:
                lib_text = f.read()
                lib_path = del_marks(split_last_char(App.path + "\\" + correct_path(lib.text), ["\\", "/"])[0])

        elif del_marks(lib.text)[0:4] == "<homl":
            lib_text = lib.text
            lib_path = App.path + f"\\dist\\{App.ID}"
        else:
            with open(f"{App.path}\\lib\\{del_marks(correct_path(lib.text))}\\lib.homl", "r") as f:
                lib_text = f.read()
                lib_path = ""

        lib_ = XML(lib_text)
        lib_id = del_marks(lib_.find("homl/inf/id").text)

        if lib_path == "":
            lib_path = App.path + f"\\dist\\{App.ID}\\lib\\{lib_id}"

        lib_files = lib_.findall("homl/content/file")

        out[lib_id] = {
            "lib_files": parse_files(lib_files, lib_id, lib_path, lib.text),
            "lib_path": lib_path
        }

    return out

def parse(file_path):
    global App

    App = Application(file_path)

    with open(file_path + "\\main.homl", "r") as f:
        code = f.read()

    homl = XML(code)

    App.ID = del_marks(homl.find("homl/inf/id").text)
    App.Width = del_marks(homl.find("homl/inf/width").text)
    App.Height = del_marks(homl.find("homl/inf/height").text)

    App.Includes = del_marks(homl.find("homl/inf/includes").text)

    App.Dirs = homl.findall("homl/inf/dir")
    App.Files = homl.findall("homl/inf/file")
    
    App.Libs = parse_libs(homl.findall("homl/inf/lib"))
    App.Vars = parse_vars(homl.findall("homl/content/var"), App.Includes)
    App.Pages = parse_pages(homl.findall("homl/content/page"))

    App.gen_class_app()

    code = 0
    msg = f"Parsing completed successfully, no errors found. Exit code {code}"

    return code, msg, App