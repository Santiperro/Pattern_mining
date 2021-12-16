from converter import ConvertToTransactions
from pattern_miner import Mine
import output


majorsdata, bachelorsdata = ConvertToTransactions('data.xlsx')
patterns = Mine(bachelorsdata)
output.ToXLSX(patterns)