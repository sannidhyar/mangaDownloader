import os
import sys
from tqdm import trange
import argparse

import srcs.crawler as crawler
import srcs.garbage as garbage
import srcs.html_maker as html_maker

def getSubFolder(chapterNum):
    if chapterNum < 10:
        subFolder = f'Chapter_000{chapterNum}'
    elif chapterNum < 100:
        subFolder = f'Chapter_00{chapterNum}'
    elif chapterNum < 1000:
        subFolder = f'Chapter_0{chapterNum}'
    else:
        subFolder = f'Chapter_{chapterNum}'
    return subFolder

parser = argparse.ArgumentParser(description='Save Manga')
parser.add_argument('-f', '--fullManga', action='store_true',
                    help='Save all chapters of the manga or only current chapter')
parser.add_argument('-r', '--removeGarbage', action='store_true',
                    help='Save all chapters of the manga or only current chapter')
parser.add_argument('--html', action='store_true',
                    help='Save all chapters of the manga or only current chapter')
parser.add_argument('--url', type=str, required=True, 
                    help='URL to last chapter')
args = parser.parse_args()

crawl = True
removeGarbage = True
html = True
doZip = True

cropping = False
pdf = False


# url = "https://asuratoon.com/8223257861-return-of-the-shattered-constellation-chapter-2/"
# url = "https://asuratoon.com/9766692502-return-of-the-unrivaled-spear-knight-chapter-112/"
# url = "https://asuratoon.com/9766692502-return-of-the-shattered-constellation-chapter-87/"

url= args.url

urlName = url.split('/')[-2].split('-')

i = url.find('chapter')
url = url[:i+8]

mangaName = ''
for i in range(len(urlName)):
    n = urlName[i]
    if n[0].isnumeric():
        continue
    if n == 'chapter':
        x = urlName[i+1]
        break
    mangaName += n + '_'
mangaName = mangaName[:-1].title()
if args.fullManga == False:
    start = int(x)
    end = start + 1
else:
    start = 1
    end = int(x)+1

print(mangaName)
t = trange(start, end, desc='Bar desc', leave=True)
for x in t:
    # x = str(x)
    # Create the nameing system
    chapterNum = x
    subFolder = getSubFolder(chapterNum)
    # set folder as manga and its chapter
    folderName = f'/home/sannidhyar/coding/python/mangaDownloader/{mangaName}/'
    imgDir = folderName + subFolder + '/'
    count = 0
    if crawl:
        # print('CRAWLING:\n')
        t.set_description(f"Chapter {x}: Crawling")
        t.refresh()
        if x == start:
            # exit()
            count, nextUrl = crawler.starterFunction(f'{url}{x}/', f'{imgDir}')
        else:
            count, nextUrl = crawler.starterFunction(nextUrl, f'{imgDir}')
        # exit()
        # os.system(f'python crawler.py {url}{x}/ {imgDir}')
    if removeGarbage:
        # print('REMOVING GARBAGE:\n')
        # os.system(f'python garbage.py {imgDir}')
        t.set_description(f"Chapter {x}: Garbage Cleaning")
        t.refresh()
        failures, countDeleted = garbage.removeGarbageImages(imgDir)
        if len(failures) != 0:
            s = ''
            for f in failures:
                s += f + ', '
            t.write(s)
        t.write(f"Chapter {x}: Deleted {countDeleted} of {count}")
    if html:
        # print('CREATING HTML:\n')
        t.set_description(f"Chapter {x}: HTML making")
        t.refresh()
        html_maker.createHTML(folderName, imgDir, x, x<end-1)
        # os.system(f'python html_maker.py {folderName} {imgDir} {x}')
        
    if cropping:
        print('CROPPING:\n')
        for i in os.listdir(dir[:-1]):
            os.system('python cropper.py ' + dir + i)
    if pdf:
        print('MAKING PDF:\n')
        os.system('python pdf_maker.py ' + x)
        
if doZip:
    print('\nZIPPING:\n')
    os.chdir(f'{mangaName}')
    os.system(f'zip -r ../{mangaName}.zip ./')