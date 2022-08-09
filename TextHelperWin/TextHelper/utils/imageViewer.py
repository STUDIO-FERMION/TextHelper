#coding:utf-8

import sys, codecs, os, importlib, inspect
from os import path, environ, getenv


from utils.graphical import MOD_LOG, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from java.awt import Dimension, Color, BorderLayout
from javax.swing import JPanel, JScrollPane, ScrollPaneConstants
from java.awt.image import BufferedImage
from java.awt.geom import Rectangle2D

class ImageBank(object):
    def __init__(self, preset):
        if preset.__class__ is BufferedImage:
            self.preset = preset 
            self.attached, self.target = (self.preset, self.preset)
        else: raise AttributeError

    def __get__(self, this, that):
        if self.target is self.preset:
            self.attached = BufferedImage(this.width, this.height, BufferedImage.TYPE_3BYTE_BGR)
            self.attached.getGraphics().drawImage(self.preset, 0, 0, this.width, this.height, None)
            this.setPreferredSize(this.parent.getSize())
        else:
            self.attached = self.target
            this.setPreferredSize(Dimension(self.target.width, self.target.height))
        return self.attached

    def __set__(self, this, image):
        if image.__class__ is BufferedImage:
            this.sPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_AS_NEEDED)
            this.sPane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED)
            self.__dict__['target'] = image
            if this.getTopLevelAncestor() is not None: 
                this.getTopLevelAncestor().setVisible(True)
                this.setSize(this.sPane.getSize())
                this.sPane.getVerticalScrollBar().setVisible(True)
                this.sPane.getHorizontalScrollBar().setVisible(True)

        elif image is None:
            this.sPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER)
            this.sPane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_NEVER)
            self.target = self.preset

        else: raise AttributeError
    
    def __delete__(self, this):
        this.sPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER)
        this.sPane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_NEVER)
        self.target = self.preset
        if this.getTopLevelAncestor() is not None: 
            this.getTopLevelAncestor().setVisible(True)

class Preview(JPanel):
    imageData = None
    def __init__(self, imageBank):
        super(self.__class__, self).__init__(BorderLayout())
        self.__class__.imageData = imageBank
        self.setBackground(Color(16, 16, 16))
        self.sPane = JScrollPane()
        self.vPort = self.sPane.getViewport();
        self.vPort.add(self, BorderLayout.CENTER)

    def paintComponent(self, graph):
        super(self.__class__, self).paintComponent(graph)
        imageWidth, imageHeight = (self.imageData.width, self.imageData.height)
        self.setMinimumSize(self.parent.getSize())
        self.setPreferredSize(self.parent.getSize())
        frameWidth, frameHeight = (self.parent.width, self.parent.height)
        x = 0 if imageWidth >= frameWidth else (frameWidth-imageWidth)//2
        y = 0 if imageHeight >= frameHeight else (frameHeight-imageHeight)//2
        graph.setBackground(Color.GRAY)
        graph.clearRect(0, 0, imageWidth if x == 0 else frameWidth, imageHeight if y == 0 else frameHeight)
        graph.drawImage(self.imageData, x, y, imageWidth, imageHeight, None)
    
    def initialize(self, replacer):
        if replacer.__class__ is BufferedImage:
            self.__class__.__dict__['imageData'].__dict__['preset'] = replacer
            self.sPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER)
            self.sPane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_NEVER)
            self.repaint()
            self.updateUI()
