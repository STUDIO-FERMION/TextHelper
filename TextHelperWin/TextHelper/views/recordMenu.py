#coding:utf-8

import sys, codecs, jarray
from os import path, getenv

from org.sikuli.script import (
    App, Screen, Finder, Pattern, Region, Match, Env, Key, KeyModifier
    )
from org.sikuli.script.Sikulix import popat, popup, popError

from java.awt import Dimension, Font, BorderLayout, Cursor, Container
from javax.swing import (
    JSplitPane, JPanel, DefaultCellEditor, JTextField, JOptionPane, JFrame, SwingUtilities, JDialog
    )
from java.awt.event import (
    MouseAdapter, MouseEvent, WindowAdapter, WindowEvent, ActionListener, KeyAdapter, KeyEvent
    )
from javax.swing.event import CellEditorListener

from views.default import info, title, notice, button, warn, caution
from views.recordView import preview, tPanel, dataView, titleCol, phraseCol, viewMode, editMode

from views.recordCtrl import (
    xBox, cPanel, doEdit, doActivate, doSave, goBack, doOffset, doCapture, doReset, doQuit,
    dryRun, gauge, eCtrl, vCtrl, iLabel, nLabel, xPanel
    )

from utils.graphical import MOD_LOG, FONT_JP, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

h2Pane = JSplitPane(JSplitPane.HORIZONTAL_SPLIT)
defSize = Dimension(512, 384);

leftMin = Dimension(476, 384)
xPanel.setMinimumSize(leftMin)
xPanel.setPreferredSize(defSize)
xPanel.setSize(defSize.width, defSize.height)

rightMin = Dimension(384, 384)
preview.sPane.setMinimumSize(rightMin)
preview.sPane.setPreferredSize(defSize)
preview.sPane.setSize(defSize.width, defSize.height)
h2Pane.setRightComponent(preview.sPane);
h2Pane.setLeftComponent(xPanel);

h2Pane.setDividerLocation(512)
h2Pane.setContinuousLayout(True)
h2Pane.setOneTouchExpandable(False);

from java.lang.String import format as fmtStr
class ViewAdapter(MouseAdapter):
    def compose(self, target):
        isActive = dataView.getValueAt(target, 6)
        if isActive is None:
            doActivate.setVisible(False)
            dryRun.setVisible(False)
        else:
            doActivate.setText(button.DEACTIVATE if isActive else button.ACTIVATE)
            doActivate.setVisible(True)
            dryRun.setVisible(True)

    def mousePressed(self, ev):
        if ev.getButton() == MouseEvent.BUTTON1:
            frame = ev.getSource().getTopLevelAncestor()
            frame.setEnabled(False) 
            frame.setCursor(Cursor(Cursor.WAIT_CURSOR))
            table = ev.getSource()
            row = table.rowAtPoint(ev.getPoint())
            dataView.changeSelection(row, row, False, False)
            self.compose(row)
            preview.imageData = dataView.getValueAt(row, 4)
            iLabel.setText(info.SELECT_RECORD)
            frame.setEnabled(True)
            frame.setCursor(Cursor(Cursor.DEFAULT_CURSOR))

vAdapter = ViewAdapter()

class DefEditor(DefaultCellEditor):
    def tryEntry(self):
        if self.source.isDisplayable(): self.stopCellEditing()

    def revert(self):
        if self.source.isDisplayable(): self.cancelCellEditing()

    def __init__(self, textFileld):
        super(self.__class__, self).__init__(textFileld)
        textFileld.setFont(Font(FONT_JP, Font.PLAIN, 13))
        self.source = textFileld

    def getTableCellEditorComponent(self, table, val ,focused, row, col):
        editor = super(self.__class__, self).getTableCellEditorComponent(table, val, focused, row, col)
        self.source.selectAll()
        return editor

titleEditor = DefEditor(JTextField(20))
phraseEditor = DefEditor(JTextField(40))
titleCol.setCellEditor(titleEditor)
phraseCol.setCellEditor(phraseEditor)

