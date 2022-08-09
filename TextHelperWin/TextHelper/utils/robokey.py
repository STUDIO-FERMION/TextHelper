#coding:utf-8

import sys, codecs, jarray
from os import environ, getenv, putenv, path

from java.awt import Robot
from java.awt.im import InputContext
from java.awt.event import KeyEvent as KE
from org.sikuli.script import (
    App, Screen, Finder, Pattern, Region, Match, Env, Key, KeyModifier
    )

from utils.graphical import MOD_LOG, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

shift_num = ('!', '"', '#', '$', '%', '&', "'", '(', ')')
mark_awt = {'^': KE.VK_CIRCUMFLEX, '@': KE.VK_AT}
mark_awt_shift = {'`': KE.VK_AT, '~': KE.VK_CIRCUMFLEX, '=': KE.VK_MINUS, '+': KE.VK_SEMICOLON}
robot = Robot()

def type_jp(word):
    for char in word:
        if char in shift_num:
            Screen().type(str(shift_num.index(char)+1), Key.SHIFT)
        elif char in mark_awt.keys():
            robot.keyPress(mark_awt[char])
        elif char in mark_awt_shift.keys():
            robot.keyPress(KE.VK_SHIFT)
            robot.keyPress(mark_awt_shift[char])
            robot.keyRelease(KE.VK_SHIFT)
        else:
            Screen().type(char)
