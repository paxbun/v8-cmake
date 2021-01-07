from .common import *
import os

def write_defs(config, config_str, target_name, root=os.getcwd()):
    v8_path = os.path.join(
        root, "v8", "out", config_str, "obj", target_name + ".ninja")
    config_path = os.path.join(
        root, "config")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    config_path = os.path.join(config_path, "definitions." + config_str + ".txt")

    with open(v8_path, "r") as config_file:
        line = config_file.readline()
    if line.startswith("defines = "):
        line = line[len("defines = "):]
    with open(config_path, "w") as config_file:
        line = line.replace(" ", ";")
        line = line.replace(r"\"", "\"")
        line = line.replace("-D", "")
        line = line.strip()
        config_file.write(line)