from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, \
    QListWidgetItem, QPushButton, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from utils import check_url
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
import requests
import bs4 as BS

class EditUrlDialog(QDialog):
    def __init__(self, database, urls, parent=None):
        super().__init__(parent)
        # self.add_url_func = add_url_func
        self.database = database
        self.urls = urls
        self.selected_urls = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EditURLs')
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        add_layout = QHBoxLayout()
        main_layout.addLayout(add_layout)

        add_label = QLabel('Add URL:')
        add_layout.addWidget(add_label)

        self.add_edit = QLineEdit()
        self.add_edit.returnPressed.connect(self.add_url)
        add_layout.addWidget(self.add_edit)

        self.add_button = QPushButton('Add URL')
        self.add_button.clicked.connect(self.add_url)
        add_layout.addWidget(self.add_button)

        self.url_list = QListWidget()
        self.url_list.setSelectionMode(QAbstractItemView.MultiSelection)
        for url in self.urls:
            print(url[1])
            item = QListWidgetItem(url[1])
            item.setData(Qt.UserRole, url[0])
            self.url_list.addItem(item)
        print(self.url_list.count())
        print(self.url_list.item(0))
        main_layout.addWidget(self.url_list)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        select_all_button = QPushButton('Select All')
        select_all_button.clicked.connect(self.select_all)
        button_layout.addWidget(select_all_button)

        deselect_all_button = QPushButton('Deselect All')
        deselect_all_button.clicked.connect(self.deselect_all)
        button_layout.addWidget(deselect_all_button)

        delete_button = QPushButton('Delete Selected')
        delete_button.clicked.connect(self.delete_selected)
        button_layout.addWidget(delete_button)

        close_button = QPushButton('Close')
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

    def add_url(self):
        url = self.add_edit.text()
        if check_url.check_url(url):
            if self.database.url_exists(url):
                QMessageBox.warning(self, "Warning", "URL Already Exist!")
                self.add_edit.clear()
            else:
                self.urls.append(url)
                self.database.add_url(url)
                item = QListWidgetItem(url)
                self.url_list.addItem(item) 
                self.add_edit.clear()
                # add content and modified first time
                response = requests.get(url)
                html = response.text
                self.database.add_content(html)
                modified_time = response.headers.get('Last-Modified')
                self.database.add_last_modified(url, modified_time)
        else:
            QMessageBox.warning(self, "Warning", "Invalid URL!")
        #添加完清空输入框，并刷新下面的所有url显示


    def select_all(self):
        for i in range(self.url_list.count()):
            self.url_list.item(i).setSelected(True)
        self.selected_urls = [i.data(Qt.UserRole) for i in self.url_list.selectedItems()]

    def deselect_all(self):
        for i in range(self.url_list.count()):
            self.url_list.item(i).setSelected(False)
        self.selected_urls = []

    def delete_selected(self):
        selected_items = self.url_list.selectedItems()
        if not selected_items:
            return
        reply = QMessageBox.question(self, 'Delete URLs', 'Are you sure you want to delete the selected URLs?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for item in selected_items:
                url_id = item.data(Qt.UserRole)
                if url_id != -1:
                    #self.selected_urls.remove(url_id)
                    self.database.delete_url(url_id)
                self.url_list.takeItem(self.url_list.row(item))
    
    # def add_content_firsttime(self, url):
    #     response = requests.get(url)
    #     if response.status_code != 200:
    #         return None
    #     content_type = response.headers.get('content-type')
    #     if not content_type or not content_type.startswith('text/html'):
    #         return None
    #     else:
    #         html = response.text
    #         self.database.add_content(html)
    #         print(html)
    #     return 

    # def accept(self):
    #     for url in self.urls:
    #         if url[0] in self.selected_urls:
    #             continue
    #         self.add_url_func(url[1])
    #     super().accept()

