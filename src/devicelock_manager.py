import subprocess
import re
from typing import Tuple

import pandas as pd

from src.settings import (
    PS_EXEC_PATH,
    REGEDIT_UNINSTAL_PATH,
    PROGRAM_NAME,
)
from src.utils import (
    get_psexec_cmd,
    get_remove_command
)


# Функция для выполнения команды на удалённом ПК и парсинга результата
def get_devicelock_guid(
        comp_name: str,
        username,
        password
) -> Tuple[bool, None | str]:
    command = get_psexec_cmd(
        comp_name=comp_name,
        command=f'reg query {REGEDIT_UNINSTAL_PATH} /f {PROGRAM_NAME} /s /d',
        username=username,
        password=password,
    )

    try:
        # Выполнение команды и сохранение вывода
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Ошибка при выполнении команды на {comp_name}: {stderr}")
            return False, None

        # Регулярное выражение для поиска GUID в фигурных скобках
        match = re.search(
            r'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{([A-F0-9\-]+)}',
            stdout,
            flags=re.IGNORECASE,
        )

        if match:
            guid = match.group(1)
            return True, guid
        else:
            return False, None
    except Exception as e:
        print(f"Ошибка: {e}")
        return False, None


def remove_devicelock(
        comp_name: str,
        username,
        password,
        guid: str = None,
) -> Tuple[bool, None | str]:
    if guid is None:
        res, guid = get_devicelock_guid(comp_name)
        if not res:
            return False, guid

    command = get_psexec_cmd(
        comp_name,
        command=get_remove_command(guid),
        waiting=False,
        username=username,
        password=password,
    )

    try:
        subprocess.Popen(
            command,
        )
        return True, guid
    except Exception as e:
        print(f"Ошибка: {e}")
        return False, guid


def check_devicelock_on_comps(
        items,
        item_type,
        username,
        password
):
    data = []
    size = len(items)

    for num, item in enumerate(items, start=1):
        res, guid = get_devicelock_guid(item, username, password)
        print(f'{num}/{size} Компьютер: {item} GUID: {guid}')

        data.append({
            'Name': item,
            'GUID': guid,
            'Note': res,
        })

    df = pd.DataFrame(data)

    return df


def remove_devicelock_from_comps(
        items,
        item_type,
        username,
        password
):
    # Логика удаления
    data = []
    size = len(items)

    for num, item in enumerate(items, start=1):
        res, guid = remove_devicelock(item, username, password)
        print(f'{num}/{size} '
              f'Компьютер: {item} '
              f'{res and "Задание на удаление отправлено" or "Проблема с удалением"} '
              f'GUID: {guid}')

        data.append({
            'Name': item,
            'GUID': guid,
            'Задание отправлено': res,
        })

    df = pd.DataFrame(data)

    return df