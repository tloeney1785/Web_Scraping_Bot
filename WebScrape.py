# import libraries
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint
from selenium import webdriver
import csv

page=input("Enter the webpage:\n") 

############################################################################################
#LOOP THROUGH PAGES

# no = 1
# def test(n):
#     global no
#     pages= page + "?page=" + str(n) 
#     driver = webdriver.Chrome()
#     driver.get(pages)  
#     sleep(randint(2,10))
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     if soup.findAll("span",text="Next"):
#         no += 1
#         test(no)
# test(no)

#GETTING DOCTOR INFO

driver = webdriver.Chrome()
driver.get(page)  
sleep(randint(5,15))
soup = BeautifulSoup(driver.page_source, 'html.parser')
urls = [item.get("href") for item in soup.find_all("a")]
    
#Remove duplicates and none values
urls_final = list(dict.fromkeys(urls))
urls_final = list(filter(None, urls_final)) 

#Remove if not starting with /doctors/
url_final = [x for x in urls_final if x.startswith('/doctors/')]
   
string = 'https://www.leafly.com'
final_list=[string + s for s in url_final]
print(final_list)

for i in range(0,len(final_list)):
    url = final_list[i]
    driver2 = webdriver.Chrome()
    driver2.get(url)  
    # sleep(randint(10,20))
    soup = BeautifulSoup(driver2.page_source, 'html.parser')
    
    temp = []
    tels_final = []
    for n in soup.find_all('h1'):
        temp.append(n.text)

    tels = [item.get("href") for item in soup.find_all("a")]
    #Remove duplicates and none values
    tels_final = list(dict.fromkeys(tels))
    tels_final = list(filter(None, tels_final)) 

    #filter for tel
    tels_final = [x for x in tels_final if x.startswith('tel:')]
    for n in soup.findAll("div", {"class": "text-sm mb-xs flex items-center"}):
        tels_final.append(n.text)
    
    with open('info.csv', mode='a') as info:
            employee_writer = csv.writer(info, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([temp, tels_final])

#################################################################################
#BOTH LOOP THROUGH PAGES AND GET DOCTOR DATA
############################################################################################

# no = 1
# def test(n):
#     global no
#     pages= page + "?page=" + str(n) 
#     driver = webdriver.Chrome()
#     driver.get(pages)  
#     sleep(2)#randint(2,10))
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     urls = [item.get("href") for item in soup.find_all("a")]
    
#     #Remove duplicates and none values
#     urls_final = list(dict.fromkeys(urls))
#     urls_final = list(filter(None, urls_final)) 

#     #Remove if not starting with /doctors/
#     url_final = [x for x in urls_final if x.startswith('/doctors/')]
    
#     string = 'https://www.leafly.com'
#     final_list=[string + s for s in url_final]
#     print(final_list)

#     for i in range(0,len(final_list)):
#         url = final_list[i]
#         driver2 = webdriver.Chrome()
#         driver2.get(url)  
#         # sleep(randint(10,20))
#         soup1 = BeautifulSoup(driver2.page_source, 'html.parser')
        
#         temp = []

#         for n in soup1.find_all('h1'):
#             temp.append(n.text)

#         tels = [item.get("href") for item in soup1.find_all("a")]
#         #Remove duplicates and none values
#         tels_final = list(dict.fromkeys(tels))
#         tels_final = list(filter(None, tels_final)) 

#         #filter for tel
#         tels_final = [x for x in tels_final if x.startswith('tel:')]
            
#         with open('info.csv', mode='a') as info:
#                 employee_writer = csv.writer(info, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                 employee_writer.writerow([temp, tels_final])
#     if soup.findAll("span",text="Next"):
#         no += 1
#         test(no)
# test(no)

