from text_funces import split_first_char, del_marks, staples_to_dict, tokenize, split_last_char

def is_active(text, pos):

    if text[pos - 1] == "\\":
        return not is_active(text, pos - 1)
    return True

class Fragment:
    def __init__(self, tag_data, tag_name, tag_isopen, tag_attributes):
        self.data = tag_data
        self.name = tag_name
        self.isopen = tag_isopen
        self.attributes = tag_attributes

    def __repr__(self):
        if self.name == None and self.isopen == None and self.attributes == None:
            return f"Fragment with text='{self.data}'"
        return f"Fragment with name='{self.name}', isopen='{self.isopen}', attributes='{self.attributes}'"

class XML:
    def __init__(self, text, name=None, attributes={}, text_on_parse=None):
        self.text = text
        self.xml = {}
        self.attributes = attributes
        self.fragments = []
        
        if text_on_parse == None:
            self.text_on_parse = text
        else:
            self.text_on_parse = text_on_parse

        if name == None:
            if len(tokenize(self.text_on_parse)) > 0:
                self.name = tokenize(self.text_on_parse)[1]
            else:
                self.name = ""
        else:
            self.name = name

        self.parse_xml()

        self.correct_text()

    def show(self, tabs=0):
        tab = " "*4
        if self.xml == {}:
            print(f"{tab * tabs} {self.name} {self.attributes}: '{self.text}'")
        else:
            if tabs == 0:
                print(f"{tab * tabs}XML-tree {self.name} {self.attributes} " + "{")
            else:
                print(f"{tab * tabs} {self.name} " + "{")

        for key in self.xml:
            value = self.xml[key]

            if value.name == None:
                print(f"{tab * tabs}{value.text}")
            else:
                value.show(tabs + 1)
        
        if self.xml != {}:
            print(f"{tab * tabs}" + " }")

    def parse_xml(self):
        def get_tag_data(text, pos):
            out = ""

            text = text[pos + 1:]

            opens = 1
            closes = 0

            i = -1
            while i < len(text) - 1:
                i += 1
                char = text[i]

                if char == "<" and is_active(text, i):
                    opens += 1

                if char == ">" and is_active(text, i):
                    closes += 1

                if opens == closes:
                    return "<" + out + ">"
                
                if char != "\\" or (char == "\\" and not is_active(text, i)):
                    out += char

            raise SyntaxError("Invalid syntax")
        
        def get_tag_name(data):
            if tokenize(data)[1] == "/":
                return tokenize(data)[2]
            return tokenize(data)[1]
        
        def get_tag_isopen(data):
            return not tokenize(data)[1] == "/"
        
        def get_tag_attributes(data):
            if not "=" in data:
                return {}
            
            tokens = tokenize(data)
            if tokens[1] == "/":
                if tokens[3] == ">":
                    return {}
                arg = tokens[3]
            else:
                if tokens[2] == ">":
                    return {}
                arg = tokens[2]

            text = f"{arg}={split_first_char(data, "=")[1]}"

            out = staples_to_dict(text)
            if ">" in out.keys():
                del out[">"]

                for key in out:
                    out[key] = del_marks(out[key])
                return out
            return out

        def parse_fragments(text):
            fragments = []

            data = ""

            in_marks = False

            i = -1
            while i < len(text) - 1:
                i += 1
                char = text[i]

                if char == "\"" and is_active(text, i):
                    in_marks = not in_marks

                if char == "<" and is_active(text, i) and not in_marks:
                    fragments.append(Fragment(data, None, None, None))
                    data = ""

                    tag_data = get_tag_data(text, i)
                    tag_name = get_tag_name(tag_data)
                    tag_isopen = get_tag_isopen(tag_data)
                    tag_attributes = get_tag_attributes(tag_data)
                    fragments.append(Fragment(tag_data, tag_name, tag_isopen, tag_attributes))

                    i += len(tag_data) - 1
                else:
                    if char != ">" or not is_active(text, i) or in_marks:
                        data += char

            self.fragments = fragments

        def get_fragment_content(pos):
            root_name = None
            root_fragment = None
            root_attributes = None

            opens = 1
            closes = 0

            fragments = []

            i = -1
            while i < len(self.fragments[pos:]) - 1:
                i += 1
                fragment = self.fragments[pos + i]
                fragment : Fragment

                if root_name == None:
                    if fragment.isopen:
                        root_name = fragment.name
                        root_fragment = fragment
                        root_attributes = fragment.attributes
                else:
                    if fragment.name == root_name and fragment.isopen:
                        opens += 1
                    elif fragment.name == root_name and not fragment.isopen:
                        closes += 1

                    if opens == closes:
                        text = ""
                        for fragment in fragments:
                            fragment : Fragment
                            text += fragment.data

                        xml = XML(text, root_name, root_attributes, f"{root_fragment.data}{text}</{root_fragment.name}>")
                        return xml
                    
                    fragments.append(fragment)
            else:
                raise SyntaxError(f"Unclosed root tag, root_name='{root_name}', opens={opens}, closes={closes}")

        parse_fragments(self.text_on_parse)

        root_name = None
        root = None

        opens = 1
        closes = 0

        content = []

        i = -1
        while i < len(self.fragments) - 1:
            i += 1
            fragment = self.fragments[i]
            fragment : Fragment

            if root_name == None:
                if fragment.isopen:
                    root_name = fragment.name
                    root = fragment
            else:
                if fragment.name == root_name and fragment.isopen:
                    opens += 1
                elif fragment.name == root_name and not fragment.isopen:
                    closes += 1

                if opens == closes:
                    break

                if fragment.name != None and fragment.name != root_name and fragment.isopen:
                    local_content = get_fragment_content(i)
                    content.append(local_content)
                    i += len(local_content.fragments) - 1

        i = -1
        while i < len(content) - 1:
            i += 1
            tag = content[i]
            tag : XML

            self.xml[f"{tag.name}_{i}"] = tag

        if root != None:
            self.attributes = root.attributes

    def correct_text(self):
        out = ""

        i = -1
        while i < len(self.text) - 1:
            i += 1
            char = self.text[i]

            if (not char in "\\") or not is_active(self.text, i):
                out += char

        self.text = out

    def __repr__(self, tabs=0):
        out = ""

        tab = " "*4
        if self.xml == {}:
            out += f"{tab * tabs} {self.name} {self.attributes}: '{self.text}'\n"
        else:
            if tabs == 0:
                out += f"{tab * tabs}XML-tree {self.name} {self.attributes} " + "{\n"
            else:
                out += f"{tab * tabs} {self.name} " + "{\n"

        for key in self.xml:
            value = self.xml[key]
            value : XML

            if value.name == None:
                out += f"{tab * tabs}{value.text}\n"
            else:
                out += value.__repr__(tabs + 1)
        
        if self.xml != {}:
            out += f"{tab * tabs}" + " }\n"
        
        return out

    def refind(self, path_els, pos):
        tag_name = path_els[pos]

        for key in self.xml:
            if split_last_char(key, ["_"])[0] == tag_name:
                if pos + 1 == len(path_els):
                    return self.xml[key]
                else:
                    return self.xml[key].refind(path_els, pos + 1)
        else:
            return XML("")

    def find(self, path : str):
        path_els = path.replace("/", "\\").split("\\")
        if path_els[0] != self.name:
            return XML("")
        path_els = path_els[1:]

        if len(path_els) == 0:
            return self
        
        return self.refind(path_els, 0)
    
    def findall(self, path : str):
        tag_path, tag_name = split_last_char(path, ["\\", "/"])
        xml = self.find(tag_path).xml

        out = []
        for key in xml:
            if split_last_char(key, ["_"])[0] == tag_name:
                out.append(xml[key])

        return out