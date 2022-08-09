#coding:utf-8

import sys, codecs, jarray
from os import path, getenv

from utils.graphical import MOD_LOG, drawLog, FONT_JP
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from javax.swing.event import ChangeListener
from javax.swing import (
    JLabel, JRadioButton, ButtonGroup, JComboBox, Box, JCheckBox, JButton, SwingConstants,
    BorderFactory, JFrame, JOptionPane
    )

from utils.supplement import genConst
from java.awt.event import ActionListener
from java.awt import (
    Container, GridBagConstraints, GridBagLayout, Cursor, Font, Insets, Dimension, Color
    )

contents = Container()
params = GridBagConstraints()
layout = GridBagLayout()

text_bundle = {}
text_bundle['ALPHA'] = 'ABCDEFGHIJKLNMOPQRSTUVWXYZ'
text_bundle['ETC'] = r'1234567890-[;:],./'
text_bundle['UNAVAILABLE'] = r'^\@:'
text_bundle['CAPTION'] = u'HotKey設定メニュー'
text_bundle['MENU'] = u'%sHotKey設定'
text_bundle['RADIO'] = u'メインキー文字種別：'
text_bundle['ALPHA_MODE'] = u'アルファベット'
text_bundle['ETC_MODE'] = u'数字・記号'
text_bundle['MAIN_KEY'] = u'メインキー選択：'
text_bundle['MODIFIER'] = u'特殊キー選択:'
text_bundle['CONFIRM'] = u'特殊キーは[Ctrl]か[Alt]またはその両方を必ず指定してください' 
text_bundle['CANCEL'] = u'キャンセル'
text_bundle['OK'] = u'ＯＫ'

bundle = genConst(text_bundle)

class DefLabel(JLabel):
    def __init__(self, text):
        super(self.__class__, self).__init__(text)
        self.setFont(Font(FONT_JP, Font.PLAIN, 15))

descTop = DefLabel(bundle.MENU)
descTop.setFont(Font(FONT_JP, Font.BOLD, 24))

params.insets = Insets(30, 50, 30, 0)
params.gridx = 0
params.gridy = 0
params.gridwidth = 6
params.gridheight = 2
params.anchor = GridBagConstraints.NORTH;
params.fill = GridBagConstraints.HORIZONTAL;
layout.setConstraints(descTop, params)
contents.add(descTop)

descGroup = DefLabel(bundle.RADIO)
params.insets = Insets(20, 50, 20, 0)
params.gridx = 0
params.gridy = 2
params.gridwidth = 3
params.gridheight = 2

params.anchor = GridBagConstraints.WEST
params.fill = GridBagConstraints.NONE
layout.setConstraints(descGroup, params)
contents.add(descGroup)

class Radio(JRadioButton):
    def __init__(self, text):
        super(self.__class__, self).__init__(text)
        self.setText(text)
        self.setPreferredSize(Dimension(240, 20))
        self.setFont(Font(FONT_JP, Font.BOLD, 15))
        self.setForeground(Color.DARK_GRAY)

alpMode = Radio(bundle.ALPHA_MODE)
etcMode = Radio(bundle.ETC_MODE)
listMode = ButtonGroup()
listMode.add(alpMode)
listMode.add(etcMode)

params.insets = Insets(5, 0, 5, 0);
params.gridx = GridBagConstraints.RELATIVE
params.fill = GridBagConstraints.HORIZONTAL
params.gridwidth = 3
params.gridy = 2
params.gridheight = 1
layout.setConstraints(alpMode, params)
contents.add(alpMode)
params.gridy = 3
layout.setConstraints(etcMode, params)
contents.add(etcMode)

descChar = DefLabel(bundle.MAIN_KEY)
params.insets = Insets(20, 50, 20, 0)
params.gridx = 1
params.gridy = 4
params.gridwidth = 3
layout.setConstraints(descChar, params)
contents.add(descChar)

class DefCombo(JComboBox):
    def __init__(self, seed):
        super(self.__class__, self)
        for key in seed: self.addItem(key)
        self.setPreferredSize(Dimension(50, 30))
        self.setFont(Font(FONT_JP, Font.BOLD, 18))
        self.setForeground(Color.DARK_GRAY)
        self.setVisible(False)

alpList = DefCombo([ fmtStr(' %s', char) for char in bundle.ALPHA]);
etcList = DefCombo([ fmtStr(' %s', char) for char in bundle.ETC]);
dummy = Box.createRigidArea(Dimension(40, 25))

params.insets = Insets(30, 20, 20, 0)
params.gridx = 3
params.gridy = 4
params.gridwidth = 3
params.fill = GridBagConstraints.NONE
layout.setConstraints(alpList, params)
contents.add(alpList)
layout.setConstraints(etcList, params)
contents.add(etcList)
layout.setConstraints(dummy, params)
contents.add(dummy)

