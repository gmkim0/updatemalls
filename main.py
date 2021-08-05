from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import telegram
import time
import re

# 한섬몰 : http://www.thehandsome.com/ko/
brand_dict = {'TIME' : 'http://www.thehandsome.com/ko/b/br01',
              'OBZEE' : 'http://www.thehandsome.com/ko/b/br43',
              'MINE' : 'http://www.thehandsome.com/ko/b/br02',
              'LATT' : 'http://www.thehandsome.com/ko/b/br31',
              'LANVIN' : 'http://www.thehandsome.com/ko/b/br19',
              "O'2ND" : 'http://www.thehandsome.com/ko/b/br45',
              'SYSTEM' : 'http://www.thehandsome.com/ko/b/br03',
              'SJSJ' : 'http://www.thehandsome.com/ko/b/br04',
              'THECASHMERE' : 'http://www.thehandsome.com/ko/b/br08',
              'CLUBMONACO' : 'http://www.thehandsome.com/ko/b/br44',
              'TIMEHOMME' : 'http://www.thehandsome.com/ko/b/br06',
              'SYSTEMHOMME' : 'http://www.thehandsome.com/ko/b/br07',
              }

# re
r = re.compile('onclick=\'GA_Event\("브랜드_메인","상품_NEW","(.*?)"\)')

# 크롬 드라이버
driver_path = r'C:\Users\gm960\Desktop\chromedriver_win32\chromedriver'
driver = webdriver.Chrome(driver_path)

# Telegram : token
my_token = '1914798109:AAEk4OpTryyRr7CXD_n6C4LHT3lsAPiGCxI'
bot = telegram.Bot(token=my_token)
chat_id = '1928940395'

if __name__ == '__main__':
    for 브랜드명, url in brand_dict.items():
        globals()['last_{}'.format(브랜드명)] = ''
    s = 0
    while True:
        for 브랜드명, url in brand_dict.items():
            print(브랜드명, "update 확인 시작!")
            driver.get(url=url)
            time.sleep(2)
            body = driver.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_DOWN)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            globals()['new_{}'.format(브랜드명)] = str(soup.find('div', {'class': 'bx-viewport'}))
            globals()['new_{}'.format(브랜드명)] = globals()['new_{}'.format(브랜드명)].split("</li><li>")[0]
            globals()['new_{}'.format(브랜드명)] = r.search(globals()['new_{}'.format(브랜드명)]).group(1)
            # 이전 저장된 내역과 다르면 봇에 메세지 전송
            if globals()['last_{}'.format(브랜드명)] != globals()['new_{}'.format(브랜드명)]:
                a = globals()['last_{}'.format(브랜드명)]
                globals()['last_{}'.format(브랜드명)] = globals()['new_{}'.format(브랜드명)]
                if s == 0:
                    continue
                bot.sendMessage(chat_id, "[업데이트 알림]{} \n {}".format(브랜드명, url,)
                print(브랜드명, "결과 : update 되었습니다!", "상품명 : {} -> {}".format(a, globals()['new_{}'.format(브랜드명)]))
            else:
                print(브랜드명, "결과 : update 되지 않았습니다.")
            time.sleep(2)
        time.sleep(60) # 60초 간격으로 체크
        s += 1