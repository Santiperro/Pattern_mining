from converter import convert_to_transactions
from pattern_miner import mine
import output


majors_data, bachelors_data = convert_to_transactions('data.xlsx')
patterns = mine(bachelors_data)
output.to_xlsx(patterns)
