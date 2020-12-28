import random
from os.path import join

import matplotlib.pyplot as plt
# import glob.glob
import numpy
import numpy as np
from PIL import Image

labal_list = []
data_list = []


def crop(image, pixel):
    return image[pixel[0] - 41: pixel[0] + 40, pixel[1] - 41: pixel[1] + 40]


def insert_to_data_list(data, labal):
    data = np.asarray(data)
    if data.shape == (81,81,3):
        data_list.append(data)
        labal_list.append(labal)


def save_data():
    data_array = numpy.array(data_list)
    # print(data_array)
    print("*****************************************************")
    labal_array = numpy.array(labal_list)
    # print(labal_array)
    np.array(data_array).tofile('data_dir/train/data.bin', sep=',')
    np.array(labal_array).tofile('data_dir/train/label.bin', sep=',')


def load_tfl_data(data_dir, crop_shape=(81, 81)):
    images = np.memmap(join(data_dir, 'data.bin'), mode='r', dtype=np.uint8).reshape([-1] + list(crop_shape) + [3])
    labels = np.memmap(join(data_dir, 'label.bin'), mode='r', dtype=np.uint8)
    return {'images': images, 'labels': labels}


def viz_my_data(images, labels, predictions=None, num=(2, 4), labels2name=None):
    if labels2name is None:
        labels2name = {0: 'No TFL', 1: 'Yes TFL'}
    print(images.shape[0], labels.shape[0])
    assert images.shape[0] == labels.shape[0]
    assert predictions is None or predictions.shape[0] == images.shape[0]
    h = 5
    n = num[0] * num[1]
    ax = plt.subplots(num[0], num[1], figsize=(h * num[0], h * num[1]), gridspec_kw={'wspace': 0.05}, squeeze=False,
                      sharex=True, sharey=True)[1]  # .flatten()
    idxs = np.random.randint(0, images.shape[0], n)
    for i, idx in enumerate(idxs):
        ax.flatten()[i].imshow(images[idx])
        title = labels2name[labels[idx]]
        if predictions is not None: title += ' Prediction: {:.2f}'.format(predictions[idx])
        ax.flatten()[i].set_title(title)


def init_data_set(image_labal, image):
    list_ = np.argwhere(image == 19)
    if len(list_):
        print(list_)
        pixel = random.choice(list_)
        data = crop(image, pixel)
        insert_to_data_list(data, 1)
        if len(np.argwhere(image_labal != 19)):
            pixel = random.choice(np.argwhere(image_labal != 19))
            data = crop(image, pixel)
            insert_to_data_list(data, 0)


def read_all_images(path_):
    image_list = []
    for root, dirs, files in np.os.walk(path_):
        # print(1)
        root.split(np.os.sep)
        for file in files:
            if file.endswith('_gtFine_labelIds.png'):
                image_list.append(np.asarray(Image.open(path_ + '/' + np.os.path.basename(root) + '/' + file)))
    return image_list


def read_from_leftImg8bit():
    path_ = "CityScapes/leftImg8bit/train"
    image_list = []
    for root, dirs, files in np.os.walk(path_):
        root.split(np.os.sep)
        for file in files:
            image_list.append(np.asarray(Image.open(path_ + '/' + np.os.path.basename(root) + '/' + file)))
    return image_list


def abc():
    labal_images = read_all_images('CityScapes/gtFine/train')
    amount_of_images = len(labal_images)
    print("amount of images:", amount_of_images)
    images = read_from_leftImg8bit()
    for i in range(amount_of_images):
        print(f"^^^^^^^^^   {i}    ^^^^^^^^")
        init_data_set(labal_images[i], images[i])
    save_data()


abc()

# init_data_set("aachen_000001_000019")
# data_dir = './data_dir/'
# datasets = {
#     'train': load_tfl_data(join(data_dir, 'train')),
# }
#
# viz_my_data(num=(1, 1), **datasets['train'])
