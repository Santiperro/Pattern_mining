import pandas as pd


def convert_to_transactions(filename):

    data = pd.read_excel(filename)

    bachelors_data = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 3]
    majors_data = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 1]

    majors_data.reset_index(drop=True, inplace=True)
    bachelors_data.reset_index(drop=True, inplace=True)

    bachelors_id = bachelors_data['STUDENT_ID'].unique
    majors_id = bachelors_data['STUDENT_ID'].unique

    return majors_data, bachelors_data
