import argparse
import sys
from datetime import datetime

import pandas as pd

from src.utils import save_results
from src.devicelock_manager import (
    check_devicelock_on_comps,
    remove_devicelock_from_comps,
)

UNINSTALL_REG_PATH = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
KEYWORD = 'DeviceLock'


def parse_args():
    parser = argparse.ArgumentParser(description="Утилита для проверки и удаления DeviceLock с ПК.")

    # Аргумент type
    parser.add_argument(
        '-t', '--type',
        required=True,
        choices=['computers', 'departments'],
        help="Тип элемента: 'computers' (компьютеры) или 'departments' (подразделения)."
    )

    # Аргумент action
    parser.add_argument(
        '-a', '--action',
        required=True,
        choices=['check', 'remove'],
        help="Действие: 'check' (проверить) или 'remove' (удалить)."
    )

    # Аргументы filename и item-list
    parser.add_argument(
        '-f', '--filename',
        type=str,
        help="Имя файла с перечислением компьютеров или подразделений."
    )
    parser.add_argument(
        '-l', '--item-list',
        nargs='+',
        help="Список компьютеров или подразделений."
    )

    # Аргументы username и password
    parser.add_argument(
        '-u', '--username',
        type=str,
        help="Имя пользователя учетной записи, от которой будет выполняться PsExec"
    )
    parser.add_argument(
        '-p', '--password',
        type=str,
        help="Пароль к имени пользователя учетной записи от которой будет выполняться PsExec"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    username = args.username
    password = args.password

    # Проверка на наличие одновременно и filename, и item-list
    if args.filename and args.item_list:
        print("Ошибка: нельзя использовать одновременно --filename и --item-list.", file=sys.stderr)
        sys.exit(1)

    # Чтение списка компьютеров/подразделений
    if args.filename:
        try:
            with open(args.filename, 'r') as file:
                items = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Файл '{args.filename}' не найден.", file=sys.stderr)
            sys.exit(1)
    else:
        items = args.item_list

    # Действие check или remove с учётом типа
    df = None
    if args.action == 'check':
        df = check_devicelock_on_comps(items, args.type, username=username, password=password)
    elif args.action == 'remove':
        df = remove_devicelock_from_comps(items, args.type, username=username, password=password)

    filename = save_results(df)
    print(f'Результаты сохранены в {filename}')


if __name__ == "__main__":
    main()
