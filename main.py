from transactional_transformer import transform as tf
from pattern_miner import search
import output


majorsdata, bachelorsdata = tf('data.xlsx')
patterns = search(bachelorsdata)
output.toXLSX(patterns)
