import undetected_chromedriver as uc
import numpy as np
from datetime import datetime
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
#import schedule
import time
#from fp.fp import FreeProxy

last_info = ''


def get_info():
    global last_info
    ua = UserAgent()
    userAgent = ua.random
       
    #proxy = FreeProxy().get()
    options = uc.ChromeOptions()
    options.add_argument(f'user-agent={userAgent}')
    #options.add_argument('--headless') # Need to fix in headless mode
    #options.add_argument('--proxy-server=%s' % proxy)
    
    driver = uc.Chrome(options=options, version = 94)
    driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled":True})
    try:
        driver.get("https://announcements.bybit.com/en-US/?category=&page=1")
       
        
        articles = driver.find_element(By.CLASS_NAME, "article-list")
        if articles.text != last_info:
            last_info = articles.text
            
            dates = articles.find_elements(By.CLASS_NAME, "article-item-date")
            titles = articles.find_elements(By.CLASS_NAME, "article-item")
            refs = articles.find_elements(By.CLASS_NAME, "no-style")
        
            dates = [datetime.strptime(date.text, '%b %d, %Y') for date in dates]
            
            date_num = np.argmax(dates)
            
            title_full = titles[date_num].text
            ref = refs[date_num].get_attribute('href')

            driver.close()
            driver.quit()
            
            if 'Top' in title_full:
                title = title_full[4:].split('\n')[0]
            else:
                title = title_full.split('\n')[0]
            
            with open('parsing_last_data.csv', 'a+', newline='') as file:
                file.write(f'{dates[date_num]}; {title} ;{ref}\n')
        else:
            driver.close()
            driver.quit()
    except:
        print('error')
        driver.close()
        driver.quit()
        pass

if __name__ == '__main__':
    while True:
        time.sleep(1)
        get_info()

'''

Not working correctly yet (task manager overwhelmed)

schedule.every(1).seconds.do(get_info)

while True:
    schedule.run_pending()
'''





