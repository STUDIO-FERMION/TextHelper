#coding:utf-8

import sys, codecs, jarray
from os import path

from java.lang.String import format as fmtStr
from java.awt import BorderLayout, Dimension, Cursor, Font, Color
from javax.swing import (
    JPanel, BoxLayout, JTable, JLabel, ListSelectionModel, JScrollPane, JSplitPane,
    BorderFactory
    )
from javax.swing.table import (
    AbstractTableModel, TableModel, DefaultTableCellRenderer, DefaultTableModel, 
    DefaultTableColumnModel, TableColumn, TableColumnModel
    )

from utils.graphical import MOD_LOG, drawLog, FONT_JP
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from java.lang import String
from math import ceil

from views.recordCtrl import tBody, caption, tPanel
for row in range(len(tBody)): tBody[row][0] = row+1

tHeader = jarray.array([ u'ID', u'タイトル', u'入力テキスト', u'操作', u'画像', u'位置', u'状態' ], String)

class DataTable(AbstractTableModel):
    def __init__(self): super(self.__class__, self).__init__()
    def getColumnCount(self): return len(tHeader)
    def getRowCount(self): return len(tBody)
    def getValueAt(self, row, col): return tBody[row][col]
    def getColumnName(self, column): return tHeader[column]
    def getColumnClass(self, clazz): return self.getValueAt(0, clazz).__class__
    def isCellEditable(self, row, col): return col not  in (0, 4, 5)
    def setValueAt(self, val, row, col): tBody[row][col] = val

tModel = DataTable()
dataView = JTable(tModel)

dataView.getTableHeader().setReorderingAllowed(False)
dataView.setRowSelectionAllowed(True)
dataView.setColumnSelectionAllowed(False);
dataView.setIntercellSpacing(Dimension(1, 6))
dataView.setFont(Font(FONT_JP, Font.PLAIN, 12))
dataView.setForeground(Color.BLACK)
dataView.setRowHeight(38)
dataView.setAutoResizeMode(JTable.AUTO_RESIZE_NEXT_COLUMN)
dataView.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
dataView.setMinimumSize(Dimension(384, 384))
dataView.setMaximumSize(Dimension(490, 384))
dataView.setShowHorizontalLines(False)
dataView.setShowVerticalLines(False)
dataView.setBackground(Color.WHITE)
dataView.setSelectionForeground(Color.YELLOW.brighter())
dataView.setSelectionBackground(Color.CYAN.darker())
dataView.setEnabled(False)

class Header(DefaultTableCellRenderer):
    def __init__(self, toolTip):
        super(Header, self)
        self.help = toolTip

    def setValue(self, value):
        super(self.__class__, self).setValue(value)
        self.setEnabled(True)
        self.setToolTipText(self.help)
        self.setText(value)
        self.setFont(Font(FONT_JP, Font.BOLD, 12))
        self.setHorizontalAlignment(JLabel.CENTER)
        self.setForeground(Color.DARK_GRAY)
        self.setBackground(Color.WHITE)
        self.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1, False))

idCol = dataView.getColumnModel().getColumn(0)
idCol.setWidth(24)
idCol.setMinWidth(24)
idCol.setMaxWidth(24)
idCol.setPreferredWidth(24)
idCol.setResizable(False)

titleCol = dataView.getColumnModel().getColumn(1)
titleCol.setWidth(120)
titleCol.setMinWidth(100)
titleCol.setMaxWidth(120)
titleCol.setPreferredWidth(120)
titleCol.setResizable(True)

phraseCol = dataView.getColumnModel().getColumn(2)
phraseCol.setWidth(180)
phraseCol.setMinWidth(120)
phraseCol.setMaxWidth(400)
phraseCol.setPreferredWidth(180)
phraseCol.setResizable(True)

methodCol = dataView.getColumnModel().getColumn(3)
imageCol = dataView.getColumnModel().getColumn(4)
offsetCol = dataView.getColumnModel().getColumn(5)
actCol = dataView.getColumnModel().getColumn(6)

