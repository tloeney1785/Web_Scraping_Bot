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
#Loop to go over all pages
# pages = np.arange(1, 3, 1)
data=[]

for page in pages:
    
    page= "https://www.leafly.com/finder/doctors/ontario-or?page=" + str(page) 
    driver = webdriver.Chrome()
    driver.get(page)  
    sleep(randint(2,10))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    my_table = soup.find_all(class_=['description', 'price-label body-3','price title-5',\
                                    'score orange big'])

    for tag in my_table:
        data.append(tag.get_text())

##############################
#First loop: getting the URLs 
##############################

pages = np.arange(1, 3, 1)

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

#Remove if not starting with pwa, remove if ending with display=reviews
url_final = [x for x in urls_final if x.startswith('/doctors/')]
# url_final = [x for x in url_final if not x.endswith('display=reviews')]
   
string = 'https://www.leafly.com'
final_list=[string + s for s in url_final]
print(final_list)