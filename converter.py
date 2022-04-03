import pandas as pd
import numpy as np

hes_limit = 80  # Установленный лимит среднего балла для высокобальника

hqap_percentages = [50, 75, 85, 100]  # Установленные проценты оценок не ниже 4 за сессию


# Удаление всех элементов nan из массива
def nan_array_check(arr):
    for i in range(len(arr)):
        if i > len(arr) - 1:
            break
        if np.isnan(arr[i]):
            arr.pop(i)


# Добавление транзакций
def add_transactions(data):
    transactions = []

    ids = data['STUDENT_ID'].unique()  # Список всех уникальных идентификаторов студнентов

    for id in ids:
        terms = list(data[data['STUDENT_ID'].isin([id])]['TERM_NUM'].unique())  # Список номеров семестров
        nan_array_check(terms)  # Удаление элементов nan

        id_adding_area = data[data['STUDENT_ID'].isin([id])]  # Область данных только со значением конкрентного id
        id_adding_area.reset_index(drop=True, inplace=True)

        for number in terms:
            term_adding_area = id_adding_area[id_adding_area['TERM_NUM'].isin([number])]  # Область данных со значением
            term_adding_area.reset_index(drop=True, inplace=True)                    # конкретного id и номера семестра

            transaction = [f'Term{int(number)}']  # Добавление товара семестра

            begin_year = term_adding_area['BEGIN_YEAR'][0]  # Добавление товара годов обучения
            end_year = term_adding_area['END_YEAR'][0]
            transaction.append(f'{begin_year}-{end_year}')

            # Добавление товара высоких или средних баллов
            points = id_adding_area[id_adding_area['MARK_KIND'].isin(['1. Вступительные испытания'])]['MARK']
            if (len(points) != 0) and (points.sum() / len(points) >= hes_limit):
                transaction.append('HES')
            else:
                transaction.append('OES')

            if id_adding_area['STATUS_NAME'][0] == 'отчислен':  # Добавление товара закончил или отчислен
                max_term = id_adding_area['TERM_NUM'].max()
                transaction.append(f'Expelled{int(max_term)}')
            else:
                transaction.append('Finished')

            # Добавление товара с средней качественной успеваемостью
            marks = term_adding_area[term_adding_area['MARK_KIND'].isin(['2. Промежуточная аттестация'])]['MARK']
            cur_percent = -50
            for percent in hqap_percentages:
                if len(marks) != 0:
                    if len(marks[marks >= 4]) / len(marks) * 100 >= percent:
                        cur_percent = percent
            transaction.append(f'HQAP{int(cur_percent)}')

            # Добавление товара с оценкой защиты ВКР
            fqw = id_adding_area[id_adding_area['SUBJECT_NAME'].isin(['Защита выпускной квалификационной работы'])][
                'MARK']
            if not fqw.empty:
                transaction.append(f'FQW{int(fqw)}')
            else:
                transaction.append('NoFQW')

            # Добавление товара пересдача или не пересдача
            if term_adding_area['IS_REEXAM'].isin(['пересдача']).any():
                transaction.append('Retake')
            else:
                transaction.append('NoRetake')

            transactions.append(transaction)

    return pd.DataFrame(transactions)


# Разделение данных на данные для бакалавров и магистров, преобразование их в транзации
def convert_to_transactions(filename):
    data = pd.read_excel(filename)

    bachelors_data = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 3]  # Разделение данных о бакалаврах и магистрах
    majors_data = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 1]

    majors_data.reset_index(drop=True, inplace=True)
    bachelors_data.reset_index(drop=True, inplace=True)

    bachelors_transactions = add_transactions(bachelors_data)  # Преобразования данных в транзакции
    majors_transactions = add_transactions(majors_data)

    return bachelors_transactions, majors_transactions

