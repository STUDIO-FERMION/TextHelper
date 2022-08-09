#coding:utf-8

import sys, codecs, os, importlib, inspect
from os import environ, getenv, putenv, path

from java.lang import System, Runnable, StringIndexOutOfBoundsException, IllegalArgumentException

from org.sikuli.script import (
    App, Screen, Finder, Pattern, Location, Region, Match, Env, Key, KeyModifier, Mouse
    )
from org.sikuli.basics import Debug, Settings, HotkeyListener
from org.sikuli.script.Sikulix import popat, popup, popAsk, popError, wait

from java.awt import Robot, TrayIcon, SplashScreen, Image, RenderingHints, Color, AlphaComposite
from java.awt.event import MouseAdapter, MouseEvent, ActionListener, ActionEvent
from java.awt.event.MouseEvent import BUTTON1, BUTTON3, MOUSE_RELEASED, MOUSE_CLICKED

from javax.swing import JFrame, JDialog, JPopupMenu, SwingUtilities

def inspection(this=None, event=None): status.stats(modal=False, work=True, hotkey=False)

def key_config(this=None, event=None):
    hotkeySet.doRender(studio, u'スキャン開始')
    while not studio.isVisible(): TimeUnit.MILLISECONDS.sleep(500)

def form_config(this=None, event=None):
    recordMenu.doRender(studio)
    while not studio.isVisible(): TimeUnit.MILLISECONDS.sleep(500)

def finalize(this=None, event=None): status.quit = True

from java.net import URL
from javax.imageio import ImageIO
import Main
splashScreen = SplashScreen.getSplashScreen()
if splashScreen is not None:
    imageIn = Main.getResourceAsStream('/META-INF/images/welcome-text.png')
    welcome = ImageIO.read(ImageIO.createImageInputStream(imageIn))
    graph = splashScreen.createGraphics()
    graph.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
    graph.drawImage(welcome, 50, 380, 540, 20, None)
    splashScreen.update()

from startup import (
    status, clean_tray, tray, column, notice, confirm, FONT_JP, bundle, icon
    )
from utils.supplement import wideNum
from java.lang.String import format as fmtStr
from views.trayUI import TaskTray, TrayCtx, TrayMenu, PopupImpl, buildTray
ctx = TrayCtx(u'TEXT HELPERメニュー')

def mouseAction(client=None, event=None):
    if status.busy or status.work: return
    if event.getID() == MOUSE_CLICKED and event.button == BUTTON1:
        status.stats(modal=False, work=True)

trayIcon = TaskTray(image=icon.LOAD, mouseHandler=mouseAction, tooltip=tray.STARTUP)

def popupHandle(this=None, event=None):
    if not status.busy: trayIcon.setImage(icon.CONCEPT)

buildTray(icon=trayIcon, context=ctx, reaction=popupHandle)

class HotkeyHandle(HotkeyListener):
    def __init__(self): super(self.__class__, self)
    def hotkeyPressed(self, ev):status.stats(hotkey=True, work=True)

hotkeyHandle = HotkeyHandle()

from common.configuration import Config
config = Config.factory()
from views.default import Studio
studio = Studio(config, bundle)
from views import hotkeySet, recordMenu

