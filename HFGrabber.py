import time
import os
import sys
import requests

if os.name == "nt":
    SLASH = "\\"
else:
    SLASH = "/"

CWD = os.path.dirname(os.path.realpath(__file__)) + SLASH
HEADERS = requests.utils.default_headers()
HEADERS.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",})
COOKIE = {}
FILTER = { # uncomment to enable the filter 
"YII_CSRF_TOKEN":"", #do not edit
"filter_media":"A", # not relevant
"filter_order":"date_new", # not relevant
"filter_type":"0", # not relevant
"rating_beast":"0",
#"rating_beast":"1", # uncomment/comment to enable/disable Bestiality content
"rating_female":"0",
#"rating_female":"1", # uncomment/comment to enable/disable female nudity content
"rating_furry":"0",
#"rating_furry":"1", # uncomment/comment to enable/disable Anthropomorphic/furry content
"rating_futa":"0",
#"rating_futa":"1", # uncomment/comment to enable/disable Contains Futanari/Dickgirl/Transgender/Hermaphrodite content
"rating_guro":"0",
#"rating_guro":"1", # uncomment/comment to enable/disable Gore, scat, similar macabre content
"rating_incest":"0",
#"rating_incest":"1", # uncomment/comment to enable/disable Incest content
"rating_male":"0",
#"rating_male":"1", # uncomment/comment to enable/disable male nudity content
"rating_nudity":"3", # 0 = None, 1 = Mild Nudity, 2 = Moderate Nudity, 3 = Explicit Nudity
"rating_other":"0",
#"rating_other":"1", # uncomment/comment to enable/disable Other offensive content
"rating_profanity":"3", # 0 = None, 1 = Mild Profanity, 2 = Moderate Profanity, 3 = Proliferous or Severe Nudity 
"rating_racism":"3", # 0 = None, 1 = Mild Racist themes or content, 2 = Racist themes or content, 3 = Strong racist themes or content
"rating_rape":"0",
#"rating_rape":"1", # uncomment/comment to enable/disable Non-consensual/Rape/Forced content
"rating_scat":"0",
#"rating_scat":"1", # uncomment/comment to enable/disable Scat/Coprophilia/Feces content
"rating_sex":"3", # 0 = None, 1 = Mild suggestive content, 2 = Moderate suggestive or sexual content, 3 = Explicit or adult sexual content
"rating_spoilers":"3", # 0 = None, 1 = Mild Spoiler Warning, 2 = Moderate Spoiler Warning, 3 = Major Spoiler Warning
"rating_teen":"0",
#"rating_teen":"1", # uncomment/comment to enable/disable Teen content
"rating_violence":"3", # 0 = None, 1 = Comic or Mild Violence, 2 = Moderate Violence, 3 = Explicit or Graphic Violence
"rating_yaoi":"0",
#"rating_yaoi":"1", # uncomment/comment to enable/disable Shonen-ai (male homosexual) content
"rating_yuri":"0",
#"rating_yuri":"1" # uncomment/comment to enable/disable Shoujo-ai (female homosexual) content
}

WISHLIST = CWD + "wishlist.txt"
SES = requests.Session()

def get_file(srcfile, srcurl, counter=0, ftype=0):#ftype indicates if video or not
    """Function to Downloadad and verify downloaded Files"""
    if counter == 5:
        print("Could not download File:", srcfile, "in 5 attempts")
        return 1
    counter = counter + 1
    if not os.path.isfile(srcfile):
        time.sleep(5)
        print("Downloading", srcurl, "as", srcfile)
        with open(srcfile, "wb") as fifo:#open in binary write mode
            response = requests.get(srcurl, headers=HEADERS, cookies=COOKIE)#get request
            print("\n\n\n", response.headers,"\n\n\n") # check against actual filesize
            fifo.write(response.content)#write to file
        if int(str(os.path.getsize(srcfile)).strip("L")) < 25000 and ftype: #Assumes Error in Download and redownlads File
            print("Redownloading", srcurl, "as", srcfile)
            autocleanse(srcfile)
            return get_file(srcfile, srcurl, counter)
        else: #Assume correct Filedownload
            return 0
    else:
        if int(str(os.path.getsize(srcfile)).strip("L")) < 25000 and ftype: #Assumes Error in Download and redownlads File
            print(srcfile, "was already downloaded but the filesize does not seem to fit -> Redownl0ading")
            autocleanse(srcfile)
            return get_file(srcfile, srcurl, 0)
        else: #Assume correct Filedownload
            print("File was downloaded correctly on a previous run")
            return 0

def autocleanse(cleansefile):
    """ Function for safer deleting of files """
    if os.path.exists(cleansefile):
        os.remove(cleansefile)
        print("Removed:", cleansefile)
        return
    else:
        print("File", cleansefile, "not deleted, due to File not existing")
        return

def init():
    init_req = SES.get("http://www.hentai-foundry.com/?enterAgree=1&size=0", headers=HEADERS)
    cookies = init_req.cookies
    print(cookies)
    csrf_set = False
    for cookie in cookies:
        cookie = str(cookie)
        COOKIE[cookie.split("Cookie ")[1].split("=")[0]] = cookie.split("=")[1].split(" for")[0]
    filted_req = SES.post("http://www.hentai-foundry.com/site/filters", headers=HEADERS, data=FILTER, cookies=COOKIE)
    for line in init_req.content.decode("UTF-8").split("\n"):
        if "YII_CSRF_TOKEN" in line and not csrf_set:
            print(line)
            FILTER["YII_CSRF_TOKEN"] = line.split("value=\"")[1].split("\" name=")[0]
            csrf_set = True
    print(FILTER)
    print(COOKIE)
    with open(WISHLIST, "r") as whl:
        for line in whl:
            if not "#" in line:
                line = str(line).replace("\n", "")
                folder = CWD + str(line) + SLASH
                if not os.path.exists(folder):
                    os.mkdir(folder)
                retrive_source(line, folder)

def retrive_source(name, folder):
    url = "http://www.hentai-foundry.com/pictures/user/" + str(name)
    req = SES.get(url, headers=HEADERS, cookies=COOKIE)
    lastpage = None
    for line in req.content.decode("UTF-8").split("\n"):
        if ">Last" in line:
            lastpage = int(float(line.split("\">Last")[0].split("/page/")[1]))
    if lastpage is not None:
        for page in range(1, lastpage):
            get_gallery(url + "/page/" + str(page), folder)

def get_gallery(url, folder):
    req = SES.get(url, headers=HEADERS, cookies=COOKIE)
    pagelist = []
    for line in req.content.decode("UTF-8").split("\n"):
        if "thumbLink" in line:
            for reference in line.split("</a>"):
                if "profile" not in reference and len(reference) >= 10:
                    print()
                    print(reference)
                    page_url = "http://www.hentai-foundry.com" + reference.split("href=\"")[1].split("\">")[0]
                    pagelist.append(page_url)
    pagelist = list(set(pagelist))
    for page in pagelist:
        print(page)
    for page in pagelist:
        get_page(page, folder)

def get_page(page, folder):
    req = SES.get(page, headers=HEADERS, cookies=COOKIE)
    image_url = None
    for line in req.content.decode("UTF-8").split("\n"):
        if "class=\"center\"" in line:
            image_url = "http:" + line.split("src=\"")[1].split("\" alt=\"")[0]
    if image_url is not None:
        name = image_url.split("/")[len(image_url.split("/")) - 1]
        get_file(folder + name, image_url, 0, 1)
              
def main():
    init()

main()

