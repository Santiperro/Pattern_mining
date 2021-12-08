from transactional_transformer import transform as tf
from pattern_miner import search
import output


majorsdata, bachelorsdata = tf('data.xlsx')
patternss = search(bachelorsdata)
output.toXLSX(patternss)