class Org(TrayMenu):
    active_target = []

    @staticmethod
    def pre_action():
        status.stats(busy=True, hotkey=False)
        ctx.lockout = True
        trayIcon.setImage(icon.SLEEP)
        try: Env.removeHotkey(config.charkey, config.shift+config.ctrl+config.alt)
        except IllegalArgumentException as ex:
            Debug.error('HotKey unregister failed: `%s`', ex.getLocalizedMessage())

    @classmethod
    def post_action(cls):
        try: Env.addHotkey(config.charkey, config.shift+config.ctrl+config.alt, hotkeyHandle)
        except (StringIndexOutOfBoundsException, IllegalArgumentException) as ex:
            Debug.error('HotKey register failed: `%s`', ex.getLocalizedMessage())
        isDirect = u'オフ' if config.direct else u'オン'
        ctx.getComponent(2).setLabel(fmtStr(tray.MENU1, isDirect))
        ctx.getComponent(3).setLabel(fmtStr(tray.MENU2, config.hotkey()))
        isActive = len([prof for prof in studio.profile.values() if prof[5] is True])
        isValid = len([prof for prof in studio.profile.values() if prof[5] is not None])
        ctx.getComponent(4).setLabel(fmtStr(tray.MENU3, wideNum(isActive), wideNum(isValid)))
        trayIcon.toolTip = fmtStr(tray.TIP_HELP, isDirect, config.hotkey(), wideNum(isActive), wideNum(isValid))
        trayIcon.setImage(icon.CONCEPT)
        cls.active_target = [ ID for ID, item in studio.profile.items() if item[column.ACTIVE] is True ]
        status.stats(busy=False, hotkey=False)
        ctx.lockout = False

    @classmethod
    def modeless(cls):
        while studio.isVisible() or status.busy:
            TimeUnit.MILLISECONDS.sleep(500)
            if studio.isVisible() is status.busy: continue
            if not studio.isVisible() and status.busy: cls.post_action()
            status.busy = studio.isVisible()

    def __init__(self, name, action):
        self.actionHook = action
        super(self.__class__, self).__init__(name, self.main_action)

    def main_action(self, that, ev):
        self.__class__.pre_action()
        self.actionHook(this=that, event=ev)

def mode_switch(this=None, event=None): status.modal = True

def warning(parts):
    template = u'<html><h2><font face="%s" color=red>%s</font></h2></html>'
    return fmtStr(template, FONT_JP, parts)

ctx.add(TrayMenu(name=u'スキャン開始', action=inspection))
ctx.addSeparator()
ctx.add(Org(name=u'確認ダイアログ', action=mode_switch))
ctx.add(Org(name=u'HotKey', action=key_config))
ctx.add(Org(name=u'プロファイル', action=form_config))
ctx.addSeparator()
ctx.add(TrayMenu(name=u'終了', action=finalize))

robot = Robot()
Org.post_action()
JDialog.setDefaultLookAndFeelDecorated(True)

if Debug.isLogToFile():
    infoLog = os.path.join(os.path.dirname(Debug.logfile), 'infout.log')
    Debug.setLogFile(infoLog)

from utils.robokey import type_jp
def attention(key):
    record = studio.profile[key]
    popat(Location(Screen().getW()-150, Screen().getH()-130))
    robot.mouseMove(Screen().getW()-200, Screen().getH()-80)
    Org.pre_action()
    method =  u'タイプ' if record[column.IS_TYPE] else u'ペースト'
    detail = fmtStr(confirm.DETAIL, 'ID:', u'タイトル:', u'入力テキスト:', u'入力方法:')
    content = fmtStr(confirm.CONTENT, FONT_JP, detail)
    offer = fmtStr(confirm.OFFER, FONT_JP, u'自動入力しますか？', content)
    message = fmtStr(offer, key, record[column.SYMBOL], record[column.PHRASE], method)
    JDialog.setDefaultLookAndFeelDecorated(True)
    try: choice = popAsk(message, u'画像スキャン結果')
    except: choice = False
    finally: return choice

def nothing():
    popat(Location(Screen().getW()-150, Screen().getH()-115))
    robot.mouseMove(Screen().getW()-150, Screen().getH()-75)
    Org.pre_action()
    JDialog.setDefaultLookAndFeelDecorated(True)
    popError(warning(u'識別パターン検出不可'), u'画像スキャン結果')
    Org.post_action()

def headless():
    popat(Location(Screen().getW()-260, Screen().getH()-115))
    robot.mouseMove(Screen().getW()-260, Screen().getH()-85)
    Org.pre_action()
    JDialog.setDefaultLookAndFeelDecorated(True)
    popError(warning(notice.REJECTED), u'パターン認識不可')
    Org.post_action()

