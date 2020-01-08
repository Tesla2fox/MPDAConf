import sys
import os
import numpy as np

import plotly.graph_objects as go
import plotly
from scipy.stats import wilcoxon
from  functools import cmp_to_key
import functools
import readcfg as r_d



def sWRank(data1,data2):
    # print(data1[0], data2[0])
    return wRank(data1[1],data2[1])

def wRank(data1,data2):
    stat, p = wilcoxon(data1, data2)
    alpha = 0.05
    # print('Statistics=%.3f, p=%.3f' % (stat, p))
    if p > alpha:
        # print(p)
        # print('equal ')
        # raise Exception('xxxx')
        return 0
    else:
        # print('no equal')
        return np.mean(data2) - np.mean(data1)


AbsolutePath = os.path.abspath(__file__)
SuperiorCatalogue = os.path.dirname(AbsolutePath)
WBaseDir = os.path.dirname(SuperiorCatalogue)

class DataPro(object):
    def __init__(self,insName):
        BaseDir = '/vol//grid-solar//sgeusers//guanqiang//mpda_exp_data//' + insName
        # localSearchLst = ['_None', '_SWAP', '_SWAP', '_INSERT', '_TRI' ,'_TRISWAP']
        localSearchLst = ['_None', '_MSWAP','_MOSWAP','_MNSWAP','_SWAP',]
        # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
        reStartLst = ['_NORE0.5','_NORE0.75','_NORE1']
        # reStartLst = ['_NORE0.5']
        # ,'_NORE0.75','_NORE1']

        self.insName = insName
        self.fitDic = dict()
        self.genDic = dict()
        self.NFEDic = dict()
        self.HOFDic = dict()
        self.HOFNFEDic = dict()

        cmpLst = []

        for localSearch in localSearchLst:
            for reStart in reStartLst:
                dir = 'ga_opt_' + localSearch + reStart
                cmpLst.append(dir)
        cmpLst.append('eda_opt_')
        # root, exsit_dirs, files =
        # print(os.walk(BaseDir))
        # print(list(os.walk(BaseDir)))
        # # print(exsit_dirs)
        # for root, exsit_dirs, files in os.walk(BaseDir):
        #     print('xxx')
        #     break
        # exit()
        for root, exsit_dirs, files in os.walk(BaseDir):
            # figData = []
            # print('xxxxx')
            for dir in cmpLst:
                    # print(dir)
                if dir not in exsit_dirs:
                    print(dir,' is not exsit')
                    continue
                dataDir = BaseDir + '//' + dir
                # print(dataDir)
                print(dataDir)
                for root, dirs, files in os.walk(dataDir):
                    print(files)
                genLstLst = []
                #    [[] for _ in range(len(files))]
                fitLstLst = []
                NFELstLst = []
                self.HOFDic[dir] = []
                self.HOFNFEDic[dir] = []
                # [[] for _ in range(len(files))]
                print('file Num = ', len(files))
                for i,file in enumerate(files):
                        # exit()
                    # print(i)
                    if len(self.HOFDic[dir]) == 30:
                        break
                    if len(self.HOFNFEDic[dir]) == 30:
                        break
                    # print(i)
                    # if i >= 30:
                    #     break
                    genLst = []
                    fitLst = []
                    NFELst = []
                    with open(dataDir + '//' + file) as txtData:
                        lines = txtData.readlines()
                        for line in lines:
                            lineData = line.split()
                            if (len(lineData) == 0):
                                continue
                            if (len(lineData) == 7):
                                # print(lineData)
                                if lineData[0] == 'gen':
                                    genLst.append(int(lineData[1]))
                                    fitLst.append(float(lineData[5]))
                                    NFELst.append(float(lineData[2]))
                                    # if NFELst[-1] > 1.5E5:
                                    #     self.HOFNFEDic[dir].append(fitLst[-1])
                                        # break
                    # print(file,' ', len(genLst))
                    fitLstLst.append(fitLst)
                    genLstLst.append(genLst)
                    NFELstLst.append(NFELst)
                    # print(len())
                    rdData = r_d.Read_Cfg(dataDir + '//' + file)
                    try:
                        self.HOFDic[dir].append(rdData.getSingleVal('min'))
                        # print(self.HOFDic[dir])
                    except Exception as e:
                        print(dataDir +'//' + file)
                        print(e)
                        pass
                if self.HOFDic[dir] == 30:
                    pass
                # elif
                    # print(genLst)
                    # print(fitLst)
                self.fitDic[dir] = fitLstLst
                self.genDic[dir] = genLstLst
                self.NFEDic[dir] = NFELstLst
                # print(self.fitDic)
            break
            # print(self.fitDic)
    def drawGen(self):
        mean_figData = []
        min_figData = []
        for key in self.fitDic:
            fitLstLst = self.fitDic[key]
            _fitLstLst = [[] for _ in range(len(fitLstLst[0]))]
            # print(_fitLstLst)
            for rt in range(len(fitLstLst)):
                for ind, unit in enumerate(fitLstLst[rt]):
                    _fitLstLst[ind].append(unit)
            _minLst = []
            _meanLst = []
            _genLst = []
            for gen, _data in enumerate(_fitLstLst):
                _meanLst.append(np.mean(_data))
                _genLst.append(gen)
                _minLst.append(min(_data))
            mean_trace = go.Scatter(mode='lines', x=_genLst, y=_meanLst, name=key)
            mean_figData.append(mean_trace)
            min_trace = go.Scatter(mode='lines', x=_genLst, y=_minLst, name=key)
            min_figData.append(min_trace)

        layout = dict()
        layout['xaxis'] = dict(title='gen')
        layout['yaxis'] = dict(title='makespan (s)')
        layout['title'] = 'mean'
        fig = go.Figure(data=mean_figData, layout=layout)
        # fig.show()
        # plotly.offline.plot(fig, image = 'png',
        #                     image_filename = WBaseDir + '//fig//mean_'+ self.insName )
        plotly.offline.plot(fig, filename= WBaseDir + '//fig//mean_'+ self.insName + '.png')
        # fig.write_image(WBaseDir + '//fig//mean_'+ self.insName )
        layout = dict()
        layout['title'] = 'min'
        layout['xaxis'] = dict(title='gen')
        layout['yaxis'] = dict(title='makespan (s)')
        fig = go.Figure(data=min_figData, layout=layout)
        # fig.show()
        plotly.offline.plot(fig, filename= WBaseDir + '//fig//min_'+ self.insName + '.png')
        # fig.write_image(WBaseDir + '//fig//min_'+ self.insName + '.png')
        # exit()

    def drawNFE(self):
        mean_figData = []
        min_figData = []
        for key in self.fitDic:
            # if len(self.HOFDic[key]) != 30:
            #     continue
            fitLstLst = self.fitDic[key]
            # print(key)
            # for xx in fitLstLst:
            #     print(len(xx))
            max_gen = len(max(fitLstLst,key = lambda  x: len(x)))
            print('max_gen', max_gen)
            _fitLstLst = [[] for _ in range(max_gen)]
            # print(_fitLstLst)
            for rt in range(len(fitLstLst)):
                # for ind, unit in enumerate(fitLstLst[3]):
                for ind, unit in enumerate(fitLstLst[rt]):
                    _fitLstLst[ind].append(unit)
                # break

            NFELstLst = self.NFEDic[key]
            _NFELstLst = [[] for _ in range(max_gen)]
            # print(_fitLstLst)
            for rt in range(len(NFELstLst)):
                # for ind, unit in enumerate(NFELstLst[3]):
                for ind, unit in enumerate(NFELstLst[rt]):
                    _NFELstLst[ind].append(unit)
                break
            _minLst = []
            _meanLst = []
            # _genLst = []
            _nfeLst = []
            for gen, _data in enumerate(_fitLstLst):
                if gen <= 10:
                    continue
                if len(_data) == 0 :
                    break
                _meanLst.append(np.mean(_data))
                _nfeLst.append(np.mean(_NFELstLst[gen]))
                # _genLst.append(gen)
                # _nfeLst.append()
                _minLst.append(min(_data))
            mean_trace = go.Scatter(mode='lines', x=_nfeLst, y=_meanLst, name=key)
            mean_figData.append(mean_trace)
            min_trace = go.Scatter(mode='lines', x=_nfeLst, y=_minLst, name=key)
            min_figData.append(min_trace)

        layout = dict()
        layout['xaxis'] = dict(title='NFE')
        layout['yaxis'] = dict(title='makespan (s)')
        layout['title'] = 'mean'
        fig = go.Figure(data=mean_figData, layout=layout)
        # fig.show()
        # plotly.offline.plot(fig, image = 'png',
        #                     image_filename = WBaseDir + '//fig//mean_'+ self.insName )
        plotly.offline.plot(fig, filename= WBaseDir + '//fig//nfe_mean_'+ self.insName + '.png')
        # fig.write_image(WBaseDir + '//fig//mean_'+ self.insName )
        layout = dict()
        layout['title'] = 'min'
        layout['xaxis'] = dict(title='NFE')
        layout['yaxis'] = dict(title='makespan (s)')
        fig = go.Figure(data=min_figData, layout=layout)
        # fig.show()
        # plotly.offline.plot(fig, filename= WBaseDir + '//fig//nfe_min_'+ self.insName + '.png')
        # fig.write_image(WBaseDir + '//fig//min_'+ self.insName + '.png')
        # exit()

    def drawBox(self):
        figData = []
        for key in self.HOFDic:
        # for key in self.HOFNFEDic:
            figData.append(go.Box(y=self.HOFDic[key],name = key))
        layout = dict()
        fig = go.Figure(data=figData, layout=layout)
        # fig.show()
        plotly.offline.plot(fig, filename=WBaseDir + '//fig//_' + self.insName + '_box')

    def rankSum(self):

        # rankDicData = dict()
        rankLstData = []
        for key in self.HOFDic:
        # for key in self.HOFNFEDic:
            if len(self.HOFDic[key]) >= 10:
                # rankDicData[]
                rankLstData.append((key,self.HOFDic[key]))
                print(key,len(self.HOFDic[key]))
            else:
                print(key,len(self.HOFDic[key]))
                # print(key,self.HOFDic[key])
        print(rankLstData)
        # rankLstData = sorted(rankLstData, key = cmp_to_key(sWRank))
        # for key,data in rankLstData:
        #     print(key)
        rankLstData = sorted(rankLstData, key = lambda x : np.mean(x[1]) )
        # rankLstData = sorted(rankLstData, key = lambda x : np.min(x[1]) )
        # print(rankLstData)
        rankLst = []
        i = 1
        for key,data in rankLstData:
            # print(key,' ',np.mean(data))
            print(key,' ',np.mean(data))
            rankLst.append((key,i))
            i += 1
        return rankLst

