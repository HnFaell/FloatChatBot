import sys
import requests
import json
from PyQt5 import QtWidgets, QtCore, QtGui

# ----------------- Konfigurasi API -----------------

OPENAI_API_KEY =  "API_KEY_OPENAI_DI_SINI" # Ganti dengan API Key OpenAI milik Anda
DEFAULT_MODEL = "gpt-3.5-turbo"

# ----------------- Dialog Konfigurasi -----------------

class ConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚠︎ Perhatian ⚠︎")  
        self.setFixedSize(300, 250)
        self.setup_ui()
        self.apply_stylesheet()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        info_label = QtWidgets.QLabel(
            "- Selamat datang di AIdea!\n"
            "- Ini adalah aplikasi chatbot mengambang yang menggunakan API OpenAI.\n"
            "- Gunakan dengan bijak dan Hemat token untuk menghindari biaya berlebih.\n"
            "- enjoy!"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        close_btn = QtWidgets.QPushButton("Tutup")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QDialog { background: #2a2a2a; color: white; }
            QLabel { background: transparent; font-weight: bold; font-size: 14px; color: white; }
            QPushButton {
                background: grey; border: none; border-radius: 6px; padding: 8px 20px; color: black; font-weight: bold;
            }
            QPushButton:hover {
                background: #5aa0f2;
            }
        """)


#----------------- Worker Thread untuk API -----------------

class APIWorker(QtCore.QThread):
    response_received = QtCore.pyqtSignal(str)
    error_occurred = QtCore.pyqtSignal(str)

    def __init__(self, model, messages, temperature, maxtokens):
        super().__init__()
        self.model = model
        self.messages = messages
        self.temperature = temperature
        self.maxtokens = maxtokens

    def run(self):
        if not OPENAI_API_KEY or OPENAI_API_KEY == "API_KEY_OPENAI_DI_SINI":
            self.error_occurred.emit("API Key OpenAI belum diatur.")
            return
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "max_tokens": self.maxtokens,
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                self.response_received.emit(ai_response)
            else:
                errormessage = response.text
                try:
                    errorjson = response.json()
                    errormessage = errorjson.get("error", {}).get("message", errormessage)
                except json.JSONDecodeError:
                    pass
                self.error_occurred.emit(f"HTTP {response.status_code}: {errormessage}")
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Permintaan time out setelah 30 detik. Coba lagi.")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Kesalahan koneksi: {e}")
        except Exception as e:
            self.error_occurred.emit(f"Kesalahan umum: {e}")


# ----------------- Aplikasi Utama -----------------

class FloatingChatbot(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(400, 500)
        self.model = DEFAULT_MODEL
        self.temperature = 0.7
        self.maxtokens = 300
        self.messages = []
        self.dragpos = None
        self.isminimized = False
        self.setup_ui()
        self.apply_stylesheet()
        self.screenwidth = QtWidgets.QApplication.desktop().screenGeometry().width()
        self.screenheight = QtWidgets.QApplication.desktop().screenGeometry().height()
        self.add_message("⚠︎", "Halo! AIdea siap digunakan. klik ikon ⚙ untuk melihat S&K.", "#C2C2C2")

    def setup_ui(self):
        self.mainlayout = QtWidgets.QVBoxLayout(self)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.container = QtWidgets.QWidget()
        self.container.setObjectName("container")
        containerlayout = QtWidgets.QVBoxLayout(self.container)
        containerlayout.setContentsMargins(12, 12, 12, 12)
        containerlayout.setSpacing(8)
        self.create_header(containerlayout)
        self.create_chat_display(containerlayout)
        self.create_input_area(containerlayout)
        self.mainlayout.addWidget(self.container)
        self.bubble = QtWidgets.QLabel("AI")
        self.bubble.setObjectName("bubble")
        self.bubble.setAlignment(QtCore.Qt.AlignCenter)
        self.bubble.setFixedSize(60, 60)
        self.bubble.hide()
        self.bubble.mousePressEvent = self.bubble_clicked
        self.mainlayout.addWidget(self.bubble, alignment=QtCore.Qt.AlignCenter)

    def create_header(self, parentlayout):
        header = QtWidgets.QWidget()
        headerlayout = QtWidgets.QHBoxLayout(header)
        headerlayout.setContentsMargins(0, 0, 0, 0)
        titlelabel = QtWidgets.QLabel("⏣ AIdea")
        titlelabel.setStyleSheet("background: transparent; font-weight: bold; font-size: 18px; color: white;")
        headerlayout.addWidget(titlelabel)
        headerlayout.addStretch()
        configbtn = QtWidgets.QPushButton("⚙")
        configbtn.setFixedSize(30, 30)
        configbtn.clicked.connect(self.show_config)
        configbtn.setObjectName("headerBtn")
        headerlayout.addWidget(configbtn)
        self.togglebtn = QtWidgets.QPushButton("•")
        self.togglebtn.setFixedSize(30, 30)
        self.togglebtn.clicked.connect(self.toggle_minimize)
        self.togglebtn.setObjectName("headerBtn")
        headerlayout.addWidget(self.togglebtn)
        closebtn = QtWidgets.QPushButton("⨂")
        closebtn.setFixedSize(30, 30)
        closebtn.clicked.connect(self.close)
        closebtn.setObjectName("headerBtn")
        headerlayout.addWidget(closebtn)
        parentlayout.addWidget(header)

    def create_chat_display(self, parentlayout):
        self.chatdisplay = QtWidgets.QTextEdit()
        self.chatdisplay.setReadOnly(True)
        self.chatdisplay.setObjectName("chatDisplay")
        parentlayout.addWidget(self.chatdisplay)

    def create_input_area(self, parentlayout):
        inputcontainer = QtWidgets.QWidget()
        inputlayout = QtWidgets.QHBoxLayout(inputcontainer)
        inputlayout.setContentsMargins(0, 0, 0, 0)
        inputlayout.setSpacing(8)
        self.inputfield = QtWidgets.QLineEdit()
        self.inputfield.setPlaceholderText("Ketik pesan Anda...")
        self.inputfield.setObjectName("inputField")
        self.inputfield.returnPressed.connect(self.send_message)
        inputlayout.addWidget(self.inputfield)
        sendbtn = QtWidgets.QPushButton("Kirim")
        sendbtn.setObjectName("sendBtn")
        sendbtn.clicked.connect(self.send_message)
        sendbtn.setFixedWidth(80)
        inputlayout.addWidget(sendbtn)
        parentlayout.addWidget(inputcontainer)

# ----------------- Stylesheet -----------------

    def apply_stylesheet(self):
        self.setStyleSheet("""
            #container {
                background: rgba(30, 30, 30, 240);
                border-radius: 12px;
            }
            #chatDisplay {
                background: rgba(20, 20, 20, 150);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            #inputField {
                background: rgba(50, 50, 50, 200);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            #sendBtn {
                background: grey;
                border: none;
                border-radius: 6px;
                color: black;
                font-weight: bold;
                padding: 8px;
            }
            #sendBtn:hover {
                background: rgba(90, 150, 255, 220);
            }
            #headerBtn {
                background: transparent;
                border: none;
                color: white;
                font-weight: bold;
                font-size: 18px;
            }
            #headerBtn:hover {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            #bubble {
                background: rgba(50, 50, 50, 200);
                border-radius: 30px;
                color: white;
                font-weight: bold;
                font-size: 20px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)

