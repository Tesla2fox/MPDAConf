import sys
import os
import numpy as np

import plotly.graph_objects as go
import plotly
from scipy.stats import wilcoxon
from  functools import cmp_to_key
import functools
import readcfg as r_d
import random

import dataProcess.convertData as cd
import math

def sWRank(data1,data2):
    print(data1[0], data2[0])
    return wRank(data1[1],data2[1])

def wRank(data1,data2):
    if len(data2) <len(data1):
        while len(data2) != len(data1):
            data2.append(data2[random.randint(0,len(data2)-1)])
    stat, p = wilcoxon(data1, data2)
    alpha = 0.05
    # print('Statistics=%.3f, p=%.3f' % (stat, p))
    if p > alpha:
        print(p)
        print('equal ')
        # print(data,data2)
        # raise Exception('xxxx')
        return 0
    else:
        # print('no equal')
        return np.mean(data1) - np.mean(data2)


AbsolutePath = os.path.abspath(__file__)
SuperiorCatalogue = os.path.dirname(AbsolutePath)
WBaseDir = os.path.dirname(SuperiorCatalogue)

figBaseDir = '/vol//grid-solar//sgeusers//guanqiang//mpda_new_data//fig//'
figBaseDir = '/Users/leona/code/data/SOMEDATA//fig//'

markLst = ['circle-dot','square-dot','diamond-dot','triangle-up','pentagon']