if __name__ == '__main__':
    insNameLst = [
        '5_5_ECCENTRIC_RANDOM_SVSCV_LVSCV_thre0.1MPDAins',
        '5_4_RANDOMCLUSTERED_RANDOMCLUSTERED_SVLCV_SVSCV_thre0.1MPDAins',
        '8_8_CLUSTERED_CLUSTERED_SVLCV_UNITARY_thre0.1MPDAins',
                '8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins',
                  '11_11_RANDOMCLUSTERED_CLUSTERED_MSVFLV_QUADRANT_thre0.1MPDAins',
                  '17_23_RANDOMCLUSTERED_CLUSTERED_LVLCV_LVSCV_thre0.1MPDAins',
                  '20_20_CLUSTERED_RANDOM_QUADRANT_LVSCV_thre0.1MPDAins',
                  '20_18_RANDOM_ECCENTRIC_QUADRANT_SVLCV_thre0.1MPDAins',
                  # '32_32_ECCENTRIC_RANDOM_QUADRANT_QUADRANT_thre0.1MPDAins',
                  # '29_36_ECCENTRIC_CLUSTERED_SVSCV_LVSCV_thre0.1MPDAins',
                  # '26_29_CLUSTERED_RANDOM_SVSCV_SVSCV_thre0.1MPDAins',
                  ]
    rankDic = dict()
    for insName in insNameLst:
        print('insName = ',insName)
        d_pro  = DataPro(insName)
        d_pro.drawBox()
        # break
        rankLst = d_pro.rankSum()
        for key,order in rankLst:
            if key not in rankDic:
                rankDic[key] = []
            rankDic[key].append(order)
        # for key in rankDic:
        #     print(key, '   ', rankDic[key])
        # break
        # break
        # d_pro.drawNFE()
        # break
    for key in rankDic:
        print(key,'   ',rankDic[key])
   # d_pro.rankSum()
   # d_pro.drawNFE()
   # d_pro.drawGen()

