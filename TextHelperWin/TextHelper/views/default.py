#coding:utf-8

import sys, codecs, jarray
from os import path, getenv

from java.lang.String import format as fmtStr
from utils.graphical import MOD_LOG, drawLog
from startup import icon

drawLog(fmtStr(MOD_LOG, __name__))

from java.awt import Dimension, Font, Color, Point, RenderingHints, Toolkit
from javax.swing import JFrame
from java.awt.image import BufferedImage

from utils.supplement import genConst, wideNum
from common.configuration import Config

class Workbench(JFrame):
    def __init__(self, title, size):
        self.setTitle(title)
        self.setSize(size)
        self.centering()
        self.setIconImage(icon.CONCEPT)
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

    def centering(self): self.setLocationRelativeTo(None)

from common.persistence import update_profile_db

class Studio(Workbench):
    def __init__(self, preset, body):
        super(Studio, self).__init__(None, Dimension(0, 0))
        self.config = preset
        self.profile = body

    def supply(self, table):
        row = table.getSelectedRow()
        for seq in range(5):
            table.setValueAt(self.profile[row+1][seq], row, seq+1)

    def inject(self, table):
        row = table.getSelectedRow()
        for seq in range(5):
            self.profile[row+1][seq] = table.getValueAt(row, seq+1)

    def restAct(self, table):
        row = table.getSelectedRow()
        table.setValueAt(self.profile[row+1][5], row, 6)
        vAdapter.preview(dataView, dataView.getSelectedRow(), info.SELECT_RECORD)

    def initialize(self, table):
        for ID, prof in self.profile.items():
            table.setValueAt(ID, ID-1, 0)
            for seq in range(6): table.setValueAt(prof[seq] , ID-1, seq+1)

    def finalize(self, table):
        for seq in range(table.getRowCount()):
            self.profile[seq+1][5] = table.getValueAt(seq, 6)

    def persistent_config(self): self.config.save()

    def persistent_profile(self): update_profile_db(self.profile)


title_string = {}
title_string['MAIN_MENU'] = u'TEXT HELPER | プロファイルメニュー'
title_string['VIEW_MODE'] = u'<html><font color=maroon>プロファイル選択モード</font></html>'
title_string['EDIT_MODE'] = u'<html><font color=navy>プロファイル編集モード</font></html>'
title_string['TITLE_COLUMN'] = u'タイトル'
title_string['PHRASE_COLUMN'] = u'入力テキスト'
title_string['KEYTYPE_COLUMN'] = u'操作'
title_string['METHOD_COLUMN'] = u'送信方法'
title_string['SIZE_COLUMN'] = u'サイズ'
title_string['IMAGE_COLUMN'] = u'画像'
title_string['AXES_COLUMN'] = u'位置'
title_string['OFFSET_COLUMN'] = u'入力座標'
title_string['ACTIVE_COLUMN'] = u'状態'

title = genConst(title_string)

info_desc = {}
info_desc['SELECT_RECORD'] = u'リストをクリックしてレコードを選択'
info_desc['MODE_CHANGE'] = u'［タイトル］［入力テキスト］［送信方法］セルをクリックで編集'
info_desc['CANCEL_PHRASE'] = u'入力テキストの編集をキャンセルしました'
info_desc['PHRASE_LIMIT'] = u'40文字以内で入力テキストを編集'
info_desc['PHRASE_UPDATE'] = u'入力テキストを設定、送信方法は%sです'
info_desc['TITLE_LIMIT'] = u'20文字以内でタイトルを編集'
info_desc['TITLE_UPDATE'] = u'レコードタイトルを設定しました'
info_desc['CANCEL_TITLE'] = u'タイトルの編集をキャンセルしました'
info_desc['RESET_RECORD'] = u'設定をクリアしました'
info_desc['ACTIVATED'] = u'レコードID:%dのスキャンを有効化しました'
info_desc['DEACTIVATED'] = u'レコードID:%dのスキャンを無効化しました'
info_desc['CANCEL_OFFSET'] = u'オフセットをキャンセルしました'
info_desc['CANCEL_CAPTURE'] = u'画像クリップをキャンセルしました'
info_desc['IMAGE_VALID'] = u'識別パターン画像を登録しました。'
info_desc['MODIFY_OFFSET'] = u'オフセット座標を取得しました。'

info = genConst(info_desc)

