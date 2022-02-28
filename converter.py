import pandas as pd
import numpy as np


def nan_array_check(arr):
    for i in range(len(arr)):
        if i > len(arr) - 1:
            break
        if np.isnan(arr[i]):
            arr.pop(i)


def convert_to_transactions(filename):
    data = pd.read_excel(filename)

    bachelors_data = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 3]
    majors_data = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 1]

    majors_data.reset_index(drop=True, inplace=True)
    bachelors_data.reset_index(drop=True, inplace=True)

    bachelors_id = bachelors_data['STUDENT_ID'].unique()
    majors_id = majors_data['STUDENT_ID'].unique()

    bachelors_transactions = pd.DataFrame()

    for id in bachelors_id:
        terms = list(bachelors_data[bachelors_data['STUDENT_ID'].isin([id])]['TERM_NUM'].unique())
        nan_array_check(terms)

        id_adding_area = bachelors_data[bachelors_data['STUDENT_ID'].isin([id])]
        id_adding_area.reset_index(drop=True, inplace=True)

        for number in terms:
            term_adding_area = id_adding_area[id_adding_area['TERM_NUM'].isin([number])]
            term_adding_area.reset_index(drop=True, inplace=True)

            transaction = [f'Term{int(number)}']

            begin_year = term_adding_area['BEGIN_YEAR'][0]
            end_year = term_adding_area['END_YEAR'][0]
            transaction.append(f'{begin_year}-{end_year}')

            points = id_adding_area[id_adding_area['MARK_KIND'].isin(['1. Вступительные испытания'])]['MARK']

            if points.sum() / len(points) >= 80:
                transaction.append('HES')
            else:
                transaction.append('OES')

            if id_adding_area['STATUS_NAME'] == 'Отчислен':
                max_term = id_adding_area['TERM_NUM'].max()
                transaction.append(f'Expelled{max_term}')
            else:
                transaction.append('Finished')

            term_adding_area[term_adding_area['MARK_KIND'].isin(['2. Промежуточная аттестация'])]['MARK']

            print(transaction)
    return bachelors_data, majors_data


convert_to_transactions('data.xlsx')