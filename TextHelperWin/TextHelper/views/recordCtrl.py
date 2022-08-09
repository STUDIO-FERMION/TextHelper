#coding:utf-8

import sys, codecs, jarray
from os import path

from java.awt import (
    Dimension, Color, Font, Insets, BorderLayout, GridBagLayout, GridBagConstraints, 
    )
from javax.swing import (
    JPanel, JLabel, JButton, BoxLayout, Box, JTable, ListSelectionModel, BorderFactory, 
    JScrollPane, JSplitPane, SwingConstants
    )

from views.default import title, info, notice, button

from utils.graphical import MOD_LOG, FONT_JP, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from java.lang import Object
tBody = jarray.array([ jarray.zeros(7, Object) for _ in range(30) ], Object)

cPanel = JPanel(BorderLayout())
cPanel.setPreferredSize(Dimension(490, 110))
cPanel.setMinimumSize(Dimension(464, 110))

xBox = JPanel()
xBox.setLayout(BoxLayout(xBox, BoxLayout.X_AXIS))
xBox.setPreferredSize(Dimension(490, 110))
xBox.setMinimumSize(Dimension(464, 110))
xBox.add(Box.createRigidArea(Dimension(4,110)))
xBox.add(cPanel)
xBox.add(Box.createRigidArea(Dimension(6,110)))

class TextBar(JLabel):
    def __init__(self, text, align):
        super(self.__class__, self).__init__(text, align)
        self.defH = 32
        self.setFont(Font(FONT_JP, Font.PLAIN, 14))
        self.setVerticalAlignment(SwingConstants.CENTER)
        self.setPreferredSize(Dimension(490, self.defH))
        self.setMinimumSize(Dimension(464, self.defH))
        self.setBackground(Color.WHITE)

caption = TextBar(title.VIEW_MODE, JLabel.CENTER)
caption.setFont(Font(FONT_JP, Font.BOLD, 20))
iLabel = TextBar(info.SELECT_RECORD, JLabel.LEFT)
nLabel = TextBar(notice.SAVE_OFFER, JLabel.RIGHT)

cPanel.add(iLabel, BorderLayout.NORTH)

class Gauge(TextBar):
    def __init__(self, text):
        super(TextBar, self).__init__(text, JLabel.CENTER)
        self.setFont(Font(FONT_JP, Font.BOLD, 14))
        aColor = '<font color=orange>%-2d</font>'
        iColor = '<font color=green>%-2d</font>'
        rColor = '<font color=navy>%-2d</font>'
        uColor = '<font color=gray>%-2d</font>'
        self.iBar = fmtStr(self.getText(), aColor, iColor, rColor, uColor)

    def override(self):
        rCount = len([prof for prof in tBody if prof[6] is not None ])
        aCount = len([prof for prof in tBody if prof[6] is True ])
        iCount = rCount-aCount
        uCount = len(tBody)-rCount
        self.setText(self.iBar)
        self.setText(fmtStr(self.iBar, aCount, iCount, rCount, uCount))

gauge = Gauge(u'<html>有効:%s 無効:%s 登録済:%s 未登録:%s</html>')
gauge.override()
cPanel.add(gauge, BorderLayout.CENTER)

class Cbox(JPanel):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.defH =36
        self.setLayout(BoxLayout(self, BoxLayout.X_AXIS))
        self.add(Box.createHorizontalGlue())
        self.setPreferredSize(Dimension(490, self.defH))
        self.setMinimumSize(Dimension(464, self.defH))

class Tctrl(JButton):
    @staticmethod
    def gap(): return Box.createRigidArea(Dimension(3,1))

    def __init__(self, label):
        super(self.__class__, self).__init__(label)
        self.setFont(Font(FONT_JP, Font.BOLD, 14))
        self.setHorizontalTextPosition(SwingConstants.TRAILING)
        self.setPreferredSize(Dimension(90, 28))
        self.setMaximumSize(Dimension(90, 28))
        self.setMargin(Insets(1, 1, 1, 1))
        self.setForeground(Color.DARK_GRAY)
        self.setBorder(BorderFactory.createLineBorder(Color.GRAY, 2, True))


vCtrl = Cbox()

dryRun = Tctrl(button.DRY_RUN)
doActivate = Tctrl(u'有効化')
doEdit = Tctrl(u'編集')
doQuit = Tctrl(u'終了')

vCtrl.add(dryRun)
vCtrl.add(Tctrl.gap())
vCtrl.add(doActivate)
vCtrl.add(Tctrl.gap())
vCtrl.add(doEdit)
vCtrl.add(Tctrl.gap())
vCtrl.add(doQuit)

eCtrl = Cbox()
doOffset= Tctrl(u'オフセット')
doCapture = Tctrl(u'クリップ')
doReset = Tctrl(u'クリア')
doSave = Tctrl(u'保存')
goBack = Tctrl(u'戻る')

eCtrl.add(doOffset)
eCtrl.add(Tctrl.gap())
eCtrl.add(doCapture)
eCtrl.add(Tctrl.gap())
eCtrl.add(doReset)
eCtrl.add(Tctrl.gap())
eCtrl.add(doSave)
eCtrl.add(Tctrl.gap())
eCtrl.add(goBack)

tPanel = JPanel(BorderLayout(5, 5))

xPanel = JPanel(BorderLayout())
xPanel.add(caption, BorderLayout.NORTH)
xPanel.add(tPanel, BorderLayout.CENTER)
xPanel.add(xBox, BorderLayout.SOUTH)
xPanel.updateUI()
