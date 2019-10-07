from os import environ, listdir, path
from functools import reduce
import toml

# from https://stackoverflow.com/a/7205107
def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            else:
                pass # same leaf value
        else:
            a[key] = b[key]
    return a

class OpenStruct:
    def __init__(self, data):
        self.keys = data.keys();
        for key, val in data.items():
            if isinstance(val, dict):
                val = OpenStruct(val)
            setattr(self, key, val)
    def __repr__(self):
        data = [f"'{key}': {getattr(self, key)}"
                for key in self.keys]
        return f"OpenStruct({{{','.join(data)}}})"

def load():
    load_path = environ.get('TINYLAND_CONFIG', '.:./config/')
    dirs = load_path.split(':')
    files = [[ path.join(d, f)
               for f in listdir(d)
               if f.endswith('.toml')]
             for d in dirs]

    config = reduce(merge, [toml.load(f) for f in files])
    return OpenStruct(config)
