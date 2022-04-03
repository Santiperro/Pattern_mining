from converter import convert_to_transactions
from pattern_miner import mine
from output import to_xlsx


bachelors_data, majors_data = convert_to_transactions('data.xlsx')  # Преобразование данных в транзакции

bachelors_patterns = mine(bachelors_data, 0.25)  # Поиск шаблонов с установаленной минимальной поддержкой
majors_patterns = mine(majors_data, 0.4)

# Импорт в excel
to_xlsx(bachelors_patterns, r'C:\Users\megan\PycharmProjects\PatternMining\translated_bachelors_rules.xlsx')
to_xlsx(majors_patterns, r'C:\Users\megan\PycharmProjects\PatternMining\translated_majors_rules.xlsx')
