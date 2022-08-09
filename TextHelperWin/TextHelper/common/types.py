#coding:utf-8

import sys, codecs, jarray
from os import path, getenv

from utils.graphical import MOD_LOG, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

class Flag(object):
    def __init__(self, preset):
        if isinstance(preset, bool):
            self.state, self.shadow = (preset, preset)
        else: raise AttributeError

    def __get__(self, this, that): return self.state

    def __set__(self, this, value):
        if isinstance(value, bool): self.__dict__['state'] = value
        else: raise AttributeError

class Const(object):
    def __init__(self, code, modify):
        self.code = code
        self.modify = modify

    def __get__(self, this, that): return self.code if self.modify else 0

    def __set__(self, this, value):
        if isinstance(value, bool): self.__dict__['modify'] = value
        else: raise AttributeError

from java.util.regex.Pattern import compile as genRE, CASE_INSENSITIVE
class Subset(object):
    def __init__(self, char, regex):
        self.char = char
        self.pattern = genRE(regex, CASE_INSENSITIVE)

    def __get__(self, this, that): return self.char

    def __set__(self, this, char):
        if isinstance(char, str) and len(char) == 1:
            if self.pattern.matcher(char).matches():
                self.__dict__['char'] = char
                return True
            else: return False
        raise AttributeError


class Within(object):
    def __init__(self, seconds, min_val, max_val):
        self.seconds = seconds
        self.min = min_val
        self.max = max_val

    def __get__(self, this, that): return self.seconds

    def __set__(self, this, value):
        if isinstance(value, int) and self.min <= value <= self.max:
            self.__dict__['seconds'] = value
        else:
            raise AttributeError

class Status(object):
    def __new__(cls, **kwargs):
        if len(kwargs) < 1: raise AttributeError
        for key, val in kwargs.items():
            cls.__setattr__(cls, key, Flag(val))
        return super(cls.__class__, cls).__new__(cls)
    
    def __init__(self, **kwargs): self.member = tuple(kwargs.keys())
    
    def stats(self, **kwargs):
        for key, val in kwargs.items():
            if key in self.member: self.__setattr__(key, val)
            else: raise AttributeError
        return { key: self.__getattribute__(key) for key in self.member }
