import zlib
import sys

def main(fname):
    with open(fname, 'rb') as f:
        data = f.read()
    
    d = zlib.decompress(data)
    print(d)

if __name__ == "__main__":
    fname = sys.argv[1]
    print(fname)
    main(fname)