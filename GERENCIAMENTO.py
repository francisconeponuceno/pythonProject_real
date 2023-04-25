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


#VALIDAR O LOGIN
def cheklogin():
    try:
        USUARIO = login.txt01_usuario.text().strip()
        SENHA = login.txt01_senha.text().strip()
        banco = sqlite3.connect('banco03.db')
        cursor = banco.cursor()
        cursor.execute(f" SELECT * FROM tab_usuarios WHERE USUARIO = '{USUARIO}' AND SENHA = '{SENHA}'")
        RESP = cursor.fetchall()
        if RESP[0][1] == USUARIO and RESP[0][2] == SENHA and RESP[0][4] == 'ADMINISTRADOR':
            login.close()
            sistema.show()
        if RESP[0][1] == USUARIO and RESP[0][2] == SENHA and RESP[0][4] == 'USUARIO':
            login.close()
            sistema.show()
            sistema.btn02_cad_usuario.setVisible(False)
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('ALERTA!')
        msg.setInformativeText('USUÁRIO OU SENHA INVÁLIDA!')
        msg.exec()


############################################CRIAR BANCO DE DADOS##########################################
def cad_usuario():
    try:
        NOME = sistema.txt02_nome.text().strip()
        USUARIO = sistema.txt02_usuario.text().strip()
        SENHA = sistema.txt02_senha.text().strip()
        SENHA2 = sistema.txt02_senha2.text().strip()
        PERFIL = sistema.cb02_perfil.currentText().strip()
        if USUARIO =='' or SENHA == '' or SENHA2 != SENHA:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('ALERTA!')
            msg.setInformativeText('USUÁRIO OU SENHA NÃO PODE FICAR VASIO,OU SENHA2 NÃO PODE SER DIFERENTE DE SENHA!')
            msg.exec()
            return None
        else:
            banco = sqlite3.connect('banco03.db')
            cursor = banco.cursor()
            cursor.execute(f"INSERT INTO tab_usuarios VALUES{NOME,USUARIO,SENHA,SENHA2,PERFIL}");
            banco.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle('ALERTA!')
            msg.setInformativeText('USUÁRIO CADASTRADO COM SUCESSO!')
            msg.exec()
            banco.close()
            sistema.txt02_nome.setText('')
            sistema.txt02_usuario.setText('')
            sistema.txt02_senha.setText('')
            sistema.txt02_senha2.setText('')
            sistema.txt02_nome.setFocus()
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('ALERTA!')
        msg.setInformativeText('ERRO AO CADASTRAR USUÁRIO!')
        msg.exec()
############################################INFERCAFE GRÁFICA###############################################
app=QtWidgets.QApplication([])
sistema = uic.loadUi('progeto_real.ui')
login = uic.loadUi('logalt.ui')


############################################PAGINAS DO SISTEMA##############################################
sistema.btn_home.clicked.connect(lambda: sistema.pg_mestre.setCurrentWidget(sistema.pg_home))
sistema.btn_tabelas.clicked.connect(lambda: sistema.pg_mestre.setCurrentWidget(sistema.pg_tabelas))
sistema.btn02_cad_usuario.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_usuario))
sistema.btn_sobre.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_sobre))
sistema.btn_contatos.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_contatos))


############################################BOTÕES DA TELA DE LOGIN##########################################
login.btn01_login.clicked.connect(cheklogin)


############################################BOTÕES DA TELA CADASTRO DE USUÁRIO###############################
sistema.btn02_cadastrar.clicked.connect(cad_usuario)


login.show()
app.exec()