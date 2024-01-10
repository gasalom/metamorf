from metamorf.tools.filecontroller import FileControllerFactory
from metamorf.constants import *
from datetime import datetime
import os

class Log:

    def __init__(self):
        file_controller_properties = FileControllerFactory().get_file_reader(FILE_TYPE_YML)
        file_controller_properties.set_file_location(os.path.join(PACKAGE_PATH, PROPERTIES_FILE_PATH), PROPERTIES_FILE_NAME)
        self.properties_file = file_controller_properties.read_file()

        os.system('')
        self.file_log = FileControllerFactory().get_file_reader(FILE_TYPE_LOG)
        self.file_log.set_file_location(ACTUAL_PATH, LOG_FILE_NAME)
        self.file_log.setup_writer(FILE_WRITER_APPEND)

        actual_size_log_file = os.stat(self.file_log.final_path).st_size / (1024*1024)
        if 'options' not in self.properties_file: return
        if 'max_size_mega_bytes_log_file' not in self.properties_file['options']: return
        if actual_size_log_file > self.properties_file['options']['max_size_mega_bytes_log_file']:
            self.file_log.close()
            os.rename(self.file_log.final_path, self.file_log.final_path+"."+datetime.now().strftime("%Y%m%d%H%M%S"))
            self.file_log = FileControllerFactory().get_file_reader(FILE_TYPE_LOG)
            self.file_log.set_file_location(ACTUAL_PATH, LOG_FILE_NAME)
            self.file_log.setup_writer(FILE_WRITER_APPEND)


    def log(self, subject: str, message: str, level: int):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file_log.write_file(date_now + " [" + subject + "] " + message + "\n")
        message = self._get_message_with_color(level, message)
        if 'options' not in self.properties_file: return
        if 'log_print' not in self.properties_file['options']: return
        if level == LOG_LEVEL_ONLY_LOG: return
        if self.properties_file['options']['print_debug'] == 'N' and level == LOG_LEVEL_DEBUG: return
        if self.properties_file['options']['log_print'] == "Y":
            print(COLOR_LIGHT_GRAY + date_now + " " + COLOR_DEFAULT + "["
                  + COLOR_DARK_GRAY + subject +
                  COLOR_DEFAULT + "]" + "" + COLOR_DEFAULT + ": " + message)

    def close(self):
        self.file_log.close()

    def _get_message_with_color(self, level: int, message: str):
        result = COLOR_RED + message + COLOR_DEFAULT
        if level == LOG_LEVEL_DEBUG:
            result = COLOR_BLUE + message + COLOR_DEFAULT
        if level == LOG_LEVEL_INFO or level == LOG_LEVEL_ONLY_LOG:
            result = COLOR_DEFAULT + message + COLOR_DEFAULT
        if level == LOG_LEVEL_WARNING:
            result = COLOR_YELLOW + message + COLOR_DEFAULT
        if level == LOG_LEVEL_ERROR:
            result = COLOR_LIGHT_RED + message + COLOR_DEFAULT
        if level == LOG_LEVEL_CRITICAL:
            result = COLOR_RED + message + COLOR_DEFAULT
        if level == LOG_LEVEL_OK:
            result = COLOR_GREEN + message + COLOR_DEFAULT
        return result