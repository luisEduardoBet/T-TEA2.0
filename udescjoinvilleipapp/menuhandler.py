from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QLabel,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from udescjoinvilleipview.registerplayer import RegisterPlayer
from udescjoinvilleiputil.pathconfig import PathConfig

class MenuHandler:
    """Classe para gerenciar ações do menu"""
    def __init__(self, parent):
        self.parent = parent
        self._is_exiting = False  # Flag para evitar chamadas duplicadas

    def do_nothing(self):
        """Ação placeholder para funcionalidades não implementadas"""
        dialog = QDialog(self.parent)  # Usa QDialog e passa o parent
        dialog.setWindowTitle("Placeholder")
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(QPushButton("Do nothing button"))
        dialog.exec()  # Executa como modal

    def confirm_exit(self, event=None):
        """Confirmação de saída do sistema"""
        # Verifica se já está no processo de saída para evitar duplicação
        if self._is_exiting:
            if event is not None:
                event.accept()
            return

        msg_box = QMessageBox()
        msg_box.setWindowIcon(self.parent.windowIcon())
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("IPlane")
        msg_box.setText("Deseja sair do sistema?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)

        # Traduzir os botões
        msg_box.button(QMessageBox.Yes).setText("Sim")
        msg_box.button(QMessageBox.No).setText("Não")

        response = msg_box.exec()
        
        if response == QMessageBox.Yes:
            self._is_exiting = True  # Define a flag para indicar que está saindo
            if event is not None:  # Se for um evento de fechamento da janela
                event.accept()
            else:  # Se for chamado pelo menu
                QApplication.quit()
        elif event is not None:  # Apenas ignorar se for evento de janela
            event.ignore()


    def call_register(self):
        """Chama a janela de registro como modal"""
        register = RegisterPlayer(self.parent)  # Passa o parent (janela principal)
        register.exec()  # Executa como modal


    def call_KarTEA(self): 
        pass
        


    def show_about(self, image=None):
        """Exibe janela de sobre como modal"""
        about_window = QDialog(self.parent)  # Usa QDialog e passa o parent
        about_window.setWindowTitle("Sobre")
        about_window.setFixedSize(300, 200)

        if image is None:
            image = PathConfig.image("ttealogo.png")
        
        layout = QVBoxLayout()
        logo = QPixmap(image)
        logo_label = QLabel()
        logo_label.setPixmap(logo)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        about_window.setLayout(layout)
        about_window.exec()  # Executa como modal
