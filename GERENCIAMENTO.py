print('olá mundo!')
from barcode import EAN13
from  barcode.writer import ImageWriter
from datetime import datetime
from datetime import date,timedelta
import reportlab
import PyQt5
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib import colors
import webbrowser
import os
from random import randint
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import *
import sqlite3
from time import sleep
from num2words import num2words
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve
from PyQt5 import QtCore,QtWidgets
import requests
import json
#import auto_py_to_exe
import sys
print('estou aprendendo a gerenciar repositorio!')

app=QtWidgets.QApplication([])
sistema = uic.loadUi('progeto_real.ui')
sistema.show()
app.exec()