import itertools
import pandas as pd
import numpy as np

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
    def caldtab(self):
        self.result = self.caltop() / self.calbottom()

        #NaNを１に置換して返す
        return self.result.fillna(1)

    #dt(a, b)の計算（caldtabの結果）を条件に合うのは1,合わないのは0にしてdfを書き換えてリストで返す
    def calresultlist(self):
        
        self.calresult = np.where(self.caldtab() < 0.05 , 1, 0)

        return self.calresult


### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝以下ポイント計算クラス＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class Point:
    def __init__(self) -> None:
        self.cal = Cal()
        self.countlist = []

    #分母の合計の条件判定
    def bottomfit(self):
        if self.cal.bottomsum() >= 5500:
            return True

        else:
            return False

    def pointcount(self):
        if self.bottomfit() == True:
            #グループ化
            self.grouplist = [list(g) for k , g in itertools.groupby(self.cal.calresultlist())]

            #15連続してたら残す
            for i in self.grouplist:
                if len (i) > 14:
                    self.countlist.append(i)

            # リスト内包表記を使用して、0以上の数を含むリストの長さだけを抽出する
            self.OKlist = [len(sublist) for sublist in self.countlist if any (x > 0 for x in sublist)]

            #６０分の合計スコアを計算
            self.point = sum(self.OKlist) - (14 * len(self.OKlist))

            return self.point





### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝以下Appに相当＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class App:
    def __init__(self) -> None:
        self.data1 = Data1()
        self.data2 = Data2()
        self.cal = Cal()
        self.point = Point()

        self.datatest = pd.DataFrame()

        print(self.point.pointcount())

        self.cal.caldtab().to_csv('/Users/ryudai/Desktop/output.csv')

App()