class EditAdapter(MouseAdapter):
    def __init__(self): self.preset = None

    def editTitle(self):
        phraseEditor.tryEntry()
        if dataView.isEditing(): return
        row = dataView.getSelectedRow()
        iLabel.setText(info.TITLE_LIMIT)
        nLabel.setText(notice.NAVIGATION)
        dataView.editCellAt(row, 1)
        titleEditor.source.requestDefaultFocus()
        titleEditor.source.selectAll()

    def editPhrase(self):
        titleEditor.tryEntry()
        if dataView.isEditing(): return
        row = dataView.getSelectedRow()
        iLabel.setText(info.PHRASE_LIMIT)
        nLabel.setText(notice.NAVIGATION)
        dataView.editCellAt(row, 2)
        phraseEditor.source.requestDefaultFocus()
        phraseEditor.source.selectAll()

    def mousePressed(self, ev):
        table, point = (ev.getSource(), ev.getPoint())
        row, col = (table.rowAtPoint(point), table.columnAtPoint(point))
        if ev.getButton() != MouseEvent.BUTTON1: return
        if row == table.getSelectedRow():
            if col == 1:
                if not titleEditor.source.isDisplayable(): self.editTitle()
            if col == 2:
                if not phraseEditor.source.isDisplayable(): 
                    self.preset = dataView.getValueAt(row, 3)
                    self.editPhrase()
            if col == 3:
                if titleEditor.source.isDisplayable(): return
                toggle = table.getValueAt(row, col)
                if phraseEditor.source.isDisplayable():
                    table.setValueAt((False if toggle is None else not toggle), row, col)
                else:
                    if dataView.getValueAt(row, 2) is None: return
                    self.preset = toggle
                    table.setValueAt((False if toggle is None else not toggle), row, col)
                    self.editPhrase()
                    phraseEditor.tryEntry()
                dataView.updateUI()
        else: nLabel.setText(fmtStr(notice.SELECTION, table.getSelectedRow()+1))

eAdapter = EditAdapter()

class EditImpl(ActionListener):
    def actionPerformed(self, ev):
        editMode.switch()
        frame = ev.getSource().getTopLevelAncestor()
        row = dataView.getSelectedRow()
        iLabel.setText(info.MODE_CHANGE)
        cPanel.remove(gauge)
        cPanel.add(nLabel, BorderLayout.CENTER)
        nLabel.setText(fmtStr(notice.SELECTION, row+1))
        cPanel.remove(vCtrl)
        cPanel.add(eCtrl, BorderLayout.SOUTH)
        doSave.setEnabled(False)
        doOffset.setVisible(False if dataView.getValueAt(row, 4) is None else True)
        dataView.removeMouseListener(vAdapter)
        dataView.addMouseListener(eAdapter) 
        dataView.updateUI()
        cPanel.updateUI()
        tPanel.setCursor(Cursor(Cursor.DEFAULT_CURSOR))

doEdit.addActionListener(EditImpl())

