from LabelDataModel import LabelingTargetImage


class Controller:
    def __init__(self, view=None):
        self._data = LabelingTargetImage()
        self._view = view
        self._patch_start_index = 0
        self._patch_image_count = None

    def notify_label_change(self, index, label):
        self._data.set_label(index, label)
        if self._view is not None:
            self._view.update_main_image(self._data.get_image_with_label(index))
        else:
            print('Controller: notify_label_change')

    def notify_view_selected(self, index):
        if self._view is not None:
            self._view.update_main_image(self._data.get_image_with_label(index))
        else:
            print('Controller: notify view selected')

    def open_image(self, path):
        self._patch_start_index = 0
        self._data.load_image(path)
        self._patch_image_count = self._data.patch_count
        if self._view is not None:
            self._view.update_main_image(self._data.get_image())
            self._view.update_image_patch(self._data.get_patch_list(self._view.image_patch_count, self._patch_start_index))
        else:
            print('Controller: open image')

    def save_label(self):
        self._data.sync_label()
        if self._view is not None:
            self._view.show_message('edited label data is saved')
        else:
            print('Controller: save label')

    def next_patch(self):
        if self._view is None:
            print('Controller: next patch')
            return

        if self._view.is_updated():
            self._data.sync_label()

        if self._patch_start_index + self._view.image_patch_count > self._patch_image_count:
            self._patch_start_index = 0
        else:
            self._patch_start_index = self._patch_start_index + self._view.image_patch_count

        self._view.update_image_patch(self._data.get_patch_list(self._view.image_patch_count, self._patch_start_index))

    def prev_patch(self):
        if self._view is None:
            print('Controller: previous patch')
            return

        if self._view.is_updated():
            self._data.sync_label()

        if self._patch_start_index - self._view.image_patch_count < 0:
            self._patch_start_index = self._patch_image_count - self._view.image_patch_count
        else:
            self._patch_start_index = self._patch_start_index - self._view.image_patch_count

        self._view.update_image_patch(self._data.get_patch_list(self._view.image_patch_count, self._patch_start_index))