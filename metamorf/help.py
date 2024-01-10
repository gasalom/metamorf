from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.constants import *
import os

def print_help():
    file_controller_properties = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
    file_controller_properties.set_file_location(os.path.join(PACKAGE_PATH, PROPERTIES_FILE_PATH), PROPERTIES_FILE_NAME)
    properties_file = file_controller_properties.read_file()

    print(properties_file['logo'] + '  ' + properties_file['version'])
    print()
    print(properties_file['description'])
    print()
    print('usage: metamorf [command] [arguments | optional] ')
    print()
    print('commands:')

    for com in properties_file['commands']:
        all_args = []
        if 'args' in com:
            for opt in com['args']:
                for x in opt['options']:
                    all_args.append(x)
        all_args_string = ""
        for x in all_args: all_args_string += x + ", "
        all_args_string = all_args_string[:-2]

        if all_args_string == "": print("  " + com['name'] + " : " + com['description'])
        else: print("  " + com['name'] + " : " + com['description'] + " Optional arguments [" + all_args_string + "]")