class BackImpl(ActionListener):
    def selectMode(self, stage):
        viewMode.switch()
        row = dataView.getSelectedRow()
        iLabel.setText(info.SELECT_RECORD)
        cPanel.remove(nLabel)
        cPanel.add(gauge, BorderLayout.CENTER)
        gauge.override()
        cPanel.remove(eCtrl)
        cPanel.add(vCtrl, BorderLayout.SOUTH)
        doSave.setEnabled(False)
        dataView.removeMouseListener(eAdapter)
        dataView.addMouseListener(vAdapter)
        vAdapter.compose(row)
        dataView.updateUI()
        cPanel.updateUI()
        tPanel.setCursor(Cursor(Cursor.HAND_CURSOR))
        stage.setCursor(Cursor(Cursor.DEFAULT_CURSOR))

    def actionPerformed(self, ev):
        frame = ev.getSource().getTopLevelAncestor()
        row = dataView.getSelectedRow()
        forRollBack = False

        if dataView.isEditing():
            JDialog.setDefaultLookAndFeelDecorated(True)
            choice = JOptionPane.showConfirmDialog(frame, warn.SKIP_EDIT, warn.FORCE_QUIT, JOptionPane.YES_NO_OPTION)
            if choice == JOptionPane.NO_OPTION or choice == JOptionPane.CLOSED_OPTION: return
            if choice == JOptionPane.YES_OPTION: pass

        if doSave.isEnabled():
            JDialog.setDefaultLookAndFeelDecorated(True)
            choice = JOptionPane.showConfirmDialog(frame, warn.SKIP_SAVE, warn.FORCE_QUIT, JOptionPane.YES_NO_OPTION)
            if choice == JOptionPane.NO_OPTION or choice == JOptionPane.CLOSED_OPTION: return
            if choice == JOptionPane.YES_OPTION: forRollBack = True

        titleEditor.revert()
        phraseEditor.revert()
        if forRollBack:
            frame.supply(dataView)
            preview.imageData = dataView.getValueAt(dataView.getSelectedRow(), 4)
            iLabel.setText(info.SELECT_RECORD)

        self.selectMode(frame)


bImpl = BackImpl()
goBack.addActionListener(bImpl)

class CloseAdapter(WindowAdapter):
     def windowClosing(self, ev):
        frame = ev.getSource()
        row = dataView.getSelectedRow()

        if dataView.isEditing():
            JDialog.setDefaultLookAndFeelDecorated(True)
            choice = JOptionPane.showConfirmDialog(frame, warn.EDIT_DISCARD, warn.FORCE_CLOSE, JOptionPane.YES_NO_OPTION)
            if choice == JOptionPane.NO_OPTION or choice == JOptionPane.CLOSED_OPTION: return
            if choice == JOptionPane.YES_OPTION: pass

        if eCtrl.isDisplayable() and doSave.isEnabled():
            JDialog.setDefaultLookAndFeelDecorated(True)
            choice = JOptionPane.showConfirmDialog(frame, warn.SAVE_DISCARD, warn.FORCE_CLOSE, JOptionPane.YES_NO_OPTION)
            if choice == JOptionPane.NO_OPTION or choice == JOptionPane.CLOSED_OPTION: return
            if choice == JOptionPane.YES_OPTION: pass

        titleEditor.revert()
        phraseEditor.revert()

        frame.finalize(dataView)
        frame.persistent_profile()
        bImpl.selectMode(frame)
        frame.removeWindowListener(self)
        frame.dispose()

closeAdapter = CloseAdapter()

class ActivateImpl(ActionListener):
    def actionPerformed(self, ev):
        row = dataView.getSelectedRow()
        flag = dataView.getValueAt(row, 6)
        if flag:
            dataView.setValueAt(False, row, 6)
            doActivate.setText(button.ACTIVATE)
            iLabel.setText(fmtStr(info.DEACTIVATED, row+1))
        else:
            dataView.setValueAt(True, row, 6)
            doActivate.setText(button.DEACTIVATE)
            iLabel.setText(fmtStr(info.ACTIVATED, row+1))
        gauge.override()
        dataView.updateUI()

doActivate.addActionListener(ActivateImpl())

from utils import imageClip, clickPoint
from java.util.concurrent import TimeUnit
from java.lang import Thread, Runnable

from math import ceil

