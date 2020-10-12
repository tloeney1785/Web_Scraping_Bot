# import libraries
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint
from selenium import webdriver
import csv
from tkinter import *

page=input("Enter the webpage:\n") 

############################################################################################
#LOOP THROUGH PAGES

# no = 1
# def test(n):
#     global no
#https://www.leafly.com/finder/doctors/miami-fl?lat=25.7747146&lng=-80.2189312&zoom=10&view=map&page=4
#Works with these type of links, have to adjust map and click "search this area first" then add &view=map&page= to the end
#     pages= page + "&view=map&page=" + str(n) 
#     driver = webdriver.Chrome()
#     driver.get(pages)  
#     sleep(randint(2,10))
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     if soup.findAll("span",text="Next"):
#         no += 1
#         test(no)
# test(no)

############################################################################################

#GETTING DOCTOR INFO

# driver = webdriver.Chrome()
# driver.get(page)  
# sleep(randint(5,15))
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# urls = [item.get("href") for item in soup.find_all("a")]
    
# #Remove duplicates and none values
# urls_final = list(dict.fromkeys(urls))
# urls_final = list(filter(None, urls_final)) 

# #Remove if not starting with /doctors/
# url_final = [x for x in urls_final if x.startswith('/doctors/')]
   
# string = 'https://www.leafly.com'
# final_list=[string + s for s in url_final]
# print(final_list)

# for i in range(0,len(final_list)):
#     url = final_list[i]
#     driver2 = webdriver.Chrome()
#     driver2.get(url)  
#     # sleep(randint(10,20))
#     soup = BeautifulSoup(driver2.page_source, 'html.parser')
    
#     temp = []
#     tels_final = []
#     for n in soup.find_all('h1'):
#         temp.append(n.text)

#     tels = [item.get("href") for item in soup.find_all("a")]
#     #Remove duplicates and none values
#     tels_final = list(dict.fromkeys(tels))
#     tels_final = list(filter(None, tels_final)) 

#     #filter for tel
#     tels_final = [x for x in tels_final if x.startswith('tel:')]
#     for n in soup.findAll("div", {"class": "text-sm mb-xs flex items-center"}):
#         tels_final.append(n.text)
    
#     with open('info.csv', mode='a') as info:
#             employee_writer = csv.writer(info, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             employee_writer.writerow([temp, tels_final])

#################################################################################
#BOTH LOOP THROUGH PAGES AND GET DOCTOR DATA
#################################################################################
# https://www.leafly.com/finder/doctors/garden-grove-ca
# https://www.leafly.com/finder/doctors/baldwin-new york
link = ''
current_page = 1
speed = 10

def Scrape(link,n,speed):
    global current_page
    pages= link + "&view=map&page=" + str(n) 
    driver = webdriver.Chrome()
    driver.get(pages)  

    #WAIT FOR PAGE PAGE TO LOAD BEFORE PARSE
    sleep(2)

    #PARSE PAGE INTO HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #RETRIEVE ALL URLS FOUND IN THE CURRENT_PAGE
    urls = [item.get("href") for item in soup.find_all("a")]

    #REMOVE ANY DUPLICATE OR NONE VALUES FROM LIST OF URLS
    urls_final = list(dict.fromkeys(urls))
    urls_final = list(filter(None, urls_final)) 

    #FILTER FOR /doctors/ URLS
    url_final = [x for x in urls_final if x.startswith('/doctors/')]

    #CONCATENATE DOCTOR URLS TO SITE URL TO OBTAIN DIRECT LINKS
    string = 'https://www.leafly.com'
    final_list=[string + s for s in url_final]

    #LOOP THROUGH LIST OF DOCTOR URLS
    for i in range(0,len(final_list)):
        url = final_list[i]
        driver2 = webdriver.Chrome()
        driver2.get(url)  
        sleep(speed) #OPTION TO SLOW DOWN PROGRAM

        #PARSE DOCTOR URLS TO HTML 
        soup1 = BeautifulSoup(driver2.page_source, 'html.parser')
        
        #EMPTY DATA FIELDS
        title = []
        tels_final = []
        address = []
        email = []
        tags =[]

        #NAME SEARCH
        for n in soup1.find_all('h1'):
            title.append(n.text)

        #ADDRESS SEARCH
        for n in soup1.find_all("span", attrs={'data-testid':'primary-location'}):
            address.append(n.text)

        #EMAIL SEARCH
        mail = [item.get("href") for item in soup1.find_all("a")]
        #REMOVE ANY DUPLICATE OR NONE VALUES FROM LIST OF ANCHOR TAGS
        email = list(dict.fromkeys(mail))
        email = list(filter(None, email)) 
        #FILTER FOR EMAIL FROM LIST ABOVE
        email = [x for x in email if x.startswith('mailto:')]

        #PHONE SEARCH
        tels = [item.get("href") for item in soup1.find_all("a")]
        #REMOVE ANY DUPLICATE OR NONE VALUES FROM LIST OF ANCHOR TAGS
        tels_final = list(dict.fromkeys(tels))
        tels_final = list(filter(None, tels_final)) 
        #FILTER FOR NUMBER FROM LIST ABOVE
        tels_final = [x for x in tels_final if x.startswith('tel:')]
        for n in soup1.findAll("div", {"class": "text-sm mb-xs flex items-center"}):
            tels_final.append(n.text)
            
        #TAG SEARCH
        for n in soup1.find_all("span", attrs={'class':'tag mr-xs mb-xs'}):
            tags.append(n.text)

        #WRITE DATA FIELDS CSV FILE
        with open('doctors.csv', mode='a', newline='',encoding="utf-8") as doctors:
                writer = csv.writer(doctors, delimiter=',')
                writer.writerow([title, tels_final,address,email,tags])

    #IF NEXT BUTTON IS DETECTED ADD 1 TO CURRENT PAGE AND RUN AGAIN
    if soup.findAll("span",text="Next"):
        current_page += 1
        Scrape(link,current_page,speed)

#VERY BASIC FRONT END 
def form():
    root = Tk() 
    root.geometry("400x220")
    root.title('Leafly Scraper') 
    top = Label(root, text='Leafy Scraper',font="times 20 bold") 
    top.place(x=110,y=0)
    urlL = Label(root, text='URL of Map:',font="times 12") 
    urlL.place(x=10,y=80)
    urlEL = Entry(root,font="times 12",width=35)
    urlEL.place(x=100,y=80)
    speedL = Label(root, text='Speed (0 fastest):',font="times 12") 
    speedL.place(x=10,y=120)
    w2 = Scale(root, from_=0, to=10, orient=HORIZONTAL)
    w2.place(x=180,y=105)
    def linkget():
        global link
        global speed
        link = urlEL.get()
        speed = w2.get()
    def close():
        root.destroy()
    scrapeB = Button(root, text='Scrape', command=lambda:[linkget(),Scrape(link,current_page,speed),close()],font = "time 14 italic bold",padx=50) 
    scrapeB.place(x=120,y=170)
    root.mainloop()

form()