class DataPro(object):
    def __init__(self,insName,localSearchLst,reStartLst):
        BaseDir = '/vol//grid-solar//sgeusers//guanqiang//mpda_new_data//' + insName
        BaseDir = '/Users/leona/code/data/SOMEDATA//' + insName
        # localSearchLst = ['_None', '_SWAP', '_SWAP', '_INSERT', '_TRI' ,'_TRISWAP']
        # localSearchLst = ['_None','_SWAP','_MSWAP']
        # localSearchLst = ['_SWAP','_MSWAP']
        # # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
        # reStartLst = ['_NORE2','_DTRI2']
        # reStartLst = ['_NORE2']
        # ,'_NORE0.75','_NORE1']

        self.insName = insName
        self.fitDic = dict()
        self.genDic = dict()
        self.NFEDic = dict()
        self.HOFDic = dict()
        self.HOFNFEDic = dict()
        self.runTimeDic = dict()

        cmpLst = []
        # cmpLst.append('eda_opt_')
        for localSearch in localSearchLst:
            for reStart in reStartLst:
                dir = 'ga_opt_' + localSearch + reStart
                cmpLst.append(dir)
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
                self.runTimeDic[dir] = []
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
                        self.runTimeDic[dir].append(rdData.getSingleVal('runTime'))
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
            if len(fitLstLst) == 0:
                continue
            print(fitLstLst)
            # print(key)
            # for xx in fitLstLst:
            #     print(len(xx))
            max_gen = len(max(fitLstLst,key = lambda  x: len(x)))
            print('max_gen', max_gen)

            _fitLstLst = [[] for _ in range(max_gen)]
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
        plotly.offline.plot(fig, filename= figBaseDir + 'mean_'+ self.insName )
        # fig.write_image(WBaseDir + '//fig//mean_'+ self.insName )
        layout = dict()
        layout['title'] = 'min'
        layout['xaxis'] = dict(title='gen')
        layout['yaxis'] = dict(title='makespan (s)')
        fig = go.Figure(data=min_figData, layout=layout)
        # fig.show()
        # plotly.offline.plot(fig, filename= WBaseDir + '//fig//min_'+ self.insName + '.png')
        # fig.write_image(WBaseDir + '//fig//min_'+ self.insName + '.png')
        # exit()

    def drawNFE(self,benchmarkID,keyNameDic,prefix):
        mean_figData = []
        min_figData = []
        i = 0
        for key in self.fitDic:
            # if len(self.HOFDic[key]) != 30:
            #     continue
            fitLstLst = self.fitDic[key]
            if len(fitLstLst) == 0:
                continue
            # print(fitLstLst)
            # print(key)
            # for xx in fitLstLst:
            #     print(len(xx))
            # exit()
            max_gen = len(max(fitLstLst,key = lambda  x: len(x)))
            # print('max_gen', max_gen)
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
            min_gen = len(min(fitLstLst,key = lambda  x: len(x)))

            for gen, _data in enumerate(_fitLstLst):
                # if gen <= 2:
                #     continue
                if gen > min_gen:
                    break
                if len(_data) == 0 :
                    break
                mean_data  = np.mean(_data)

                if mean_data >20000:
                    _meanLst.append(2000)
                else:
                    _meanLst.append(mean_data)

                # print(len((_data)))
                # print(np.mean(_data))
                if len(_meanLst) > 2:
                    if _meanLst[-1] > _meanLst[-2]:
                        print('xxx')
                        # exit()exit
                _nfeLst.append(np.mean(_NFELstLst[gen]))
                # _genLst.append(gen)
                # _nfeLst.append()
                _minLst.append(min(_data))

            if key in keyNameDic:
                name = keyNameDic[key]
            # elif key == 'ga_opt__MSWAP_NORE2':
            #     name = 'MA-MLS'
            # elif key == 'ga_opt__None_NORE2':
            #     name = 'GA'
            else:
                name = key
            if i <= 4:
                mean_trace = go.Scatter(mode='markers+lines', x=_nfeLst, y=_meanLst,
                                    name=name,
                                    marker = dict(symbol = markLst[i],size = 10))
            else:
                mean_trace = go.Scatter(mode='markers+lines', x=_nfeLst, y=_meanLst,
                                    name=name)
            i += 1
            mean_figData.append(mean_trace)
            min_trace = go.Scatter(mode='lines', x=_nfeLst, y=_minLst, name=key)
            min_figData.append(min_trace)

        layout = dict()
        layout['xaxis'] = dict(title='NFE')
        layout['yaxis'] = dict(title='makespan (s)')
        # layout['title'] = 'mean'
        fig = go.Figure(data=mean_figData, layout=layout)
        fontSize = 30
        fig.update_layout(
            legend=go.layout.Legend(
                font = dict(size = fontSize),
                x=0.7,
                y=1),
        margin = go.layout.Margin(
            l= fontSize *4,
            r=0,
            b=15,
            t=0,
            pad=0
        ),
            font = dict(size = fontSize)
        )

        # fig.show()
        # plotly.offline.plot(fig, image = 'png',
        #                     image_filename = WBaseDir + '//fig//mean_'+ self.insName )
        # plotly.offline.plot(fig, filename= figBaseDir +'nfe_mean_'+ self.insName )
        # exit()
        fig.show()
        fig.write_image(figBaseDir +prefix+ str(benchmarkID) +'.pdf' )
        # layout = dict()
        # layout['title'] = 'min'
        # layout['xaxis'] = dict(title='NFE')
        # layout['yaxis'] = dict(title='makespan (s)')
        # fig = go.Figure(data=min_figData, layout=layout)
        # fig.show()
        # plotly.offline.plot(fig, filename= WBaseDir + '//fig//nfe_min_'+ self.insName + '.png')
        # fig.write_image(WBaseDir + '//fig//min_'+ self.insName + '.png')
        # exit()
    def drawTime(self,benchmarkID,keyNameDic,prefix,p1,p2):
        mean_figData = []
        min_figData = []
        i = 0
        for key in self.fitDic:
            # if len(self.HOFDic[key]) != 30:
            #     continue

            fitLstLst = self.fitDic[key]
            if len(fitLstLst) == 0:
                continue
            # print(fitLstLst)
            # print(key)
            # for xx in fitLstLst:
            #     print(len(xx))
            # exit()
            max_gen = len(max(fitLstLst,key = lambda  x: len(x)))
            # print('max_gen', max_gen)
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
                # break
            _minLst = []
            _meanLst = []
            # _genLst = []
            _nfeLst = []
            min_gen = len(min(fitLstLst,key = lambda  x: len(x)))
            runTime =np.mean(self.runTimeDic[key])
            max_NFE = np.mean(_NFELstLst[max_gen - 1])
            p_time = runTime/max_NFE
            if key == 'ga_opt__SWAP_NORE2':
                p_time = p_time *p1
            if key == 'ga_opt__MSWAP_NORE2':
                p_time = p_time*p2
            for gen, _data in enumerate(_fitLstLst):
                # if gen <= 2:
                #     continue
                if gen > min_gen:
                    break
                if len(_data) == 0 :
                    break
                mean_data  = np.mean(_data)

                if mean_data >20000:
                    _meanLst.append(2000)
                else:
                    _meanLst.append(mean_data)
                if len(_meanLst) > 2:
                    if _meanLst[-1] > _meanLst[-2]:
                        print('xxx')
                        break
                        # exit()exit
                _nfeLst.append(np.mean(_NFELstLst[gen]) * p_time)
                _minLst.append(min(_data))

            if key in keyNameDic:
                name = keyNameDic[key]
            # elif key == 'ga_opt__MSWAP_NORE2':
            #     name = 'MA-MLS'
            # elif key == 'ga_opt__None_NORE2':
            #     name = 'GA'
            else:
                name = key
            if i <= 4:
                mean_trace = go.Scatter(mode='markers+lines', x=_nfeLst, y=_meanLst,
                                    name=name,
                                    marker = dict(symbol = markLst[i],size = 10))
            else:
                mean_trace = go.Scatter(mode='markers+lines', x=_nfeLst, y=_meanLst,
                                    name=name)
            i += 1
            mean_figData.append(mean_trace)
            min_trace = go.Scatter(mode='lines', x=_nfeLst, y=_minLst, name=key)
            min_figData.append(min_trace)

        layout = dict()
        layout['xaxis'] = dict(title='running time (s)')
        layout['yaxis'] = dict(title='makespan (s)')
        # layout['title'] = 'mean'
        fig = go.Figure(data=mean_figData, layout=layout)
        fontSize = 30
        fig.update_layout(
            legend=go.layout.Legend(
                font = dict(size = fontSize),
                x=0.7,
                y=1),
        margin = go.layout.Margin(
            l= fontSize *4,
            r=0,
            b=15,
            t=0,
            pad=0
        ),
            font = dict(size = fontSize)
        )

        # fig.show()
        # plotly.offline.plot(fig, image = 'png',
        #                     image_filename = WBaseDir + '//fig//mean_'+ self.insName )
        # plotly.offline.plot(fig, filename= figBaseDir +'nfe_mean_'+ self.insName )
        # exit()
        fig.show()
        fig.write_image(figBaseDir +prefix+ str(benchmarkID) +'.pdf' )


    def drawBox(self):
        figData = []
        for key in self.HOFDic:
        # for key in self.HOFNFEDic:
            figData.append(go.Box(y=self.HOFDic[key],name = key))
        layout = dict()
        fig = go.Figure(data=figData, layout=layout)
        # fig.show()
        plotly.offline.plot(fig, filename=figBaseDir +'_' + self.insName + '_box')

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
        try:
            rankLstData = sorted(rankLstData, key = cmp_to_key(sWRank))
        except:
            rankLstData = sorted(rankLstData, key = lambda x : np.mean(x[1]) )

        rankLst = []
        i = 1
        for key,data in rankLstData:
            # print(key,' ',np.mean(data))
            print(key,' ',np.mean(data))
            print(key, 'min &',cd.Etype2str(np.min(data)))
            print(key, 'avg &',cd.Etype2str(np.mean(data)))
            rankLst.append((key,i))
            i += 1
        return rankLst

    def rankTime(self):
        # rankDicData = dict()
        rankLstData = []
        for key in self.runTimeDic:
        # for key in self.HOFNFEDic:
            if len(self.runTimeDic[key]) >= 10:
                # rankDicData[]
                rankLstData.append((key,self.runTimeDic[key]))
                print(key,len(self.runTimeDic[key]))
            else:
                print(key,len(self.runTimeDic[key]))
                # print(key,self.HOFDic[key])
        print(rankLstData)
        try:
            rankLstData = sorted(rankLstData, key = cmp_to_key(sWRank))
        except:
            rankLstData = sorted(rankLstData, key = lambda x : np.mean(x[1]) )
        rankLst = []
        i = 1
        for key,data in rankLstData:
            # print(key,' ',np.mean(data))
            print(key,' ',np.mean(data))
            print(key, 'min time &',cd.Etype2str(np.min(data)))
            print(key, 'avg time &',cd.Etype2str(np.mean(data)))
            rankLst.append((key,i))
            i += 1
        # exit()
        return rankLst

    def sameTime(self,p):
        i = 0
        for key in self.fitDic:
            # if len(self.HOFDic[key]) != 30:
            #     continue
            fitLstLst = self.fitDic[key]
            if key == 'ga_opt__MSWAP_NORE2' or key == 'ga_opt__SWAP_NORE2':
                continue
            if len(fitLstLst) == 0:
                continue
            # print(fitLstLst)
            # print(key)
            # for xx in fitLstLst:
            #     print(len(xx))
            # exit()
            max_gen = len(max(fitLstLst,key = lambda  x: len(x)))
            # print('max_gen', max_gen)
            _fitLstLst = [[] for _ in range(max_gen)]
            # print(_fitLstLst)
            print(self.HOFDic[key])
            for rt in range(len(fitLstLst)):
                # for ind, unit in enumerate(fitLstLst[3]):
                for ind, unit in enumerate(fitLstLst[rt]):
                    _fitLstLst[ind].append(unit)
                # break
            print(p)
            if p < 1:
                 self.HOFDic[key] = _fitLstLst[math.ceil(max_gen * p)]
            print(self.HOFDic[key])
            # exit()

    def writeTable(self,conFile,insNo):
        # conFile.write()
        conFile.write('\\multirow{4}{*}{\shortstack{'+str(insNo)+'}}')
        lessStr = '(-)'
        equalStr = '($\\approx$)'
        greatStr = '(+)'

        # if wRank(self.HOFDic)
        v = wRank(self.HOFDic['ga_opt__SWAP_NORE2'], self.HOFDic['eda_opt_'])
        # x = object
        if  v == 0:
            swap_x = equalStr
            pass
        elif v > 0:
            swap_x = lessStr
        else:
            swap_x = greatStr

        v = wRank(self.HOFDic['ga_opt__MSWAP_NORE2'], self.HOFDic['eda_opt_'])
        # x = object
        if v == 0:
            mswap_x = equalStr
            pass
        elif v > 0:
            mswap_x = lessStr
        else:
            mswap_x = greatStr
            # pass
        conFile.write(' &mean ')
        for i,key in enumerate(self.HOFDic):
            if key == 'ga_opt__MSWAP_NORE2':
                conFile.write(' &' + cd.Etype2str(np.mean(self.HOFDic[key])) + mswap_x+ str(' ')  )
            elif key == 'ga_opt__SWAP_NORE2':
                conFile.write(' &' + cd.Etype2str(np.mean(self.HOFDic[key])) + swap_x+ str(' ')  )
            else:
                conFile.write(' &' + cd.Etype2str(np.mean(self.HOFDic[key])) + str(' ')  )

        conFile.write('\\\\')
        conFile.write('\n')
        conFile.flush()


        conFile.write(' &std ')
        for i,key in enumerate(self.HOFDic):
            conFile.write(' &' + cd.Etype2str(np.std(self.HOFDic[key])) + str(' '))
        conFile.write('\\\\')
        conFile.write('\n')
        conFile.flush()

        conFile.write('&best ')
        for i,key in enumerate(self.HOFDic):
            conFile.write(' &' + cd.Etype2str(np.min(self.HOFDic[key])) + str(' '))
        conFile.write('\\\\')
        conFile.write('\n')
        conFile.flush()
        conFile.write('\\hline')
        conFile.write('\n')





