# import libraries
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint
from selenium import webdriver

no = 1

def test(n):
    global no
    page= "https://www.leafly.com/finder/doctors/ontario-or?page=" + str(n) 
    driver = webdriver.Chrome()
    driver.get(page)  
    sleep(randint(2,10))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if soup.findAll("span",text="Next"):#class_="mr-xs") :
        print("ayy")
        no += 1
        test(no)

test(no)
data=[]

##############################
#First loop: getting the URLs 
##############################

# for page in pages:
page="https://www.leafly.com/finder/doctors/salem-or" 
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