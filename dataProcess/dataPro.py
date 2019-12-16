import sys
import os

AbsolutePath = os.path.abspath(__file__)
SuperiorCatalogue = os.path.dirname(AbsolutePath)
BaseDir = os.path.dirname(SuperiorCatalogue)

localSearchLst = ['_None', '_SWAP', '_INSERT', '_TRI', '_VINSERT']

for localSearch in localSearchLst:
    dataDir = BaseDir + '//debugData//ga_opt_'+localSearch
    for root, dirs, files in os.walk(dataDir):
        print(files)

    genLstLst = [[] for _ in range(len(files))]
    fitLstLst = [[] for _ in range(len(files))]
    for file in files:
        genLst = []
        fitLst = []
        with open(dataDir +'//'+ file) as txtData:
            lines = txtData.readlines()
            for line in lines:
                lineData = line.split()
                if (len(lineData) == 0):
                    continue
                if (len(lineData)== 7):
                    print(lineData)
                    if lineData[0] == 'gen':
                        genLst.append(int(lineData[1]))
                        fitLst.append(float(lineData[5]))
        print(genLst)
        print(fitLst)



                # exit()
