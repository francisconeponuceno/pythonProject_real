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
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase,QSqlTableModel
from PyQt5 import QtCore,QtWidgets
from PyQt5 import Qt
import requests
import json
#import auto_py_to_exe
import sys
import xml.etree.ElementTree as Et
from xml.dom import minidom
import re
import pandas as pd
import matplotlib.pyplot as plt
from utils import mensagem,cadastrar
############################################LOGIN#########################################################


#VALIDAR O LOGIN
def cheklogin():
    try:
        DATA = date.today()
        DATA = str(DATA.strftime('%d/%m/%Y'))
        USUARIO = login.txt01_usuario.text().strip()
        SENHA = login.txt01_senha.text().strip()
        NFe = '557316'
        banco = sqlite3.connect('banco03.db')
        cursor = banco.cursor()
        cursor.execute(f" SELECT * FROM tab_usuarios WHERE USUARIO = '{USUARIO}' AND SENHA = '{SENHA}'")
        RESP = cursor.fetchall()
        if RESP[0][1] == USUARIO and RESP[0][2] == SENHA and RESP[0][4] == 'ADMINISTRADOR':
            login.close()
            sistema.lbl_usuario.setText(f'{USUARIO}'.upper())
            sistema.lbl_data.setText(f'{DATA}')
            sistema.show()
        if RESP[0][1] == USUARIO and RESP[0][2] == SENHA and RESP[0][4] == 'USUARIO':
            login.close()
            sistema.lbl_usuario.setText(f'{USUARIO}'.upper())
            sistema.lbl_data.setText(f'{DATA}')
            sistema.show()
            sistema.btn02_cad_usuario.setVisible(False)
    except:
        mensagem('USUÁRIO OU SENHA INVÁLIDO!')



############################################CRIAR BANCO DE DADOS##########################################


def cad_usuario():
    try:
        NOME = sistema.txt02_nome.text().strip()
        USUARIO = sistema.txt02_usuario.text().strip()
        SENHA = sistema.txt02_senha.text().strip()
        SENHA2 = sistema.txt02_senha2.text().strip()
        PERFIL = sistema.cb02_perfil.currentText().strip()
        DADOS = [NOME,USUARIO,SENHA,SENHA2,PERFIL]

        if USUARIO =='' or SENHA == '' or SENHA2 != SENHA:
            mensagem('USUÁRIO OU SENHA NÃO PODE FICAR VASIO,OU SENHA2 NÃO PODE SER DIFERENTE DE SENHA!')
            return None
        else:
            cadastrar('tab_usuarios', DADOS)
            #banco = sqlite3.connect('banco03.db')
            #cursor = banco.cursor()
            #cursor.execute(f"INSERT INTO tab_usuarios VALUES{NOME,USUARIO,SENHA,SENHA2,PERFIL}");
            #banco.commit()
            #mensagem('USUÁRIO CADASTRADO COM SUCESSO!')
            #banco.close()
            sistema.txt02_nome.setText('')
            sistema.txt02_usuario.setText('')
            sistema.txt02_senha.setText('')
            sistema.txt02_senha2.setText('')
            sistema.txt02_nome.setFocus()
    except:
        mensagem('ERRO AO CADASTRAR USUÁRIO!')


def lerarquivo():
    try:
        caminho,_ = QFileDialog.getOpenFileNames(sistema,"Abrir o arquivo xml","Arquivos de xml (.xml)")
        sistema.txt02_xml.setText(f'{caminho}')
    except:
        mensagem('ERRO! O ARQUIVO QUE VOCÊ ESTA TENTANDO ABRIR NÃO E XML!')


