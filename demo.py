"""Demo for use yolo v3
"""
import os
import time
import cv2
import numpy as np
from model.yolo_model import YOLO


def process_image(img):

    image = cv2.resize(img, (416, 416),
                       interpolation=cv2.INTER_CUBIC)
    image = np.array(image, dtype='float32')
    image /= 255.
    image = np.expand_dims(image, axis=0)

    return image


def get_classes(file):

    with open(file) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]

    return class_names


def draw(image, boxes, scores, classes, all_classes):

    for box, score, cl in zip(boxes, scores, classes):
        x, y, w, h = box

        top = max(0, np.floor(x + 0.5).astype(int))
        left = max(0, np.floor(y + 0.5).astype(int))
        right = min(image.shape[1], np.floor(x + w + 0.5).astype(int))
        bottom = min(image.shape[0], np.floor(y + h + 0.5).astype(int))

        cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
        cv2.putText(image, '{0} {1:.2f}'.format(all_classes[cl], score),
                    (top, left - 6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255), 1,
                    cv2.LINE_AA)

        print('class: {0}, score: {1:.2f}'.format(all_classes[cl], score))
        print('box coordinate x,y,w,h: {0}'.format(box))

    print()


def detect_image(image, yolo, all_classes):

    pimage = process_image(image)

    start = time.time()
    boxes, classes, scores = yolo.predict(pimage, image.shape)
    end = time.time()

    print('time: {0:.2f}s'.format(end - start))

    if boxes is not None:
        draw(image, boxes, scores, classes, all_classes)

    return image


def detect_video(video, yolo, all_classes):

    video_path = os.path.join("videos", "test", video)
    camera = cv2.VideoCapture(video_path)
    

    # Prepare for saving the detected video
    sz = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc(*'mpeg')

    vout = cv2.VideoWriter()
    vout.open(os.path.join("videos", "res", video), fourcc, 20, sz, True)

    while True:
        res, frame = camera.read()

        if not res:
            break

        image = detect_image(frame, yolo, all_classes)
        #cv2.imshow("detection", image)

        # Save the video frame by frame
        vout.write(image)

        if cv2.waitKey(110) & 0xff == 27:
                break

    vout.release()
    camera.release()
    
def main(src):
    yolo = YOLO(0.6, 0.5)
    file = 'data/coco_classes.txt'
    all_classes = get_classes(file)

    # detect images in test floder.
    for (root, dirs, files) in os.walk('images/test'):
        if files:
            for f in files:
                print(f)
                path = os.path.join(root, f)
                image = cv2.imread(path)
                image = detect_image(image, yolo, all_classes)
                cv2.imwrite('images/res/' + f, image)

    # detect videos one at a time in videos/test folder    
    video = src
    detect_video(video, yolo, all_classes)
    aa="/final"
    return aa

if __name__ == '__main__':
    main("Snapchat-538507425.mp4")
