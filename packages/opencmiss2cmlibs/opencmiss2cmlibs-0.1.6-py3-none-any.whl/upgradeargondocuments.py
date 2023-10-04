import json
import optparse
import os
import sys

OLD_KEY = "OpenCMISS-Argon Version"
NEW_KEY = "CMLibs Argon Version"


def refactor_file(filename):
    try:
        with open(filename) as f:
            json_data = json.load(f)

        if OLD_KEY in json_data:
            json_data[NEW_KEY] = ["0", "4", "0"]
            del json_data[OLD_KEY]

            with open(filename, "w") as f:
                json.dump(json_data, f, default=lambda o: o.__dict__, sort_keys=True, indent=2)

    except json.decoder.JSONDecodeError:
        pass


def main(args):
    parser = optparse.OptionParser(usage="upgradeargondocument [options] file|dir ...")

    # Parse command line arguments
    options, args = parser.parse_args(args)

    if not args:
        return 1

    input_base_dir = os.path.commonprefix(args)
    if (input_base_dir and not input_base_dir.endswith(os.sep)
            and not os.path.isdir(input_base_dir)):
        # One or more similar names were passed, their directory is the base.
        # os.path.commonprefix() is ignorant of path elements, this corrects
        # for that weird API.
        input_base_dir = os.path.dirname(input_base_dir)

    json_ext = os.extsep + "json"
    for dir_path, dir_names, filenames in os.walk(input_base_dir):
        dir_names.sort()
        filenames.sort()
        for name in filenames:
            if (not name.startswith(".") and
                    os.path.splitext(name)[1] == json_ext):
                fullname = os.path.join(dir_path, name)
                refactor_file(fullname)
        # Modify dir_names in-place to remove subdirs with leading dots
        dir_names[:] = [dn for dn in dir_names if not dn.startswith(".")]


def entry_point():
    return main(sys.argv[1:])


if __name__ == "__main__":
    entry_point()
