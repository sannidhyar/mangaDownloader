# import webbrowser
import os
import sys

def getFileName(mangaName, chapterNum):
    chapterNum = int(chapterNum)
    if chapterNum < 10:
        filename = f'{mangaName}_000{chapterNum}.html'
    elif chapterNum < 100:
        filename = f'{mangaName}_00{chapterNum}.html'
    elif chapterNum < 1000:
        filename = f'{mangaName}_0{chapterNum}.html'
    else:
        filename = f'{mangaName}_{chapterNum}.html'
    
    return filename

def createHTML(saveDir, imgDir, chapterNum:int, nextAvailable:bool):
    if chapterNum == 1:
        prevAvailable = False
    else:
        prevAvailable = True
    chapter = 'Chapter'
    filename = os.path.join(saveDir, getFileName(chapter, chapterNum))
    f = open(f'{filename}','w')

    html = """<!DOCTYPE html>\n<html>\n<head>\n<title>""" + getFileName(chapter, chapterNum)
    html += """</title>
<style>
    .image {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    }
</style>
</head>
<body>
    <div class="image-gallery">
    """
    img = []
    images = sorted(os.listdir(imgDir))
    [mangaName, chapterName] = imgDir.split('/')[-3:-1]
    phoneDir = f'/storage/emulated/0/Download/{mangaName}/{chapterName}'
    htmlDir = f'/storage/emulated/0/Download/{mangaName}'
    for i in range(len(images)):
        if i == 0:
            html += f'    <img src="{os.path.join(phoneDir, images[i])}" class="image">\n'
        else:
            html += f'        <img src="{os.path.join(phoneDir, images[i])}" class="image">\n'
    html += '    </div>\n'
    if nextAvailable or prevAvailable:
        # print(saveDir, getFileName(mangaName, chapterName))
        if prevAvailable:
            a_ref_prev = f'''\t<div style="float: left;">\n\t\t<a href="{os.path.join(htmlDir, getFileName(chapter, chapterNum-1))}"><h3>Chapter {chapterNum-1} </h3></a>\n\t</div>\n'''
            html += a_ref_prev
        
        if nextAvailable:
            a_ref_next = f'''\t<div style="float: right;">\n\t\t<a href="{os.path.join(htmlDir, getFileName(chapter, chapterNum+1))}"><h3>Chapter {chapterNum+1} </h3></a>\n\t</div>'''
            html += a_ref_next
        
        
    html += '''\n</body>\n</html>'''



    # f.write(message)
    # f.close()

    #Change path to reflect file location
    # filename = 'file:///Users/username/Desktop/programming-historian/' + 'helloworld.html'
    # webbrowser.open_new_tab(filename)
    f.write(html)
    f.close()
    
if __name__ == '__main__':
    saveDir = sys.argv[1]
    imgDir = sys.argv[2]
    chapterNum = int(sys.argv[3])
    createHTML(saveDir, imgDir, chapterNum, False)