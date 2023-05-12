import sys
from PyQt5.QtWidgets import QApplication
from gui.mainwindow import MainWindow
from gui.editurl import EditUrlDialog
from gui.settings import SettingsDialog
from utils.database import Database
from utils.spider import Spider
from utils.timer import Timer
# from utils import get_urls

if __name__ == '__main__':
    app = QApplication(sys.argv)
    database = Database('urls.db')
    spider = Spider(database)
    main_window = MainWindow(database,)
    urls = database.get_urls()
    edit_url_dialog = EditUrlDialog(database, urls,)
    settings_dialog = SettingsDialog(database)
    timer = Timer(database.get_refresh_time() * 60, spider.check_urls)
    timer.start()

    def edit_url():
        edit_url_dialog.exec_()
        main_window.refresh()

    def settings():
        settings_dialog.exec_()
        timer.set_interval(database.get_refresh_time() * 60)

    main_window.edit_url_clicked.connect(edit_url)
    main_window.settings_clicked.connect(settings)

    main_window.show()
    sys.exit(app.exec_())
