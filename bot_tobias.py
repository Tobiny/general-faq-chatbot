import asyncio
import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette, QTextCursor
from PyQt6.QtWidgets import QVBoxLayout, QSizePolicy, QLabel, QWidget, QPushButton
from rasa.core.agent import Agent

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, agent):
        super(MainWindow, self).__init__()
        self.agent = agent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tobias - Robotino Informativo")
        self.setFixedSize(800, 600)

        # Establecer una paleta de colores personalizada
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f2f2f2"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#333333"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#e5e5e5"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#333333"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#333333"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#3daee9"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#3daee9"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        self.setPalette(palette)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel("¡Hola! Soy Tobias, tu asistente de IA")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; margin-bottom: 20px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.text_display = QtWidgets.QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.text_display.setStyleSheet(
            "QTextEdit { background-color: #ffffff; border: none; border-radius: 10px; padding: 10px; font-size: 14px; color: #333333; }"
        )
        self.layout.addWidget(self.text_display)

        self.text_input = QtWidgets.QLineEdit()
        self.text_input.setStyleSheet(
            "QLineEdit { background-color: #ffffff; border: none; border-bottom: 2px solid #3daee9; padding: 5px; font-size: 14px; color: #333333; }"
        )
        self.text_input.setPlaceholderText("Escribe tu mensaje aquí...")
        self.text_input.returnPressed.connect(self.handle_input)
        self.layout.addWidget(self.text_input)

        self.text_input.setFocus()

    def handle_input(self):
        message = self.text_input.text()
        self.text_input.clear()

        # Añadir el mensaje del usuario al cuadro de diálogo
        self.add_user_message(message)

        response = asyncio.run(self.agent.handle_text(message))
        bot_response = response[0]["text"]

        # Añadir la respuesta del bot al cuadro de diálogo
        self.add_bot_message(bot_response)

    def add_user_message(self, message):
        self.text_display.append("<b style='color: #3daee9;'>Tú:</b> " + message)

    def add_bot_message(self, message):
        self.text_display.append("<b style='color: #333333;'>Tobias:</b> " + message)
        self.text_display.moveCursor(QTextCursor.MoveOperation.End)

def run_bot():
    agent = Agent.load("./models")
    app = QtWidgets.QApplication(sys.argv)

    # Configurar la fuente global de la aplicación
    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(12)
    app.setFont(font)

    main_window = MainWindow(agent)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_bot()