from java.lang import Runnable
from java.util.concurrent import Executors, CompletableFuture, TimeUnit
from java.lang import Exception as JException

pool30 = Executors.newFixedThreadPool(30)

class AsyncTask(Runnable):
    space, axes, score_map = (None, None, {})

    def __init__(self, target):
        super(self.__class__, self).__init__()
        self.ID = target
        self.image = studio.profile[self.ID][column.IMAGE]
        self.pattern = Pattern().setBImage(self.image).similar(0.9)

    def run(self):
        if self.__class__.space.width < self.image.width or self.__class__.space.height < self.image.height:
            return
        finder = Finder(self.__class__.space)
        finder.find(self.pattern)
        if finder.hasNext():
            match = finder.next()
            match.moveTo(match.offset(self.__class__.axes).getTopLeft())
            JFrame.setDefaultLookAndFeelDecorated(False)
            try:
                match.highlightOn('GRAY')
                TimeUnit.MILLISECONDS.sleep(500)
                match.highlightOff()
            except: match.highlight(1, 'GRAY')
            JFrame.setDefaultLookAndFeelDecorated(True)
            size = match.w * match.h
            Debug.user('profile ID:%s [%s] %spx is matched.', (self.ID, studio.profile[self.ID][column.SYMBOL], size))
            self.__class__.score_map[self.ID] = match


def async_inspect(area, target_list):
    AsyncTask.space = Screen().capture(area).getImage()
    AsyncTask.axes = area.getTopLeft() 
    AsyncTask.score_map.clear()
    future_list = [CompletableFuture.runAsync(AsyncTask(ID) , pool30) for ID in target_list]    
    CompletableFuture.allOf(*future_list).join()
    valid_record = [(key, val) for key, val in AsyncTask.score_map.items() if val is not None ]
    if len(valid_record) > 0:
        top_rank = max(valid_record, key=lambda seq: seq[1].w * seq[1].h)
        ID, angle = top_rank
        record = studio.profile[ID]
        angle.setTargetOffset(*studio.profile[ID][column.OFFSET])
        params = (ID, record[column.SYMBOL], angle.x, angle.y, len(valid_record))
        Debug.user('ID:%d [%s] @%d:%d is adopted from %ditem(s).', *params)
        if True if config.direct else attention(ID):
            angle.click()
            angle.type('a', Key.CTRL)
            angle.type(Key.DELETE)
            if record[column.IS_TYPE]:
                type_jp(record[column.PHRASE])
            else:
                angle.paste(angle, record[column.PHRASE])
    else: nothing()

splashScreen = SplashScreen.getSplashScreen()
if splashScreen is not None: splashScreen.close()
while not status.quit:
    TimeUnit.MILLISECONDS.sleep(500)
    Org.modeless()
    if status.modal:
        config.direct = not config.direct
        config.save()
        popat(Location(Screen().getW()-150, Screen().getH()-115))
        robot.mouseMove(Screen().getW()-150, Screen().getH()-85)
        Org.pre_action()
        toggle = notice.TURN_ON if config.direct else notice.TURN_OFF
        content = fmtStr(notice.CONTENT, toggle)
        JDialog.setDefaultLookAndFeelDecorated(True)
        popup(fmtStr(notice.NOTICE, FONT_JP, content), u'確認ダイアログ')
        Org.post_action()
        status.modal=False
    if status.work:
        if not status.hotkey: Screen().type(Key.ESC, Key.ALT)
        trayIcon.setImage(icon.WORK)
        frontend = App.focusedWindow()
        if frontend is not None and frontend.isValid():
            ctx.lockout = True
            async_inspect(frontend, Org.active_target)
        else: headless()
        Org.post_action()
        status.stats(work=False, hotkey=False)

Env.removeHotkey(config.charkey, config.shift+config.ctrl+config.alt)
if studio.isVisible(): studio.dispose()
clean_tray()
pool30.shutdown()
os._exit(0)
