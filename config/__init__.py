from os import environ, listdir, path
import toml

def load():
    load_path = environ.get('TINYLAND_CONFIG', '.:./config/')
    dirs = load_path.split(':')
    files = []
    for d in dirs:
        config_files = [path.join(d, f) for f in listdir(d) if f.endswith('.toml')]
        files += config_files

    config = {}
    for f in files:
        config.update(toml.load(f))
    return config
