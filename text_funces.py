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

def tokenize(text):
    import re
    return re.findall(r'\w+|\s+|\S', text)

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