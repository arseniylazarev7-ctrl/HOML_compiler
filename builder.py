import os

from text_funces import del_garbage, split_last_char, get_staples, tokenize, correct_path, del_marks

import cpp

App = None

def copy_folder(source_folder, destination_folder):
    import os
    import shutil

    """
    Копирует папку source_folder в destination_folder, включая все подпапки и файлы.
    """
    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)))

    except FileExistsError:
        pass
    except Exception as e:
        pass

def move_items():
    import os
    import shutil

    global App

    os.system(f"mkdir {App.path}\\dist")
    os.system(f"mkdir {App.path}\\dist\\{App.ID}")

    for i in App.Dirs:
        i.text = del_marks(i.text)
        if i.text[1:3] == ":\\":
            dir_path = i.text
            dir_name = os.path.basename(dir_path)
        else:
            dir_path = os.path.join(App.path, i.text)
            dir_name = i.text

        target_dir = os.path.join(App.path, f"dist\\{App.ID}", dir_name)

        if os.path.exists(dir_path):
            try:
                shutil.copytree(dir_path, target_dir, dirs_exist_ok=True)
            except Exception:
                pass

    for i in App.Files:
        if i.text[1:3] == ":\\":
            file_path = i.text
        else:
            file_path = os.path.join(App.path, i.text)

        target_dir = os.path.join(App.path, f"dist\\{App.ID}")

        if os.path.exists(file_path):
            try:
                shutil.copy2(file_path, target_dir)
            except Exception:
                pass 

def build_var(var, path):
    if var.is_out:
        with open(f"{path}\\{split_last_char(var.text, ["\\", "/"])[0]}\\__{var.name}.h", "w") as f:
            if var.value != "":
                f.write(f"#pragma once\n{var.includes}\n{var.type} __{var.name} = {var.value};\n")
            else:
                f.write(f"#pragma once\n{var.includes}\n{var.type} __{var.name};\n")

def build_el(el, path):
    if el.is_out:
        with open(f"{path}\\{split_last_char(el.text, ["\\", "/"])[0]}\\__{el.id}.h", "w") as f:
            if el.args != "":
                f.write(f"#pragma once\n{el.includes}\n{el.type} __{el.id}{el.args};\n")
            else:
                f.write(f"#pragma once\n{el.includes}\n{el.type} __{el.id};\n")

def build_page(page):
    import os

    global App

    PathF = correct_path(App.path + f"\\dist\\{App.ID}\\{page.path}")

    os.system(f"mkdir {PathF}")

    with open(PathF + f"\\ClassPage{page.ID}.h", "w") as f:
        page.includes += "\n" + page.includes_items

        out_include = ""
        for include in page.includes.split("\n"):
            if del_garbage(include) != "":
                out_include += del_garbage(include) + "\n"
        out_include += "\n"

        was_include = []
        for type in page.types:
            file_path = del_garbage(type["file_path"][len(App.path) + len(f"dist\\{App.ID}") + 2:])
            file_name = del_garbage(type["file_name"])
            
            if not [file_path, file_name] in was_include:
                was_include.append([file_path, file_name])
                out_include += f"#include \"{file_path}\\{file_name}.h\"\n"

        f.write(del_garbage(del_garbage(cpp.StartH) + "\n\n#include \"lib/homl/Page.h\"" f"\n\n{out_include}\n" + page.code_classH))

    with open(PathF + f"\\ClassPage{page.ID}.cpp", "w") as f:
        f.write(del_garbage(f"#include \"ClassPage{page.ID}.h\"\n" + page.code_classCpp))

    for el in page.els:
        build_el(el, PathF)

    for var in page.vars:
        build_var(var, PathF)

def build_app():
    global App

    with open(App.path + f"\\dist\\{App.ID}\\ClassApp{App.ID}.h", "w") as f:
        ClassAppAppH = cpp.StartH + "\n// These are the main includes of your application\n"

        for include in App.Includes.split("\n"):
            if del_garbage(include) != "":
                ClassAppAppH += del_garbage(include) + "\n"

        for var in App.Vars:
            build_var(var, f"{App.path}\\dist\\{App.ID}")

        for page in App.Pages:
            ClassAppAppH += f"\n// This include is for page, with id \"{page.ID}\"\n"
            NameH = "ClassPage" + del_garbage(page.ID)

            if page.path != "":
                ClassAppAppH += f"#include \"{page.path}\\{NameH}.h\"\n"
            else:
                ClassAppAppH += f"#include \"{NameH}.h\"\n"

            for include in page.includes.split("\n"):
                if del_garbage(include) != "":
                    ClassAppAppH += del_garbage(include) + "\n"

            build_page(page)

        ClassAppAppH = del_garbage(ClassAppAppH + "\n" + App.CodeClassH)
        f.write(ClassAppAppH)

    with open(App.path + f"\\dist\\{App.ID}\\ClassApp{App.ID}.cpp", "w") as f:
        f.write(App.CodeClassCpp)

def build_libs():
    global App

    for lib_name in App.Libs:
        lib_files = App.Libs[lib_name]["lib_files"]
        lib_path = App.Libs[lib_name]["lib_path"]

        build_files(lib_files)

def build_files(lib_files):
    import os

    for file_name in lib_files:
        file_code = lib_files[file_name]["file_code"]
        file_type = lib_files[file_name]["file_type"]
        file_path = lib_files[file_name]["file_path"]
        file_include = lib_files[file_name]["file_include"]
            
        if file_type == "__class__":
            index = 0

            tokens = tokenize(file_code)
            for token in tokens:
                if token != file_name:
                    index += len(token)
                else:
                    index += len(token)
                    break

            index = get_staples(file_code, index, "{}")[1]
            text_classH = del_garbage(file_code[:index + 1] + ";")

            text_classCpp = del_garbage(file_code[len(text_classH):])
            if len(text_classCpp) > 0:
                if text_classCpp[0] == ";":
                    text_classCpp = del_garbage(text_classCpp[1:])
                text_classCpp = del_garbage(f"#include \"{file_name}.h\"\n\n" + text_classCpp)

            include_out = ""
            if file_include != "":
                for include in file_include.split("\n"):
                    include_out += del_garbage(include) + "\n"

            os.system(f"mkdir {file_path}")

            with open(f"{file_path}\\{file_name}.h", "w") as f:
                f.write(del_garbage(include_out) + "\n\n" + text_classH)
                
            with open(f"{file_path}\\{file_name}.cpp", "w") as f:
                f.write(text_classCpp)

def build(data, Path):
    global App
    App = data

    os.system(f"rmdir /s /q \"{App.path}\\dist\"")

    os.system(f"mkdir {App.path}\\dist\\{App.ID}")

    with open(App.path + f"\\dist\\{App.ID}\\main.cpp", "w") as f:
        MainCpp = cpp.MainCpp
        MainCpp = MainCpp.replace("/*ClassName*/", f"ClassApp{App.ID}")
        MainCpp = MainCpp.replace("/*Name*/", App.ID)

        f.write(del_garbage(MainCpp))

    build_app()
    
    build_libs()

    move_items()

    copy_folder(Path + "\\src\\SDL\\SDL3", App.path + f"\\dist\\{App.ID}")
    copy_folder(Path + "\\src\\SDL\\SDL3_image", App.path + f"\\dist\\{App.ID}")
    copy_folder(Path + "\\src\\SDL\\SDL3_ttf", App.path + f"\\dist\\{App.ID}")

    code = 0
    msg = f"Building completed successfully, no errors found. Exit code {code}"

    return code, msg