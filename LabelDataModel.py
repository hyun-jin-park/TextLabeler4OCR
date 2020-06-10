import numpy as np
import copy
import cv2
import os


class ImagePatchData:
    def __init__(self, index, image, label, box):
        self._index = index
        self._image = image
        self._label = label
        self._box = box

    @property
    def image(self):
        return self._image

    @property
    def label(self):
        return self._label

    @property
    def box(self):
        return self._box

    @property
    def index(self):
        return self._index


class LabelingTargetImage:
    def __init__(self):
        self._label_path = None
        self._image = None
        self._word_boxes = []
        self._labels = []

    def load_image(self, image_path):
        label_path = image_path.replace('.jpg', '.txt')
        im = cv2.imread(image_path)
        if im is None:
            print('can not open image')
            return

        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        self._label_path = label_path
        self._image = im
        self._word_boxes = []
        self._labels = []

        if os.path.exists(label_path):
            with open(label_path) as f:
                lines = f.readlines()
            for index, line in enumerate(lines):
                items = line.split('\t')
                boxes = np.array([int(item) for item in items[1:]], dtype=np.int32)
                boxes = np.reshape(boxes, (4, 2))
                self._word_boxes.append(boxes)
                self._labels.append(items[0])
        else:
            print('there is no labeling file')

    def get_image_with_all_label(self):
        if self._image is None:
            print('get_image_with_all_label called for None image')
            return None

        im = copy.deepcopy(self._image)
        for box_pos in self._word_boxes:
            box_pos = box_pos.reshape((1, -1, 1, 2)).astype(np.int32)
            im = cv2.polylines(im, box_pos, True, (255, 0, 0), 1)
        return im

    def get_image_with_label(self, index):
        if self._image is None:
            print('get_image_with_label called for None image')
            return None

        im = copy.deepcopy(self._image)
        box_pos = self._word_boxes[index]
        box_pos = box_pos.reshape((1, -1, 1, 2)).astype(np.int32)
        im = cv2.polylines(im, box_pos, True, (255, 0, 0), 2)
        return im

    def get_label(self, index):
        if self._labels is None:
            print('get_label called for None image')
            return None

        return self._labels[index]

    def get_patch_list(self, count, start=0):
        if self._word_boxes is None:
            print('get_patch_list called for empty word boxes')
            return None

        image_patch_list = []
        end = min(start + count, len(self._word_boxes))
        for i in range(start, end):
            box_pos = self._word_boxes[i]
            im = self._image[box_pos[0][1]:box_pos[2][1],box_pos[0][0]:box_pos[2][0]]
            im = np.ascontiguousarray(im)
            label = self._labels[i]
            patch = ImagePatchData(i, im, label, box_pos)
            image_patch_list.append(patch)
        return image_patch_list

    def get_image(self):
        return self._image

    @property
    def patch_count(self):
        return len(self._word_boxes)

    def set_label(self, index, label):
        if len(self._labels) > index:
            self._labels[index] = label

    def set_deleted_mark(self, index):
        self._labels[index] = '__#TO_BE_DELETED#__'

    def sync_label(self):
        if len(self._word_boxes) == 0 :
            print('sync_label called for empty word boxes')
            return

        with open(self._label_path, 'wt') as f:
            for label, box_pos in zip(self._labels, self._word_boxes):
                f.write(label + '\t' + str(box_pos[0][0]) + '\t' + str(box_pos[0][1]) + '\t' +
                        str(box_pos[1][0]) + '\t' + str(box_pos[1][1]) + '\t' +
                        str(box_pos[2][0]) + '\t' + str(box_pos[2][1]) + '\t' +
                        str(box_pos[3][0]) + '\t' + str(box_pos[3][1]) + '\n')
