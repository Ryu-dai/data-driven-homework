from turtle import Turtle
import pandas as pd

### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝でーた読み込みクラス＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class Data1:
    def __init__(self) -> None:
        self.filepathroot = '/Users/ryudai/Desktop/data_sfc/A_'
        self.filepath_no = 1
        self.filepath_no_zfill = str(self.filepath_no).zfill(2)

        #スライスの起点と終点を定義
        self.slicestart = 533
        self.sliceend = 592

    
    def data60return(self):

        #csvを読み込んでself.dataにパス
        self.filepath = self.filepathroot + self.filepath_no_zfill + '.csv'
        self.data = pd.read_csv(self.filepath)

        #self.dataから60分の検索窓枠を設定
        self.data60 = self.data.loc[ self.slicestart : self.sliceend ,  'steps' ]
        
        #検索した６０分のデータを返す
        return self.data60


class Data2:
    def __init__(self) -> None:
        self.filepathroot = '/Users/ryudai/Desktop/data_sfc/A_'
        self.filepath_no = 2
        self.filepath_no_zfill = str(self.filepath_no).zfill(2)

        #スライスの起点と終点を定義
        self.slicestart = 533
        self.sliceend = 592

    
    def data60return(self):
        print('メソッド通過')

        #csvを読み込んでself.dataにパス
        self.filepath = self.filepathroot + self.filepath_no_zfill + '.csv'
        self.data = pd.read_csv(self.filepath)

        #self.dataから60分の検索窓枠を設定
        self.data60 = self.data.loc[ self.slicestart : self.sliceend , 'steps' ]
        
        #検索した６０分のデータを返す
        return self.data60

### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝以下計算クラス＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class Cal:
    def __init__(self) -> None:
        self.data1 = Data1()
        self.data2 = Data2()

    #分子の計算

    def caltop(self):
        self.topdata = (self.data1.data60return() - self.data2.data60return()) ** 2

        return self.topdata

    #分母の計算

    def calbottom(self):
        self.bottomdata = (self.data1.data60return() ** 2 ) + (self.data2.data60return() ** 2)
        
        return self.bottomdata

    #分母の合計値の計算
    def bottomsum(self):
        self.sumbottom = self.calbottom().sum()

        return self.sumbottom

    #dt（a, b)の計算

    def calresult(self):
        self.result = self.caltop() / self.calbottom()

        #NaNを１に置換して返す
        return self.result.fillna(1)


### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝以下ポイント計算クラス＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class Point:
    def __init__(self) -> None:
        self.cal = Cal()

    #分母の合計の条件判定
    def bottomfit(self):
        if self.cal.bottomsum() >= 5500:
            return True

        else:
            return False



### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝以下Appに相当＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class App:
    def __init__(self) -> None:
        self.data1 = Data1()
        self.data2 = Data2()
        self.cal = Cal()

        self.datatest = pd.DataFrame()

        print(self.cal.bottomsum())

        self.cal.calresult().to_csv('/Users/ryudai/Desktop/output.csv')

App()