class Trimer(Runnable):
    def __init__(self): self.owner = None

    def run(self):
        self.owner.setState(JFrame.ICONIFIED)
        self.owner.setCursor(Cursor(Cursor.WAIT_CURSOR))
        clip = imageClip.doRender(0.5, 300.0)
        row = dataView.getSelectedRow()
        if clip is None:
            iLabel.setText(info.CANCEL_CAPTURE)
            nLabel.setText(fmtStr(notice.SELECTION, row+1))
        else:
            iSize = ceil(clip.getWidth() * clip.getHeight() / 100.0) / 10.0
            self.owner.setEnabled(False)
            self.owner.setCursor(Cursor(Cursor.WAIT_CURSOR))
            dataView.setValueAt(clip, row, 4)
            doSave.setEnabled(True)
            preview.imageData = dataView.getValueAt(row, 4)
            iLabel.setText(info.IMAGE_VALID)
            dataView.setValueAt(jarray.array([0, 0], int), row, 5)
            nLabel.setText(fmtStr(notice.GREEN, notice.SAVE_OFFER))
            doOffset.setVisible(True)

        preview.setSize(preview.sPane.getSize())
        preview.sPane.getVerticalScrollBar().setVisible(True)
        preview.sPane.getHorizontalScrollBar().setVisible(True)

        self.owner.setCursor(Cursor(Cursor.DEFAULT_CURSOR))
        self.owner.setState(JFrame.NORMAL)
        self.owner.setEnabled(True)

trimer = Trimer()

class CaptureImpl(ActionListener):
    def actionPerformed(self, ev):
        row = dataView.getSelectedRow()
        titleEditor.tryEntry()
        phraseEditor.tryEntry()
        if dataView.isEditing(): return
        trimer.owner = ev.getSource().getTopLevelAncestor()
        thread = Thread(trimer)
        thread.start()
        dataView.updateUI()

doCapture.addActionListener(CaptureImpl())

from utils.robokey import type_jp
class Pointer(Runnable):
    def __init__(self):
        self.asTest = False
        self.owner = None

    def allocate(self, rect, record):
        axes = clickPoint.doRender(rect)
        if axes is None:
            iLabel.setText(info.CANCEL_OFFSET)
            nLabel.setText(fmtStr(notice.SELECTION, record+1))
        else:
            dataView.setValueAt(axes, record, 5)
            doSave.setEnabled(True)
            iLabel.setText(info.MODIFY_OFFSET)
            nLabel.setText(fmtStr(notice.GREEN, notice.SAVE_OFFER))
    def xfer(self, record, target):
        phrase = dataView.getValueAt(record, 2)
        target.setTargetOffset(*dataView.getValueAt(record, 5))
        target.click()
        target.type('a', Key.CTRL)
        target.type(Key.DELETE)
        if dataView.getValueAt(record, 3):
            type_jp(phrase)
        else:
            target.paste(target, phrase)
        TimeUnit.MILLISECONDS.sleep(1500)

    def discord(self, record):
        ID = dataView.getValueAt(record, 0)
        title = dataView.getValueAt(record, 1)
        popat()
        header = fmtStr(caution.HEADER, FONT_JP)
        detail = fmtStr(caution.DETAIL, FONT_JP, *caution.STYLE)
        content = fmtStr(caution.CONTENT, header, detail)
        JDialog.setDefaultLookAndFeelDecorated(True)
        popError(fmtStr(content, u'識別パターン検出不可', ID, title), u'画像スキャン結果')

    def collate(self, testee, scrap):
        row = dataView.getSelectedRow()
        finder = Finder(Screen().capture(testee).getImage())
        pattern = Pattern().setBImage(scrap).similar(0.9)
        finder.find(pattern)
        if finder.hasNext():
            match = finder.next()
            match.moveTo(match.offset(testee.getTopLeft()).getTopLeft())
            JFrame.setDefaultLookAndFeelDecorated(False)
            try:
                match.highlightOn('GRAY')
                TimeUnit.MILLISECONDS.sleep(500)
                match.highlightOff()
            except: match.highlight(1, 'GRAY')
            JFrame.setDefaultLookAndFeelDecorated(True)
            if self.asTest: self.xfer(row, match)
            else: self.allocate(match.getRect(), row)
        else: self.discord(row)

    def run(self):
        self.owner.setEnabled(False)
        self.owner.setState(JFrame.ICONIFIED)
        self.owner.setCursor(Cursor(Cursor.WAIT_CURSOR))
        row = dataView.getSelectedRow()
        area = App.focusedWindow()
        if area is None:
            JDialog.setDefaultLookAndFeelDecorated(True)
            popError(fmtStr(caution.DECORATE, caution.REJECTED), u'パターン認識不可')
        else:
            image = dataView.getValueAt(row, 4)
            if area.w < image.width or area.h < image.height: self.discord(row)
            else: self.collate(area, image)
        self.owner.setCursor(Cursor(Cursor.DEFAULT_CURSOR))
        self.owner.setState(JFrame.NORMAL)
        self.owner.setEnabled(True)

