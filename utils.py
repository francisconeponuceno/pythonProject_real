from PyQt5.QtWidgets import QMessageBox
import sqlite3
def mensagem(frase):
    try:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('ALERTA!')
        msg.setInformativeText(f'{frase}')
        msg.exec()
        return msg
    except:
        mensagem('ERRO!')


def cadastrar(tabela,dados):
    try:
        banco = sqlite3.connect('banco03.db')
        cursor = banco.cursor()
        for d in dados:
            cursor.execute(f"INSERT INTO '{tabela}' VALUES '{d}'");
            banco.commit()
        mensagem('CADASTRO REALIZADO COM SUCESSO!')
        banco.close()
    except:
        mensagem('NÃO FOI POSSÍVEL REALIZAR O CADASTRO')