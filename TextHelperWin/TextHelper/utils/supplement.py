#coding:utf-8

import sys, codecs, jarray, importlib, inspect
from os import putenv, path
from java.lang import System, Class

from utils.graphical import MOD_LOG, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from collections import namedtuple
def genConst(constSet):
    NameProxy = namedtuple('NameProxy', constSet.keys())
    return NameProxy(**constSet)

def wideNum(plusNum):
    if type(plusNum) is int and not plusNum < 0:
        return str().join([ unichr(65296+int(col)) for col in str(plusNum) ])
    else: raise AttributeError
