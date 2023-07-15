"""Напишите следующие функции:
Нахождение корней квадратного уравнения
Генерация csv файла с тремя случайными числами в каждой строке. 100-1000 строк.
Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла.
Декоратор, сохраняющий переданные параметры и результаты работы функции в json файл.
"""

import csv
import datetime
import json
import math
import os.path
from random import randint


def solve_csv(func):
    create_csv_file()
    def wrapper():
        with open('test.csv', 'r', encoding='UTF-8') as file:
            data = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
            """Константа csv.QUOTE_NONNUMERIC указывает объектам записи указывать все не числовые поля.
            Так же csv.QUOTE_NONNUMERIC указывает объекту чтения преобразовать все поля без кавычек в тип float."""
            for item in data:
                if item and item[0] != 0:
                    func(*item)

    return wrapper


def json_result(func):
    result = {}
    if os.path.exists('res.json'):
        with open('res.json', 'r', encoding='UTF-8') as file:
            result = json.load(file)

    def wrapper(*args):
        roots = func(*args)
        solve_dict = {'a': args[0], 'b': args[1], 'c': args[2], 'roots': roots}
        res_key = f'{datetime.datetime.now()}'[:-7]
        result[res_key] = result.get(res_key) + [solve_dict] if result.get(res_key) else [solve_dict]
        with open('res.json', 'w', encoding='UTF-8') as file:
            json.dump(result, file)
        return roots
    return wrapper


def create_csv_file():
    with open('test.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in range(randint(100, 1000)):
            writer.writerow([randint(-100, 100), randint(-100, 100), randint(-100, 100)])


@solve_csv
@json_result
def solve_square_equation(*args) -> tuple | float | None:
    a, b, c = args
    disc = b ** 2 - 4 * a * c
    if disc > 0:
        x1 = (-b + math.sqrt(disc)) / (2 * a)
        x2 = (-b - math.sqrt(disc)) / (2 * a)
        return round(x1, 2), round(x2, 2)
    elif disc == 0:
        x = -b / (2 * a)
        return round(x, 2)


solve_square_equation()