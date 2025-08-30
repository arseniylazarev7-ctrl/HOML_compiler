from Application import Application
from Page import Page
from Var import Var
from El import El

from text_funces import del_garbage, get_homl_type, split_first_char, split_last_char, get_staples, tokenize, correct_path

from XML import XML

App = None

def collect_args(string):
    string = string[1:-1]

    args = []

    in_marks = False

    arg = ""
    count = -1
    while count < len(string) - 1:
        count += 1

        i = string[count]

        if i == ",":
            if not in_marks:
                if arg != "":
                    args.append(arg)
                    arg = ""
            else:
                arg += i
        
        elif i == "\"":
            if not in_marks:
                in_marks = True
                arg += "\""
            else:
                in_marks = False
                arg += "\""
                args.append(arg)
                arg = ""

        elif i == "{":
            arg_staples, count = get_staples(string, count, "{}")
            arg += arg_staples

        elif (i != " " and i != "\n" and i != "\t") or in_marks:
            arg += i
    else:
        if arg != "":
            args.append(arg)
            arg = ""

    return args

def staples_to_dict(text):
    out = {}
    args = collect_args(text)

    for arg in args:
        arg_key, arg_value = split_first_char(arg, "=")
        out[arg_key] = arg_value

    return out

def find_comments(text):
    import re

    pattern = r'/\*([\s\S]*?)\*/'
    matches = re.findall(pattern, text)

    return matches

def add_type(text, file_path, file_id):
    #global App

    index = 0

    tokens = tokenize(text)

    for token in tokens:
        if token != file_id:
            index += len(token)
        else:
            index += len(token)
            break

    #print(f"<{text[index-2:index+2]}>", f"<{text[index]}>", index)
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
            try:
                out_dict[arg] = default_dict[arg]
            except KeyError:
                print("ERROR!")
                exit()

    for arg in out_dict:
        if out_dict[arg] in default_list:
            out_dict[arg] = out_dict[out_dict[arg]]

        if arg == "id":
            el_id = out_dict[arg][1:-1]

        out_string += out_dict[arg] + ", "
    out_string = out_string[:-2] + ")"

    return out_string, el_id

def parse_els(els):
    global App

    el_list = []

    for el in els:
        if el.text[-5:] == ".homl":
            is_out = True
            if el.text[1] != ":":
                with open(App.path + "\\" + el.text, "r") as f:
                    el_text = del_garbage(XML(f.read()).find("homl/content").text)
            else:
                pass

        elif el.text[0:4] == "<homl":
            is_out = False
            el_text = del_garbage(XML(el.text).find("homl/content").text)

        else:
            is_out = False
            el_text = el.text

        el_type = el.attributes["type"]
        
        if App.Types[el_type]["args"] != "":
            el_args, el_id = parse_args(el_text, App.Types[el_type]["args"])

        el_list.append(El(el_text, el_type, el_id, el_args, is_out))

    return el_list

def parse_vars(vars, page_=None):
    var_list = []
    
    for var in vars:
        if var.text[-5:] == ".homl":
            is_out = True
            if var.text[1] != ":":
                with open(App.path + "\\" + var.text, "r") as f:
                    var_text = del_garbage(XML(f.read()).find("homl/content").text)
            else:
                pass

        elif var.text[0:4] == "<homl":
            is_out = False
            var_text = del_garbage(XML(var.text).find("homl/content").text)

        else:
            is_out = False
            var_text = var.text

        if is_out:
            var_includes = XML(var.text).find("homl/inf/include").text

        elif page_ != None:
            var_includes = page_.find("homl/inf/include").text

        else:
            var_includes = ""

        var_type = var.attributes["type"]
        var_name, var_value = split_first_char(var_text, "=")
        var_name, var_value = del_garbage(var_name), del_garbage(var_value)
        
        var_list.append(Var(var_text, var_type, var_name, var_value, var_includes, is_out))

    return var_list

