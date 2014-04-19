import lxml
import sys

def parse(content):
    return content

if __name__ == '__main__':
    f = open(sys.argv[1])
    print parse(f.read())
