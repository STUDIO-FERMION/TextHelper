#coding:utf-8

import sys, codecs, jarray, importlib, inspect
from os import getenv, path

from org.sikuli.basics import Settings, Debug

DistPath = path.dirname(path.dirname(path.dirname(__file__)))
LogPath = path.join(DistPath, 'logs')
BootLog = path.join(LogPath, 'bootout.log')
UserLog = path.join(LogPath, 'userout.log')
Debug.setLogFile(BootLog)
Debug.setUserLogFile(UserLog)
Debug.logJython(True)

Settings.LogTime = True
Settings.ClickFast = True
Settings.InputFontMono = True
Settings.ActionLogs = True
Settings.DebugLogs = True
Settings.ProfileLogs = False
Settings.TraceLogs = True
Settings.DefaultHighlightTime = 0.5
Settings.UserLogTime = True
Settings.MoveMouseDelay = 0
Settings.ClickDelay =  0.0
Settings.TypeDelay =  0
Settings.WaitScanRate = 0.0
Settings.ObserveScanRate = 1.0
Settings.setShowActions(False)

from java.lang.String import format as fmtStr
from utils.graphical import MOD_LOG, drawLog, FONT_JP
drawLog(fmtStr(MOD_LOG, __name__))

from java.awt import SystemTray, TrayIcon
def clean_tray():
    sys_tray = SystemTray.getSystemTray()
    for icon in sys_tray.getTrayIcons(): sys_tray.remove(icon)

from utils.supplement import genConst
from common.types import Flag, Const, Subset, Within, Status

status = Status(busy=False, work=False, modal=False, hotkey=False, quit=False)

from common.persistence import load_icon_db, load_profile_db
icon = load_icon_db()
bundle = load_profile_db()
blankImage = bundle.pop(0)[3]

tray_label = {}
tray_label['STARTUP'] = u'TEXT HELPER 起動処理中...'
tray_label['TIP_HELP'] = u'TEXT HELPER\n事前確認:%s\n%s\nプロファイル:%s/%s'
tray_label['MENU1'] = u'確認ダイアログ:%s'
tray_label['MENU2'] = u'HotKey (%s)'
tray_label['MENU3'] = u'プロファイル:%s/%s'
tray = genConst(tray_label)

column_item = {}
column_item['SYMBOL'] = 0
column_item['PHRASE'] = 1
column_item['IS_TYPE'] = 2
column_item['IMAGE'] = 3
column_item['OFFSET'] = 4
column_item['ACTIVE'] = 5
column = genConst(column_item)

notice_item = {}
notice_item['NOTICE'] = u'<html><h3><font face="%s">%s</font></h3></html>'
notice_item['CONTENT'] = u'<確認ダイアログを%sに設定しました'
notice_item['TURN_ON'] = u'<font color=green>オフ</font>'
notice_item['TURN_OFF'] = u'<font color=red>オン</font>'
notice_item['REJECTED'] = u'有効なウィンドウが見つかりません'
notice = genConst(notice_item)

confirm_item = {}
confirm_item['OFFER'] = u'<html><h2><font face="%s" color=#FF8C00>%s</font></h2>%s</html>'
confirm_item['CONTENT'] = u'<pre><font face="%s" size=4>%s</font></pre>'
confirm_item['DETAIL'] = '%s<font color=blue>%%d   </font>%s<font color=green>%%s   </font><br>%s%%s<br>%s%%s'
confirm = genConst(confirm_item)
