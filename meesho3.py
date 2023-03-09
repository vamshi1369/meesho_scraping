import time
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(ChromeDriverManager().install())
main_web = driver.get("https://www.meesho.com/women-kurtis/pl/3j0")
driver.maximize_window()
time.sleep(10)

count = 0
SCROLL_PAUSE_TIME = 4

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")



#scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;") # get the screen height of the web
i = 2
while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 2
    count += 1
    time.sleep(SCROLL_PAUSE_TIME)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if count == 30:
        break
#     if (screen_height) * i > scroll_height:
#         break

page_source = driver.page_source

p_urls = []
soup = BeautifulSoup(page_source, 'lxml')
urls = soup.find_all('div', class_=["sc-pyfCe ProductList__GridCol-sc-8lnc8o-0", "eqLVZD", "FGMeB"])
for url in urls:
    ur = "https://www.meesho.com" + url.a['href']
    print(ur)
    p_urls.append(ur)
print(len(p_urls))

Product_t = []
Product_p = []
Product_ra = []
Product_re = []
Seller_n = []
Seller_ra = []
Seller_f = []
Seller_pro = []

def scrape_urls(p_url):
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    for url in p_url:
        time.sleep(3)
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        
        try:
            title = soup.find('title').text.strip()            
        except:
            title = "NA"
        
        try:
            price = soup.find('h4', class_=["sc-gswNZR", "hZkDgi"]).text.strip()
        except:
            price = "NA"
            
        rating = soup.find('span', class_=["ShippingInfo__RatingsRow-sc-frp12n-2", "edtAlz"])
        try:
            rat = rating.find('span', class_=["sc-gswNZR", "ipmWxf"]).text.strip()
        except:
            rat = "NA"
            
        review = soup.find("span", class_=["ShippingInfo__RatingsRow-sc-frp12n-2", "edtAlz"])
        try:
            rev = review.find_all('span')[-2].text.split(',')[1].strip()            
        except:
            rev = "NA"
            
        seller = soup.find('div', class_=["sc-jSUZER bOYugM", "ShopCardstyled__ShopCardWrapper-sc-du9pku-1", "kbhhA-d", "ShopCardstyled__ShopCardWrapper-sc-du9pku-1", "kbhhA-d"])
        try:
            sel_name = seller.find('span', class_=["sc-gswNZR", "cxYErM", "ShopCardstyled__ShopName-sc-du9pku-6", "bdcHGu", "ShopCardstyled__ShopName-sc-du9pku-6", "bdcHGu"]).text.strip()
        except:
            sel_name = "NA"
            
        seller_info = soup.find('div', class_=["sc-jSUZER bOYugM", "ShopCardstyled__ShopCardWrapper-sc-du9pku-1", "kbhhA-d", "ShopCardstyled__ShopCardWrapper-sc-du9pku-1", "kbhhA-d"])
        if seller_info is not None:


            sel_inf = seller_info.find('div', class_=["sc-jSUZER ewsmjv", "ShopCardstyled__BottomSection-sc-du9pku-5", "hPfDac", "ShopCardstyled__BottomSection-sc-du9pku-5", "hPfDac"])
            try:
                sel_rat = sel_inf.find_all('div')[0].text.strip()
            except:
                sel_rat = "NA"
                
            try:
                sel_follow = sel_inf.find_all('div')[-2].text.strip()
            except:
                sel_follow = "NA"
                
            try:
                sel_prod = sel_inf.find_all('div')[-1].text.strip()
                
            except:
                sel_prod = "NA"

        else:
            sel_rat = "NA"
            sel_follow = "NA"
            sel_prod = "NA"
            
        
        Product_t.append(title)
        Product_p.append(price)
        Product_ra.append(rat)
        Product_re.append(rev)
        Seller_n.append(sel_name)
        Seller_ra.append(sel_rat)
        Seller_f.append(sel_follow)
        Seller_pro.append(sel_prod)
    return title, price, rat, rev, sel_name, sel_rat, sel_follow, sel_prod


scrape_urls(p_urls)


df = pd.DataFrame(list(zip(Product_t, Product_p, Product_ra, Product_re, Seller_n, Seller_ra, Seller_f, Seller_pro)), 
             columns=['Product Title', 'Product Price', 'Product Rating', 'Product Reviews', 'Seller Name', 'Seller Rating', 'Seller Followers', 'Seller Products'])

df.to_csv('meesho3.csv', index=False)