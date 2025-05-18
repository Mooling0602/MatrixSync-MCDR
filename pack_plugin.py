#!/usr/bin/env python3
import configparser
import zipfile
import os
import sys

def add_directory_to_zip(zipf, dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, os.getcwd())
            zipf.write(full_path, arcname)

def main():
    config_file = "config.ini"
    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Not exist {config_file}!")
        
    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        framework_ver = config.get("framework", "ver")
        main_ver = config.get("main", "ver")
        is_stable = config.getint("release", "test")
        build_plg = config.getint("ci", "plugin")
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Config options error: {e}", file=sys.stderr)
        sys.exit(1)

    if build_plg == 1:
        if is_stable == 1:
            output_name = f"MatrixSync-v{main_ver}-{framework_ver}.mcdr"
            files_to_add = ["mcdreforged.plugin.json", "requirements.txt", "LICENSE"]
            dirs_to_add = ["lang", "matrix_sync"]
        else:
            output_name = f"MatrixSync-v{main_ver}.mcdr"
            files_to_add = ["README.md", "README_en_us.md", "mcdreforged.plugin.json", "requirements.txt", "LICENSE"]
            dirs_to_add = ["lang", "matrix_sync"]

        with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_add:
                if os.path.isfile(file):
                    zipf.write(file, os.path.relpath(file, os.getcwd()))
                else:
                    print(f"Warning: not exists {file}, skipped.")
            for dir_name in dirs_to_add:
                if os.path.isdir(dir_name):
                    add_directory_to_zip(zipf, dir_name)
                else:
                    print(f"Warning: not exists {dir_name}, skipped")

        print(f"Build success, output {output_name}")
    else:
        print("Build disabled, do nothing.")

if __name__ == "__main__":
    main()