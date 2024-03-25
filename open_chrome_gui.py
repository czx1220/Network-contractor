import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit,QWidget
from selenium.webdriver import Chrome
import os
from selenium.webdriver.chrome.options import Options

class PacketSenderWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("打开浏览器")
        self.resize(500,200)
        # self.setStyleSheet("background-color: #F0F0F0; color: #333333; font-size: 12px;")

        self.source_ip_label = QLabel("URL地址:", self)
        self.source_ip_label.move(50, 50)
        self.source_ip_entry = QLineEdit(self)
        self.source_ip_entry.move(150, 50)
        
        
        self.send_button = QPushButton("前往", self)
        self.send_button.move(150, 80)
        self.send_button.clicked.connect(self.go)
        
    def go(self):
        source_ip = self.source_ip_entry.text()
        chrome_options = Options()
        driver = Chrome(options=chrome_options)
        driver.get(source_ip)
        driver.quit()

# 创建应用程序对象
app = QApplication(sys.argv)

# 创建主窗口对象
window = PacketSenderWindow()

# 显示主窗口
window.show()

# 运行应用程序的消息循环
sys.exit(app.exec_())