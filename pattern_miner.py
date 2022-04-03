import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


def digit_search(string):  # Нахождение и возврат цифр из строки
    digits = ''
    for s in string:
        if s.isdigit():
            digits += s
    return digits


def translate(column, _goods_dict):  # Перевод массива кодовых товаров в понимаемые
    for i in range(len(column)):
        cell = list(column[i])
        for j in range(len(cell)):
            for k in range(len(_goods_dict)):
                if _goods_dict['good'][k] in cell[j]:
                    digit = digit_search(cell[j])
                    cell[j] = str(_goods_dict['semantics'][k]) + digit
        column[i] = cell
    return column


# Используемый словарь для декодирования товаров
goods_dict = pd.read_excel(r'C:\Users\megan\PycharmProjects\PatternMining\dictionary_of_goods.xlsx')


def mine(transactions, _min_supp): # Поиск шаблонов с установаленной минимальной поддержкой

    # Преобразование в вид разреженной матрицы
    columns = list(transactions.columns)
    transactions_matrix = pd.get_dummies(transactions, columns=columns)

    # Редактирование названий столбцов
    columns = list(transactions_matrix.columns)
    for column in columns:
        transactions_matrix.rename(columns={column: column[2:]}, inplace=True)

    # Поиск частых наборов с параметром минимальной поддержки
    freaquent_itemsets = apriori(transactions_matrix, min_support=_min_supp, use_colnames=True)

    # Поиск ассоциативных правил с заданной метрикой и её минимальным значением
    rules = association_rules(freaquent_itemsets, metric='lift', min_threshold=1)

    # Перевод столбцов антецендента и консеквента в понимаемый вид
    rules['antecedents'] = translate(list(rules['antecedents']), goods_dict)
    rules['consequents'] = translate(list(rules['consequents']), goods_dict)

    return rules


# ts = pd.read_csv('bachelors_transactions.csv')
# print(mine(ts, 0.25))
