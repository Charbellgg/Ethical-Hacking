# Ethical Hacking
## Disclaimer:  You can try your script on Metasploit which is an open-source framework for developing, testing, and executing exploits against remote targets. It provides a suite of tools and utilities for exploiting vulnerabilities in software systems, including web applications, servers, and network devices. There also websites that are designed to be hacked such as tryhackme.com.
Definition: Ethical hacking, also known as "white hat" hacking, refers to the practice of using the same methods and techniques that a malicious attacker would use to attempt to penetrate a computer system or network, but with the goal of identifying and fixing security vulnerabilities, rather than causing harm.

This project will tackle extracting meaningful information from a website, such as directories, files, subdomains and their respective urls. You will have to write a Python script that takes a master url from the shell and executes the instructions on it.

## Steps:
1. Import the relevant libraries using the following statements: 
- import urllib.request
- import requests
- import re
- import sys

Each one will have its use later in the project.

2. Write a function that validates a url using regular expressions. There are many different possible expressions, but the most common one is:
"^((http|https):\/\/)?(www\.)?([\w\-\.]+)+$"

3. After you have a function to validate a url, a user might enter a valid url but in many different ways. Http/https:// and www. are optional. That's why we will have a function that fixes these urls to one format: http/https://[domain-name]

4. Now you have a valid and correctly formatted url. It's better to split the url into three parts, the "http/https://" alone and the [domain-name] apart. It's time to start extracting the information.

### Extracting Links:

1. You should use this line of code: request = urllib.request.Request(url=[master-url], headers={'User-Agent': 'Mozilla/5.0'}) 
<br>
The urllib library in Python's purpose is to create a request object to send an HTTP request to the server specified by the URL [master-url]. The request includes a User-Agent header that is set to 'Mozilla/5.0'.

Here is a breakdown of the different components of the code:

urllib.request.Request: This creates a new HTTP request object that can be used to send a request to a server. It takes the URL as the first argument and any additional headers or data as optional keyword arguments.

url=[master-url]: This specifies the URL that the request should be sent to. main_url is a variable that should contain a valid URL.

headers={'User-Agent': 'Mozilla/5.0'}: This specifies the headers that should be included in the HTTP request. The User-Agent header identifies the client that is making the request, and in this case, it is set to 'Mozilla/5.0'. This is a common user agent string that is used to identify the request as coming from the Mozilla Firefox web browser.

2. You should then send a url open request using the previously made request

3. The .read() and .decode() methods are typically used when retrieving the response from an HTTP request in Python using the urllib library.

When you send an HTTP request to a server using urllib, the server will typically respond with some data that you may want to use in your Python code. The data returned by the server is typically encoded in bytes, so it needs to be decoded before it can be processed.

The .read() method is used to read the response data from the HTTP request object. This method returns the response data as a sequence of bytes.

The .decode() method is then used to convert the sequence of bytes into a string that can be processed by Python. This method takes an encoding as a parameter and uses it to decode the bytes into a string.

After having the data decoded, you can know use the re.findall(pattern, data) to extract the html from the file.

4. Use regular expressions to extract the href="" that are inside the <a> tags.

5. Now that you have a list of all hrefs, store them in a file.

### Extracting Directories/Files:

1. The Directories/Files need to be concatenated with the master link in order to be extracted. The format is the following: [master-link]/(Directory or File).

2. You will now need to send a request and extract its status code in order to make sure the directory or file is found. You can extract the code using this syntax: status_code = requests.get([master-url] + url.rstrip('\n')).status_code.
If the error code is 404, this means that the request did not find the directory or file you were looking for.
What you want to receive is a status code between 200 and 299 indicating a succesful request. In this case, you'd have to extract the links from the found urls. You can use the same function that was previously used to extract links from the master url.
You may also care about 403 error code which means that you found said directory or file but the access is denied. One of the difficulties you might face is trying to extract the links from this url. You won't be able to as the access is denied. 
One error you might face is an error code of 429, which occurs when too many requests are sent in a short period of time. In this case, you won't be able to extract the html.
3. Store the directories and files that had a status code between 200 and 299 or 403.

### Extracting Subdomains:

1. The Subdomains need to be concatenated with the master link in order to be extracted. The format is the following: (http or https)://[subdomain-name].[master-link]

2. You will now need to send a request and extract its status code in order to make sure the subdomain is found. One error you might face will be related to connection. This can be fixed by surrounding the request with try except.
If the error code is 404, this means that the request did not find the subdomain you were looking for.
What you want to receive is a status code between 200 and 299 indicating a succesful request. In this case, you'd have to extract the links from the found urls. You can use the same function that was previously used to extract links from the master url and directories or files.
You may also care about 403 error code which means that you found said directory or file but the access is denied. One of the difficulties you might face is trying to extract the links from this url. You won't be able to as the access is denied. 
One error you might face is an error code of 429, which occurs when too many requests are sent in a short period of time. In this case, you won't be able to extract the html.
3. Store the subdomains that had a status code between 200 and 299 or 403.

5. Now that you have functions to extract links, files and directories, and subdomains, it's time to execute the code. You will use the previously implemented functions on a list of already existing and known files, directories and subdomains. It's better to extract these and store the files and directories in a file, and the subdomains in another. You will have to loop throught the files and send continuous requests to make extract the information.

6. The sys library that was previously imported will be used to extract the shell script arguments. The code can be executed by using the python3 [filename] [url] in the shell. To access the master url in the Python script, you will need to use: sys.argv[1].

## Congrats! Now you have a Python script capable of extracting links, files, directories and subdomains from a target url that you chose. Use it wisely.