pointer = Pointer()

class OffsetImpl(ActionListener):
    def actionPerformed(self, ev):
        titleEditor.tryEntry()
        phraseEditor.tryEntry()
        if dataView.isEditing(): return
        pointer.asTest = False
        pointer.owner = ev.getSource().getTopLevelAncestor()
        thread = Thread(pointer)
        thread.start()

doOffset.addActionListener(OffsetImpl())

class TestImpl(ActionListener):
    def actionPerformed(self, ev):
        pointer.asTest = True
        pointer.owner = ev.getSource().getTopLevelAncestor()
        thread = Thread(pointer)
        thread.start()

dryRun.addActionListener(TestImpl())

class ResetImpl(ActionListener):
    def actionPerformed(self, ev):
        frame = ev.getSource().getTopLevelAncestor()
        frame.setCursor(Cursor(Cursor.WAIT_CURSOR))
        titleEditor.revert()
        phraseEditor.revert()
        row = dataView.getSelectedRow()
        for col in range(1, 6): dataView.setValueAt(None, row, col)
        dataView.updateUI()
        doCapture.setText(button.CAPTURE)
        doOffset.setVisible(False)
        doSave.setEnabled(True)
        preview.imageData = dataView.getValueAt(dataView.getSelectedRow(), 4)
        iLabel.setText(info.RESET_RECORD)
        nLabel.setText(notice.SAVE_OFFER)
        frame.setCursor(Cursor(Cursor.DEFAULT_CURSOR))

doReset.addActionListener(ResetImpl())

class SaveImpl(ActionListener):
    def actionPerformed(self, ev):
        frame = ev.getSource().getTopLevelAncestor()
        frame.setEnabled(False)
        frame.setCursor(Cursor(Cursor.WAIT_CURSOR))
        row = dataView.getSelectedRow()
        titleEditor.tryEntry()
        phraseEditor.tryEntry()

        if not dataView.isEditing():
            frame.inject(dataView)
            if dataView.getValueAt(row, 3) is None or dataView.getValueAt(row, 4) is None:
                dataView.setValueAt(None, row, 6)
            elif dataView.getValueAt(row, 6) is None: dataView.setValueAt(True, row, 6) 
            nLabel.setText(fmtStr(notice.SAVE_COMPLETED, row+1))
            doSave.setEnabled(False)

        cPanel.updateUI()
        dataView.updateUI()
        frame.setCursor(Cursor(Cursor.DEFAULT_CURSOR))
        frame.setEnabled(True)

doSave.addActionListener(SaveImpl())

class QuitImpl(ActionListener):
    def actionPerformed(self, ev):
        frame = ev.getSource().getTopLevelAncestor()
        frame.setCursor(Cursor(Cursor.WAIT_CURSOR))
        frame.finalize(dataView)
        frame.persistent_profile()
        frame.setCursor(Cursor(Cursor.DEFAULT_CURSOR))
        frame.removeWindowListener(closeAdapter)
        frame.dispose()

doQuit.addActionListener(QuitImpl())