def drawDecodingTime(insNameLst):
    rankDic = dict()
    keyNameDic = dict()
    keyNameDic['ga_opt__SWAP_NORE2'] = 'MA-OLS'
    keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS'
    keyNameDic['ga_opt__SWAP_DTRI2'] = 'MA-OLS-TD'
    keyNameDic['ga_opt__MSWAP_DTRI2'] = 'MA-MLS-TD'
    validNoLst = [1,2,3,4,5,6,7,8]
    # validNoLst = [1]
    p1_Lst = [0.8,0.7,0.7,0.79,0.89,0.89,0.89,1]
    p2_Lst = [0.5,0.6,0.6,0.79,0.89,0.89,0.89,1]

    localSearchLst = ['_SWAP', '_MSWAP']
    # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
    reStartLst = [ '_DTRI2','_NORE2']
    prefix = 'decodeTime'
    conFile = open('time table.txt', 'w')

    for insID,insName in enumerate(insNameLst):
        print('insName = ',insName)
        if (insID +1 ) not in validNoLst:
            continue
        d_pro  = DataPro(insName,localSearchLst,reStartLst)
        # d_pro.drawBox()
        # break
        if len(d_pro.HOFDic) == 4:
            print('success ',insName)
        rankLst = d_pro.rankSum()
        d_pro.rankTime()
        for key,order in rankLst:
            if key not in rankDic:
                rankDic[key] = []
            rankDic[key].append(order)
        # d_pro.writeTable(conFile,insID+1)
        d_pro.drawTime(insID+ 1,keyNameDic,prefix,p1_Lst[insID],p2_Lst[insID])
    for key in rankDic:
        print(key,'   ',rankDic[key])


