import os
import cv2
import sys


def checkAndRemove(imgName, countDeleted):
    img = cv2.imread(imgName, 1)
    failures = []
    try:
        height, width, _ = img.shape
        if(height < 2000 or width > 1000):
            # print(img.shape)
            # print(image)
            os.remove(imgName)
            countDeleted += 1
    except:
        # print('\n')
        failures.append(imgName)
        # print('\n')
        # os.system('\^C')
    return failures, countDeleted


def removeGarbageImages(imgDir):

    # x = sys.argv[1]
    # print(os.listdir("D:\\manga\\Solo_leveling-" + x))
    failures = []
    countDeleted = 0
    for image in os.listdir(imgDir):
        # print(image)
        img = cv2.imread(imgDir+"/"+image, 1)
        # cv2.imshow("image", img)
        # cv2.waitKey(0)
        try:
            height, width, _ = img.shape
            if(height < 2000 or width > 1000):
                # print(img.shape)
                # print(image)
                os.remove(imgDir+"/"+image)
                countDeleted += 1
        except:
            # print('\n')
            failures.append(imgDir + "/" + image)
            # print('\n')
            # os.system('\^C')
            continue
    cv2.destroyAllWindows()
    return failures, countDeleted

if __name__ == '__main__':
    imgDir = sys.argv[1]
    removeGarbageImages(imgDir)