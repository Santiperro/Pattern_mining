import pandas as pd
import numpy as np


hes_limit = 80  # Установленный лимит среднего балла для высокобальника

hqap_percentages = [50, 75, 85, 100]  # Установленные проценты оценок не ниже 4 за сессию


def nan_array_check(arr):
    for i in range(len(arr)):
        if i > len(arr) - 1:
            break
        if np.isnan(arr[i]):
            arr.pop(i)


def add_transactions(data):
    transactions = []

    ids = data['STUDENT_ID'].unique()

    for id in ids:
        terms = list(data[data['STUDENT_ID'].isin([id])]['TERM_NUM'].unique())
        nan_array_check(terms)

        id_adding_area = data[data['STUDENT_ID'].isin([id])]
        id_adding_area.reset_index(drop=True, inplace=True)

        for number in terms:
            term_adding_area = id_adding_area[id_adding_area['TERM_NUM'].isin([number])]
            term_adding_area.reset_index(drop=True, inplace=True)

            transaction = [f'Term{int(number)}']

            begin_year = term_adding_area['BEGIN_YEAR'][0]
            end_year = term_adding_area['END_YEAR'][0]
            transaction.append(f'{begin_year}-{end_year}')

            points = id_adding_area[id_adding_area['MARK_KIND'].isin(['1. Вступительные испытания'])]['MARK']
            if points.sum() / len(points) >= hes_limit:
                transaction.append('HES')
            else:
                transaction.append('OES')

            if id_adding_area['STATUS_NAME'][0] == 'отчислен':
                max_term = id_adding_area['TERM_NUM'].max()
                transaction.append(f'Expelled{int(max_term)}')
            else:
                transaction.append('Finished')

            marks = term_adding_area[term_adding_area['MARK_KIND'].isin(['2. Промежуточная аттестация'])]['MARK']
            cur_percent = -50
            for percent in hqap_percentages:
                if len(marks) != 0:
                    if len(marks[marks >= 4]) / len(marks) * 100 >= percent:
                        cur_percent = percent
            transaction.append(f'HQAP{int(cur_percent)}')

            fqw = id_adding_area[id_adding_area['SUBJECT_NAME'].isin(['Защита выпускной квалификационной работы'])]['MARK']
            if not fqw.empty:
                transaction.append(f'FQW{int(fqw)}')

            if term_adding_area['IS_REEXAM'].isin(['пересдача']).any():
                transaction.append('Retake')
            else:
                transaction.append('NoRetake')

            transactions.append(transaction)

    return pd.DataFrame(transactions)


def convert_to_transactions(filename):
    data = pd.read_excel(filename)

    bachelors_data = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 3]
    majors_data = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 1]

    majors_data.reset_index(drop=True, inplace=True)
    bachelors_data.reset_index(drop=True, inplace=True)

    bachelors_transactions = add_transactions(bachelors_data)
    majors_transactions = add_transactions(majors_data)

    return bachelors_transactions, majors_transactions
