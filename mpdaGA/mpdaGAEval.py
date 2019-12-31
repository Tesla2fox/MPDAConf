import numpy as np
import sys
from mpdaDecodeMethod.mpdaDecode import MPDADecoder
# from MPDA_decode.MPDA_decode_discrete import MPDA_Decode_Discrete_NB,MPDA_Decode_Discrete_RC
IND_ROBNUM = 0
IND_TASKNUM = 0
ga_eval_mpda = object
# MPDADecoder.decode(x)
def mpda_eval(individual):
    encode =  np.zeros((IND_ROBNUM, IND_TASKNUM), dtype=int)
    i = 0
    for robID in range(IND_ROBNUM):
        for taskID in range(IND_TASKNUM):
            encode[robID][taskID] = individual[i]
            i += 1
    # mpda_decode_nb = MPDA_Decode_Discrete_NB()
    # print(encode)
    validBoolean,actSeq = ga_eval_mpda.decode(encode)
    if not validBoolean:
        ms = 9999999999
    else:
        ms = actSeq[-1].eventTime
    return ms,actSeq
