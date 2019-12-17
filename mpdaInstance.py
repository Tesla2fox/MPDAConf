import random
import numpy as np
import readcfg as rd

from enum import Enum

class TaskModelType(Enum):
    ExpModel = 1
    LineModel = 2

class MPDAInstance(object):
    def __init__(self):
        pass
    def loadCfg(self,fileName : str):
        # print(fileName)
        self._insName = fileName
        readCfg = rd.Read_Cfg(fileName)
        self._robNum = int(readCfg.getSingleVal('robNum'))
        self._taskNum = int(readCfg.getSingleVal('taskNum'))
        self._threhold = readCfg.getSingleVal('comp_threhold')
        self._robAbiLst  = []
        self._robVelLst = []
        self._taskStateLst = []
        self._taskRateLst = []
        readCfg.get('rob_abi',self._robAbiLst)
        readCfg.get('rob_vel',self._robVelLst)
        readCfg.get('tsk_rat',self._taskRateLst)
        readCfg.get('tsk_state',self._taskStateLst)
        self._rob2taskDisMat = np.zeros((self._robNum,self._taskNum))
        disLst = []
        readCfg.get('rob2tskDis', disLst)
        for i in range(self._robNum):
            for j in range(self._taskNum):
                self._rob2taskDisMat[i][j] = disLst[i * self._taskNum + j]

        self._taskDisMat = np.zeros((self._taskNum, self._taskNum))
        disLst = []
        readCfg.get('tskDis', disLst)
        for i in range(self._taskNum):
            for j in range(self._taskNum):
                self._taskDisMat[i][j] = disLst[i * self._taskNum + j]

    def __str__(self):
        return 'robNum = ' + str(self._robNum) + '  taskNum = ' + str(self._taskNum) +'\n'+ self._insName


if __name__ == '__main__':
    # print('test')
    insFileName = './/benchmark//8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins.dat'
    ins = MPDAInstance()
    ins.loadCfg(fileName= insFileName)
    print(ins)