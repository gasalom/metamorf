from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.constants import *
import os

class ArgParser:

    def __init__(self, arguments: list):
        self.arguments = arguments
        file_controller_properties = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_properties.set_file_location(os.path.join(PACKAGE_PATH, PROPERTIES_FILE_PATH), PROPERTIES_FILE_NAME)
        self.properties_file = file_controller_properties.read_file()
        self.all_commands = self.get_all_commands()

    def get_arguments_parsed(self):
        """Returns a dictionary with all the arguments parsed"""
        result = {}
        if len(self.arguments)==0:
            result['error'] = "No parameter specified."
            return result

        if self.arguments[0] not in self.all_commands:
            result['error'] = "The command ["+ self.arguments[0]+ "] does not exist."
            return result
        result['command'] = self.arguments[0]

        all_options_available = self.get_options_from_command(result['command'])

        all_options = self.arguments[1:]
        pass_iteration = False
        for index, arg in enumerate(all_options):
            if pass_iteration:
                pass_iteration = False
                continue
            if arg.lower() in all_options_available:
                values = self.get_values_from_command_and_option(result['command'], arg)
                accept_all_values = self.get_accept_all_values_from_command_and_option(result['command'], arg)
                if all_options[index+1].lower() in [x.lower() for x in values] or accept_all_values=='Y':
                    result[self.get_name_from_command_and_option(result['command'], arg)] = all_options[index+1]
                else:
                    result['error'] = "The command [" + self.arguments[0]+ "] with the argument [" + arg + "] does not accept the value [" + all_options[index+1] + "]"
                pass_iteration = True
            else:
                result['error'] = "The command [" + self.arguments[0]+ "] does not accept the argument [" + arg + "]"
                return result
                break
        return result

    def get_all_commands(self):
        all_commands = []
        for command in self.properties_file['commands']:
            all_commands.append(command['name'])
        return all_commands

    def get_options_from_command(self, command: str):
        all_options = []
        for com in self.properties_file['commands']:
            if com['name'] == command:
                if 'args' not in com: return all_options
                for opt in com['args']:
                    for d in opt['options']:
                        all_options.append(d)
        return all_options

    def get_accept_all_values_from_command_and_option(self, command: str, option: str):
        accept_all_values = "N"
        for com in self.properties_file['commands']:
            if com['name'] == command:
                if 'args' not in com: return accept_all_values
                for opt in com['args']:
                    if option in opt['options']:
                        if 'accept_all_values' in opt:
                            accept_all_values = opt['accept_all_values']
        return accept_all_values

    def get_values_from_command_and_option(self, command: str, option: str):
        all_values = []
        for com in self.properties_file['commands']:
            if com['name'] == command:
                if 'args' not in com: return all_values
                for opt in com['args']:
                    if option in opt['options']:
                        all_values = opt['values']
                        break
        return all_values

    def get_name_from_command_and_option(self, command: str, option: str):
        name = None
        for com in self.properties_file['commands']:
            if com['name'] == command:
                if 'args' not in com: return name
                for opt in com['args']:
                    if option in opt['options']:
                        name = opt['name']
                        break
        return name