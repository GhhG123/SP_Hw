from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMessageBox
from PyQt5.QtGui import QIntValidator

class SettingsDialog(QDialog):
    def __init__(self, refresh_time, parent=None):
        super().__init__(parent)
        self.init_ui(refresh_time)

    def init_ui(self, refresh_time):
        self.setWindowTitle('Settings')
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        time_layout = QHBoxLayout()
        main_layout.addLayout(time_layout)

        time_label = QLabel('Update time (hour):')
        time_layout.addWidget(time_label)

        self.time_edit = QLineEdit()
        self.time_edit.setText(str(refresh_time))
        self.time_edit.setValidator(QIntValidator(1, 24, self))
        time_layout.addWidget(self.time_edit)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        self.refresh_time = refresh_time

    def accept(self):
        time = int(self.time_edit.text())
        if time == self.refresh_time:
            super().accept()
            return
        reply = QMessageBox.question(self, 'Update Time', 'Are you sure you want to update the update time?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.refresh_time = time
            super().accept()
