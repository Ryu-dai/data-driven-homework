import pandas as pd

class Data1:
    def __init__(self) -> None:
        self.filepathroot = '/Users/ryudai/Desktop/data_sfc/A_'
        self.filepath_no = 1
        self.filepath_no_zfill = str(self.filepath_no).zfill(2)

        #スライスの起点と終点を定義
        self.slicestart = 0
        self.sliceend = 59

        print('通過')
    
    def datareturn(self):
        print('メソッド通過')

        #csvを読み込んでself.dataにパス
        self.filepath = self.filepathroot + self.filepath_no_zfill + '.csv'
        self.data = pd.read_csv(self.filepath)

        #self.dataから60分の検索窓枠を設定
        self.data60 = self.data.loc[ self.slicestart : self.sliceend , 'date' : 'steps' ]
        
        #検索した６０分のデータを返す
        return self.data60


### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝以下Appに相当＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class App:
    def __init__(self) -> None:
        self.data1 = Data1()

        self.data1.datareturn.to_csv('/Users/ryudai/Desktop/output.csv')

    staticmethod
    def test(self):
        print('static機能')
        print(self.data1.datareturn())

App()