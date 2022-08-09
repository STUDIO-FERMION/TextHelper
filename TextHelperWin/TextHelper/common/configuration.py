#coding:utf-8

import sys, codecs, jarray
from os import path, getenv

from org.sikuli.script.Sikulix import popat, popup, popError
from org.sikuli.basics import Debug

from utils.graphical import MOD_LOG, CON_LOG, DIS_LOG, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from java.sql import DriverManager, ResultSet, Types, JDBCType, SQLException as JSQLException
from java.io import File, FileInputStream
from java.nio.file import Files, Paths
from java.lang import System, Class, Integer
from java.net import URI, URL
from utils.image_rw import *

distPath = path.dirname(path.dirname(path.dirname(path.dirname(__file__))))

from org.sikuli.script import KeyModifier
from common.types import Flag, Subset, Const

class Config(object):
    direct = Flag(False)
    charkey = Subset('K', r'[0-9A-Z]|[-^\\@\[;:\],./]')
    shift = Const(KeyModifier.KEY_SHIFT, True)
    ctrl = Const(KeyModifier.KEY_CTRL, False)
    alt = Const(KeyModifier.KEY_ALT, True)

    @staticmethod
    def prepare():
        rdbPath = Paths.get(distPath, 'data', 'resource_data_pg')
        resource = DriverManager.getConnection(r'jdbc:h2:file:'+ rdbPath.toString() + r';MODE=PostgreSQL', None)
        drawLog(fmtStr(CON_LOG, rdbPath.getFileName()))
        return (rdbPath, resource)
    
    @classmethod
    def load(cls):
        rdb = None
        try:
            db_path, rdb = cls.prepare()
            query_config = r"SELECT charkey, direct, shift, ctrl, alt FROM settings WHERE symbol='config';"
            query = rdb.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_UPDATABLE)
            settings = query.executeQuery(query_config)
            settings.next()
            cls.__dict__['charkey'].__dict__['char'] = settings.getString('charkey')
            cls.__dict__['direct'].__dict__['state'] = settings.getBoolean('direct')
            cls.__dict__['shift'].__dict__['modify'] = settings.getBoolean('shift')
            cls.__dict__['ctrl'].__dict__['modify'] = settings.getBoolean('ctrl')
            cls.__dict__['alt'].__dict__['modify'] = settings.getBoolean('alt')
        except JSQLException as ex:
            popat()
            popError(ex.getLocalizedMessage(), u'エラー・メッセージ')
            Debug.error('SQL Exception %d is risen.', ex.getErrorCode())
            if (not rdb.isClosed()) if rdb is not None else False:
                rdb.rollback()
        finally:
            if (not rdb.isClosed()) if rdb is not None else False:
                rdb.close()
                drawLog(fmtStr(DIS_LOG, db_path.getFileName()))

    @classmethod
    def save(cls):
        rdb = None
        try:
            db_path, rdb = cls.prepare()
            Debug.info(CON_LOG, db_path.getFileName())
            rdb.setAutoCommit(False)
            update_config = r"UPDATE settings SET (direct, charkey, shift, ctrl, alt) = (?, ?, ?, ?, ?) WHERE symbol='config';"
            query = rdb.prepareStatement(update_config)
            query.setBoolean(1, cls.direct)
            query.setString(2, cls.charkey)
            query.setBoolean(3, cls.shift)
            query.setBoolean(4, cls.ctrl)
            query.setBoolean(5, cls.alt)
            query.executeUpdate()
        except JSQLException as ex:
            popat()
            popError(ex.getLocalizedMessage(), u'エラー・メッセージ')
            Debug.error('SQL Exception %d is risen.', ex.getErrorCode())
            if (not rdb.isClosed()) if rdb is not None else False:
                rdb.rollback()
        else:
            rdb.commit()
        finally:
            if (not rdb.isClosed()) if rdb is not None else False:
                rdb.close()
                drawLog(fmtStr(DIS_LOG, db_path.getFileName()))

    @classmethod
    def hotkey(cls):
        keyset = cls.charkey
        if cls.__dict__['shift'].modify: keyset += '+shift' 
        if cls.__dict__['ctrl'].modify: keyset += '+ctrl'
        if cls.__dict__['alt'].modify: keyset += '+alt'
        return keyset

    @classmethod
    def factory(cls):
        cls.load()
        return cls()
