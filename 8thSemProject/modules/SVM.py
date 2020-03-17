import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm as sksvm, metrics, datasets
from sklearn.utils import Bunch
from sklearn.model_selection import GridSearchCV, train_test_split
import skimage
from skimage.io import imread
from skimage.transform import resize
import cv2
from PIL import Image
import os
import time
from colorama import Fore, Back, Style
from . import HTMLFactory


class SVMfactory:

    mapper = {1: "Input", 0: "Image"}

    def __init__(self, loading=False, img_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'HTMLElements'))):

        self.STATIC_PATH = None

        if not loading:
            self.image_dataset = self.load_image_files(img_dir)
            print(Fore.GREEN + "Images have been loaded")
        self.param_grid = [
            {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
            {'C': [1, 10, 100, 1000], 'gamma': [
                0.001, 0.0001], 'kernel': ['rbf']},
        ]

        self.X_train = self.X_test = self.y_train = self.y_test = []

        self.y_pred = self.clf = None

        self.dimension = (64, 64)
        self.samp_data = []

    def load_image_files(self, container_path, dimension=(64, 64)):

        image_dir = Path(container_path)
        folders = [directory for directory in image_dir.iterdir()
                   if directory.is_dir()]
        categories = [fo.name for fo in folders]

        descr = "A image classification dataset"
        images = []
        flat_data = []
        target = []
        for i, direc in enumerate(folders):
            for file in direc.iterdir():
                img = skimage.io.imread(file)
                img_resized = resize(
                    img, dimension, anti_aliasing=True, mode='reflect')
                flat_data.append(img_resized.flatten())
                images.append(img_resized)
                target.append(i)
        flat_data = np.array(flat_data)
        target = np.array(target)
        images = np.array(images)

        return Bunch(data=flat_data,
                     target=target,
                     target_names=categories,
                     images=images,
                     DESCR=descr)

    def test_train_split(self, test_size=0.3, random_state=109):

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.image_dataset.data,
                                                                                self.image_dataset.target,
                                                                                test_size=test_size,
                                                                                random_state=random_state)

        print("Test train split has been completed =>")
        print("Training parameters = %s" % (len(self.X_train)))
        print("Testing parameters = %s" % (len(self.X_test)))

    def train_and_fit(self):
        print("Model will now begin training. This could take a while")
        start_time = time.time()
        svc = sksvm.SVC()
        self.clf = GridSearchCV(svc, self.param_grid)
        self.clf.fit(self.X_train, self.y_train)
        self.y_pred = self.clf.predict(self.X_test)
        print("SVM training is completed. \n Time elapsed =>",
              (time.time() - start_time))

    def display_svm_scores(self):

        print("Classification report for - \n{}:\n{}\n".format(self.clf,
                                                               metrics.classification_report(
                                                                   self.y_test, self.y_pred)
                                                               ))

    def image_process(self, image):

        hsv_image = cv2.imread(image, 1)  # pretend its HSV
        #noise_img = sp_noise(hsv_image,0.2)
        rgbimg = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)
        image_gray = cv2.cvtColor(rgbimg, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(image_gray, 127, 255, 0)
        plt.imshow(image_gray, cmap='gray')

        contours, hierarchy = cv2.findContours(
            threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        left_arr = []
        right_arr = []
        top_arr = []
        bottom_arr = []

        for cnt in contours:
            leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
            rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
            topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
            bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
            left_arr.append(leftmost)
            right_arr.append(rightmost)
            top_arr.append(topmost)
            bottom_arr.append(bottommost)

        left_arr.sort()
        right_arr.sort(reverse=True)
        top_arr.sort(key=lambda x: x[1])
        bottom_arr.sort(reverse=True, key=lambda x: x[1])

        left_arr.pop(0)
        right_arr.pop(0)
        top_arr.pop(0)
        bottom_arr.pop(0)

        advanced_coords = (left_arr[0][0]-10, top_arr[0]
                           [1]-10, right_arr[0][0]+10, bottom_arr[0][1]+10)
        im = Image.open(image)
        im1 = im.crop(advanced_coords)
        newsize = (200, 200)
        im1 = im1.resize(newsize)
        os.remove(image)
        im1.save(image)

    def predict_images(self):

        file_name = []

        for file in os.listdir("samples"):
            if file == "content.jpg":
                continue
            self.image_process(os.path.join("samples", file))
            img = skimage.io.imread(os.path.join("samples", file))
            img_resized = resize(img, self.dimension,
                                 anti_aliasing=True, mode='reflect')
            self.samp_data.append(img_resized.flatten())
            file_name.append(file)

        fitr = 0
        for i in list(self.clf.predict(self.samp_data)):
            HTMLFactory.build_elements(SVMfactory.mapper[i])
            fitr += 1

    def save_model(self):

        try:
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'SVM.pkl')), 'wb') as fid:
                pickle.dump(self.clf, fid)
                print("Model has been saved")
        except Exception as e:
            print("Error occured")
            print(e)

    def load_model(self):
        with open(os.path.join(os.path.join(os.path.dirname(__file__), '..', 'models', 'SVM.pkl')), 'rb') as f:
            self.clf = pickle.load(f)
            print(Fore.GREEN + "Model has been loaded")


def make_prediction(n=3):
    if not n:
        print("Unable to build SVM")
        return
    try:
        svm = SVMfactory(True)
        svm.load_model()
        print("Model was loaded successfully")
        svm.predict_images()
    except:
        print("Error occured, model does not exist or is damaged. Preparing new model...")
        svm = SVMfactory()
        svm.test_train_split()
        svm.train_and_fit()
        svm.display_svm_scores()
        svm.save_model()
        make_prediction(n-1)
