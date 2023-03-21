import urllib.request
import requests
import re
import sys


def validateUrl(url):

    pattern = r"^((http|https):\/\/)?(www\.)?([\w\-\.]+)+$"
    obj = re.match(pattern, url)
        
    return obj

def fixUrls(main_url):

    if not main_url.startswith("http"):

            if not main_url.startswith("www."):

               main_url = "https://www." + main_url

            else: 

                main_url = "https://" + main_url
    else:

            if not re.sub("https?:\/\/", "", main_url).startswith("www."):

                secure = False
                if main_url.find("http") != -1:

                    secure = True

                main_url = ("http" if not secure else "https") + "://www." + re.sub(r"https?://", "", main_url)


            
    components = main_url.split("//")
    main_url= main_url.split("//")[0] + "//" + main_url.split("//")[1] + "/"
    pre_url = components[0] + "//"
    post_url = re.sub("www\.", "", components[1])
    
    return (main_url, pre_url, post_url)

def extractLinks(main_url,links_output):

    request = urllib.request.Request(url=main_url, headers={'User-Agent': 'Mozilla/5.0'})    
    websiteUrl = urllib.request.urlopen(request)

    link_pattern = r'href="[^#\"]{2,}?"'

    refs = re.findall(link_pattern, websiteUrl.read().decode())

    web_pattern = r'".*"'

    links_output.write(main_url + ":\n\n")

    for ref in refs:
        ref = re.findall(web_pattern, ref)[0][1:-1]
        links_output.write("\t" + ref + "\n")
        links_output.flush()
       

    links_output.write("\n")