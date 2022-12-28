import pandas as pd

filepath = '/Users/ryudai/Desktop/data_sfc/A_02.csv'

data = pd.read_csv(filepath)

data60 = data.loc[ 0 : 59 , 'date':'steps']

data60.to_csv('/Users/ryudai/Desktop/output.csv')