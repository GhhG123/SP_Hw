# from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
#                              QListWidget, QListWidgetItem, QMessageBox)
# from PyQt5.QtCore import Qt

# from utils import check_url


# class EditUrl(QWidget):
#     def __init__(self, urls, parent=None):
#         super().__init__(parent)
#         self.urls = urls
#         self.initUI()

#     def initUI(self):
#         # url input area
#         url_label = QLabel("Add URL:")
#         self.url_edit = QLineEdit()
#         add_button = QPushButton("Add")
#         add_button.clicked.connect(self.addUrl)

#         url_input_layout = QHBoxLayout()
#         url_input_layout.addWidget(url_label)
#         url_input_layout.addWidget(self.url_edit)
#         url_input_layout.addWidget(add_button)

#         # url list area
#         self.url_list = QListWidget()
#         self.url_list.setSelectionMode(QListWidget.MultiSelection)

#         for url in self.urls:
#             item = QListWidgetItem(url)
#             self.url_list.addItem(item)

#         # button area
#         return_button = QPushButton("Return")
#         return_button.clicked.connect(self.close)

#         delete_button = QPushButton("Delete")
#         delete_button.clicked.connect(self.deleteUrl)

#         button_layout = QHBoxLayout()
#         button_layout.addStretch(1)
#         button_layout.addWidget(return_button)
#         button_layout.addWidget(delete_button)

#         # main layout
#         main_layout = QVBoxLayout()
#         main_layout.addLayout(url_input_layout)
#         main_layout.addWidget(self.url_list)
#         main_layout.addLayout(button_layout)

#         self.setLayout(main_layout)
#         self.setWindowTitle("Edit URLs")

#     def addUrl(self):
#         url = self.url_edit.text()
#         if check_url(url):
#             self.urls.append(url)
#             item = QListWidgetItem(url)
#             self.url_list.addItem(item)
#         else:
#             QMessageBox.warning(self, "Warning", "Invalid URL!")

#     def deleteUrl(self):
#         selected_items = self.url_list.selectedItems()
#         if not selected_items:
#             QMessageBox.warning(self, "Warning", "No item selected!")
#             return

#         reply = QMessageBox.question(self, "Confirm", "Are you sure to delete selected items?",
#                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#         if reply == QMessageBox.Yes:
#             for item in selected_items:
#                 self.urls.remove(item.text())
#                 self.url_list.takeItem(self.url_list.row(item))
#         else:
#             return



from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, \
    QListWidgetItem, QPushButton, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from utils import check_url

class EditUrlDialog(QDialog):
    def __init__(self, urls, parent=None):
        super().__init__(parent)
        #self.add_url_func = add_url_func
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

        for url in self.urls:
            item = QListWidgetItem(url[1])
            item.setData(Qt.UserRole, url[0])
            self.url_list.addItem(item)

    def add_url(self):
        url = self.url_edit.text()
        if check_url(url):
            self.urls.append(url)
            item = QListWidgetItem(url)
            self.url_list.addItem(item) 
            #清除文本框
            self.url_edit.clean()
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
                    self.selected_urls.remove(url_id)
                self.url_list.takeItem(self.url_list.row(item))

    # def accept(self):
    #     for url in self.urls:
    #         if url[0] in self.selected_urls:
    #             continue
    #         self.add_url_func(url[1])
    #     super().accept()