idCol.setHeaderRenderer(Header(u'レコード数:30'))
titleCol.setHeaderRenderer(Header(u'最大文字数:20'))
phraseCol.setHeaderRenderer(Header(u'最大文字数:40'))
methodCol.setHeaderRenderer(Header(u'送信方法'))
imageCol.setHeaderRenderer(Header(u'最大サイズ:300Kpx'))
offsetCol.setHeaderRenderer(Header(u'x:y座標指定'))
actCol.setHeaderRenderer(Header(u'クリックで切替'))

class VmodeRenderer(DefaultTableCellRenderer):
    def getTableCellRendererComponent(self, table, val, isSelected, hasFocus, row, col):
        renderer = super(VmodeRenderer, self).getTableCellRendererComponent(table, val, isSelected, hasFocus, row, col)
        renderer.setEnabled(True)
        renderer.setFont(Font(FONT_JP, Font.PLAIN, 14))
        renderer.setBorder(BorderFactory.createLineBorder(Color.YELLOW.darker(), 3, True))
        if isSelected:
            renderer.setForeground(Color.MAGENTA.darker())
        else:
            renderer.setBackground(Color(128, 196, 196))
            renderer.setForeground(Color.LIGHT_GRAY.brighter())
        return renderer

class VidRenderer(VmodeRenderer):
    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR))
        self.setHorizontalAlignment(JLabel.RIGHT)
        self.setVerticalAlignment(JLabel.CENTER)
        self.setToolTipText(fmtStr(u'レコード:%d', val))

class VdefRenderer(VmodeRenderer):
    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.setHorizontalAlignment(JLabel.LEFT)
        self.setVerticalAlignment(JLabel.CENTER)
        self.setToolTipText(fmtStr(u'%s', val))

class BadgeRenderer(DefaultTableCellRenderer):
    def getTableCellRendererComponent(self, table, val, isSelected, hasFocus, row, col):
        renderer = super(BadgeRenderer, self).getTableCellRendererComponent(table, val, isSelected, hasFocus, row, col)
        renderer.setHorizontalAlignment(JLabel.CENTER)
        renderer.setVerticalAlignment(JLabel.CENTER)
        column = table.getColumnModel().getColumn(col)
        column.setWidth(35)
        column.setMinWidth(35)
        column.setMaxWidth(35)
        column.setPreferredWidth(35)
        column.setResizable(False)
        if isSelected:
            renderer.setBorder(BorderFactory.createLineBorder(Color.YELLOW.darker(), 3, True))
            renderer.setBackground(Color(224, 255, 255))
        else:
            renderer.setBorder(BorderFactory.createLineBorder(Color.PINK.darker(), 3, True))
            renderer.setBackground(None)
        if val is None: renderer.setBackground(Color(245, 245, 220))
        return renderer

from common.persistence import load_badge_db
badge = load_badge_db()
class MethodRenderer(BadgeRenderer):
    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setText(None)
        if val is None:
            self.setToolTipText(u'[編集]ボタンで変更')
            self.setIcon(badge.EMPTY)
        elif val is True:
            self.setToolTipText(u'現在値：タイプ')
            self.setIcon(badge.KEYBOARD)
        elif val is False:
            self.setToolTipText(u'現在値：ペースト')
            self.setIcon(badge.CLIPBOARD)

class PatternRenderer(BadgeRenderer):
    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setText(None)
        if val is None:
            self.setIcon(badge.BLANK)
            self.setToolTipText(u'[編集]モードで登録')
        else:
            self.setIcon(badge.FIGURE)
            self.setToolTipText(u'[編集]モードで変更')

class OffsetRenderer(BadgeRenderer):
    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setToolTipText(u'[編集]モードで変更')
        self.setText(None)
        if val is None:
            self.setIcon(badge.EMPTY)
        else:
            self.setIcon(badge.LOCATION)

