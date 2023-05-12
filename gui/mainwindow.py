from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, \
    QListWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from gui.editurl import EditUrlDialog
from gui.settings import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self, add_url_func,):
        super().__init__()
        self.add_url_func = add_url_func
        # self.get_urls_func = get_urls_func
        self.current_urls = []
        self.init_ui()
        self.refresh_urls()
        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(24*60*60*1000)
        self.refresh_timer.timeout.connect(self.refresh_urls)
        self.refresh_timer.start()

    def init_ui(self):
        self.setWindowTitle('My App')
        self.resize(600, 400)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        label = QLabel('Latest updates:')
        main_layout.addWidget(label)

        self.url_list = QListWidget()
        main_layout.addWidget(self.url_list)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        edit_url_button = QPushButton('Edit URLs')
        edit_url_button.clicked.connect(self.show_edit_url_dialog)
        button_layout.addWidget(edit_url_button)

        refresh_button = QPushButton('Refresh')
        refresh_button.clicked.connect(self.refresh_urls)
        button_layout.addWidget(refresh_button)

        settings_button = QPushButton('Settings')
        settings_button.clicked.connect(self.show_settings_dialog)
        button_layout.addWidget(settings_button)

    def refresh_urls(self):
        #self.current_urls = self.get_urls_func()
        self.current_urls = []
        self.url_list.clear()
        for url in self.current_urls:
            item = QListWidgetItem(f"{url[1]} ({url[2]})")
            item.setData(Qt.UserRole, url[0])
            self.url_list.addItem(item)

    def show_edit_url_dialog(self):
        dialog = EditUrlDialog(self.add_url_func, self.current_urls, self)
        dialog.exec_()
        self.refresh_urls()

    def show_settings_dialog(self):
        dialog = SettingsDialog(self.refresh_timer.interval()/(60*60*1000), self)
        if dialog.exec_():
            self.refresh_timer.setInterval(int(dialog.time_edit.text())*60*60*1000)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
