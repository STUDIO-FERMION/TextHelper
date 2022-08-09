#coding:utf-8

import sys, codecs, jarray
from os import path, getenv

from org.sikuli.script.Sikulix import popat, popup, popError

from utils.graphical import MOD_LOG, drawLog
from java.lang.String import format as fmtStr
drawLog(fmtStr(MOD_LOG, __name__))

from java.sql import ResultSet, Types, SQLException as JSQLException
from java.io import FileInputStream, FileOutputStream, ByteArrayInputStream, ByteArrayOutputStream
from java.awt import SystemTray, TrayIcon
from javax.imageio import ImageIO
from java.nio.file import Files, Paths, Path
from java.awt.image import BufferedImage
from java.lang import Class

__all__ = ['encode_png', 'decode_png', 'get_image_fs', 'put_image_fs', 'put_image_db', 'get_image_db']

distPath = path.dirname(path.dirname(path.dirname(path.dirname(__file__))))

def encode_png(imageBytes):
    if imageBytes.__class__ is BufferedImage: 
        pngOut = ByteArrayOutputStream()
        succeed = ImageIO.write(imageBytes, 'PNG', ImageIO.createImageOutputStream(pngOut))
        pngBytes = pngOut.toByteArray()
        return pngBytes
    else: return None

def decode_png(pngBytes):
    if pngBytes:
        pngIn = ByteArrayInputStream(pngBytes)
        imageBytes = ImageIO.read(ImageIO.createImageInputStream(pngIn))
        return imageBytes
    else: return None

def cloneImage(imageBytes):
    if imageBytes.__class__ is BufferedImage: 
        return BufferedImage(imageBytes.getColorModel(), imageBytes.getData(), False, None)
    else: return None

from java.awt.image import ColorConvertOp
from java.awt.color import ColorSpace
def RGBtoMono(imageBytes):
    operator = ColorConvertOp(ColorSpace.getInstance(ColorSpace.CS_GRAY), None)
    return operator.filter(imageBytes, None)

def imgB3BGR(imageBytes):
    if imageBytes.__class__ is BufferedImage:
        image = BufferedImage(imageBytes.width, imageBytes.height, BufferedImage.TYPE_3BYTE_BGR)
        image.getGraphics().drawImage(imageBytes, 0, 0, imageBytes.width, imageBytes.height, None)
        return image
    else: return None
