# Dependencies 
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from datetime import date
from datetime import timedelta
import time

########## date fields for later use...
curr_date = date.today()
y_date = curr_date - timedelta(days = 1)
dby_date = curr_date - timedelta(days = 2)
# print(curr_date, y_date, dby_date)
cstr = curr_date.strftime('%b %d, %Y')
ystr = y_date.strftime('%b %d, %Y')
dstr = dby_date.strftime('%b %d, %Y')
# print(cstr, ystr, dstr)
###########

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    ### Part-1 : Latest Mars News - web scraping
    # Visit mars news webpage section...
    url = 'https://mars.nasa.gov/news/'
    browser = init_browser()
    browser.visit(url)
    
    # sleep before parsing
    time.sleep(3)
    
    # Create BeautifulSoup object; parse with 'html.parser' 
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Close the browser after scraping
    browser.quit()
    
    # Scraping...
    res = soup.find_all('li', class_="slide")
    for results in res:
        #print(results.a.h3.text)
        news_title = results.a.h3.text
        #print("-----")
        #print(results.a.text)
        news_p = results.a.text
        break
    #print(news_title)
    #print(news_p)
    print("Completed part-1")

    ### Part-2 : Featured Mars Image - web scraping
    # Visit jpl website
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = init_browser()
    browser.visit(url2)
    html = browser.html
    soup2 = bs(html, 'html.parser')

    # Sleep and close the browser after scraping
    time.sleep(3)
    browser.quit()
    
    # Scraping...
    title = soup2.find('h1', class_="media_feature_title").text.strip()
    x = 'article'
    res2 = soup2.find(x, alt=title)
    imgurl = res2["style"].split()[1]
    url = imgurl[imgurl.find("'")+1 : imgurl.find(")")-1]
    featured_image_url = 'https://jpl.nasa.gov'+url
    print("Completed part-2")

    ### Part-3 : Current Mars Weather - web scraping
    url3 = 'https://twitter.com/marswxreport?lang=en'
    
    # Visit Twitter website
    browser = init_browser()
    browser.visit(url3)
    html = browser.html
    
    # Create BeautifulSoup object; parse with 'html.parser' 
    soup3 = bs(html, 'html.parser')

    # Sleep and close the browser after scraping
    time.sleep(3)
    browser.quit()

    # Scraping...
    res3 = soup3.find_all('span')
    # print(res3)
    wstr = ""
    mars_weather = ""
    # finding the latest weather by comapring today's/yesterday/dbyesterday dates...
    for result in res3:
        print(result)
        if ((result.text).find(str(curr_date)) != -1):
            wstr = result.text
            wstr = wstr.replace(str(curr_date), cstr)
            break
        elif ((result.text).find(str(y_date)) != -1):
            wstr = result.text
            wstr = wstr.replace(str(y_date), ystr)
            break
        elif ((result.text).find(str(dby_date)) != -1):
            wstr = result.text
            wstr = wstr.replace(str(dby_date), dstr)
            break
        print(wstr)
        if len(wstr) > 10:
            wstr = wstr.rsplit(' ',1)[0]
            mars_weather = wstr.split(' ',1)[1]
    print(mars_weather)
    print("Completed part-3")
    
    ### Part-4 : Mars Facts - web scraping
    #use Pandas for scraping
    import pandas as pd
    
    url4 = 'https://space-facts.com/mars'
    tables = pd.read_html(url4)
    
    df = tables[0]
    df.columns = ['Description','Value']
    df.set_index('Description', inplace=True)
    html_table1 = df.to_html()
    html_table2 = html_table1.replace('border="1"', '')
    html_table = html_table2.replace('dataframe', 'table table-bordered table-sm')
    html_table.replace('\n', '')
    # print(html_table)
    print("Completed part-4")
    
    ### Part-5 : Mars Hemispheres - web scraping
    # Visit the USGS Astrogeology site
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Retrieve page with the requests module
    response5 = requests.get(url5)
    
    # Create BeautifulSoup object; parse with 'html.parser' 
    soup5 = bs(response5.text, 'html.parser')
    
    # Scraping...
    res = soup5.find_all('div', class_="item")
    
    # sometimes the website goes down for maintenance
    # so checking whether the website is down before scraping....
    down_mes = '503 Service Temporarily Unavailable'
    part5_down = ''
    title = []
    ref = []
    # t1 = soup5.title.text.find(down_mes)
    # print(type(t1))
    if (soup5.title.text.find(down_mes) != '-1'):
        for x in res:
            try:
                if (x.h3.text and x.a['href']):
                    print(x.h3.text)
                    title.append(x.h3.text)
                    print(x.a['href'])
                    ref.append(x.a['href'])
            except AttributeError as e:
                print(e)
    else:
        print("Service temporarily unavailable")
        part5_down = down_mes + ' for '+ url5 + ' Please try later.'

    # checking whether the list is empty
    if not title:
        if len(part5_down) > 5:
            print(part5_down)
        else:
            print("Something went wrong with scraping method")
            part5_down = 'Something went wrong, please notify webadmin.'
    else:
        print("-------")
        print(title, ref)
    
    hemisphere_image_urls = []
    if not part5_down:
        for i in range(len(ref)):
            print(ref[i])
            baseurl = 'https://astrogeology.usgs.gov'
            curl = baseurl+ref[i]
            print(curl)
            #browser.click_link_by_href(curl)
            #browser.click_link_by_href(ref[i])
            url51 = curl
            response51 = requests.get(url51)
            soup51 = bs(response51.text, 'html.parser')
            #res51 = soup51.find_all('div', class_="downloads")
            res51 = soup51.find_all('img', class_="wide-image")
            hemisphere_image_urls.append({"title":title[i], "img_url":baseurl+res51[0]['src']})
        print(hemisphere_image_urls)

    else:
        print(part5_down)
        hemisphere_image_urls.append(part5_down)
    print("Completed part-5")
    
    # Assembling all the results into one dictionary variable...
    mars_data = {}
    mars_data = {
        "news_title":news_title,
        "news_para":news_p,
        "image_url":featured_image_url,
        "weather":mars_weather,
        "facts":html_table,
        "hemisphere_images":hemisphere_image_urls
                }
    print("Completed scraping...")
    # Return results
    return mars_data
