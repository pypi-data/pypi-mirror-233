import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication


# creating main window class
class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setFixedWidth(1024)
        self.setFixedHeight(712)

        # creating a QWebEngineView
        self.browser = QWebEngineView()

        # setting default browser url as google
        self.browser.setUrl(QUrl(sys.argv[1]))

        # set this browser as central widget or main window
        self.setCentralWidget(self.browser)

        # showing all the components
        self.show()


# creating a pyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("Us2.ai")

# creating a main window object
window = MainWindow()

# loop
app.exec_()
