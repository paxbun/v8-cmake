# Checking out the V8 source code: https://v8.dev/docs/source-code

from .common import *
import sys
import os
import shutil
import urllib.request

def install_depot_tools(root=os.getcwd(), skip_intall_if_exists=True):
    out_path = os.path.join(root, "depot_tools")
    if os.path.exists(out_path):
        if os.path.isdir(out_path):
            if not skip_intall_if_exists:
                os.removedirs(out_path)
        else:
            os.remove(out_path)
    if os.path.exists(out_path) and skip_intall_if_exists:
        return out_path
    if sys.platform == "win32":
        url = "https://storage.googleapis.com/chrome-infra/depot_tools.zip"
        zip_path = os.path.join(root, "depot_tools.zip")
        with urllib.request.urlopen(url) as i:
            with open(zip_path, "wb") as o:
                o.write(i.read())
        shutil.unpack_archive(zip_path, out_path)
        os.remove(zip_path)
    else:
        url = "https://chromium.googlesource.com/chromium/tools/depot_tools.git"
        run("git", "clone", url, cwd=root)
    return out_path

def update_depot_tools(root=os.getcwd()):
    run_cmd("gclient", cwd=root, root=root)

def v8_src_downloaded(root=os.getcwd()):
    gclient_path = os.path.join(root, ".gclient")
    if os.path.exists(gclient_path):
        with open(gclient_path, "r") as gclient:
            return gclient.read().find('"name": "v8"') != -1
    return False

def get_v8_src_code(root=os.getcwd()):
    run_cmd("fetch", "v8", cwd=root, root=root, print_result=True)

def download_all_build_deps(root=os.getcwd()):
    run_cmd("gclient", "sync", cwd=root, root=root, print_result=True)

def switch_to_version(version, root=os.getcwd()):
    v8_path = os.path.join(root, "v8")
    run_cmd("git", "checkout", "tags/{0}".format(version), cwd=v8_path, root=root, print_result=True)

def download_additional_build_deps(root=os.getcwd()):
    if sys.platform == "linux":
        script_path = os.path.join(root, "v8", "build", "install-build-deps.sh")
        run_cmd(script_path, cwd=root, root=root, print_result=True)

def checkout(version, root=os.getcwd()):
    print_colored("Checking out the V8 source code...")
    print_colored("See https://v8.dev/docs/source-code for more information.")
    if not v8_src_downloaded(root=root):
        print_colored("Installing depot_tools...")
        install_depot_tools(root=root)
        print_colored("Updating depot_tools... This may take some time.")
        update_depot_tools(root=root)
        print_colored("Retrieving V8 source code...")
        get_v8_src_code(root=root)
        print_colored("Downloading all the build dependencies...")
        download_all_build_deps(root=root)
        print_colored("Downloading additional build dependencies...")
        download_additional_build_deps(root=root)
    print_colored("Switch to version {0}".format(version))
    switch_to_version(version, root=root)
