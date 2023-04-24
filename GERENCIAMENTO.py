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

############################################LOGIN#########################################################
def logar():
    try:
        if login.txt01_usuario.text() == 'admin' and login.txt01_senha.text() == 'admin':
           sistema.show()
           login.close()
    except:
        'ERRO'


############################################INFERCAFE GRÁFICA###############################################
app=QtWidgets.QApplication([])
sistema = uic.loadUi('progeto_real.ui')
login = uic.loadUi('logalt.ui')


############################################PAGINAS DO SISTEMA##############################################
sistema.btn_home.clicked.connect(lambda: sistema.pg_mestre.setCurrentWidget(sistema.pg_home))
sistema.btn_tabelas.clicked.connect(lambda: sistema.pg_mestre.setCurrentWidget(sistema.pg_tabelas))
sistema.btn_cadastrar.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_usuario))
sistema.btn_sobre.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_sobre))
sistema.btn_contatos.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_contatos))
login.btn01_login.clicked.connect(logar)
login.show()
app.exec()