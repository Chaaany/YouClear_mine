from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)
driver.implicitly_wait(3)
driver.get('https://www.youtube.com/')

# css_selector 추천함
search_input = driver.find_element_by_name('search_query')
search_input.send_keys('쇼메이커') #검색 키우드 입력
search_input.send_keys(Keys.RETURN) #엔터키(입력)


search_keywords = driver.find_elements_by_css_selector('#video-title > yt-formatted-string')
for keyword in search_keywords:
    news_link = keyword.get_attribute('href')
    keyword_text = keyword.text
    # print(news_link)
    print(keyword_text)

# 파이썬 코드 실행을 멈춤
time.sleep(2)

driver.quit()
