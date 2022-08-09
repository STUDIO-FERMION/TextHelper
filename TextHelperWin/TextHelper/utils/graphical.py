#coding:utf-8

import sys, codecs, jarray
from os import path, getenv

from java.lang import System, Boolean
from javax.swing import UIManager, JDialog, JFrame
from java.awt import SplashScreen
from java.awt.image import BufferedImage
from java.awt.geom import Rectangle2D, Ellipse2D
from javax.swing.plaf.metal import MetalLookAndFeel

from java.awt import (
    Font, Toolkit, RenderingHints, GradientPaint, Color, BasicStroke, Dimension, Point, Insets
    )

UIManager.put("swing.boldMetal", Boolean.TRUE)
JDialog.setDefaultLookAndFeelDecorated(True)
JFrame.setDefaultLookAndFeelDecorated(True)
Toolkit.getDefaultToolkit().setDynamicLayout(True)
System.setProperty("sun.awt.noerasebackground", "true")
UIManager.setLookAndFeel(MetalLookAndFeel())

MOD_LOG = 'module:  <%s> is imported.'
RES_LOG = 'resource:  <%s> is loaded.'
CON_LOG = 'database:  <%s> is connected.'
DIS_LOG = 'database:  <%s> is closeed.'

FONT_JP = 'VL Gothic Regular'
from org.sikuli.basics import Debug
from java.lang.String import format as fmtStr
def drawLog(logText):
    Debug.info(logText)
    splashScreen = SplashScreen.getSplashScreen()
    if splashScreen is not None:
        rect = splashScreen.getBounds()
        width, height = (rect.width, rect.height)
        graph = splashScreen.createGraphics()
        graph.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        graph.setFont(Font(FONT_JP, Font.PLAIN, 18))
        graph.setColor(Color.WHITE)
        graph.setBackground(Color(0, 0, 0, 0))
        graph.clearRect(0, 0, width, height)
        splashScreen.update()
        graph.drawString(fmtStr('+++ %-50s +++', logText), 50, height-5)
        splashScreen.update()

from java.awt import Font, GraphicsEnvironment
from java.awt.GraphicsEnvironment import getLocalGraphicsEnvironment
import Main

fontFile = 'VL-Gothic-Regular.ttf'
fontIn = Main.getResourceAsStream(str.join('/', ['/META-INF/fonts', fontFile]))
regFont = Font.createFont(Font.TRUETYPE_FONT, fontIn)
GraphicsEnvironment.getLocalGraphicsEnvironment().registerFont(regFont)
drawLog(fmtStr(RES_LOG, fontFile))

drawLog(fmtStr(MOD_LOG, __name__))
