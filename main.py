import os
import sys
from tqdm import trange
import argparse

import srcs.crawler as crawler
import srcs.garbage as garbage
import srcs.html_maker as html_maker

import requests
from bs4 import * 

def getLinksToAllChapters(url:str, urlName):
    # urlName = url.split('/')[-2].split('-')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    allRefs = soup.findAll('a')
    mangaName = []
    for name in urlName:
        if not name.isnumeric():
            mangaName.append(name)
    mangaName.append('chapter')
    mangaName = '-'.join(mangaName)
    allLinks = []
    for ref in allRefs:
        try:
            if mangaName in ref['href']:
                allLinks.append(ref['href'])
        except:
            break
    return allLinks


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
parser.add_argument('--url', type=str, required=True, 
                    help='URL to last chapter')
parser.add_argument('-f', '--fullManga', action='store_true',
                    help='Save all chapters of the manga or only current chapter')
parser.add_argument('-r', '--removeGarbage', action='store_true',
                    help='Remove garbage explicitly')
parser.add_argument('--coverPage', action='store_true', 
                    help='URL to cover Page')
parser.add_argument('--html', action='store_true',
                    help='Make html')
parser.add_argument('--zip', action='store_true',
                    help='make a zip of the manga')
parser.add_argument('--crop', action='store_true', 
                    help='Use crop if you are going to make a pdf')
parser.add_argument('--pdf', action='store_true', 
                    help='Makes a pdf, but image quality reduces')

args = parser.parse_args()

crawl = True
removeGarbage = args.removeGarbage
html = args.html
doZip = args.zip

cropping = args.crop
pdf = args.pdf



# url = "https://asuratoon.com/8223257861-return-of-the-shattered-constellation-chapter-2/"
# url = "https://asuratoon.com/9766692502-return-of-the-unrivaled-spear-knight-chapter-112/"
# url = "https://asuratoon.com/9766692502-return-of-the-shattered-constellation-chapter-87/"

url= args.url

urlName = url.split('/')[-2].split('-')

i = url.find('chapter')
# urlWithoutChapNum = url[:i+8]
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
# if single manga

print(mangaName)
if args.fullManga == False:
    start = int(x)
    end = start + 1
    print('Crawling')
    subFolder = getSubFolder(int(x))
    folderName = f'/home/sannidhyar/coding/python/mangaDownloader/{mangaName}/'
    imgDir = folderName + subFolder + '/'
    count, nextUrl = crawler.starterFunction(url, imgDir)
    if html:
        html_maker.createHTML(folderName, imgDir, x, x<end-1)

# if full series
else:
    allLinks = sorted(getLinksToAllChapters(url, urlName))
    start = 0
    end = len(allLinks)

    t = trange(start, end, desc='Bar desc', leave=True)
    for x in t:
        url = allLinks[x]
        # x = str(x)
        # Create the nameing system
        urlSplit = url.split('/')[-2].split('-')
        chapterNum = []
        for i in urlSplit:
            if i.isnumeric() and len(i) < 5:
                chapterNum.append(i)
        try:
            chapterNum = int('.'.join(chapterNum))
        except:
            chapterNum = float('.'.join(chapterNum))
            
        # print(chapterNum)
        # continue
        # exit()
        subFolder = getSubFolder(chapterNum)
        # set folder as manga and its chapter
        # folderName = f'/home/sannidhyar/coding/python/mangaDownloader/{mangaName}/'
        folderName = os.path.join(os.getcwd(), mangaName)
        imgDir = os.path.join(folderName, subFolder) + '/'
        count = 0
        if crawl:
            # print('CRAWLING:\n')
            t.set_description(f"Chapter {chapterNum}: Crawling")
            t.refresh()
            # if x == start:
            #     # exit()
            #     count, nextUrl = crawler.starterFunction(f'{url}{x}/', f'{imgDir}')
            # else:
            #     count, nextUrl = crawler.starterFunction(nextUrl, f'{imgDir}')
            count = crawler.starterFunction(url, imgDir)
            # if chapterNum == 100:
            #     exit()
            # os.system(f'python crawler.py {url}{x}/ {imgDir}')
        if removeGarbage:
            # print('REMOVING GARBAGE:\n')
            # os.system(f'python garbage.py {imgDir}')
            t.set_description(f"Chapter {chapterNum}: Garbage Cleaning")
            t.refresh()
            failures, countDeleted = garbage.removeGarbageImages(imgDir)
            if len(failures) != 0:
                s = ''
                for f in failures:
                    s += f + ', '
                t.write(s)
            t.write(f"Chapter {chapterNum}: Deleted {countDeleted} of {count}")
        if html:
            # print('CREATING HTML:\n')
            t.set_description(f"Chapter {chapterNum}: HTML making")
            t.refresh()
            html_maker.createHTML(folderName, imgDir, chapterNum, chapterNum<end-1)
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