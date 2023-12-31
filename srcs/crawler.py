import sys
from bs4 import *
import requests
import os
from tqdm import trange
import threading
from srcs.garbage import checkAndRemove
# CREATE FOLDER
def folder_create(images, folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
        
    # # if folder exists with that name, ask another name
    # os.chdir(folder_name)
    # check if ther are images already in the folder
    # meaning it has already been crawled
    allFiles = os.listdir(folderName)
    count = len(allFiles)
    if len(allFiles) == 0:    
        # image downloading start
        count = download_images(images, folderName)
    return count
    # else:
    #     print(f'These are present {allFiles}\n')


def getNextUrl(refs):
    with open('./logs/log.txt', 'w') as f:
        nextUrl = None
        try:
            allInRefs = refs[18].string.split(',')
            for x in range(len(allInRefs)):
                if 'nextUrl' in allInRefs[x]:
                    nextUrl = allInRefs[x].split('"')[-2].replace('\\', '')
        except:
            for i, ref in enumerate(refs):
                allInRefs = ref.string.split(',')
                for x in range(len(allInRefs)):
                    if 'nextUrl' in allInRefs[x]:
                        nextUrl = allInRefs[x].split('"')[-2].replace('\\', '')
        f.write(nextUrl)
    return nextUrl        
        
# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):
    # initial count is zero
    count = 0
    totalImgs = len(images)
    # print total images found in URL
    # print(f"Total {len(images)} Image Found!")
    # print(images)
    # checking if images is not zero
    countDeleted = 0
    if totalImgs != 0:
        # for i, image in enumerate(images):
        t = trange(totalImgs, leave=False)
        for i in t:
            image = images[i]
            try:
                # In image tag ,searching for "data-srcset"
                image_link = image["data-srcset"]
            # then we will search for "data-src" in img
            # tag and so on..
            except:
                try:
                    # In image tag ,searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag ,searching for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # In image tag ,searching for "src"
                            image_link = image["src"]
                        # if no Source URL found
                        except:
                            pass

            try:
                r = requests.get(image_link).content
                try:
                    # possibility of decode
                    r = str(r, 'utf-8')

                except UnicodeDecodeError:
                    # After checking above condition, Image Download start
                    t.set_description(f"Downloading {count}/{totalImgs}")
                    if i < 9:
                        # if i != 2:
                        with open(f"{folder_name}/images0{i+1}.jpg", "wb+") as f:
                            f.write(r)
                        countDeleted = checkAndRemove(f"{folder_name}/images0{i+1}.jpg", countDeleted)
                    else:
                        with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                            f.write(r)
                        countDeleted = checkAndRemove(f"{folder_name}/images{i+1}.jpg", countDeleted)

                    # counting number of image downloaded
                    count += 1
            except:
                pass

        # if count != len(images):
        #     print(f"Total {count} Images Downloaded Out of {len(images)}")
        # else:
        #     print("All Images Downloaded!")
        return f"{count}/{len(images)}"

# MAIN FUNCTION START
def starterFunction(url, folderName):

    # content of URL
    r = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')

    # find all images in URL
    images = soup.findAll('img')
    # refs = soup.findAll('script')
    # nextUrl = getNextUrl(refs)

    # Call folder create function
    count = folder_create(images, folderName)
    
    # return count, nextUrl
    return count



if __name__ == '__main__':
    # take url
    url = sys.argv[1]
    # folderName
    folderName = sys.argv[2]
        
    # CALL MAIN FUNCTION
    print(starterFunction(url, folderName))
