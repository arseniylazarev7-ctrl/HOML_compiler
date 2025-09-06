import re

def get_homl_type(code):
    #
    return (code.split(">")[0].split("=")[1])[1:-1]

def del_garbage(string):
    if string == None:
        return ""
    
    if len(string) == 0:
        return ""
    
    count = 0
    while count < len(string):
        char = string[count]
        if char == " " or char == "\t" or char == "\n":
            count += 1
        else:
            string = string[count:]
            break
    
    count = len(string) - 1
    while count > -1:
        char = string[count]
        if char == " " or char == "\t" or char == "\n":
            count -= 1
        else:
            string = string[:count + 1]
            return string
        
    return ""

def split_first_char(text, char):
    first = ""

    count = -1
    for i in text:
        count += 1

        if i != char:
            first += i
        else:
            return first, text[count+1:]
    return text, ""

def split_last_char(text, chars):
    count = len(text)

    while count > 0:
        count -= 1
        i = text[count]

        if i in chars:
            return text[:count], text[len(text[:count + 1]):]
    return "", text

def get_staples(text, pos, type_staples):
    """
    Находит кусок текста внутри скобок заданного типа, начиная с указанной позиции.
    Если символ по заданному индексу не является открывающей скобкой, выдает исключение.

    Аргументы:
        text: Строка текста для поиска.
        pos: Индекс в строке, с которого начинается поиск.
        type_staples: Кортеж из двух символов, представляющих открывающую и закрывающую скобки.

    Возвращает:
        Кортеж: (найденный_текст_вместе_со_скобками, индекс_конца_скобок)

    Вызывает:
        IndexError: Если pos < 0 или если pos >= len(text).
        SyntaxError: Если в тексте не найдена закрывающая скобка.
    """

    if pos < 0:
        raise IndexError("Invalid argument: pos < 0")
    if pos >= len(text):
        raise IndexError("Invalid argument: pos >= len(text)")

    left, right = type_staples
    
    # Добавлено: ищем ближайшую открывающую скобку начиная с pos
    start_pos = -1
    for i in range(pos, len(text)):
        if text[i] == left:
            start_pos = i
            break # Нашли открывающую скобку, выходим из цикла

    if start_pos == -1:
         return None, None

    count = 1  # Счетчик открывающих скобок (начинаем с 1, так как первую уже нашли)
    end_pos = start_pos + 1
    while end_pos < len(text):
        char = text[end_pos]
        if char == left:
            count += 1
        elif char == right:
            count -= 1

        if count == 0:
            return text[start_pos:end_pos + 1], end_pos  # Возвращаем текст вместе со скобками и индекс конца
        end_pos += 1

    raise SyntaxError("Invalid argument: in text must be close staple") # Закрывающая скобка не найдена

def correct_path(path):
    #
    return path.replace("/", "\\")

def del_marks(text):
    if text == None:
        return None
    
    if len(text) == 0:
        return ""
    
    text = del_garbage(text)

    if text[0] == "\"" and text[-1] == "\"":
        return del_garbage(text[1:-1])
    return text

def collect_args(string):
    string = del_garbage(string)
    if len(string) == 0:
        return []
    
    if string[0] == "(":
        string = string[1:]
    if string[-1] == ")":
        string = string[:-1]

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
    return re.findall(r'/\*([\s\S]*?)\*/', text)

def tokenize(text):
    #pattern = r'\w+|\s+|\S'
    pattern = r'\w+|\S'
    return re.findall(pattern, text)