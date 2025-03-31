from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class MenuHandler:
    """Classe para gerenciar ações do menu (Princípio Single Responsibility)"""
    def __init__(self, parent):
        self.parent = parent
        self._is_exiting = False  # Flag para evitar chamadas duplicadas

    def do_nothing(self):
        """Ação placeholder para funcionalidades não implementadas"""
        dialog = QWidget()
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(QPushButton("Do nothing button"))
        dialog.show()

    def confirm_exit(self, event=None):
        """Confirmação de saída do sistema"""
        # Verifica se já está no processo de saída para evitar duplicação
        if self._is_exiting:
            if event is not None:
                event.accept()
            return

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("T-TEA")
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

    def show_about(self, image):
        """Exibe janela de sobre"""
        about_window = QWidget()
        about_window.setWindowTitle("Sobre")
        about_window.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        logo = QPixmap(image)
        logo_label = QLabel()
        logo_label.setPixmap(logo)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        about_window.setLayout(layout)
        about_window.show()
