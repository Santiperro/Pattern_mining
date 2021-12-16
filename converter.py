import pandas as pd
import numpy as np


def ConvertToTransactions(filename):
    print("Transformation to transactions")
    data = pd.read_excel(filename)
    majorsdata = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 1]
    majorsdata.reset_index(drop=True, inplace=True)
    bachelorsdata = data[data['END_YEAR'] - data['BEGIN_YEAR'] == 3]
    bachelorsdata.reset_index(drop=True, inplace=True)
    return majorsdata, bachelorsdata
