from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QHBoxLayout, QPushButton
from Controller import Controller


def cv_image_to_qimage(cv_image):
    return QImage(cv_image.data, cv_image.shape[1], cv_image.shape[0], cv_image.strides[0], QImage.Format_RGB888)


class MyTextEdit(QLineEdit):
    def __init__(self, controller, index):
        super().__init__()
        self._controller = controller
        self._index = index

    def focusInEvent(self, e):
        super().focusInEvent(e)
        if self._index is not None:
            self._controller.notify_view_selected(self._index)

    def set_index(self, index):
        self._index = index


class ImagePatchView(QWidget):
    def __init__(self, controller, index=None):
        super().__init__()
        self._image_patch = QLabel()
        self._text = MyTextEdit(controller, index)
        self._button = QPushButton('delete')
        self._index = index
        self._updated = False
        self._controller = controller
        self.init_ui()

    def set(self, index, image, label=None):
        self._image_patch.setPixmap(QPixmap(cv_image_to_qimage(image)))
        self._index = index
        if label is not None:
            self._text.setText(label)
            self._text.set_index(index)

    def is_updated(self):
        return self._updated

    def label_changed(self):
        if self._index is not None:
            self._updated = True
            self._controller.notify_label_change(self._index, self._text.text())

    def view_selected(self):
        self._controller.notify_view_selected(self._index)

    def delete_button_clicked(self):
        if self._index is None:
            return
        self._text.setText('__#DELETED_LABEL#__')
        self._updated = True
        self._controller.notify_label_change(self._index, self._text.text())

    def init_ui(self):
        self._text.textChanged.connect(self.label_changed)
        self._button.clicked.connect(self.delete_button_clicked)
        layout = QHBoxLayout()
        layout.addWidget(self._image_patch)
        layout.addWidget(self._text)
        layout.addWidget(self._button)
        self.setLayout(layout)


if __name__ == "__main__":
    import sys
    import cv2
    app = QApplication(sys.argv)
    my_controller = Controller()
    form = ImagePatchView(my_controller)
    im = cv2.imread('test_data/test_patch.jpg')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    form.set(1, im, 'txt')
    form.show()
    app.exec_()
