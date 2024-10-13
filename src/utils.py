from datetime import datetime

from src.settings import (
    PS_EXEC_PATH,
)


def get_remove_command(guid):
    return f'MsiExec.exe /X{{{guid}}}'


def get_psexec_cmd(
        comp_name,
        command,
        username: str,
        password: str,
        waiting: bool = True
):
    return f'{PS_EXEC_PATH} \\\\{comp_name} {waiting and '-d ' or ''}-u {username} -p {password} cmd /C "{command}"'


def save_results(df):
    now = datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = f'results_{now}.xlsx'

    df.to_excel(filename, index=False)

    return filename
