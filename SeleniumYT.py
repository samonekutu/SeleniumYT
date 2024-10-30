#!/usr/bin/env python
# coding: utf-8

# In[108]:


#INSTALL AND IMPORT ALL DEPENDENCY

#pip install selenium webdriver-manager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException

#others
import urllib
import pyperclip  #Window clipboard
from IPython.display import YouTubeVideo


# In[109]:


def youtubeSearch(textToSearch,play=True,demo=False):
    #SEARCH QUERY TEXT
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query   
    
    # Empty dictionary to extract result to
    video = {}                                                     
    
    # initialize a web driver instance to control a Chrome window viusally
    # in headless mode
    options = Options()
    if demo==True:
        options.add_argument('argument')  
        
    else:
        options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=options)


    # scraping logic...
    # visit the target page in the controlled browser
    driver.get(url)  # instructing Selenium to connect to the target page


    # CONSENT PAGE
    try:
        # wait up to 10 seconds for the consent dialog to show up
        consent_overlay = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'dialog'))
        )

        # select the consent option buttons
        consent_buttons = consent_overlay.find_elements(By.CSS_SELECTOR, '.eom-buttons button.yt-spec-button-shape-next')
        if len(consent_buttons) > 1:
            # retrieve and click the 'Accept all' button [the botton 1]
            accept_all_button = consent_buttons[1]
            accept_all_button.click()
    except TimeoutException:
        print('Cookie modal missing')




    # WAIT FOR  PAGE TO LOAD UP
    # wait for YouTube to load the page data and 'h1.ytd-watc ' is loaded
    WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h3.ytd-video-renderer'))
    )


    #FIND CONTENT
    try:
        title = driver.find_element(By.CSS_SELECTOR, 'h3.ytd-video-renderer').text

        #vid_url = vid_url
        driver2 = driver.find_element(By.ID, 'meta')  #'primary' as ID
        vid_url = driver2.find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint').get_attribute('href')

        # click on more options on 1st video result
        driverx = driver.find_element(By.ID, 'dismissible')  #'primary' as ID
        share_buttons = driverx.find_element(By.CSS_SELECTOR, 'ytd-menu-renderer.style-scope')  #'primary' as ID
        share_buttons.click()

        #click share button
        share_buttons2 = driver.find_element(By.CSS_SELECTOR, 'tp-yt-paper-listbox#items.style-scope')  #'primary ytd-menu-service-item-renderer' as ID
        share_buttons2.click()

        #click and copy embedded url to windows clip board
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,'yt-button-renderer#copy-button.style-scope')))
        share_buttons3 = driver.find_element(By.CSS_SELECTOR,'#bar.style-scope.yt-copy-link-renderer yt-button-shape')#button.yt-spec-button-shape-next  yt-button-shape
        q = share_buttons3.click()
    except TimeoutException:
        print('timed out: please try again!')
    #get meta info on video
    meta = driver.find_element(By.ID, 'metadata-line').text

    # save all results to Video dictionary
    video['title'] = title
    video['vid_url'] = vid_url
    video['meta']= meta
    video['embedded_url'] = pyperclip.paste()[17:]
 

    # close the browser and free up the resources
    driver.quit()
    # Output
    if play== True:
        print(video)
        display(YouTubeVideo(video['embedded_url']))
    else:
        return(video)
       
    
 


# In[110]:


#youtubeSearch("jays of clay worlds apart video",demo=True,play=True)

