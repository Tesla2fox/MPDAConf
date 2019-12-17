import sys
import os
import numpy as np

import plotly.graph_objects as go
import plotly
from scipy.stats import wilcoxon
from  functools import cmp_to_key
import functools




def sWRank(data1,data2):
    print(data1[0], data2[0])
    return wRank(data1[1],data2[1])

def wRank(data1,data2):
    stat, p = wilcoxon(data1, data2)
    alpha = 0.05
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    if p > alpha:
        print(p)
        print('equal ')
        # raise Exception('xxxx')
        return True
    else:
        print('no equal')
        return np.mean(data2) - np.mean(data1)

#
#
#     alpha = 0.05
#     if p > alpha:
#     	print('Same distribution (fail to reject H0)')
#         raise Exception('xxx')
#         return  0
#     else:
#         print('Different distribution (reject H0)')
#         if np.mean(data1)< np.mean(data2):
#             return True
#         else:
#             return False



AbsolutePath = os.path.abspath(__file__)
SuperiorCatalogue = os.path.dirname(AbsolutePath)
WBaseDir = os.path.dirname(SuperiorCatalogue)

class DataPro(object):
    def __init__(self,insName):
        BaseDir = '/vol//grid-solar//sgeusers//guanqiang//mpda_exp_data//' + insName
        localSearchLst = ['_None', '_SWAP', '_INSERT', '_TRI', '_VINSERT']
        self.insName = insName
        self.fitDic = dict()
        self.genDic = dict()
        self.NFEDic = dict()
        for root, exsit_dirs, files in os.walk(BaseDir):
            # figData = []
            for localSearch in localSearchLst:

                dir = 'ga_opt_' + localSearch
                print(dir)
                if dir not in exsit_dirs:
                    continue
                dataDir = BaseDir + '//ga_opt_' + localSearch
                print(dataDir)
                for root, dirs, files in os.walk(dataDir):
                    print(files)
                genLstLst = []
                # [[] for _ in range(len(files))]
                fitLstLst = []
                NFELstLst = []
                # [[] for _ in range(len(files))]
                print('file Num = ', len(files))
                for file in files:
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
                    fitLstLst.append(fitLst)
                    genLstLst.append(genLst)
                    NFELstLst.append(NFELst)
                    # print(genLst)
                    # print(fitLst)
                self.fitDic[localSearch] = fitLstLst
                self.genDic[localSearch] = genLstLst
                self.NFEDic[localSearch] = NFELstLst
                print(self.fitDic)
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
            fitLstLst = self.fitDic[key]
            _fitLstLst = [[] for _ in range(len(fitLstLst[0]))]
            # print(_fitLstLst)
            for rt in range(len(fitLstLst)):
                for ind, unit in enumerate(fitLstLst[rt]):
                    _fitLstLst[ind].append(unit)

            NFELstLst = self.NFEDic[key]
            _NFELstLst = [[] for _ in range(len(NFELstLst[0]))]
            # print(_fitLstLst)
            for rt in range(len(NFELstLst)):
                for ind, unit in enumerate(NFELstLst[rt]):
                    _NFELstLst[ind].append(unit)

            _minLst = []
            _meanLst = []
            # _genLst = []
            _nfeLst = []
            for gen, _data in enumerate(_fitLstLst):
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
        plotly.offline.plot(fig, filename= WBaseDir + '//fig//nfe_min_'+ self.insName + '.png')
        # fig.write_image(WBaseDir + '//fig//min_'+ self.insName + '.png')
        # exit()

    def rankSum(self):

        rankDicData = dict()
        for key in self.fitDic:
            rankDicData[key] = []


        for key in self.fitDic:
            fitLstLst = self.fitDic[key]

            for fitLst in fitLstLst:
                rankDicData[key].append(fitLst[-1])

        print(rankDicData)

        rankLstData = []
        for key in rankDicData:
            rankLstData.append((key,rankDicData[key]))
        print(rankLstData)
        sorted(rankLstData, key = cmp_to_key(sWRank))
        print(rankLstData)
        









if __name__ == '__main__':
   insName = '8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins'
   d_pro  = DataPro(insName)
   d_pro.rankSum()
   # d_pro.drawNFE()
   # d_pro.drawGen()

