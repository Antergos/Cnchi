#!/usr/bin/python

import os

_4SH = '    - '
_8SH = '        - '
_8S = '        '


def get_dir_entries(path):
    """ Return all .py dir entries """
    dirs = os.scandir(path)
    entries = []
    invalid = ['.', '..', '__pycache__', '__init__.py']
    print("Scanning {} ...".format(path))
    for entry in dirs:
        if entry.name not in invalid:
            if entry.is_file() and entry.name.endswith('.py'):
                entries.append(entry)
            elif entry.is_dir():
                new_path = os.path.join(path, entry.name)
                entries.extend(get_dir_entries(new_path))
    return entries


def main():
    """ Create pydocmd.yml file """
    entries = get_dir_entries('../src')
    if os.path.exists('pydocmd.yml'):
        os.rename("pydocmd.yml",
                  "pydocmd.yml.backup")
    with open('pydocmd.yml', 'w') as pydocmd:
        pydocmd.write("site_name: Cnchi\n")

        pydocmd.write("generate:\n")
        for entry in entries:
            path = entry.path
            path = path.replace("../src", "src")
            path = path.replace("/", ".")
            path = path.replace(".py", "")
            pydocmd.write(_4SH + path + ".md:\n")
            pydocmd.write(_8SH + path + "+\n")

        pydocmd.write("\npages:\n")
        for entry in entries:
            path = entry.path
            path = path.replace("../src", "src")
            path = path.replace("/", ".")
            path = path.replace(".py", "")
            pydocmd.write(_4SH + path + ":\n")
            pydocmd.write(_8S + path + ".md\n")

        pydocmd.write("\n# These options all show off their default values. ")
        pydocmd.write("You don't have to add\n")
        pydocmd.write("# them to your configuration if you're fine with the default.\n")
        pydocmd.write("docs_dir: sources\n")
        pydocmd.write(
            "gens_dir: _build/pydocmd     # This will end up as the MkDocs 'docs_dir'\n")
        pydocmd.write("site_dir: _build/site\n")
        pydocmd.write("theme:    readthedocs\n")
        pydocmd.write("loader:   pydocmd.loader.PythonLoader\n")
        pydocmd.write("preprocessor: pydocmd.preprocessor.Preprocessor\n\n")

        pydocmd.write(
            "  # Additional search path for your Python module. If you use Pydocmd from a\n")
        pydocmd.write(
            "  # subdirectory of your project (eg. docs/), you may want to add the parent\n")
        pydocmd.write("  # directory here.\n")
        pydocmd.write("additional_search_paths:\n")
        pydocmd.write("    - ..\n")
        pydocmd.write("    - ../src\n")
        pydocmd.write("    - ../src/download\n")
        pydocmd.write("    - ../src/hardware\n")
        pydocmd.write("    - ../src/hardware/modules\n")
        pydocmd.write("    - ../src/installation/\n")
        pydocmd.write("    - ../src/misc\n")
        pydocmd.write("    - ../src/pages\n")
        pydocmd.write("    - ../src/parted3\n")
        pydocmd.write("    - ../src/widgets\n\n")

main()
