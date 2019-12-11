import readcfg as r_d
from mpdaInstance import MPDAInstance,TaskModelType
import os, sys
from enum import Enum
from collections import namedtuple
import numpy as np
ActionTuple = namedtuple('ActionTuple',['robID','taskID','eventType','eventTime'])
import plotly.figure_factory as ff
import colorlover as cl


class EventType(Enum):
    arrive = 1
    leave = 2


class ActionSeq(object):

    _modelType = {TaskModelType.ExpModel: '_expCal',
                 TaskModelType.LineModel: '_lineCal'}
    def __init__(self):
        self._seq = []
        self._actionTime = 0
        self._infEvent = []

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self,_o_seq):
        if type(_o_seq) != type([]):
            raise TypeError('tuple must be LIST')
        else:
            self._seq = _o_seq
    @seq.deleter
    def seq(self):
        del self._seq
    def __eq__(self, other):
        return other._seq == self._seq

    def __len__(self):
        return len(self._seq)

    def append(self,action_tuple):
        if type(action_tuple) != ActionTuple:
            raise TypeError('tuple must be ActionTuple')
        elif action_tuple.eventTime < self._actionTime:
            print(self)
            self._seq.append(action_tuple)
            print('b',self)
            exit()
            raise Exception('time is out of order in action seq ')
        else:
            self._seq.append(action_tuple)
            self._actionTime = self._seq[-1].eventTime
            # print(self)

    def extend(self,action_tuple_lst = []):
        for action_tuple in action_tuple_lst:
            self.append(action_tuple)

    def __getitem__(self, item):
        return self._seq[item]

    def __setitem__(self, key, value):
        self._seq[key] = value

    def __str__(self):
        res_str = str()
        for x in self._seq:
            res_str = res_str + str(x) +'\n'
        return res_str
    def clear(self):
        self._seq.clear()
        self._actionTime = 0

    def convert2MultiPerm(self,robNum):

        multi_perm = [[] for i in range(robNum)]
        for unit in self._seq:
            # if unit.eventType == EventType.arrive:
            multi_perm[unit.robID].append(unit.taskID)
        return multi_perm


class MPDADecoderActionSeq(object):
    def __init__(self,ins :MPDAInstance):
        self._insName = ins._insName
        # readCfg = rd.Read_Cfg(fileName)
        self._robNum = ins._robNum
        self._taskNum = ins._taskNum
            # int(readCfg.getSingleVal('taskNum'))
        self._threhold = ins._threhold
        self._robAbiLst  = ins._robAbiLst
        self._robVelLst = ins._robVelLst
        self._taskStateLst = ins._taskStateLst
        self._taskRateLst = ins._taskRateLst
        self._rob2taskDisMat = ins._rob2taskDisMat
        self._taskDisMat = ins._taskDisMat

    def decode(self,seq : ActionSeq):
        self._seq = seq

        pass


    def drawActionSeqGantt(self):
        '''

        '''
        self.checkActionSeq()
        multiPerm = self._seq.convert2MultiPerm(self._robNum)
        print(multiPerm)
        actionRobLst = [[] for x in range(self._robNum)]
        for act in self._seq:
            actionRobLst[act.robID].append(act)
        df = []
        for robID in range(self._robNum):
            for ind in range(0,len(actionRobLst[robID]),2):
                dic = dict(Task = 'rob' + str(robID),
                           Start = actionRobLst[robID][ind].eventTime,
                           Finish = actionRobLst[robID][ind + 1].eventTime,
                           Resource = 'Task' + str(actionRobLst[robID][ind].taskID))
                df.append(dic)
            # if robID > 1:
            #     break
        colorLst = cl.scales[str(self._taskNum)]['qual']['Paired']
        colorDic = dict()
        for taskID in range(self._taskNum):
            colorDic['Task' + str(taskID)] = colorLst[taskID]
        print(colorDic)
        print(df)
        # print(actionRobLst)
        # exit()

        # for act in self._seq:
        #     pass
        #     # df.append(dict(Task = ''))
        # for robID in range(self._robNum):
        #     df.append(dict(Task = 'rob'+ str(robID), Start = 1, Finish = 5))
        fig = ff.create_gantt(df, colors=colorDic, index_col= 'Resource', show_colorbar=True, group_tasks=True)
        # fig = ff.create_gantt(df, show_colorbar= True, group_tasks= True)
        fig['layout']['xaxis']['type'] = 'linear'
        fig['layout']['xaxis']['zeroline'] = True

        fig.show()

    def drawTaskScatter(self):
        pass
    def checkActionSeq(self):
        '''

        :return:
        '''

        '''
        time ordered
        '''
        # for action in self._seq:
        for i in range(len(self._seq) - 1):
            if self._seq[i].eventTime <= self._seq[i + 1].eventTime:
                continue
            else:
                print('time ordered bug')
                exit()

        '''
        all tasks have been completed
        '''
        # cmpltTimeLst = [sys.float_info.max for taskID in range(self._taskNum)]
        cmpltLst = [False for taskID in range(self._taskNum)]
        for action in self._seq:
            if action.eventType == EventType.leave:
                taskID = action.taskID
                if not cmpltLst[taskID]:
                    cmpltLst[taskID] = True
        if False in cmpltLst:
            print(cmpltLst)
            print('all tasks have not been completed')
            exit()

        '''
        '''
        for taskID in range(self._taskNum):
            aEventNum = 0
            dEventNum = 0
            for action in self._seq:
                if action.taskID == taskID:
                    if action.eventType == EventType.leave:
                        dEventNum += 1
                    if action.eventType == EventType.arrive:
                        aEventNum += 1
            if aEventNum == dEventNum:
                continue
            else:
                print(taskID, 'task event num bug')
                # exit()
        for robID in range(self._robNum):
            aEventNum = 0
            dEventNum = 0
            for action in self._seq:
                if action.robID == robID:
                    if action.eventType == EventType.leave:
                        dEventNum += 1
                    if action.eventType == EventType.arrive:
                        aEventNum += 1
            if aEventNum == dEventNum:
                continue
            else:
                print(robID, 'rob event num bug')

        '''
        '''

        for robID in range(self._robNum):
            for action in self._seq:
                if action.robID == robID:
                    if action.eventTime < (self._rob2taskDisMat[robID][action.taskID]/self._robVelLst[robID]):
                        print('speed bug')

        for robID in range(self._robNum):
            eventBool =  False
            for action in self._seq:
                if action.robID == robID:
                    if action.eventType == EventType.arrive:
                        if not eventBool:
                            eventBool = True
                        else:
                            '''
                            
                            '''
                            print('excuate bug')
                    if action.eventType == EventType.leave:
                        if eventBool:
                            eventBool = False
                        else:
                            '''
                            '''
                            print('excuate bug')


#在“SuperiorCatalogue”的基础上在脱掉一层路径，得到我们想要的路径。

if __name__ == '__main__':
    print('test_mpdaDecoder')
    AbsolutePath = os.path.abspath(__file__)
    # 将相对路径转换成绝对路径
    SuperiorCatalogue = os.path.dirname(AbsolutePath)
    # 相对路径的上级路径
    BaseDir = os.path.dirname(SuperiorCatalogue)

    print(BaseDir)
    ins = MPDAInstance()
    insFileName = BaseDir +'//benchmark//8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins.dat'
    ins.loadCfg(fileName =  insFileName)

    decoder = MPDADecoder(ins)
