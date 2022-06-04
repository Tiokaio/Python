import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from tkinter import filedialog as file
from PIL import Image
from Janela1 import *
from Janela2 import *
import sqlite3 as conn
import os


class janela2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Close_error.clicked.connect(self.fechaMensagem)
        self.ui.pushButton.clicked.connect(self.valida1)
        self.ui.pushButton_2.clicked.connect(self.selectImage)
        self.ui.pushButton_3.clicked.connect(self.trocatela)
        self.ui.Error.hide()
        self.ui.Close_error.hide()
        self.conectabanco()

    def conectabanco(self):
        if os.path.exists("Banco.db"):
            self.Conec = conn.connect("Banco.db")

        else:
            self.Conec = conn.connect("Banco.db")
            self.cursor = self.Conec.cursor()
            self.cursor.execute("""Create table USUARIO(
                                       NOME  not null,
                                       SENHA  not null,
                                       IMAGEM not null,                                
                                       Primary key (NOME))
                                       """)

            self.Conec.commit()

    def selectImage(self):
        if not os.path.exists("Novapasta"):
            os.mkdir("Novapasta")

        Cusuario = self.ui.getUser.text()
        if not Cusuario:
            self.ui.Error.show()
            self.ui.Close_error.show()
            self.ui.Error.setAlignment(Qt.AlignCenter)
            self.ui.Error.setText("Digite um Usuario")
        else:
            self.ui.Error.hide()
            self.ui.Close_error.hide()
            self.img = file.askopenfilename(title="Escolha Uma Imagem", filetypes=[("Image File", "*.jpg")])
            if not self.img:
                return
            else:
                with Image.open(self.img) as im:
                    # Provide the target width and height of the image
                    im.thumbnail(size=(80, 70))
                    if os.path.exists(f'Novapasta/{Cusuario}+thumb.jpg'):
                        self.imagem = f'Novapasta/{Cusuario}+thumb.jpg'
                    else:
                        im.save(f'Novapasta/{Cusuario}' + 'thumb.jpg')
                        self.imagem = f'Novapasta/{Cusuario}' + 'thumb.jpg'
                self.ui.image.setStyleSheet(f'background-image:url({self.imagem});'
                                            "background-color: rgb(255, 255, 255);\n"
                                            "border:6px solid rgb(53, 53, 53);\n"
                                            "border-radius: 35px\n")

    def trocatela(self):
        self.jan1 = janela1()
        self.hide()
        self.jan1.show()

    def fechaMensagem(self):
        self.ui.Error.hide()
        self.ui.Close_error.hide()

    def valida1(self):

        usuario = self.ui.getUser.text()
        senha = self.ui.getPassword.text()

        if not usuario:
            self.ui.Error.show()
            self.ui.Close_error.show()
            self.ui.Error.setText('USUARIO INVALIDO')
            self.ui.Error.setAlignment(Qt.AlignCenter)
        if not senha:
            self.ui.Error.show()
            self.ui.Close_error.show()
            self.ui.Error.setText('SENHA INVALIDA')
            self.ui.Error.setAlignment(Qt.AlignCenter)

        if usuario != '' and senha != '' and self.imagem != '':
            self.ui.Error.hide()
            conc = conn.connect('Banco.db')
            cursor = conc.cursor()
            sql = f"SELECT * FROM `USUARIO` WHERE `NOME` = '{usuario}'"
            cursor.execute(sql)

            if cursor.fetchone():
                self.ui.Error.show()
                self.ui.Close_error.show()
                self.ui.Error.setAlignment(Qt.AlignCenter)
                self.ui.Error.setText("Usuario já existe\n Tente Novamente")
            else:
                cursor.execute("INSERT INTO USUARIO (NOME,SENHA,IMAGEM) VALUES (?,?,?)",
                               (usuario, senha, self.imagem))
                conc.commit()
                self.ui.Error.setStyleSheet("background-color: rgb(0,255,127)")
                self.ui.Error.setText("Cadastramento Efetuado com Sucesso")
                self.ui.Error.setAlignment(Qt.AlignCenter)
                self.ui.Error.show()


class janela1(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.jan2 = janela2()
        self.conectabanco()
        self.ui.pushButton.clicked.connect(self.mudajanela)
        self.ui.Login.clicked.connect(self.valida)
        self.ui.Close_error.clicked.connect(self.fechaMensagem)

    def mudajanela(self):
        self.jan2.show()
        self.hide()

    def conectabanco(self):
        if os.path.exists("Banco.db"):
            self.Conec = conn.connect("Banco.db")

        else:
            self.Conec = conn.connect("Banco.db")
            self.cursor = self.Conec.cursor()
            self.cursor.execute("""Create table USUARIO(
                                   NOME  not null,
                                   SENHA  not null,
                                   IMAGEM not null,                                
                                   Primary key (NOME))
                                   """)

            self.Conec.commit()

    def fechaMensagem(self):
        self.ui.frame_3.hide()

    def valida(self):
        usuario = self.ui.getUser.text()
        senha = self.ui.getPassword.text()
        conc = conn.connect('Banco.db')
        cursor = conc.cursor()
        sql = f"SELECT * FROM `USUARIO` WHERE `NOME`= '{usuario}' AND `SENHA`='{senha}'"
        cursor.execute(sql)
        consulta=cursor.fetchone()
        if not consulta:
            self.ui.frame_3.show()
            self.ui.Error.setText('USUARIO NÃO CADASTRADO')
            self.ui.Error.setAlignment(Qt.AlignCenter)
        else:
            self.ui.frame_3.setStyleSheet("background-color: rgb(0,255,127);"
                                          "border-radius: 10px")
            self.ui.Error.setText("Login Efetuado Com Sucesso")
            self.ui.Error.setAlignment(Qt.AlignCenter)
            self.ui.frame_3.show()
            self.ui.image.setStyleSheet(f'background-image:url({consulta[2]});'
                                        "background-color: rgb(255, 255, 255);\n"
                                        "border:6px solid rgb(53, 53, 53);\n"
                                        "border-radius: 35px\n")
        if not senha:
            self.ui.frame_3.show()
            self.ui.Error.setText('INSIRA A SENHA')
            self.ui.Error.setAlignment(Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = janela1()

    w.show()
    sys.exit(app.exec_())
