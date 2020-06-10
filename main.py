import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox

from ImagePatchLabelView import ImagePatchView
from BottomButtonGroup import BottomButtonGroup
from TopButtonGroup import TopButtonGroup
from LabelDataModel import LabelingTargetImage
from Controller import Controller


class LabelWindow(QWidget):
    def __init__(self, image_patch_count=12):
        super(QWidget, self).__init__()
        self._main_image = QLabel()
        self._target_image = LabelingTargetImage()
        self._controller = Controller(self)
        self._top_button_group = TopButtonGroup(self._controller)
        self._bottom_button_group = BottomButtonGroup(self._controller)
        self._image_patch_count = image_patch_count
        self._image_patch_view_list = [ImagePatchView(self._controller) for _ in range(0, image_patch_count)]
        self.init_ui()

    @property
    def image_patch_count(self):
        return self._image_patch_count

    def is_updated(self):
        for view in self._image_patch_view_list:
            if view.is_updated():
                return True
        return False

    def show_message(self, message):
        QMessageBox.about(self, 'message', message)

    def init_ui(self):
        self.setMinimumWidth(1440)
        self.setMinimumHeight(1280)

        main_layout = QHBoxLayout()
        left_body_layout = QVBoxLayout()
        right_body_layout = QVBoxLayout()
        main_layout.addLayout(left_body_layout)
        main_layout.addLayout(right_body_layout)

        left_body_layout.addWidget(self._top_button_group, alignment=Qt.AlignTop)
        left_body_layout.addWidget(self._main_image, alignment=Qt.AlignBottom)

        for i in range(0, self._image_patch_count):
            right_body_layout.addWidget(self._image_patch_view_list[i], alignment=Qt.AlignTop)
        right_body_layout.addWidget(self._bottom_button_group, alignment=Qt.AlignTop)

        self.setLayout(main_layout)

    def update_main_image(self, im):
        image = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
        self._main_image.setPixmap(QPixmap(image))

    def update_image_patch(self, patch_list):
        for index, patch in enumerate(patch_list):
            self._image_patch_view_list[index].set(patch.index, patch.image, patch.label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LabelWindow()
    form.show()
    app.exec_()
