from importlib.util import find_spec

def packages_are_installed(packages):
    for package in packages:
        if find_spec(package) is None:
            return False
    return True