def importat_xml():
    try:
        contador = 0
        caminho,_ = QFileDialog.getOpenFileNames(sistema,"Abrir o arquivo xml","Arquivos de xml (.xml)")
        if caminho == []:
            return
        sistema.txt02_xml.setText(f'{caminho}')
        sistema.pbr_xml.setMaximum(len(caminho))
        for a in caminho:
            DADOS_EMITENTE = []
            nfe = minidom.parse(a)
            NFe = nfe.getElementsByTagName('nNF')
            banco = sqlite3.connect('banco03.db')
            cursor = banco.cursor()
            cursor.execute(f" SELECT * FROM NOTAS WHERE NFe = '{NFe[0].firstChild.data}'")
            RESP1 = cursor.fetchall()
            if RESP1 != []:
                mensagem(f'A NF-e {NFe[0].firstChild.data} JA EXISTE NO BANCO, EXCLUA DA SELEÇÃO!')
                sistema.txt02_xml.setText(f'')
                return
            SERIE = nfe.getElementsByTagName('serie')
            DATA_EMISSAO = nfe.getElementsByTagName('dhEmi')
            CHAVE = nfe.getElementsByTagName('chNFe')
            CNPJ_EMITENTE = nfe.getElementsByTagName('CNPJ')
            NOME_EMITENTE = nfe.getElementsByTagName('xNome')
            VALOR_NF = nfe.getElementsByTagName('vNF')
            DATA_EMISSAO[0].firstChild.data = f"{DATA_EMISSAO[0].firstChild.data[8:10]}/{DATA_EMISSAO[0].firstChild.data[5:7]}/{DATA_EMISSAO[0].firstChild.data[:4]}"
            EMITENTE = [NFe,SERIE,DATA_EMISSAO,CHAVE,CNPJ_EMITENTE,NOME_EMITENTE,VALOR_NF]
            for e in EMITENTE:
                DADOS_EMITENTE.append(e[0].firstChild.data)
            sistema.txt02_xml.setText('')
            contador +=1
            itens = nfe.getElementsByTagName('det')
            codigo = nfe.getElementsByTagName('cProd')
            QANTIDADE = nfe.getElementsByTagName('qCom')
            produto = nfe.getElementsByTagName('xProd')
            UNIMED = nfe.getElementsByTagName('uCom')
            V_PRODUTO = nfe.getElementsByTagName('vProd')
            ITEM_NOTA = []
            COD = []
            DESCRICAO = []
            QNTD = []
            UNIDADE_MEDIDA = []
            VALOR_PRODUTO = []
            DADOS = []
            DATA_IMPORTACAO = date.today()
            DATA_IMPORTACAO = str(DATA_IMPORTACAO.strftime('%d/%m/%Y'))
            USUARIO = sistema.lbl_usuario.text()
            DATA_SAIDA = ''
            IMPORTACAO = [DATA_IMPORTACAO,USUARIO,DATA_SAIDA]
            for i in itens:
                ITEM_NOTA.append(i.attributes['nItem'].value)
            for c in codigo:
                COD.append(c.firstChild.data)
            for p in produto:
                DESCRICAO.append(p.firstChild.data)
            for q in QANTIDADE:
                QNTD.append(q.firstChild.data)
            for u in UNIMED:
                UNIDADE_MEDIDA.append(u.firstChild.data)
            for v in V_PRODUTO:
                VALOR_PRODUTO.append(v.firstChild.data)
            for a in range(0,len(itens)):
                DADOS.append(ITEM_NOTA[a]),DADOS.append(COD[a]),DADOS.append(QNTD[a]),
                DADOS.append(DESCRICAO[a]),DADOS.append(UNIDADE_MEDIDA[a]),DADOS.append(VALOR_PRODUTO[a])
                DADOS_COMPLETO = DADOS_EMITENTE + DADOS + IMPORTACAO
                ###################GRAVAÇÃO DOS DADOS NO BANCO#############################################
                banco = sqlite3.connect('banco03.db')
                cursor = banco.cursor()
                cursor.execute(f"""INSERT INTO NOTAS VALUES{DADOS_COMPLETO[0],DADOS_COMPLETO[1],DADOS_COMPLETO[2],DADOS_COMPLETO[3],
                DADOS_COMPLETO[4],DADOS_COMPLETO[5],DADOS_COMPLETO[6],DADOS_COMPLETO[7],DADOS_COMPLETO[8],DADOS_COMPLETO[9],
                DADOS_COMPLETO[10],DADOS_COMPLETO[11],DADOS_COMPLETO[12],DADOS_COMPLETO[13],DADOS_COMPLETO[14],DADOS_COMPLETO[15]}""");
                banco.commit()
                banco.close()
                DADOS = []
        reset_tabelas()
        sistema.pbr_xml.setValue(contador)
        mensagem(f'IMPORTAÇÃO CONCLUÍDA! FORAM IMPORTADOS {contador} ARQUIVOS')
        sistema.pbr_xml.setValue(0)
    except:
        mensagem('ERRO! O ARQUIVO QUE VOCÊ ESTA TENTANDO ABRIR NÃO E XML!')