descGray = DefLabel(bundle.MODIFIER)
params.insets = Insets(20, 50, 20, 0)
params.gridx = 0
params.gridy = 6
params.gridwidth = 3
params.fill = GridBagConstraints.HORIZONTAL
layout.setConstraints(descGray, params)
contents.add(descGray)

class ComboListener(ChangeListener):
    def __init__(self, combo, button):
        button.addChangeListener(self)
        self.target = combo
        self.receiver = button

    def stateChanged(self, ev):
        if ev.getSource() == self.receiver: self.target.setVisible(self.receiver.isSelected())

ComboListener(alpList, alpMode)
ComboListener(etcList, etcMode)

class DefCheck(JCheckBox):
    def __init__(self, text):
        super(self.__class__, self).__init__(text)
        self.setSelected(False)
        self.setSize(30, 30)
        self.setFont(Font(FONT_JP, Font.BOLD, 15))

sFlag = DefCheck(u'Shift')
cFlag = DefCheck(u'Ctrl')
aFlag = DefCheck(u'Alt')
params.fill = GridBagConstraints.HORIZONTAL
params.gridx = GridBagConstraints.RELATIVE
params.gridwidth = 1
params.insets = Insets(10, 0, 10, 0)
layout.setConstraints(sFlag, params)
contents.add(sFlag)
layout.setConstraints(cFlag, params)
contents.add(cFlag)
layout.setConstraints(aFlag, params)
contents.add(aFlag)

class DefButton(JButton):
    def __init__(self, text):
        super(self.__class__, self).__init__(text)
        self.setPreferredSize(Dimension(80, 26))
        self.setFont(Font(FONT_JP, Font.PLAIN, 14))
        self.setHorizontalTextPosition(SwingConstants.TRAILING)
        self.setBorder(BorderFactory.createLineBorder(Color.GRAY, 2, True))
        self.setMargin(Insets(1, 1, 1, 1))

quitACK = DefButton(bundle.OK)
params.fill = GridBagConstraints.HORIZONTAL
params.anchor = GridBagConstraints.SOUTHEAST
params.gridwidth = 3
params.insets = Insets(20, 20, 20, 128)
params.gridx = 3
params.gridy = 7
layout.setConstraints(quitACK, params)
contents.add(quitACK)

class AckListener(ActionListener):
    def actionPerformed(self, ev):
        frame = ev.getSource().getTopLevelAncestor()
        frame.setCursor(Cursor(Cursor.WAIT_CURSOR))
        if ev.getSource() == quitACK:
            if cFlag.isSelected() or aFlag.isSelected():
                mainKey = etcList.getSelectedItem() if etcMode.isSelected() else alpList.getSelectedItem()
                frame.config.charkey = str(mainKey)[1]
                frame.config.shift = sFlag.isSelected()
                frame.config.ctrl = cFlag.isSelected()
                frame.config.alt = aFlag.isSelected()
                frame.persistent_config()
                frame.dispose()
            else:
                JOptionPane.showMessageDialog(frame, bundle.CONFIRM, u'警告', JOptionPane.WARNING_MESSAGE)
        frame.setCursor(Cursor(Cursor.DEFAULT_CURSOR))

quitACK.addActionListener(AckListener())

quitNAK = DefButton(bundle.CANCEL)
params.gridx = 3
params.insets = Insets(20, 118, 20, 30)
layout.setConstraints(quitNAK, params)
contents.add(quitNAK)

class NakListener(ActionListener):
    def actionPerformed(self, ev):
        frame = ev.getSource().getTopLevelAncestor()
        if ev.getSource() == quitNAK: frame.dispose()

quitNAK.addActionListener(NakListener())

contents.setLayout(layout)

def doRender(stage, title):
    JFrame.setDefaultLookAndFeelDecorated(True)
    stage.setTitle(bundle.CAPTION)
    stage.setPreferredSize(Dimension(480, 400))
    stage.setContentPane(contents)    
    stage.setVisible(True)
    stage.setResizable(False)
    stage.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)

    if stage.config.charkey in bundle.ALPHA:
        alpMode.setSelected(True)
        alpList.setSelectedItem(' '+stage.config.charkey)
        alpList.setVisible(True)
    
    if stage.config.charkey in bundle.ETC:
        etcMode.setSelected(True)
        etcList.setSelectedItem(' '+stage.config.charkey)
        etcList.setVisible(True)

    sFlag.setSelected(stage.config.shift)
    cFlag.setSelected(stage.config.ctrl)
    aFlag.setSelected(stage.config.alt)

    descTop.setText(fmtStr(descTop.getText(), title))
    stage.pack()
    stage.centering()