def drawDecoding(insNameLst):
    rankDic = dict()
    keyNameDic = dict()
    keyNameDic['ga_opt__SWAP_NORE2'] = 'MA-OLS'
    keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS'
    keyNameDic['ga_opt__SWAP_DTRI2'] = 'MA-OLS-TD'
    keyNameDic['ga_opt__MSWAP_DTRI2'] = 'MA-MLS-TD'
    validNoLst = [1,2,3,4,5,6,7,8]
    localSearchLst = ['_SWAP', '_MSWAP']
    # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
    reStartLst = [ '_DTRI2','_NB2']
    prefix = 'decode'
    conFile = open('table.txt', 'w')

    for insID,insName in enumerate(insNameLst):
        print('insName = ',insName)
        if (insID +1 ) not in validNoLst:
            continue
        d_pro  = DataPro(insName,localSearchLst,reStartLst)
        # d_pro.drawBox()
        # break
        if len(d_pro.HOFDic) == 4:
            print('success ',insName)
        rankLst = d_pro.rankSum()
        d_pro.rankTime()
        for key,order in rankLst:
            if key not in rankDic:
                rankDic[key] = []
            rankDic[key].append(order)
        # d_pro.writeTable(conFile,insID+1)
    for key in rankDic:
        print(key,'   ',rankDic[key])

