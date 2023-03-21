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
        links_output.flush() ##forces lines to be written to file even with interruption
       

    links_output.write("\n")


def extractDirectories(url, dirs_files_output, links_output):
            
    status_code = requests.get(main_url + url.rstrip('\n')).status_code
    if status_code == 404:
            
            print('Directory or File does not exist: ' + url.rstrip('\n'))

    elif status_code // 100 == 2: ##directory/file exist
         
         print('Directory or File does exist: ' + url.rstrip('\n') + "Code: " + str(status_code)) 
                
         extractLinks(main_url + url.rstrip('\n'), links_output)

         dirs_files_output.write(main_url + url.rstrip('\n') + "\t" + "Code: " + str(status_code) + "\n" )
         dirs_files_output.flush() ##forces lines to be written to file even with interruption
            
    elif status_code == 403: ##directory/file exists but the access is denied
          
        print('Directory/File does exist: ' + url.rstrip('\n') + "Code: " + str(status_code)) 

        dirs_files_output.write(main_url + "\t" + "Code: " + str(status_code) + "\n" )
        dirs_files_output.flush() ##forces lines to be written to file even with interruption

def extractSubdomains(url, subdomains_output, links_output):
    
            
    link = pre_url + url.rstrip('\n') + "." + post_url
        
    try: ##making sure that the status code is valid to avoid error
            
        status_code = requests.get(link).status_code

    except:

            status_code = 404

    if status_code == 404:

            print('Subdomain does not exist: ' + url.rstrip('\n'))

    elif status_code // 100 == 2: ##subdomain exists

        print('Subdomain does exist: ' + url.rstrip('\n') + " " + "Code: " + str(status_code)) 
        extractLinks(link, links_output)
        subdomains_output.write(link + "\t" + "Code: " + str(status_code) + "\n" )
        subdomains_output.flush() ##forces lines to be written to file even with interruption
       

    elif status_code == 403: ##subdomain exists but the access is denied
                
        print('Subdomain does exist: ' + url.rstrip('\n') + " " +  "Code: " + str(status_code)) 
        subdomains_output.write(link + "\t" + "Code: " + str(status_code) + "\n" )
        subdomains_output.flush() ##forces lines to be written to file even with interruption

        

if(sys.argv[1]):

    main_url = sys.argv[1]
    
    if(validateUrl(main_url)): 

        (main_url, pre_url, post_url) = fixUrls(main_url)

    with open("./subdomains_output.bat", 'a') as subdomains_file:

        with open("./dirs_output.bat", 'w') as dirs_files_file:

            with open("./links_output.bat", 'w') as links_file:

                extractLinks(main_url, links_file)

                with open("input_files(1)/dirs_dictionary.bat", "r") as directories:

                    for dir in directories.readlines():
                                    
                        extractDirectories(dir, dirs_files_file, links_file)

                with open("input_files(1)/subdomains_dictionary.bat", "r") as subs:

                                for sub in subs.readlines():
                                    
                                    extractSubdomains(sub, subdomains_file, links_file)