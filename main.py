import pandas as pd

filepath = '/Users/ryudai/Desktop/data_sfc/A_01.csv'

data = pd.read_csv(filepath)


data.to_csv('/Users/ryudai/Desktop/output.csv')