def drawEDA(insNameLst):
    rankDic = dict()
    keyNameDic = dict()
    keyNameDic['ga_opt__SWAP_NORE2'] = 'MA-OLS'
    keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS'
    keyNameDic['ga_opt__SWAP_DTRI2'] = 'MA-OLS-TD'
    keyNameDic['ga_opt__MSWAP_DTRI2'] = 'MA-MLS-TD'
    validNoLst = [1,2,3,4,5,6,7,8]
    localSearchLst = ['_SWAP', '_MSWAP']
    # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
    reStartLst = [ '_NORE2']
    prefix = 'decode'
    conFile = open('edatable.txt', 'w')
    for insID,insName in enumerate(insNameLst):
        print('insName = ',insName)
        if (insID +1 ) not in validNoLst:
            continue
        d_pro  = DataPro(insName,localSearchLst,reStartLst)
        # d_pro.drawBox()
        # break
        if len(d_pro.HOFDic) == 4:
            print('success ',insName)
        rankLst = d_pro.rankSum()
        d_pro.rankTime()
        for key,order in rankLst:
            if key not in rankDic:
                rankDic[key] = []
            rankDic[key].append(order)
        d_pro.writeTable(conFile,insID+1)
    for key in rankDic:
        print(key,'   ',rankDic[key])

