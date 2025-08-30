class XML:
    class Tag:
        def __init__(self, name=None, is_open=None, attributes=None, text=None):
            self.name = name
            self.is_open = is_open
            self.attributes = attributes
            self.text = text or ""
            self.children = []
            self.parent = None

        def __repr__(self):
            return f"Tag(name='{self.name}', is_open={self.is_open}, text='{self.text}', attributes='{self.attributes}')"

    def __init__(self, text):
        self.text = text
        self.xml = self.parse_xml()

    def parse_xml(self):
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
        
        def is_garbage(text):
            for i in text:
                if i != " " and i != "\t" and i != "\n":
                    return False
            return True
        
        def del_garbage(string):
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
        
        def get_staples(pos):
            in_marks = False
            out = ""

            for i in self.text[pos:]:
                out += i

                if i == "\"":
                    in_marks = not in_marks

                if i == ">" and not in_marks:
                    return out, pos + len(out) - 1

            raise SyntaxError
        
        def parse_fragments():
            fragments = []
            fragment = ""

            in_marks = False
            i = -1

            while i < len(self.text) - 1:
                i += 1
                char = self.text[i]

                if char == "\"":
                    in_marks = not in_marks

                if char == "<" and not in_marks:
                    if not is_garbage(fragment):
                        fragments.append(fragment)
                        fragment = ""

                    fragment, i = get_staples(i)
                    if not is_garbage(fragment):
                        fragments.append(fragment)
                        fragment = ""
                else:
                    fragment += char

            return fragments
        
        def parse_tags():
            tags_data = []
            def get_name(fragment):
                name = ""

                if fragment[1] == "/":
                    name = fragment[2:-1]
                else:
                    for i in fragment[1:]:
                        if i == " " or i == ">":
                            return name
                        name += i

                return name

            def get_is_open(fragment):
                return fragment[1] == "/"
            
            def get_attributes(fragment, name):
                fragment = fragment[len(name) + 1:]
                els = []
                attributes = {}

                in_marks = False
                i = -1
                el = ""

                while i < len(fragment) - 1:
                    i += 1
                    char = fragment[i]

                    if char == "\"":
                        in_marks = not in_marks

                    if char == " " and not in_marks:
                        
                        if len(el) > 0:
                            if el[-1] == ">":
                                els.append(el[:-1])
                            else:
                                els.append(el)
                            el = ""

                    el += char

                if el[-1] == ">":
                    els.append(el[:-1])
                else:
                    els.append(el)

                for el in els:
                    key, value = split_first_char(el, "=")
                    if key != "" and value != "":
                        attributes[del_garbage(key)] = del_garbage(value)[1:-1]

                return attributes

            fragments = parse_fragments()
            for fragment in fragments:
                if fragment[0] == "<":
                    name = get_name(fragment)
                    is_open = get_is_open(fragment)
                    attributes = get_attributes(fragment, name)
                    
                    tags_data.append(XML.Tag(name, is_open, attributes))
                else:
                    tags_data.append(XML.Tag(text=fragment))

            return tags_data

        tags_data = parse_tags()
        
        root = XML.Tag(name='root')
        stack = [root]
        current_tag = root

        for tag in tags_data:
            if tag.name and not tag.is_open:
                tag.parent = current_tag
                current_tag.children.append(tag)
                stack.append(tag)
                current_tag = tag
            elif tag.name and tag.is_open:
                if not stack:
                    raise SyntaxError("Непарный закрывающий тег")

                last_tag = stack.pop()
                if last_tag.name != tag.name:
                    raise SyntaxError(f"Несоответствующий закрывающий тег: ожидался '{last_tag.name}', получен '{tag.name}'")

                if stack:
                    current_tag = stack[-1]
                else:
                    current_tag = root
            else:
                current_tag.text = tag.text

        if len(stack) > 1:
            raise SyntaxError("Незакрытые теги")

        return root
    
    def find(self, path):
        """
        Находит первый тег по заданному пути (например, "html/body/div").
        Возвращает None, если тег не найден.
        """
        tags = path.split("/")
        current = self.xml
        for tag_name in tags:
            found = None
            for child in current.children:
                if child.name == tag_name:
                    found = child
                    break
            if found is None:
                return self.Tag()
            current = found

        if current != None:
            return current
        return self.Tag()

    def findall(self, tag):
        """
        Находит все теги с именем tag_name, находящиеся по пути path.
        """
        tag_name = tag.split("/")[-1]
        path = tag[ : -1 * len(tag_name) - 1]

        def recursive_find_by_path(node, path_parts, tag_name, result):
            if not path_parts:  # Если путь пустой
                if node.name == tag_name: # Проверяем текущий узел
                    result.append(node)
                # Ищем tag_name среди потомков текущего узла
                for child in node.children:
                    recursive_find_by_path(child, [], tag_name, result) # Пустой путь - ищем везде

                return

            current_tag = path_parts[0] # Берем первый элемент пути

            for child in node.children:
                if child.name == current_tag:  # Нашли соответствие
                    recursive_find_by_path(child, path_parts[1:], tag_name, result) # Продолжаем поиск по оставшейся части пути


        path_parts = path.split("/")
        result = []
        recursive_find_by_path(self.xml, path_parts, tag_name, result)
        return result