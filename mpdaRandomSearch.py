from mpdaDecodeMethod.mpdaDecode import MPDAInstance,MPDADecoder,MPDADecoderActionSeq,generateRandEncode
import numpy as np
import sys
import time






if __name__ == '__main__':
    ins = MPDAInstance()
    insFileName =  './/benchmark//8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins.dat'
    ins.loadCfg(fileName =  insFileName)
    degRand = open('.//debugData//randRes.dat','w')
    decoder = MPDADecoder(ins)
    makespanLst = []
    np.random.seed(2)
    min_makespan = sys.float_info.max
    min_x = object
    start = time.perf_counter()
    for i in range(40000):
        x = generateRandEncode(robNum= ins._robNum, taskNum= ins._taskNum)
        # print(x)
        validStateBoolean,actSeq = decoder.decode(x)
        if validStateBoolean:
            makespan = actSeq[-1].eventTime
            print(makespan)
        else:
            makespan = sys.float_info.max
        if makespan< min_makespan:
            min_x  = x
            min_makespan = makespan

        makespanLst.append(makespan)
        degRand.write(str(i) + '  ' + str(makespan) + '\n')
        degRand.flush()
    end = time.perf_counter()
    print('time = ', end-start)
    print(min(makespanLst))
    degRand.write('min '+ str(min(makespanLst)) + '\n')
    degRand.write('x ' + str(min_x) + '\n')
    degRand.close()
    # actSeqDecoder = MPDADecoderActionSeq(ins)
    # actSeqDecoder.decode(actSeq)
    # # print(np.array(actSeq.convert2MultiPerm(ins._robNum),dtype = object))
    # for perm in actSeq.convert2MultiPerm(ins._robNum):
    #     print(perm)
    #
