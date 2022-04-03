import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


min_sup = 0.3  # Минимальная поддержка


def mine():
    bachelors_df = pd.read_csv(r'C:\Users\megan\PycharmProjects\PatternMining\bachelors_transactions.csv')
    majors_df = pd.read_csv(r'C:\Users\megan\PycharmProjects\PatternMining\majors_transactions.csv')

    bachelors_df.rename(columns={'Unnamed: 0': 'Index'}, inplace=True)
    majors_df.rename(columns={'Unnamed: 0': 'Index'}, inplace=True)

    bachelors_df = bachelors_df.set_index('Index')
    majors_df = majors_df.set_index('Index')

    bachelors_matrix = pd.get_dummies(bachelors_df, columns=['0', '1', '2', '3', '4', '5', '6'])
    columns = list(bachelors_matrix.columns)
    for column in columns:
        bachelors_matrix.rename(columns={column: column[2:]}, inplace=True)

    freaquent_itemsets = apriori(bachelors_matrix, min_support=min_sup, use_colnames=True)

    rules = association_rules(freaquent_itemsets, metric='lift', min_threshold=1)

    print(bachelors_matrix)

mine()