import os
from dotenv import load_dotenv

ENV_FILE = '.env'

load_dotenv(ENV_FILE)

PS_EXEC_PATH = os.getenv('PSEXECPATH')
PROGRAM_NAME = os.getenv('PROGRAMNAME')

REGEDIT_UNINSTAL_PATH = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall'
