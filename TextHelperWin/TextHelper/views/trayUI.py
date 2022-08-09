#coding:utf-8

import sys, codecs, jarray
from os import path, environ, getenv

from utils.graphical import MOD_LOG, drawLog, FONT_JP
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from java.awt import Font, Color, Toolkit, SystemTray, TrayIcon, Insets
from javax.swing import JDialog, JFrame, JPanel, JPopupMenu, JMenuItem

from java.awt.event import MouseEvent, ActionEvent, ActionListener, MouseAdapter
from javax.swing.event import PopupMenuListener

class TaskTray(TrayIcon):
    def __init__(self, image=None, tooltip=None, mouseHandler=lambda this, ev: None):
        super(self.__class__, self).__init__(image, tooltip)
        self.setImageAutoSize(True)
        self.handler = mouseHandler
    
    def mouseHook(self, this, ev): self.handler(this, ev)

class TrayMenu(JMenuItem, ActionListener):
    def __init__(self, name, action=lambda this, ev: None):
        super(JMenuItem, self).__init__(name)
        self.setFont(Font(FONT_JP, Font.PLAIN, 14))
        self.setMargin(Insets(2, 10, 2, 10))
        self.setForeground(Color.BLACK)
        self.handler = action
        self.addActionListener(self)
    
    def actionPerformed(self, ev): self.handler(self, ev)

overlay = JDialog()
overlay.setSize(0, 0)
overlay.setAlwaysOnTop(True)
overlay.setUndecorated(True)

trayProxy = JPanel()
overlay.add(trayProxy)

class TrayCtx(JPopupMenu):
    def __init__(self, label):
        super(self.__class__, self).__init__(label)
        self.lockout = False

    def show(self, client, srcX, srcY):
        if self.lockout: return
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        overlay.setLocation(srcX, srcY)
        overlay.setVisible(True)
        self.setInvoker(client)
        self.setVisible(True)
        pointX = srcX if srcX < screenSize.width//2 else srcX-self.getWidth()
        pointY = srcY if srcY < screenSize.height//2 else srcY-self.getHeight()
        self.setLocation(pointX, pointY)

class TrayImpl(MouseAdapter):
    def __init__(self, menu): self.context = menu
    
    def mousePressed(self, ev):
        if ev.isPopupTrigger():
            point = ev.getLocationOnScreen()
            self.context.show(trayProxy, point.x, point.y)
        else:
            icon = ev.getSource()
            icon.mouseHook(self, ev)

    def mouseReleased(self, ev):
        if ev.isPopupTrigger():
            point = ev.getLocationOnScreen()
            self.context.show(trayProxy, point.x, point.y)
        else:
            icon = ev.getSource()
            icon.mouseHook(self, ev)

    def mouseClicked(self, ev): 
        icon = ev.getSource()
        icon.mouseHook(self, ev)

class PopupImpl(PopupMenuListener):
    def __init__(self, action=lambda this, ev: None):
        self.handler = action
    
    def popupMenuWillBecomeVisible(self, ev): self.handler(self, ev)
    
    def popupMenuWillBecomeInvisible(self, ev): overlay.dispose()

    def popupMenuCanceled(self, ev): overlay.dispose()

def buildTray(icon, context, reaction=lambda this, ev: None):
    icon.addMouseListener(TrayImpl(context))
    context.addPopupMenuListener(PopupImpl(reaction))
    SystemTray.getSystemTray().add(icon)
