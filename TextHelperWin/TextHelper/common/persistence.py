#coding:utf-8

import sys, codecs, jarray
from os import path, getenv

from org.sikuli.basics import Debug, Settings
from org.sikuli.script.Sikulix import popat, popup, popError

from utils.graphical import MOD_LOG, CON_LOG, DIS_LOG, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from java.sql import DriverManager, ResultSet, Types, JDBCType, SQLException as JSQLException
from java.io import File, FileInputStream
from java.nio.file import Files, Paths
from java.lang import Class, Integer
from java.net import URI, URL
from javax.swing import ImageIcon

from utils.supplement import genConst
from utils.image_rw import decode_png, encode_png

distPath = path.dirname(path.dirname(path.dirname(path.dirname(__file__))))

def load_resource_db(table):
    def decorator(query):
        def loader():
            rdbPath = Paths.get(distPath, 'data', 'resource_data_pg')
            rdb = None
            try:
                rdb = DriverManager.getConnection(r'jdbc:h2:file:'+ rdbPath.toString() + r';MODE=PostgreSQL', None)
                drawLog(fmtStr(CON_LOG, rdbPath.getFileName()))

                query_item = fmtStr('SELECT symbol, pngimg FROM %s', table)
                item_set = rdb.prepareStatement(query_item).executeQuery()

                artifacts = query(item_set)

            except JSQLException as ex:
                popat()
                popError(ex.getLocalizedMessage(), u'エラー・メッセージ')
                Debug.error('SQL Exception %d is risen.', ex.getErrorCode())

            else: return artifacts

            finally:
                if (not rdb.isClosed()) if rdb is not None else False:
                    rdb.close()
                    drawLog(fmtStr(DIS_LOG, rdbPath.getFileName()))
        return loader
    return decorator

@load_resource_db('status_image')
def load_icon_db(items):
    image_set = {}
    while items.next():
        image_set[items.getString('symbol').upper()] = decode_png(items.getBytes('pngimg'))
    return genConst(image_set)

@load_resource_db('badge_image')
def load_badge_db(items):
    icon_set = {}
    while items.next():
        icon_set[items.getString('symbol').upper()] = ImageIcon(decode_png(items.getBytes('pngimg')))
    return genConst(icon_set)

def load_profile_db(record_list=None):
    rdbPath = Paths.get(distPath, 'data', 'profile_data_pg')

    all_record = r"SELECT id, symbol, phrase, keytype, pngimg, axes, active FROM petterns;"
    select_record = r"SELECT symbol, phrase, keytype, pngimg, axes, active FROM petterns WHERE id = ?;"
    rdb = None
    try:
        rdb = DriverManager.getConnection(r'jdbc:h2:file:'+ rdbPath.toString() + r';MODE=PostgreSQL', None)
        drawLog(fmtStr(CON_LOG, rdbPath.getFileName()))
        rdb.setAutoCommit(False)
        record_set = None
        
        def java_array(sql_array): return jarray.array(list(sql_array.getArray()), Integer)

        def get_all(record_set):
            while record_set.next():
                ID = record_set.getInt('id')
                symbol = record_set.getString('symbol')
                phrase = record_set.getString('phrase')
                keytype = None if record_set.getObject('keytype') is None else record_set.getBoolean('keytype')
                imageBytes = decode_png(record_set.getBytes('pngimg'))
                axes = None if record_set.getObject('axes') is None else java_array(record_set.getArray('axes'))
                active = None if record_set.getObject('active') is None else record_set.getBoolean('active')
                yield (ID, [symbol, phrase, keytype, imageBytes, axes, active])

        def get_selection(query, records):
            for index in records:
                query.setInt(1, index)
                record_set = query.executeQuery()
                if record_set.next(): 
                    ID = index
                    symbol = record_set.getString('symbol')
                    phrase = record_set.getString('phrase')
                    keytype = None if record_set.getObject('keytype') is None else record_set.getBoolean('keytype')
                    imageBytes = decode_png(record_set.getBytes('pngimg'))
                    axes = None if record_set.getObject('axes') is None else record_set.getArray('axes').getArray()
                    active = None if record_set.getObject('active') is None else record_set.getBoolean('active')
                    yield (ID, [symbol, phrase, keytype, imageBytes, axes, active])

        if record_list is None:
            query = rdb.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE, ResultSet.CONCUR_UPDATABLE)
            record_gen = get_all(query.executeQuery(all_record))
        else:
            query = rdb.prepareStatement(select_record)
            record_gen = get_selection(query, record_list)
    except JSQLException as ex:
        popat()
        popError(ex.getLocalizedMessage(), u'エラー・メッセージ')
        Debug.error('SQL Exception %d is risen.', ex.getErrorCode())
        if (not rdb.isClosed()) if rdb is not None else False:
            rdb.rollback()
    else:
        return { key:val for key, val in record_gen }
    finally:
        if (not rdb.isClosed()) if rdb is not None else False:
            rdb.close()
            drawLog(fmtStr(DIS_LOG, rdbPath.getFileName()))


def update_profile_db(record_list):
    rdbPath = Paths.get(distPath, 'data', 'profile_data_pg')

    update_record = """         
    UPDATE petterns SET
        (symbol, phrase, keytype, pngimg, axes, active)
        = (?, ?, ?, ?, ?, ?) WHERE id=?;
    """

    rdb = None
    try:
        rdb = DriverManager.getConnection(r'jdbc:h2:file:'+ rdbPath.toString() + r';MODE=PostgreSQL', None)
        Debug.info(CON_LOG, rdbPath.getFileName())
        
        def sql_array(x_axis, y_axis):
            java_array = jarray.array([x_axis, y_axis], Integer)
            return rdb.createArrayOf('int', java_array)
        rdb.setAutoCommit(False)
        sql_queue = rdb.prepareStatement(update_record)
    
        for ID, content in record_list.items():
            symbol, phrase, keytype, imageBytes, axes, active, = content
            sql_queue.setString(1, symbol)
            sql_queue.setString(2, phrase)
            sql_queue.setNull(3, Types.BOOLEAN) if keytype is None else sql_queue.setBoolean(3, keytype)
            sql_queue.setBytes(4, encode_png(imageBytes))
            sql_queue.setNull(5, Types.ARRAY) if axes is None else sql_queue.setArray(5, sql_array(*axes))
            sql_queue.setNull(6, Types.BOOLEAN) if active is None else sql_queue.setBoolean(6, active)
            sql_queue.setInt(7, ID)
            sql_queue.addBatch()

        sql_queue.executeBatch()
        sql_queue.clearBatch()
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
            Debug.info(DIS_LOG, rdbPath.getFileName())