class ActiveRenderer(DefaultTableCellRenderer):
    def getTableCellRendererComponent(self, table, val, isSelected, hasFocus, row, col):
        renderer = super(ActiveRenderer, self).getTableCellRendererComponent(table, val, isSelected, hasFocus, row, col)
        renderer.setHorizontalAlignment(JLabel.CENTER)
        renderer.setVerticalAlignment(JLabel.CENTER)
        column = table.getColumnModel().getColumn(col)
        column.setWidth(35)
        column.setMinWidth(35)
        column.setMaxWidth(35)
        column.setPreferredWidth(35)
        column.setResizable(False)
        renderer.setBorder(BorderFactory.createLineBorder(Color(178, 0, 178, 128), 3, True))
        if isSelected: renderer.setBackground(Color(224, 255, 255))
        else: renderer.setBackground(None)
        if val is None: renderer.setBackground(Color(245, 245, 220))
        return renderer

    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setText(None)
        if val is None:
            self.setToolTipText(u'利用不可')
            self.setIcon(badge.EMPTY)
        if val is True:
            self.setToolTipText(u'[無効化]ボタンで無効化')
            self.setIcon(badge.ENABLED)
        if val is False:
            self.setToolTipText(u'[有効化]ボタンで有効化');
            self.setIcon(badge.DISABLED)

from views.default import title
class ViewMode(object):
    def __init__(self):
        self.idRenderer = VidRenderer()
        self.defRenderer = VdefRenderer()
        self.mRenderer = MethodRenderer()
        self.pRenderer = PatternRenderer()
        self.oRenderer = OffsetRenderer()
        self.aRenderer = ActiveRenderer()


    def switch(self):
        methodCol.setHeaderValue(title.KEYTYPE_COLUMN)
        imageCol.setHeaderValue(title.IMAGE_COLUMN)
        offsetCol.setHeaderValue(title.AXES_COLUMN)
        caption.setText(title.VIEW_MODE)
        idCol.setCellRenderer(self.idRenderer)
        titleCol.setCellRenderer(self.defRenderer)
        phraseCol.setCellRenderer(self.defRenderer)
        methodCol.setCellRenderer(self.mRenderer)
        imageCol.setCellRenderer(self.pRenderer)
        offsetCol.setCellRenderer(self.oRenderer)
        actCol.setCellRenderer(self.aRenderer)


class EmodeRenderer(DefaultTableCellRenderer):
    def getTableCellRendererComponent(self, table, val, isSelected, hasFocus, row, col):
        renderer = super(EmodeRenderer, self).getTableCellRendererComponent(table, val, isSelected, hasFocus, row, col)
        renderer.setEnabled(True)
        renderer.setFont(Font(FONT_JP, Font.PLAIN, 14))
        if isSelected:
            renderer.setBackground(Color(250, 250, 200))
            renderer.setForeground(Color.BLUE.darker())
        else:
            renderer.setBackground(Color(250, 250, 250))
            renderer.setForeground(Color.DARK_GRAY)
        return renderer

class EidRenderer(EmodeRenderer):
    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR))
        self.setHorizontalAlignment(JLabel.RIGHT)
        self.setVerticalAlignment(JLabel.CENTER)
        self.setToolTipText(fmtStr(u'レコード:%d', val))
        self.setBorder(BorderFactory.createLineBorder(Color.YELLOW.darker(), 3, True))

class EdefRenderer(EmodeRenderer):
    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.setHorizontalAlignment(JLabel.LEFT)
        self.setVerticalAlignment(JLabel.CENTER)
        self.setToolTipText(fmtStr(u'%s', val))
        self.setBorder(BorderFactory.createLineBorder(Color.YELLOW.darker(), 3, True))

from views.default import initIcon, typeIcon, pasteIcon, style
class IconRenderer(DefaultTableCellRenderer):
    def getTableCellRendererComponent(self, table, val, isSelected, hasFocus, row, col):
        renderer = super(IconRenderer, self).getTableCellRendererComponent(table, val, isSelected, hasFocus, row, col)
        renderer.setBorder(BorderFactory.createLineBorder(Color.WHITE.darker(), 1, True))
        renderer.setHorizontalAlignment(JLabel.CENTER)
        renderer.setVerticalAlignment(JLabel.CENTER)
        renderer.setEnabled(True)
        column = table.getColumnModel().getColumn(col)
        column.setWidth(55)
        column.setMinWidth(55)
        column.setMaxWidth(55)
        column.setPreferredWidth(55)
        column.setResizable(False)
        if isSelected: renderer.setBackground(Color(173, 216, 230))
        else: renderer.setBackground(Color(250, 250, 250))
        return renderer

