import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages":["barcode","reportlab","PyQt5","requests","num2words"]}

base = None
if sys.platform == 'win32':
    base = 'win32GUI'
executables = [
    Executable('GERENCIAMENTO.py',base=base,icon='icon.png')
]
buildOptions = dict (
    packages = ["barcode","reportlab","PyQt5","requests","num2words","pandas","matplotlib","xml","openpyxl"],
    includes = [],
    include_files = [
    'gmail.png','gmin.png','icon.png','icons8-imposto-100.png','logo.png','user1.png','USER2.png',
    'user3.png','user4.png','zap.png','zapim.png'],

)


#includeFiles = [
    #'cadastrar.png','caixa2.png','carrinho.png','compras.png','cons_venda.png','contas.png','editar.png',
    #'excluir.png','fecha.png','icone.ico','icons8-cardápio-64.png','icons8-comprimir-64.png',
    #'icons8-maximize-32.png','impressora.png','login.png','login100x100.png','logo.jpg','novo.png','pagar.png','pesquisar.png',
    #'produto.png','receber.png','recibo.png','salvar.png','usuarios.png'
#]



setup(
    name = 'SISTEMA DE GERENCIAMENTO',
    version = '1.0',
    description = 'SISTEMA DE GERENCIAMENTO',
    options = dict(build_exe =  buildOptions),
    executables=executables
)