def drawSen(insNameLst):
    rankDic = dict()
    keyNameDic = dict()
    keyNameDic['ga_opt__SWAP_NORE10'] = 'MA-OLS-10'
    keyNameDic['ga_opt__SWAP_NORE2'] = 'MA-OLS-2'
    keyNameDic['ga_opt__SWAP_NORE50'] = 'MA-OLS-50'
    keyNameDic['ga_opt__MSWAP_NORE10'] = 'MA-MLS-10'
    keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS-2'
    keyNameDic['ga_opt__MSWAP_NORE50'] = 'MA-MLS-50'
    # keyNameDic['ga_opt__MSWAP_NORE1'] = 'MA-MLS-1'
    # keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS-2'
    # keyNameDic['ga_opt__MSWAP_NORE3'] = 'MA-MLS-3'
    # keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS-2'
    # keyNameDic['ga_opt__SWAP_DTRI2'] = 'MA-OLS-TD'
    # keyNameDic['ga_opt__MSWAP_DTRI2'] = 'MA-MLS-TD'
    validNoLst = [1,2,3,4,5,6,7,8]
    localSearchLst = ['_SWAP']
    # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
    reStartLst = [ '_NORE2','_NORE10','_NORE50']
    prefix = 'swap'
    conFile = open('edatable.txt', 'w')
    for insID,insName in enumerate(insNameLst):
        print('insName = ',insName)
        if (insID +1 ) not in validNoLst:
            continue
        d_pro  = DataPro(insName,localSearchLst,reStartLst)
        # d_pro.drawBox()
        # break
        if len(d_pro.HOFDic) == 4:
            print('success ',insName)
        rankLst = d_pro.rankSum()
        d_pro.rankTime()
        for key,order in rankLst:
            if key not in rankDic:
                rankDic[key] = []
            rankDic[key].append(order)
        # d_pro.writeTable(conFile,insID+1)
        d_pro.drawNFE(insID+ 1,keyNameDic,prefix)
    for key in rankDic:
        print(key,'   ',rankDic[key])
    rankDic = dict()
    keyNameDic = dict()
    keyNameDic['ga_opt__SWAP_NORE10'] = 'MA-OLS-10'
    keyNameDic['ga_opt__SWAP_NORE2'] = 'MA-OLS-2'
    keyNameDic['ga_opt__SWAP_NORE50'] = 'MA-OLS-50'
    keyNameDic['ga_opt__MSWAP_NORE10'] = 'MA-MLS-10'
    keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS-2'
    keyNameDic['ga_opt__MSWAP_NORE50'] = 'MA-MLS-50'
    # keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS-2'
    # keyNameDic['ga_opt__SWAP_DTRI2'] = 'MA-OLS-TD'
    # keyNameDic['ga_opt__MSWAP_DTRI2'] = 'MA-MLS-TD'
    validNoLst = [1,2,3,4,5,6,7,8]
    localSearchLst = ['_MSWAP']
    # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
    reStartLst = [ '_NORE2','_NORE10','_NORE50']
    prefix = 'mswap'
    conFile = open('edatable.txt', 'w')
    for insID,insName in enumerate(insNameLst):
        print('insName = ',insName)
        if (insID +1 ) not in validNoLst:
            continue
        d_pro  = DataPro(insName,localSearchLst,reStartLst)
        # d_pro.drawBox()
        # break
        if len(d_pro.HOFDic) == 4:
            print('success ',insName)
        rankLst = d_pro.rankSum()
        d_pro.rankTime()
        for key,order in rankLst:
            if key not in rankDic:
                rankDic[key] = []
            rankDic[key].append(order)
        # d_pro.writeTable(conFile,insID+1)
        d_pro.drawNFE(insID+ 1,keyNameDic,prefix)
    for key in rankDic:
        print(key,'   ',rankDic[key])


