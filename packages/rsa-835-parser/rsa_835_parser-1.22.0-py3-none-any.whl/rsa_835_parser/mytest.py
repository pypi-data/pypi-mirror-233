"""Testing rsa-835-parser"""
from rsa_835_parser import parse

PATH = "C:/Users/robsu/Downloads/cigna_20230201_230128090045547.835"
transaction_set = parse(PATH)

data = transaction_set.to_dataframe()
data.to_csv("C:/Users/robsu/Downloads/cigna_20230201_230128090045547.csv")