def tabela_estoque():
    try:
        sistema.tw_estoque.setStyleSheet(u" QHeaderView{ color:black}; color:#fff;font-size: 15px;")
        banco = sqlite3.connect('banco03.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT * FROM NOTAS WHERE DATA_SAIDA = ''")
        NOTAS = cursor.fetchall()
        NIVEL = ''
        for n in NOTAS:
            if n[0] == NIVEL:
                QTreeWidgetItem(sistema.campo, n)
            else:
                sistema.campo = QTreeWidgetItem(sistema.tw_estoque, n)
                sistema.campo.setCheckState(0,QtCore.Qt.CheckState.Unchecked)
            NIVEL = n[0]
        sistema.tw_estoque.setSortingEnabled(True)
        for i in range(0,15):
            sistema.tw_estoque.resizeColumnToContents(i)
    except:
        mensagem('NÃO FOI POSSÍVEL SELECIONAR OS REGISTROS!')


def tabela_saida():
    try:
        sistema.tw_saida.setStyleSheet(u" QHeaderView{ color:black}; color:#fff;font-size: 15px;")
        banco = sqlite3.connect('banco03.db')
        cursor = banco.cursor()
        cursor.execute(f"SELECT NFe,SERIE,DATA_IMPORTACAO,DATA_SAIDA,USUARIO FROM NOTAS WHERE DATA_SAIDA != ''")
        NOTAS = cursor.fetchall()
        NIVEL = ''
        for n in NOTAS:
            if n[0] == NIVEL:
                QTreeWidgetItem(sistema.campo, n)
            else:
                sistema.campo = QTreeWidgetItem(sistema.tw_saida, n)
                sistema.campo.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
            NIVEL = n[0]
        sistema.tw_saida.setSortingEnabled(True)
        for i in range(0, 5):
            sistema.tw_saida.resizeColumnToContents(i)
    except:
        mensagem("NÃO FOI POSSÍVEL SELECIONAR OS REGISTROS.")


def tabela_geral():
    try:
        sistema.tw_geral.setStyleSheet(u" QHeaderView{ color:black}; color:#fff;font-size: 15px;")
        db = QSqlDatabase('QSQLITE')
        db.setDatabaseName('banco03.db')
        db.open()
        sistema.model = QSqlTableModel(db=db)
        sistema.tw_geral.setModel(sistema.model)
        sistema.model.setTable('NOTAS')
        sistema.model.select()
        sistema.tw_geral.setSortingEnabled(True)
        for i in range(0, 15):
            sistema.tw_geral.resizeColumnToContents(i)
    except:
        mensagem("NÃO FOI POSSÍVEL SELECIONAR OS REGISTRO!")


def reset_tabelas():
    try:
        sistema.tw_estoque.clear()
        sistema.tw_saida.clear()
        tabela_saida()
        tabela_estoque()
        tabela_geral()
    except:
        mensagem('ERRO!')


def gerar_saida():
    try:
        USUARIO = sistema.lbl_usuario.text()
        NFe = sistema.txt_saida.text().strip()
        DATA_SAIDA = date.today()
        DATA_SAIDA = str(DATA_SAIDA.strftime('%d/%m/%Y'))
        msg = QMessageBox()
        msg.setWindowTitle('A NFe(S) SERÃO EXCLUÍDAS DO ESTOQUE!')
        msg.setInformativeText('DESEJA REALMENTE DAR A SAIDA DA(S) NFe(S)?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            banco = sqlite3.connect('banco03.db')
            cursor = banco.cursor()
            cursor.execute(f"UPDATE NOTAS SET DATA_SAIDA = '{DATA_SAIDA}',USUARIO = '{USUARIO}' WHERE NFe = '{NFe}'");
            banco.commit()
            banco.close()
            reset_tabelas()
            sistema.txt_saida.clear()
    except:
        mensagem('ERRO AO GERAR A SAÍDA!')

def gerar_estorno():
    try:
        USUARIO = sistema.lbl_usuario.text()
        NFe = sistema.txt_estorno.text().strip()
        DATA_SAIDA = date.today()
        DATA_SAIDA = str(DATA_SAIDA.strftime('%d/%m/%Y'))
        msg = QMessageBox()
        msg.setWindowTitle('A NFe(S) SERÃO ESTORNADA PARA O ESTOQUE!')
        msg.setInformativeText('DESEJA REALMENTE ESTORNAR A(S) NFe(S)?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        resp = msg.exec()
        if resp == QMessageBox.Yes:
            banco = sqlite3.connect('banco03.db')
            cursor = banco.cursor()
            cursor.execute(f"UPDATE NOTAS SET DATA_SAIDA = '',USUARIO = '{USUARIO}' WHERE NFe = '{NFe}'");
            banco.commit()
            banco.close()
            reset_tabelas()
            sistema.txt_estorno.clear()
    except:
        mensagem('ERRO AO GERAR A SAÍDA!')


def gerar_excel():
    try:
        banco = sqlite3.connect('banco03.db')
        result = pd.read_sql_query("SELECT * FROM NOTAS",banco)
        result.to_excel("Resumo de notas.xlsx",sheet_name='NOTAS',index=False)
        mensagem('RELATÓRIO GERADO COM SUCESSO!')
    except:
        mensagem('ERRO AO GERAR O EXCEL!')


def gerar_grafico():
    try:
        banco = sqlite3.connect('banco03.db')
        ESTOQUE = pd.read_sql_query("SELECT * FROM NOTAS", banco)
        SAIDA = pd.read_sql_query("SELECT * FROM NOTAS WHERE DATA_SAIDA != ''", banco)
        ESTOQUE = len(ESTOQUE)
        SAIDA = len(SAIDA)
        labels = "Estoque","Saída"
        sizes = [ESTOQUE,SAIDA]
        fig1, axl = plt.subplots()
        axl.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=True,startangle=90)
        axl.axis("equal")
        plt.show()
    except:
        mensagem('ERRO AO GERAR O GRÁFICO')


############################################INFERCAFE GRÁFICA###############################################
app=QtWidgets.QApplication([])
sistema = uic.loadUi('progeto_real.ui')
login = uic.loadUi('logalt.ui')
icone = QIcon(R"C:\Users\Faturamento\PycharmProjects\pythonProject_real\imagens\icon.png")
login.setWindowIcon(icone)
sistema.setWindowIcon(icone)

############################################PAGINAS DO SISTEMA##############################################
sistema.btn_home.clicked.connect(lambda: sistema.pg_mestre.setCurrentWidget(sistema.pg_home))
sistema.btn_tabelas.clicked.connect(lambda: sistema.pg_mestre.setCurrentWidget(sistema.pg_tabelas))
sistema.btn02_cad_usuario.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_usuario))
sistema.btn_sobre.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_sobre))
sistema.btn_contatos.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_contatos))
sistema.btn_pg_importar.clicked.connect(lambda:sistema.pg_mestre.setCurrentWidget(sistema.pg_import))


############################################BOTÕES DA TELA DE LOGIN##########################################
login.btn01_login.clicked.connect(cheklogin)


############################################BOTÕES DA TELA CADASTRO DE USUÁRIO###############################
sistema.btn02_cadastrar.clicked.connect(cad_usuario)
#sistema.btn02_abrir.clicked.connect(tabela_estoque)
sistema.btn02_importar.clicked.connect(importat_xml)
sistema.btn_saida.clicked.connect(gerar_saida)
sistema.btn_estorno.clicked.connect(gerar_estorno)
sistema.btn_excel.clicked.connect(gerar_excel)
sistema.btn_grafico.clicked.connect(gerar_grafico)
reset_tabelas()

login.show()
app.exec()