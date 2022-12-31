import itertools
import pandas as pd
import numpy as np

### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝でーた読み込みクラス＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class Data1:

    slicestart = 0
    sliceend = 59

    def __init__(self) -> None:
        self.filepathroot = '/Users/ryudai/Desktop/data_sfc/'
        self.filegroup = 'A'
        self.filepath_no = 1
        self.filepath_no_zfill = str(self.filepath_no).zfill(2)


    
    def data60return(self):

        #csvを読み込んでself.dataにパス
        self.filepath = self.filepathroot + self.filegroup + '_' + self.filepath_no_zfill + '.csv'
        self.data = pd.read_csv(self.filepath)

        #self.dataから60分の検索窓枠を設定
        self.data60 = self.data.loc[ self.slicestart : self.sliceend ,  'steps' ]
        
        #検索した６０分のデータを返す
        return self.data60


class Data2:
    
    slicestart = 0
    sliceend = 59
    filepath_no = 2

    def __init__(self) -> None:
        self.filepathroot = '/Users/ryudai/Desktop/data_sfc/'
        self.filegroup = 'A'
        self.filepath_no_zfill = str(self.filepath_no).zfill(2)


    
    def data60return(self):

        #csvを読み込んでself.dataにパス
        self.filepath = self.filepathroot + self.filegroup + '_' + self.filepath_no_zfill + '.csv'
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
        self.data1 = Data1()
        self.data2 = Data2()
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


        else:
            return 0






### ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝以下Appに相当＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

point = Point()
data1 = Data1()
data2 = Data2()
pointsum = 0
roopcount = 0
while True:
    
    pointsum += point.pointcount()

    outputlist_index = data1.filegroup + str(data1.filepath_no) + data2.filegroup + str(data2.filepath_no)
    outputlist = pd.DataFrame(index=[outputlist_index])

    roopcount += 1

    data1.__class__.slicestart += 1
    data1.__class__.sliceend += 1
    data2.__class__.slicestart += 1
    data2.__class__.sliceend += 1

    print(point.countlist)
    print(pointsum)




    point.countlist.clear()
    print(data1.sliceend)
    

    #最後まで処理したら
    if data1.sliceend == 21600:
        print(pointsum)

        outputlist['score'] = pointsum

        print(outputlist)

        outputlist.to_csv('/Users/ryudai/Desktop/output.csv', mode='a' , header=False)

        #参照するファイルの場所を変更する
        if data2.filepath_no < 10 :


            data1.__class__.slicestart = 0
            data1.__class__.sliceend = 59
            data2.__class__.slicestart = 0
            data2.__class__.sliceend = 59
            pointsum = 0

            data2.filepath_no += 1

        #10番目の最後まで行ったら終わる
        elif data2.filepath_no == 10 and data2.sliceend == 21600:
            print('処理終わり')
            break

