import requests
import re
from datetime import datetime

from requests.api import request

basepath= 'https://flockmod.com/gallery/index.php?q=/post/list/user_id=29797/'
flokmod_img_regex = rb'https://flockmod-[^\']*'
header_regex = rb'<title>No Images Found</title>'

def pull_from_site(page_number):
    return requests.get(basepath + str(page_number), allow_redirects=False).content

def if_image_found(html_page):
    return re.search(header_regex,  html_page) == None

def get_imageurls(html_page):
    imageurl_byte = re.findall(flokmod_img_regex, html_page)
    imageurl_clean = []
    thumb_regex = '/thumbs/'
    for image_byte in imageurl_byte:
        decoded = image_byte.decode('utf-8');
        if(re.search(thumb_regex, decoded) != None):
            imageurl_clean.append(re.sub(thumb_regex, '/images/', decoded))
        else:
            imageurl_clean.append(decoded)
    return imageurl_clean


#request the page
r = requests.get(basepath+'1', allow_redirects=False)
# #gets the images links from the page
# imageurl_byte = re.findall(flokmod_img_regex, r.content)


#decode the html links
imageurl = []

#get all from 
page_number= 1

while if_image_found(pull_from_site(page_number)):
    imageurl += (get_imageurls(pull_from_site(page_number)))
    print("page: {} processed".format(page_number))
    page_number +=1


#get Images
def get_filename_from_header(cd):
    cd = re.sub(',','',cd)
    cd = re.sub('\s+','-',cd)
    cd = re.sub(':','-',cd)
    return cd
    # if not cd:
    #     lm =r.headers.get('Last-Modified')
    #     print(lm)
    #     return lm
    # fname = re.findall('filename=(.+)', cd)
    # if len(fname) == 0:
    #     return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    # return fname[0];

print("Retreving images")

for image in imageurl:
    r = requests.get(image, allow_redirects=True)
    filename = get_filename_from_header(r.headers.get('Last-Modified'))
    save_to = 'D:\\images\\'
    if filename == None:
        continue
    savepath = save_to + filename + '.png'
    
    open(savepath, 'wb').write(r.content)

print("Done")