def drawDecodingB(insNameLst):
    rankDic = dict()
    keyNameDic = dict()
    keyNameDic['ga_opt__SWAP_NORE2'] = 'MA-OLS'
    keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS'
    keyNameDic['ga_opt__SWAP_DTRI2'] = 'MA-OLS-TD'
    keyNameDic['ga_opt__MSWAP_DTRI2'] = 'MA-MLS-TD'
    validNoLst = [1,2,3,4,5,6,7,8]
    p_Lst = [0.6,0.6,0.7,0.79,0.5,0.3,0.72,0.18]
    localSearchLst = ['_SWAP', '_MSWAP']
    # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
    reStartLst = [ '_DTRI2','_NORE2']
    prefix = 'decode'
    conFile = open('table.txt', 'w')
    for insID,insName in enumerate(insNameLst):
        print('insName = ',insName)
        if (insID +1 ) not in validNoLst:
            continue
        d_pro  = DataPro(insName,localSearchLst,reStartLst)
        d_pro.sameTime(p_Lst[insID])
        # d_pro.drawBox()
        # break
        if len(d_pro.HOFDic) == 4:
            print('success ',insName)
        rankLst = d_pro.rankSum()
        d_pro.rankTime()
        for key,order in rankLst:
            if key not in rankDic:
                rankDic[key] = []
            rankDic[key].append(order)
        d_pro.writeTable(conFile,insID+1)
    for key in rankDic:
        print(key,'   ',rankDic[key])

def drawGA(insNameLst):
    rankDic = dict()
    keyNameDic = dict()
    keyNameDic['ga_opt__SWAP_NORE2'] = 'MA-OLS'
    keyNameDic['ga_opt__MSWAP_NORE2'] = 'MA-MLS'
    keyNameDic['ga_opt__None_NORE2'] = 'GA'
    # keyNameDic['ga_opt__MSWAP_DTRI2'] = 'MA-MLS-TD'
    validNoLst = [1,2,3,4,5,6,7,8]
    localSearchLst = ['_SWAP', '_MSWAP','_None']
    # reStartLst = ['_NORE0.5','_NORE0.75','_NORE1','_ELRE']
    reStartLst = ['_NORE2']
    prefix = 'GA'
    for insID,insName in enumerate(insNameLst):
        print('insName = ',insName)
        if (insID +1 ) not in validNoLst:
            continue
        d_pro  = DataPro(insName,localSearchLst,reStartLst)
        # d_pro.drawBox()
        # break
        if len(d_pro.HOFDic) == 4:
            print('success ',insName)
        rankLst = d_pro.rankSum()
        for key,order in rankLst:
            if key not in rankDic:
                rankDic[key] = []
            rankDic[key].append(order)
        d_pro.drawNFE(insID+ 1,keyNameDic,prefix)
    for key in rankDic:
        print(key,'   ',rankDic[key])


if __name__ == '__main__':
    insNameLst = [
        '5_4_RANDOMCLUSTERED_RANDOMCLUSTERED_SVLCV_SVSCV_thre0.1MPDAins',
        '5_5_ECCENTRIC_RANDOM_SVSCV_LVSCV_thre0.1MPDAins',
        '8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins',
        '8_8_CLUSTERED_CLUSTERED_SVLCV_UNITARY_thre0.1MPDAins',
                  '11_11_RANDOMCLUSTERED_CLUSTERED_MSVFLV_QUADRANT_thre0.1MPDAins',
                  '17_23_RANDOMCLUSTERED_CLUSTERED_LVLCV_LVSCV_thre0.1MPDAins',
                  '20_18_RANDOM_ECCENTRIC_QUADRANT_SVLCV_thre0.1MPDAins',
                  '20_20_CLUSTERED_RANDOM_QUADRANT_LVSCV_thre0.1MPDAins',
                  ]
    # drawDecodingB(insNameLst)
    # drawEDA(insNameLst)
    drawSen(insNameLst)
    # drawGA(insNameLst)
    # drawDecodingTime(insNameLst)