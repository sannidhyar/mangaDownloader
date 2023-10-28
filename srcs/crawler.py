import sys
from bs4 import *
import requests
import os
from tqdm import trange

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
# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):
    # initial count is zero
    count = 0
    totalImgs = len(images)
    # print total images found in URL
    # print(f"Total {len(images)} Image Found!")
    # print(images)
    # checking if images is not zero
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
                        # with open(f"{folder_name}/images0{i+1}.png", "wb+") as f:
                        # 	f.write(r)
                        # if i != 2:
                        if i >= -1:
                            # print(f"saving images0{i+1}.jpg")
                            with open(f"{folder_name}/images0{i+1}.jpg", "wb+") as f:
                                f.write(r)
                        else:
                            print(f'Not saving images0{i+1}.jpg')
                    else:
                        # print("HELLO")
                        # with open(f"{folder_name}/images{i+1}.png", "wb+") as f:
                        # 	f.write(r)
                        # print(f"saving images{i+1}.jpg")
                        with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                            f.write(r)

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
    # print(images)

    # Call folder create function
    count = folder_create(images, folderName)
    
    return count



if __name__ == '__main__':
    # take url
    # print(sys.argv)
    url = sys.argv[1]
    
    # folderName
    folderName = sys.argv[2]

    # CALL MAIN FUNCTION
    starterFunction(url, folderName)