# ----------------- bubble minimize -----------------

    def toggle_minimize(self):
        if not self.isminimized:
            self.container.hide()
            self.bubble.show()
            self.resize(60, 60)
            self.move(self.screenwidth - 80, self.screenheight - 80)
            self.isminimized = True
        else:
            self.bubble.hide()
            self.container.show()
            self.resize(400, 500)
            self.move(self.screenwidth - 410, self.screenheight - 510)
            self.isminimized = False

    def bubble_clicked(self, event):
        self.toggle_minimize()


# ----------------- Fungsi Utama -----------------

    def show_config(self):
        dialog = ConfigDialog(self)
        dialog.exec()

    def add_message(self, role, message, color="#cccccc"):
        message_escaped = (
            message.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )
        html = f'<p style="color:{color};"><b>{role}</b>: {message_escaped}</p>'
        self.chatdisplay.append(html)

    def send_message(self):
        user_text = self.inputfield.text().strip()
        if not user_text:
            return
        self.add_message("☺︎", user_text, "#C2C2C2")
        self.inputfield.clear()
        self.messages.append({"role": "user", "content": user_text})
        self.worker = APIWorker(self.model, self.messages, self.temperature, self.maxtokens)
        self.worker.response_received.connect(self.receive_response)
        self.worker.error_occurred.connect(self.api_error)
        self.worker.start()

    def receive_response(self, response):
        self.add_message("𖠌", response, "#C2C2C2")
        self.messages.append({"role": "assistant", "content": response})

    def api_error(self, error_message):
        self.add_message("⚠︎", error_message, "#886357")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragpos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragpos)
            event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    chatbot = FloatingChatbot()
    chatbot.show()
    sys.exit(app.exec())