notice_desc = {}
notice_desc['SELECTION'] = u'レコードID:%dを編集しています' 
notice_desc['NAVIGATION'] = u'[Enter]確定　[ESC]キャンセル　[Ctrl+Z]やり直し'
notice_desc['TITLE_LIMIT_OVER'] = u'タイトルが最大文字数:20を超えています'
notice_desc['PHRASE_LIMIT_OVER'] = u'入力テキストが最大文字数:40を超えています'
notice_desc['PHRASE_INVALID'] = u'【タイプ】では「_」以外の半角英数字のみ利用できます'
notice_desc['SAVE_OFFER'] = u'[保存]ボタンでレコードを保存して下さい'
notice_desc['SAVE_COMPLETED'] = u'レコードID:%dを保存しました'
notice_desc['GREEN'] = '<html><font color=green>%s</font></html>'
notice_desc['RED'] = '<html><font color=red>%s</font><html>'

notice = genConst(notice_desc)

button_label = {}
button_label['DRY_RUN'] = u'テスト'
button_label['ACTIVATE'] = u'有効化'
button_label['DEACTIVATE'] = u'無効化'
button_label['CAPTURE'] = u'クリップ'
button_label['EDIT'] = u'編集'
button_label['QUIT'] = u'終了'
button_label['RESET'] = u'クリア'
button_label['SAVE'] = u'保存'
button_label['BACK'] = u'戻る'

button = genConst(button_label)

warn_desc = {}
warn_desc['FORCE_QUIT'] = u'編集モード終了確認'
warn_desc['SKIP_EDIT'] = u'セルの編集を中断して選択モードに戻りますか？'
warn_desc['SKIP_SAVE'] = u'レコードを保存していませんが選択モードに戻りますか？'
warn_desc['FORCE_CLOSE'] = u'レコードメニュー終了確認'
warn_desc['EDIT_DISCARD'] = u'セルの編集を中断してメニューを終了しますか？'
warn_desc['SAVE_DISCARD'] = u'レコードを保存していませんがメニューを終了しますか？'

warn = genConst(warn_desc)

caution_item = {}
caution_item['HEADER'] = '<h2 color=red><font face="%s">%%s</font></h2>'
caution_item['STYLE'] = ('<tt color=blue>%d   </tt>', '<tt color=green>%s   </tt>')
caution_item['DETAIL'] = u'<pre><font face="%1$s" size=4>レコードID:%2$sタイトル:%3$s</font></pre>'
caution_item['CONTENT'] = '<html>%1$s%2$s</html>'
caution_item['DECORATE'] = u'<html><h2><font color=red>%s</font></h2></html>'
caution_item['REJECTED'] = u'最前面のアプリケーションのウィンドウ画像を取得できません'

caution = genConst(caution_item)

style_item = {}
style_item['AXES'] = '<html><pre><b>%1$s%2$s<br>%1$s%2$s<b/></pre></html>'
style_item['AXIS'] = '<font color=green size=2>%s</font>'
style_item['VALUE'] = '<font color=blue size=2>%+7d</font>'

style = genConst(style_item)

from javax.swing import ImageIcon
from utils.graphical import FONT_JP

iconFont = Font(FONT_JP, Font.BOLD, 10)
initImage = BufferedImage(40, 20, BufferedImage.TYPE_4BYTE_ABGR)
graph = initImage.getGraphics()
graph.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
graph.setFont(iconFont)
graph.setColor(Color.WHITE)
graph.drawString(u'ペースト', 0, 8)
graph.drawString(u' タイプ', 0, 20)
initIcon = ImageIcon(initImage)

pasteImage = BufferedImage(40, 20, BufferedImage.TYPE_4BYTE_ABGR)
graph = pasteImage.getGraphics()
graph.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
graph.setFont(iconFont)
graph.setColor(Color.GREEN.darker())
graph.drawString(u'ペースト', 0, 8)
graph.setColor(Color.WHITE)
graph.drawString(u' タイプ', 0, 20)
pasteIcon = ImageIcon(pasteImage)

typeImage = BufferedImage(40, 20, BufferedImage.TYPE_4BYTE_ABGR)
graph = typeImage.getGraphics()
graph.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
graph.setFont(iconFont)
graph.setColor(Color.WHITE)
graph.drawString(u'ペースト', 0, 8)
graph.setColor(Color.RED.darker())
graph.drawString(u' タイプ', 0, 20)
typeIcon = ImageIcon(typeImage)

def axesIcon(x_axis, y_axis):
    axesImage = BufferedImage(55, 25, BufferedImage.TYPE_4BYTE_ABGR)
    graph = axesImage.getGraphics()
    graph.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
    graph.setFont(Font(FONT_JP, Font.PLAIN, 13))
    graph.setColor(Color.DARK_GRAY)
    graph.drawString('x:%+5d'.format(x_axis), 3, 10)
    graph.drawString('y:%+5d'.format(y_axis), 3, 20)
    return ImageIcon(axesImage)
