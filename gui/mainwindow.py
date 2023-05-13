from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, \
    QListWidgetItem, QPushButton, QMessageBox,QTextBrowser, QScrollArea, QScrollBar
from PyQt5.QtCore import Qt, QTimer
from gui.editurl import EditUrlDialog
from gui.settings import SettingsDialog
import PyQt5.QtCore as QtCore
import utils.spider as Spider
import PyQt5.QtGui as QtGui


class MainWindow(QMainWindow):
    edit_url_clicked = QtCore.pyqtSignal()
    settings_clicked = QtCore.pyqtSignal()
    def __init__(self, database, spider):
        super().__init__()
        # self.add_url_func = add_url_func
        # self.get_urls_func = get_urls_func
        self.database = database
        self.spider = spider
        self.current_urls = []
        self.init_ui()
        #self.refresh_any_updates()
        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(24*60*60*1000)
        self.refresh_timer.timeout.connect(self.refresh_any_updates)
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

        # that's wrong
        # self.content_update_list = QListWidget()
        # main_layout.addWidget(self.content_update_list)
        self.text_browser = QTextBrowser()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.text_browser)
        main_layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        edit_url_button = QPushButton('Edit URLs')
        edit_url_button.clicked.connect(self.show_edit_url_dialog)
        button_layout.addWidget(edit_url_button)

        refresh_button = QPushButton('Refresh')
        refresh_button.clicked.connect(self.refresh_any_updates)
        button_layout.addWidget(refresh_button)

        settings_button = QPushButton('Settings')
        settings_button.clicked.connect(self.show_settings_dialog)
        button_layout.addWidget(settings_button)

    def refresh_any_updates(self):
        exist_update = self.spider.check_all(self.database)
        if exist_update:
            self.text_browser.clear()
            self.refresh_content_mainwindow()
            QMessageBox.information(self, 'Info', 'There are new updates!')
        
    def refresh_content_mainwindow(self):
        self.text_browser.clear()
        all_links = self.database.get_all_last_content_upgrade()
        html = ""
        for link in all_links:
            html += f"<a href='{link[1]}'>{link[0]}</a><br>"
        self.text_browser.setHtml(html)
        self.text_browser.moveCursor(QtGui.QTextCursor.End)
        self.text_browser.ensureCursorVisible()
        self.text_browser.openExternalLinks()
        # self.content_update_list.clear()
        # all_links = self.database.get_all_last_content_upgrade()
        # #print(all_links)
        # for link in all_links:
        #     item = QListWidgetItem()
        #     item.setText("<a href='{0}'>{1}</a>".format(link[1], link[0]))
        #     item.setToolTip("<html><head/><body><p>" + item.text() + "</p></body></html>")
        #     self.content_update_list.addItem(item)
        #     print(item)
        
        # all_links = self.database.get_all_last_content_upgrade()
        # #self.scrollbar.setValue(self.scrollbar.maximum())
        # for link in all_links:
        #     item = "<a href='{0}'>{1}</a>".format(link[1], link[0])
        #     self.textedit.append(item)
        #     self.scrollbar.setValue(self.scrollbar.maximum())
        #     # self.scrollbar = self.scroll_area.verticalScrollBar()
        #     print(item)

        

    def refresh_urls(self):
        #self.current_urls = self.get_urls_func()
        self.current_urls = []
        self.url_list.clear()
        for url in self.current_urls:
            item = QListWidgetItem(f"{url[1]} ({url[2]})")
            item.setData(Qt.UserRole, url[0])
            self.url_list.addItem(item)
        print('refresh urls')

    def show_edit_url_dialog(self):
        urls = self.database.get_urls()
        dialog = EditUrlDialog(self.database, urls, self)
        dialog.exec_()
        #self.refresh_urls()

    def show_settings_dialog(self):
        dialog = SettingsDialog(self.refresh_timer.interval()/(60*60*1000), self)
        if dialog.exec_():
            self.refresh_timer.setInterval(int(dialog.time_edit.text())*60*60*1000)

    def scrollbar_moved(self, value):
        self.text_browser.verticalScrollBar().setValue(value)



    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  #-
        else:
            event.ignore()
