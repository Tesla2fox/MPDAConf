from mpdaDecodeMethod.mpdaDecode import MPDAInstance,MPDADecoder,MPDADecoderActionSeq,generateRandEncode
# from mpdaInstance import
import numpy as np
import mpdaGA.mpdaCrossover


if __name__ == '__main__':
    ins = MPDAInstance()
    insFileName =  './/benchmark//8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins.dat'
    ins.loadCfg(fileName =  insFileName)

    decoder = MPDADecoder(ins)

    np.random.seed(2)
    x = generateRandEncode(robNum= ins._robNum, taskNum= ins._taskNum)
    print(x)
    validStateBoolean,actSeq = decoder.decode(x)
    actSeqDecoder = MPDADecoderActionSeq(ins)
    actSeqDecoder.decode(actSeq)
    # print(np.array(actSeq.convert2MultiPerm(ins._robNum),dtype = object))
    for perm in actSeq.convert2MultiPerm(ins._robNum):
        print(perm)
    # actSeqDecoder.drawActionSeqGantt()
    # actSeqDecoder.drawTaskScatter()
    # actSeqDecoder.drawTaskDependence()

    print('first decoder is over')
    # np.random.seed(1)
    x = generateRandEncode(robNum= ins._robNum, taskNum= ins._taskNum)
    print(x)
    validStateBoolean,actSeq = decoder.decode(x)
    # print(actSeq.convert2MultiPerm(ins._robNum))
    for perm in actSeq.convert2MultiPerm(ins._robNum):
        print(perm)
    # print(actSeq)
    actSeqDecoder = MPDADecoderActionSeq(ins)
    actSeqDecoder.decode(actSeq)

    mpdaGA.mpdaCrossover.IND_TASKNUM = ins._taskNum
    mpdaGA.mpdaCrossover.IND_ROBNUM = ins._robNum
