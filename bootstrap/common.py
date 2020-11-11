import os
import sys
import subprocess
try:
    import colorama
except:
    print("Installing colorama for colored output...")
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama"], check=True)
    import colorama

def make_env(root=os.getcwd()):
    env = os.environ.copy()
    depot_tools_path=os.path.join(root, "depot_tools")
    if sys.platform == "win32":
        env["PATH"] = depot_tools_path + ";" + env["PATH"]
        env["DEPOT_TOOLS_WIN_TOOLCHAIN"] = "0"
    else:
        env["PATH"] = depot_tools_path + ":" + env["PATH"]
    return env

def run(*args, env=None, cwd=os.getcwd(), print_result=False):
    print_colored(colorama.Fore.RED + "Running" + colorama.Fore.LIGHTCYAN_EX, *args)
    if print_result:
        stdout = None
    else:
        stdout = subprocess.PIPE
    subprocess.run([*args], cwd=cwd, check=True, env=env, stdout=stdout)

def run_cmd(*args, cwd=os.getcwd(), root=os.getcwd(), print_result=False):
    if sys.platform == "win32":
        run("cmd", "/c", *args, cwd=cwd, env=make_env(root), print_result=print_result)
    else:
        run(*args, cwd=cwd, env=make_env(root), print_result=print_result)

def print_colored(*args, **kwargs):
    print(colorama.Fore.LIGHTCYAN_EX + "Bootstrap:",
          *args,
          colorama.Style.RESET_ALL,
          **kwargs,
          flush=True)
