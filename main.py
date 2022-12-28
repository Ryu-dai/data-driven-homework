import pandas as pd

class Data1:
    def __init__(self):
        self.filepathroot = '/Users/ryudai/Desktop/data_sfc/A_01.csv'

        self.filepath = self.filepathroot + self.filepath
        pass

class Data2:
    def __init__(self):
        self.filepath = '/Users/ryudai/Desktop/data_sfc/A_02.csv'
        pass



data = pd.read_csv(filepath)

data60 = data.loc[ 0 : 59 , 'date' : 'steps' ]

print(data60)

data60.to_csv('/Users/ryudai/Desktop/output.csv')