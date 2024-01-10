from metamorf.constants import *
from metamorf.tools.log import Log

class ConfigValidator:

    def __init__(self,properties_file: dict, configuration_file: dict, log: Log):
        self.modules = []
        self.databases = []
        self.properties_file = properties_file
        self.configuration_file = configuration_file
        self.log = log
        self.configvalidator_name = 'Configuration Validation'

    def validate(self):
        result_properties_file = self.validate_properties_file()
        result_configuration_file = self.validate_configuration_file()
        return result_configuration_file and result_properties_file

    def validate_properties_file(self):
        """Validate properties file. Get some functions that are used to validate configuration file."""
        #Options
        if 'options' not in self.properties_file:
            self.log.log(self.configvalidator_name, "PropertiesFile - [Options]: options section is mandatory.", LOG_LEVEL_ERROR)
            return False
        if 'log_print' not in self.properties_file['options']:
            self.log.log(self.configvalidator_name, 'PropertiesFile - Options -> Missing Value: log_print', LOG_LEVEL_ERROR)
            return False

        #Commands
        if 'commands' not in self.properties_file:
            self.log.log(self.configvalidator_name, "PropertiesFile - [Commands]: arguments section is mandatory.", LOG_LEVEL_ERROR)
            return False
        for com in self.properties_file['commands']:
            if 'name' not in com:
                self.log.log(self.configvalidator_name, "PropertiesFile - [Commands]: There are a command without name attribute", LOG_LEVEL_ERROR)
                return False
            if 'description' not in com:
                self.log.log(self.configvalidator_name, "PropertiesFile - [Commands]: There are a command without description attribute", LOG_LEVEL_ERROR)
                return False
            if 'args' in com:
                for arg in com['args']:
                    if 'name' not in arg or 'options' not in arg or 'values' not in arg:
                        self.log.log(self.configvalidator_name, "PropertiesFile - [Commands]: arguments on command ["+com['name']+"] need to have [name], [options] and [values].", LOG_LEVEL_ERROR)
                        return False

        #Properties
        if 'name' not in self.properties_file :
            self.log.log(self.configvalidator_name,"PropertiesFile - Missing Value: name", LOG_LEVEL_ERROR)
            return False
        if 'description' not in self.properties_file:
            self.log.log(self.configvalidator_name, "PropertiesFile - Missing Value: description", LOG_LEVEL_ERROR)
            return False
        if 'version' not in self.properties_file:
            self.log.log(self.configvalidator_name, "PropertiesFile - Missing Value: version", LOG_LEVEL_ERROR)
            return False
        if 'author' not in self.properties_file:
            self.log.log(self.configvalidator_name, "PropertiesFile - Missing Value: author", LOG_LEVEL_ERROR)
            return False
        if 'contact' not in self.properties_file:
            self.log.log(self.configvalidator_name, "PropertiesFile - Missing Value: contact", LOG_LEVEL_ERROR)
            return False

        # Modules
        if 'modules' not in self.properties_file:
            self.log.log(self.configvalidator_name, "PropertiesFile - [Modules]: modules section is mandatory.", LOG_LEVEL_ERROR)
            return False

        for m in self.properties_file['modules']:
            module = m['name']
            if module not in self.modules:
                self.modules.append(module)
            else:
                self.log.log(self.configvalidator_name, "PropertiesFile - Module: ' + module + ' -> Module Duplicate", LOG_LEVEL_ERROR)
                return False
            if 'version' not in m:
                self.log.log(self.configvalidator_name, "PropertiesFile - Module: ' + module + ' -> Missing Value: version", LOG_LEVEL_ERROR)
                return False
            if 'functions' not in m:
                self.log.log(self.configvalidator_name, "PropertiesFile - Module: ' + module + ' -> Missing Value: functions", LOG_LEVEL_ERROR)
                return False

            for x in m['functions']:
                if 'name' not in x:
                    self.log.log(self.configvalidator_name, 'PropertiesFile - Module: ' + module + ' - Function ' + str(x) + '-> Missing Value: name', LOG_LEVEL_ERROR)
                    return False
                if 'values' not in x:
                    self.log.log(self.configvalidator_name, 'PropertiesFile - Module: ' + module + ' - Function ' + str(x) + '-> Missing Value: values', LOG_LEVEL_ERROR)
                    return False

        #Metadata and Data
        if 'database' not in self.properties_file:
            self.log.log(self.configvalidator_name, "PropertiesFile - [Database]: database section is mandatory.", LOG_LEVEL_ERROR)
            return False

        for m in self.properties_file['database']:
            if 'name' not in m:
                self.log.log(self.configvalidator_name, "PropertiesFile - Database: There are a database without name attribute", LOG_LEVEL_ERROR)
                return False
            if 'mandatory_fields' not in m:
                self.log.log(self.configvalidator_name, "PropertiesFile - Database: There are a database without mandatory_fields attribute", LOG_LEVEL_ERROR)
                return False
            if m['name'] not in self.databases:
                self.databases.append(m['name'])
        return True

    def validate_configuration_file(self):
        if self.configuration_file is None:
            return

        #Properties
        if 'name' not in self.configuration_file:
            self.log.log(self.configvalidator_name, "ConfigurationFile - Missing Value: name", LOG_LEVEL_ERROR)
            return False
        if self.configuration_file['name'] is None:
            self.log.log(self.configvalidator_name, "ConfigurationFile - Missing Value: name", LOG_LEVEL_ERROR)
            return False

        if 'owner' not in self.configuration_file:
            self.log.log(self.configvalidator_name, "ConfigurationFile - Missing Value: owner", LOG_LEVEL_CRITICAL)
            return False
        if self.configuration_file['owner'] is None:
            self.log.log(self.configvalidator_name, "ConfigurationFile - Missing Value: owner", LOG_LEVEL_CRITICAL)
            return False

        if 'output' not in self.configuration_file:
            self.log.log(self.configvalidator_name, "ConfigurationFile - Missing Value: output", LOG_LEVEL_CRITICAL)
            return False

        # Validation OUTPUT get_type_options_for_output
        if 'type' not in self.configuration_file['output']:
            self.log.log(self.configvalidator_name, "ConfigurationFile - Output: The attribute [type] needs to be indicated", LOG_LEVEL_CRITICAL)
            return False

        if self.configuration_file['output']['type'] not in self.get_type_options_for_output():
            self.log.log(self.configvalidator_name, 'ConfigurationFile - Output: The attribute [output][type] has an impossible value', LOG_LEVEL_CRITICAL)
            return False
        if self.configuration_file['output']['type'] is None:
            self.log.log(self.configvalidator_name, "ConfigurationFile - Output: The attribute [output][type] needs to be indicated", LOG_LEVEL_CRITICAL)
            return False

        # Validation MODULES
        if 'modules' not in self.configuration_file:
            self.log.log(self.configvalidator_name, 'Configuration File - Modules: [modules] section is mandatory on the Configuration File.', LOG_LEVEL_ERROR)
            return False

        try:
            for m in self.configuration_file['modules']:
                if 'name' not in m:
                    self.log.log(self.configvalidator_name, 'ConfigurationFile - Modules: Need [name] attribute', LOG_LEVEL_ERROR)
                    return False
                if m['name'] not in self.modules:
                    self.log.log(self.configvalidator_name, 'ConfigurationFile - Module: ' + m['name'] + ' -> Doesn\'t exist: ' + m['name'], LOG_LEVEL_ERROR)
                    return False
                functions = self.get_functions_name_from_module(m['name'])
                for key,value in m.items():
                    if key=='name': continue
                    if key not in functions:
                        self.log.log(self.configvalidator_name, 'ConfigurationFile - Module: ' + m['name'] + ' -> Function: '+ key + ' doesn\'t exist', LOG_LEVEL_ERROR)
                        return False
                    values = self.get_options_from_function_and_module(m['name'], key)
                    if self.get_accept_all_values(m['name'], key): continue
                    if value not in values:
                        self.log.log(self.configvalidator_name, 'ConfigurationFile - Module: ' + m['name'] + ' -> Function: [' + key + '] has an impossible value', LOG_LEVEL_ERROR)
                        return False
        except Exception as e:
            self.log.log(self.configvalidator_name, "ConfigurationFile - Module: " + str(e), LOG_LEVEL_ERROR)


        # Validation Metadata
        if 'metadata' not in self.configuration_file:
            self.log.log(self.configvalidator_name, 'ConfigurationFile - Metadata: [metadata] section is mandatory on the Configuration File.', LOG_LEVEL_ERROR)
            return False

        metadata_information = self.configuration_file['metadata']
        if 'connection_type' not in metadata_information:
            self.log.log(self.configvalidator_name, 'ConfigurationFile - Metadata: The attribute [connection_type] needs to be indicated', LOG_LEVEL_ERROR)
            return False
        if metadata_information['connection_type'] is None:
            self.log.log(self.configvalidator_name, "[ERROR] ConfigurationFile - Metadata: The attribute [connection_type] needs to be indicated", LOG_LEVEL_CRITICAL)
            return False
        mandatory_fields = self.get_mandatory_fields_from_database(metadata_information['connection_type'])
            #First validation: All the fields are OK
        for key,value in metadata_information.items():
            if key=='connection_type': continue
            if key not in mandatory_fields:
                self.log.log(self.configvalidator_name, 'ConfigurationFile - Metadata: Field ' + key + ' is not an option for this database.', LOG_LEVEL_ERROR)
                return False
            #Second validation: There are all the fields indicated
        for key,value in metadata_information.items():
            if key=='connection_type': continue
            if value == None:
                self.log.log(self.configvalidator_name, 'ConfigurationFile - Metadata: Field ' + key + ' has not a value', LOG_LEVEL_ERROR)
                return False
            mandatory_fields.remove(key)
        if len(mandatory_fields)>0:
            self.log.log(self.configvalidator_name, 'ConfigurationFile - Metadata: The following attributes needs to be indicated to permit the connection: ' + str(mandatory_fields), LOG_LEVEL_ERROR)
            return False

        # Validation Data
        if 'data' not in self.configuration_file:
            self.log.log(self.configvalidator_name, 'ConfigurationFile - Data: [data] section is mandatory on the Configuration File.', LOG_LEVEL_ERROR)
            return False

        data_information = self.configuration_file['data']
        if 'connection_type' not in data_information:
            self.log.log(self.configvalidator_name, '[ERROR] ConfigurationFile - Data: The attribute [connection_type] needs to be indicated', LOG_LEVEL_ERROR)
            return False
        if data_information['connection_type'] is None:
            self.log.log(self.configvalidator_name, "[ERROR] ConfigurationFile - Data: The attribute [connection_type] needs to be indicated", LOG_LEVEL_CRITICAL)
            return False

        mandatory_fields = self.get_mandatory_fields_from_database(data_information['connection_type'])
        # First validation: All the fields are OK
        for key, value in data_information.items():
            if key == 'connection_type': continue
            if key not in mandatory_fields:
                self.log.log(self.configvalidator_name, 'ConfigurationFile - Metadata: Field ' + key + ' is not an option for this database.', LOG_LEVEL_ERROR)
                return False
            # Second validation: There are all the fields indicated
        for key, value in data_information.items():
            if key == 'connection_type': continue
            mandatory_fields.remove(key)
        if len(mandatory_fields) > 0:
            self.log.log(self.configvalidator_name, 'ConfigurationFile - Metadata: The following attributes needs to be indicated to permit the connection: ' + str(mandatory_fields), LOG_LEVEL_ERROR)
            return False

        return True


    def get_functions_name_from_module(self, module_name: str):
        functions = []
        for m in self.properties_file['modules']:
            if m['name'] == module_name:
                for x in m['functions']:
                    functions.append(x['name'])
        return functions

    def get_options_from_function_and_module(self, module_name: str, function_name: str):
        values = []
        for m in self.properties_file['modules']:
            if m['name'] == module_name:
                for x in m['functions']:
                    if x['name'] == function_name:
                        values = x['values']
        return values

    def get_accept_all_values(self, module_name: str, function_name: str):
        for m in self.properties_file['modules']:
            if m['name'] == module_name:
                for x in m['functions']:
                    if x['name'] == function_name:
                        if 'accept_all_values' in x:
                            if x['accept_all_values'].upper() == 'Y':
                                return True
        return False

    def get_mandatory_fields_from_database(self, database_name: str):
        result = []
        for m in self.properties_file['database']:
            if m['name'] == database_name:
                for x in m['mandatory_fields']:
                    result.append(x)
                return result
        raise ValueError('[ERROR] ConfigurationFile - The connection used: ['+ database_name + "] is not correct.")
        return None

    def it_exists_output_config(self, output_type: str, option_name: str, option_value: str):
        for x in self.properties_file['output']:
            if x['name'] == output_type:
                for y in x['options']:
                    if y['name'] == option_name and (option_value in y['values'] or y['values'] == []):
                        return True
        return False

    def get_type_options_for_output(self):
        return self.properties_file['output']['type']

