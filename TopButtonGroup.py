from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QApplication, QFileDialog
from Controller import Controller
import glob
import os


class TopButtonGroup(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._target_image_path = QLabel()
        self._open_button = QPushButton('Open')
        self._next_button = QPushButton('Next')
        self._prev_button = QPushButton('Prev')
        self._controller = controller

        self._current_path = None
        self._current_file_name = None

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self._target_image_path)
        layout.addWidget(self._open_button)
        layout.addWidget(self._prev_button)
        layout.addWidget(self._next_button)
        self.setLayout(layout)

        self._open_button.clicked.connect(self.open_image)
        self._next_button.clicked.connect(self.next_image)
        self._prev_button.clicked.connect(self.prev_image)

    def open_image(self):
        open_file_info = QFileDialog.getOpenFileName(self, 'select image file', './')
        self._current_path = os.path.dirname(open_file_info[0])
        self._current_file_name = os.path.basename(open_file_info[0])
        self._controller.open_image(open_file_info[0])

    def next_image(self):
        cur_file_list = glob.glob(self._current_path + "/*.jpg")
        if len(cur_file_list) == 0:
            print('next_image: there is not jpg file')
            return

        curr_file_index = -1
        for index, file_path in enumerate(cur_file_list):
            if os.path.basename(file_path) == self._current_file_name:
                curr_file_index = index
                break

        if curr_file_index == -1 or curr_file_index == len(cur_file_list) - 1:
            next_path = cur_file_list[0]
        else:
            next_path = cur_file_list[curr_file_index + 1]
        self._current_path = os.path.dirname(next_path)
        self._current_file_name = os.path.basename(next_path)
        print('next path is {}'.format(next_path))
        self._controller.open_image(next_path)

    def prev_image(self):
        cur_file_list = glob.glob(self._current_path + "/*.jpg")
        if len(cur_file_list) == 0:
            print('prev_image: there is not jpg file')
            return
        curr_file_index = -1
        for index, file_path in enumerate(cur_file_list):
            if os.path.basename(file_path) == self._current_file_name:
                curr_file_index = index
                break

        if curr_file_index == -1 or curr_file_index == 0:
            prev_path = cur_file_list[-1]
        else:
            prev_path = cur_file_list[curr_file_index-1]

        self._current_path = os.path.dirname(prev_path)
        self._current_file_name = os.path.basename(prev_path)
        print('prev path is {}'.format(prev_path))
        self._controller.open_image(prev_path)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    my_controller = Controller()
    form = TopButtonGroup(my_controller)
    form.show()
    app.exec_()
