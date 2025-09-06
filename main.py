import sys
from preprocessor import preprocess
from parser import parse
from builder import build

def main():
    Path = ""
    for i in sys.executable.split("\\")[:-1]:
        Path += i + "\\"
    Path = Path[:-1]

    with open(Path + "\\file_path.txt", "r") as f:
        path = ""

        for i in f.read().replace("/", "\\").split("\\"):
            path += i + "\\"
        path = path[:-1]

    code, msg = preprocess(path)
    print("\n" + msg + "\n")

    code, msg, data = parse(path)
    print("\n" + msg + "\n")

    code, msg = build(data, Path)
    print("\n" + msg + "\n")

if __name__ == "__main__":
    main()