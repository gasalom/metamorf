import sys, getopt
from metamorf.tools.log import Log
from metamorf.constants import *
from metamorf.engines.engine_init import EngineInit
from metamorf.engines.engine_deploy import EngineDeploy
from metamorf.engines.engine_validate import EngineValidate
from metamorf.engines.engine_upload import EngineUpload
from metamorf.engines.engine_process import EngineProcess
from metamorf.engines.engine_deploy_example import EngineDeployExample
from metamorf.engines.engine_download import EngineDownload
from metamorf.engines.engine_recover import EngineRecover
from metamorf.engines.engine_delete import EngineDelete
from metamorf.engines.engine_output import EngineOutput
from metamorf.engines.engine_run import EngineRun
from metamorf.engines.engine_backup import EngineBackup
from metamorf.engines.engine_manifest import EngineManifest
from metamorf.engines.engine_api import EngineApi
from metamorf.engines.engine_restore import EngineRestore
from metamorf.engines.engine_files import EngineFiles
from metamorf.engines.engine_metadata import EngineMetadata
from metamorf.tools.argparser import ArgParser
from metamorf.engines.engine_commit import EngineCommit
from metamorf.help import print_help

def main():
    os.system('')
    argp = ArgParser(sys.argv[1:])
    arguments = argp.get_arguments_parsed()
    if 'error' in arguments:
        print(COLOR_LIGHT_RED + "Error executing Metamorf: " + arguments['error'] + "\nFor more information run [metamorf help]" + COLOR_LIGHT_GRAY)
        return
    if arguments['command'] == 'help':
        print_help()
        return

    # SETUP LOG
    log = Log()
    log.log('METAMORF', '*********************************************************************', LOG_LEVEL_INFO)
    log.log('METAMORF', 'Running metamorf version "' + VERSION + '"', LOG_LEVEL_INFO)

    # COMMANDS
    if arguments['command'] == 'init':
        engine = EngineInit(log, arguments)
        engine.run()
    elif arguments['command'] == 'deploy':
        engine = EngineDeploy(log, arguments)
        engine.run()
    elif arguments['command'] == 'deploy-example':
        engine = EngineDeployExample(log, arguments)
        engine.run()
    elif arguments['command'] == 'validate':
        engine = EngineValidate(log, arguments)
        engine.run()
    elif arguments['command'] == 'upload':
        engine = EngineUpload(log, arguments)
        engine.run()
    elif arguments['command'] == 'process':
        engine = EngineProcess(log, arguments)
        engine.run()
    elif arguments['command'] == 'download':
        engine = EngineDownload(log, arguments)
        engine.run()
    elif arguments['command'] == 'commit':
        engine = EngineCommit(log, arguments)
        engine.run()
    elif arguments['command'] == 'recover':
        engine = EngineRecover(log, arguments)
        engine.run()
    elif arguments['command'] == 'delete':
        engine = EngineDelete(log, arguments)
        engine.run()
    elif arguments['command'] == 'output':
        engine = EngineOutput(log, arguments)
        engine.run()
    elif arguments['command'] == 'run':
        engine = EngineRun(log, arguments)
        engine.run()
    elif arguments['command'] == 'backup':
        engine = EngineBackup(log, arguments)
        engine.run()
    elif arguments['command'] == 'api':
        engine = EngineApi(log, arguments)
        engine.run()
    elif arguments['command'] == 'manifest':
        engine = EngineManifest(log, arguments)
        engine.run()
    elif arguments['command'] == 'restore':
        engine = EngineRestore(log, arguments)
        engine.run()
    elif arguments['command'] == 'files':
        engine = EngineFiles(log, arguments)
        engine.run()
    elif arguments['command'] == 'metadata':
        engine = EngineMetadata(log, arguments)
        engine.run()
    else:
        log.log('METAMORF', 'Command under development. More information at https://www.metamorf.io', LOG_LEVEL_CRITICAL)

    log.close()

if __name__ == "__main__":
   main()
