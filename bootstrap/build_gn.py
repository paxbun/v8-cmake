# Checking out the V8 source code: https://v8.dev/docs/build-gn

from .common import *
import sys
import os

def config_val_to_str(val):
    if type(val) == str:
        return '"{0}"'.format(val)
    elif type(val) == bool:
        if val: return "true"
        else: return "false"
    else:
        return '"{0}"'.format(str(val))

def config_to_str(config):
    return ' '.join([
        "{0}={1}".format(key, config_val_to_str(value))
        for key, value in config.items()
    ])

def get_config_str(debug=False):
    if sys.platform == "win32":
        if debug: return "x64.debug"
        else: return "x64.release"

def gen_build_files(config, config_str, root=os.getcwd()):
    v8_path = os.path.join(root, "v8")
    if not os.path.exists(os.path.join(v8_path, "out", config_str)):
        if sys.platform == "win32":
            run_cmd("gn", "gen" ,"out/{0}".format(config_str),
                    "--args={0}".format(config_to_str(config)), cwd=v8_path, root=root, print_result=True)
        else:
            pass

def compile_v8(config_str, target_name=None, root=os.getcwd()):
    v8_path = os.path.join(root, "v8")
    if sys.platform == "win32":
        args = ["ninja", "-C" ,"out/{0}".format(config_str)]
        if target_name:
            args.append(target_name)
        run_cmd(*args, cwd=v8_path, root=root, print_result=True)
    else:
        pass

def build_gn(config, config_str, target_name, root=os.getcwd()):
    print_colored("Building V8 with GN...")
    print_colored("See https://v8.dev/docs/build-gn for more information.")
    print_colored("Generating build files...")
    gen_build_files(config, config_str, root=root)
    print_colored("Compiling V8...")
    compile_v8(config_str, target_name, root=root)
