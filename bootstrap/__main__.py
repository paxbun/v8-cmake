from .checkout import checkout
from .build_gn import build_gn
from .defs import write_defs
import sys
import os

# Check platform
supported_os_list = ["win32", "linux"] # ["win32", "linux", "darwin"]
if sys.platform not in supported_os_list:
    print_colored("Fatal error: platform '{0}' is not supported".format(sys.platform))
    exit(1)

def parse_val(arg: str):
    if arg == "true":
        return True
    elif arg == "false":
        return False
    else:
        return arg

def parse_arg(arg: str):
    assert arg.startswith("--")
    arg = arg[2:]
    split = arg.split("=")
    assert len(split) == 2
    return (split[0].lower().replace("-", "_"), parse_val(split[1]))

def parse_args(args):
    return {
        key : val
        for key, val in [parse_arg(arg) for arg in args]
    }

if __name__ == '__main__':
    config = parse_args(sys.argv[1:])
    version = config.pop("version")
    config_str = config.pop("config_str")
    target_name = config.pop("target_name")
    root = os.getcwd()
    if "root" in config:
        root = config.pop("root")

    checkout(version=version, root=root)
    build_gn(config=config, config_str=config_str, target_name=target_name, root=root)
    write_defs(config=config, config_str=config_str, target_name=target_name, root=root)


# python -m bootstrap             \
#     --version=8.7.220.3         \
#     --config-str=x64.release    \
#     --target-name=v8_monolith   \
#     --is-component-build=false  \
#     --is-debug=false            \
#     --is-clang=false            \
#     --target-cpu=x64            \
#     --use-custom-libcxx=false   \
#     --use-lld=false             \
#     --v8-monolithic=true        \
#     --v8-use-external-startup-data=false