class TitleEditorListener(CellEditorListener):
    def editingStopped(self, ev):
        row = dataView.getSelectedRow()
        val = dataView.getValueAt(row, 1)
        if len(val) <= 20:
            iLabel.setText(info.TITLE_UPDATE)
            nLabel.setText(fmtStr(notice.GREEN, notice.SAVE_OFFER))
            doSave.setEnabled(True)
        else:
            nLabel.setText(fmtStr(notice.RED, notice.TITLE_LIMIT_OVER))
            dataView.editCellAt(row, 1)
            titleEditor.source.requestDefaultFocus()

    def editingCanceled(self, ev):
        row = dataView.getSelectedRow()
        iLabel.setText(info.CANCEL_TITLE)
        nLabel.setText(fmtStr(notice.SELECTION, row+1))

titleEditor.addCellEditorListener(TitleEditorListener())

from java.util.regex.Pattern import compile as genRE, CASE_INSENSITIVE
class PhraseEditorListener(CellEditorListener):

    def editingStopped(self, ev):
        row = dataView.getSelectedRow()
        val = dataView.getValueAt(row, 2)
        isType = dataView.getValueAt(row, 3)

        def validate(phrase):
            if len(phrase) > 40:
                nLabel.setText(fmtStr(notice.RED, notice.PHRASE_LIMIT_OVER))
                return False
            elif len(phrase) > 0 and isType:
                pattern = genRE(r'^[a-zA-Z0-9 -~]+$', CASE_INSENSITIVE)
                if not pattern.matcher(phrase).matches() or r'_' in val:
                    nLabel.setText(fmtStr(notice.RED, notice.PHRASE_INVALID))
                    return False
            return True

        if validate(val):
            if len(val) == 0:
                dataView.setValueAt(None, row, 3)
                method =u'未設定'
            else:
                if isType is None: dataView.setValueAt(False, row, 3)
                method = u'【タイプ】' if dataView.getValueAt(row, 3) else u'【ペースト】'
            iLabel.setText(fmtStr(info.PHRASE_UPDATE, method))
            nLabel.setText(fmtStr(notice.GREEN, notice.SAVE_OFFER))
            doSave.setEnabled(True)
            dataView.updateUI()
        else:
            dataView.editCellAt(row, 2)
            phraseEditor.source.requestDefaultFocus()

    def editingCanceled(self, ev):
        row = dataView.getSelectedRow()
        dataView.setValueAt(eAdapter.preset, row, 3)
        iLabel.setText(info.CANCEL_PHRASE)
        nLabel.setText(fmtStr(notice.SELECTION, row+1))
        dataView.updateUI()

phraseEditor.addCellEditorListener(PhraseEditorListener())

class DefKeyImpl(KeyAdapter):
    def __init__(self, defEditor):
        super(self.__class__, self)
        self.editor = defEditor
        self.ctrl = False

    def keyPressed(self, ev):
        row, col = (dataView.getEditingRow(), dataView.getEditingColumn())
        if ev.getKeyCode() == KeyEvent.VK_CONTROL: self.ctrl = True
        if self.ctrl:
            if ev.getKeyCode() == KeyEvent.VK_Z:
                self.editor.cancelCellEditing()
                dataView.editCellAt(row, col)
                self.editor.source.requestDefaultFocus()
                self.editor.source.selectAll()
                self.ctrl = False
        elif ev.getKeyCode() == KeyEvent.VK_ESCAPE: self.editor.cancelCellEditing()

    def keyReleased(self, ev):
        if ev.getKeyCode() == KeyEvent.VK_CONTROL: self.ctrl = False

doSave.setEnabled(False)
titleEditor.source.addKeyListener(DefKeyImpl(titleEditor))
phraseEditor.source.addKeyListener(DefKeyImpl(phraseEditor))

def doRender(stage):
    stage.setTitle(title.MAIN_MENU)
    stage.setSize(Dimension(1024, 384))
    stage.centering()
    stage.setContentPane(h2Pane)
    stage.initialize(dataView)
    stage.setVisible(True)
    stage.setResizable(False)
    stage.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE)
    stage.addWindowListener(closeAdapter)
    dataView.changeSelection(0, 0, False, False)
    preview.imageData = dataView.getValueAt(dataView.getSelectedRow(), 4)
    bImpl.selectMode(stage)

