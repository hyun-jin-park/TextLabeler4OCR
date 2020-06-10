from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QApplication
from Controller import Controller


class BottomButtonGroup(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._status_label = QLabel()
        self._next_button = QPushButton('Next')
        self._prev_button = QPushButton('Prev')
        self._save_button = QPushButton('Save')
        self._controller = controller

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self._status_label)
        layout.addWidget(self._prev_button)
        layout.addWidget(self._next_button)
        layout.addWidget(self._save_button)
        self.setLayout(layout)

        self._next_button.clicked.connect(self.next_image)
        self._prev_button.clicked.connect(self.prev_image)
        self._save_button.clicked.connect(self.save_label)

    def save_label(self):
        self._controller.save_label()

    def next_image(self):
        self._controller.next_patch()

    def prev_image(self):
        self._controller.prev_patch()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    my_controller = Controller()
    form = BottomButtonGroup(my_controller)
    form.show()
    app.exec_()
