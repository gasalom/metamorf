import src.metamorf.utils as utils
import src.metamorf.tools as tools
import src.metamorf as metamorf

file = utils.FileControllerFactory().get_file_reader(metamorf.FILE_TYPE_YML)
file.set_file_location(r'C:\Users\guill\Documents\GitHub\metamorf\src\configuration', 'configuration.yml')
configurationFile = file.read_file()

file = utils.FileControllerFactory().get_file_reader(metamorf.FILE_TYPE_YML)
file.set_file_location(r'C:\Users\guill\Documents\GitHub\metamorf\src\configuration', 'properties.yml')
propertiesFile = file.read_file()

validator = tools.ConfigValidator(propertiesFile,configurationFile )
validator.validate()