def parse_pages(pages):
    global App

    out = []

    for page in pages:

        page_out = Page()
        if page.text[-5:] == ".homl":
            if page.text[1] != ":":
                with open(App.path + "\\" + correct_path(page.text), "r") as f:
                    page_text = f.read()
                    if "\\" in page_text or "/" in page_text:
                        page_out.path = del_garbage(split_last_char(correct_path(page.text), ["\\", "/"])[0])
                    else:
                        page_out.path = ""
            else:
                pass
        else:
            page_text = page.text

        page_ = XML(page_text)

        page_els = page_.findall("homl/content/el")
        for el in page_els:
            page_out.types.append(App.Types[el.attributes["type"]])

        page_vars = page_.findall("homl/content/var")

        els = parse_els(page_els)
        vars = parse_vars(page_vars, page_)
        init = del_garbage(del_garbage(page_.find("homl/content/init").text)[1:-1])
        update = del_garbage(del_garbage(page_.find("homl/content/update").text)[1:-1])

        page_out.ID = del_garbage(page_.find("homl/inf/id").text)
        page_out.includes = del_garbage(del_garbage(page_.find("homl/inf/include").text)[1:-1])
        page_out.code_loop = del_garbage(del_garbage(page_.find("homl/content/loop").text)[1:-1])
        
        if page_out.path == None:
            page_out.path = App.path + "\\"
        
        bg = del_garbage(page_.find("homl/inf/bg").text)
        if bg[0] == "{":
            page_out.bg_color = bg
            page_out.bg_path = "\"\""
        else:
            page_out.bg_color = "{0, 0, 0, 0}"
            page_out.bg_path = bg

        page_out.is_main = page.attributes["ismain"]

        page_out.gen_class_pageH(els, vars, init, update)
        page_out.gen_class_pageCpp(els, vars, init, update)

        out.append(page_out)

    return out

def parse_files(files, lib_name, lib_path, lib_text_tag):
    global App

    lib = {}

    for file in files:
        if file.text[-5:] == ".homl":
            if file.text[1] != ":":
                #print(lib_text_tag[-5:])
                if lib_text_tag[-5:] != ".homl":
                    with open(App.path + f"\\lib\\{lib_name}\\" + correct_path(file.text), "r") as f:
                        file_text = f.read()
                        file_path = split_last_char(App.path + f"\\dist\\{App.ID}\\lib\\{lib_name}\\" + correct_path(file.text), ["\\", "/"])[0]
                else:
                    with open(lib_path + "\\" + correct_path(file.text), "r") as f:
                        file_text = f.read()
                        file_path = split_last_char(App.path + f"\\dist\\{App.ID}\\lib\\{lib_name}\\" + correct_path(file.text), ["\\", "/"])[0]
            else:
                pass
        else:
            file_text = file.text
            file_path = lib_path

        if file_path[-1] == "\\":
            file_path = file_path[:-1]

        file_ = XML(file_text)
        file_id = file_.find("homl/inf/id").text
        file_code = del_garbage(file_.find("homl/content").text)[1:-1]
        file_include = del_garbage(file_.find("homl/inf/include").text)[1:-1]

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
        if lib.text[-5:] == ".homl":
            if lib.text[1] != ":":
                #print("The out lib!", lib.text)
                with open(App.path + "\\" + correct_path(lib.text), "r") as f:
                    lib_text = f.read()
                    lib_path = split_last_char(App.path + "\\" + correct_path(lib.text), ["\\", "/"])[0]
                    #print(lib_path)
            else:
                pass

        elif lib.text[0] == "<":
            lib_text = lib.text
            lib_path = App.path + f"\\dist\\{App.ID}"
        else:
            with open(f"{App.path}\\lib\\{correct_path(lib.text)}\\lib.homl", "r") as f:
                lib_text = f.read()
                lib_path = ""

        lib_ = XML(lib_text)
        lib_id = lib_.find("homl/inf/id").text

        if lib_path == "":
            lib_path = App.path + f"\\dist\\{App.ID}\\lib\\{lib_id}"

        lib_files = lib_.findall("homl/content/file")
        
        #print(lib_path)
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

    App.ID = homl.find("homl/inf/id").text
   
    App.Width = homl.find("homl/inf/width").text
    App.Height = homl.find("homl/inf/height").text

    App.Dirs = homl.findall("homl/inf/dir")
    App.Files = homl.findall("homl/inf/file")
    
    App.Libs = parse_libs(homl.findall("homl/inf/lib"))

    App.Vars = parse_vars(homl.findall("homl/content/var"))

    App.Pages = parse_pages(homl.findall("homl/content/page"))

    App.gen_class_app()

    code = 0
    msg = f"Parsing completed successfully, no errors found. Exit code {code}"

    return code, msg, App