class TypeRenderer(IconRenderer):
    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setFont(Font('GothicBBB-Medium.Hankaku', Font.PLAIN, 14))
        self.setToolTipText(u'クリックして切替')
        self.setText(None)
        self.setIcon(typeIcon if val is True else pasteIcon if val is False else initIcon)

class SizeRenderer(IconRenderer):
    def setValue(self, image):
        super(self.__class__, self).setValue(image)
        self.setToolTipText(u'[クリップ]ボタンで変更')
        self.setFont(Font(FONT_JP, Font.PLAIN, 10))
        if image is None:
            self.setForeground(Color.BLUE)
            self.setText(fmtStr('%10s', '0px'))
        else:
            iSize = ceil(image.getWidth() * image.getHeight() / 100.0) / 10.0
            self.setForeground(Color.DARK_GRAY)
            self.setText(fmtStr('%,7.1fKpx', iSize))

class AxesRenderer(IconRenderer):
    def setValue(self, axes):
        super(self.__class__, self).setValue(axes)
        self.setToolTipText(u'[オフセット]ボタンで変更')
        self.setFont(Font('GothicBBB-Medium.Hankaku', Font.PLAIN, 12))
        if axes is None:
            self.setBackground(Color(220, 220, 220))
            self.setText(None)
        else:
            self.setBackground(Color(250, 250, 250))
            self.setForeground(Color.DARK_GRAY)
            tmpl = fmtStr(style.AXES, style.AXIS, style.VALUE)
            self.setText(fmtStr(tmpl, 'X', axes[0], 'Y', axes[1]))

class DisableRenderer(DefaultTableCellRenderer):
    def getTableCellRendererComponent(self, table, val, isSelected, hasFocus, row, col):
        renderer = super(DisableRenderer, self).getTableCellRendererComponent(table, val, isSelected, hasFocus, row, col)
        renderer.setHorizontalAlignment(JLabel.CENTER)
        renderer.setVerticalAlignment(JLabel.CENTER)
        column = table.getColumnModel().getColumn(col)
        column.setWidth(35)
        column.setMinWidth(35)
        column.setMaxWidth(35)
        column.setPreferredWidth(35)
        column.setResizable(False)
        renderer.setBackground(Color(192, 192, 192))
        return renderer

    def setValue(self, val):
        super(self.__class__, self).setValue(val)
        self.setToolTipText(u'選択モードに戻って変更')
        self.setText(None)
        if val is None: self.setIcon(None)
        else: self.setIcon(badge.ENABLED if val else badge.DISABLED)

class EditMode(object):
    def __init__(self):
        self.idRenderer = EidRenderer()
        self.defRenderer = EdefRenderer()
        self.tRenderer = TypeRenderer()
        self.sRenderer = SizeRenderer()
        self.xyRenderer = AxesRenderer()
        self.dRenderer = DisableRenderer()

    def switch(self):
        methodCol.setHeaderValue(title.METHOD_COLUMN)
        imageCol.setHeaderValue(title.SIZE_COLUMN)
        offsetCol.setHeaderValue(title.OFFSET_COLUMN)
        caption.setText(title.EDIT_MODE)
        idCol.setCellRenderer(self.idRenderer)
        titleCol.setCellRenderer(self.defRenderer)
        phraseCol.setCellRenderer(self.defRenderer)
        methodCol.setCellRenderer(self.tRenderer)
        imageCol.setCellRenderer(self.sRenderer)
        offsetCol.setCellRenderer(self.xyRenderer)
        actCol.setCellRenderer(self.dRenderer)

from startup import blankImage
from utils.imageViewer import ImageBank, Preview
preview = Preview(ImageBank(preset=blankImage))

viewMode = ViewMode()
editMode = EditMode()

tScrollPane = JScrollPane(dataView)
tViewport = tScrollPane.getViewport()
tScrollPane.setPreferredSize(Dimension(490, 220))
tScrollPane.setMinimumSize(Dimension(490, 220))

tPanel.setPreferredSize(Dimension(490, 210))
tPanel.setMinimumSize(Dimension(464, 210))
tPanel.setMaximumSize(Dimension(640, 210))
tPanel.add(tScrollPane, BorderLayout.CENTER)
