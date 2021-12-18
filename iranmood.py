from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

import pandas as pd
import time
import datetime

import math



# Curret Week Number 
today = datetime.date.today()
Year, Week, day_of_week = today.isocalendar()

# Shop Name 
Shop = 'iranmood'

#---------- make new driver ----------
chrome_options = webdriver.ChromeOptions()
prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications" : 2
        }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)


#---------- Urls ----------
url='https://www.iranmood.ir/search/index?ArrayBrand=37,315,342,351&moratabzai=2'


driver.get(url)


# Find how many items are exist
a = '/html/body/form/div[1]/div/div[4]/div[1]/span[2]/span[2]'
restItems =int(driver.find_element_by_xpath(a).text) 
print('Rest Of Items:',restItems)


def findItems():
    Items = driver.find_elements_by_xpath('/html/body/form/div[1]/div/div[4]/div[4]/*')
    lenItems = len(Items)  
    print('Found items:',lenItems)
    return lenItems ,  Items


foundItems,Items = findItems()
SCROLL_PAUSE_TIME = 5


while restItems > foundItems :
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(100, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Count new items
    foundItems , Items = findItems()
    
print('All products are found')  

fullList = pd.DataFrame()

products = []
oldPrice = []
finalprice = []

for a in Items :

    try: 
        Title = a.find_element_by_xpath("a//div[@class='description']").text
        products.append(Title.strip())
    except:
        Title = a.find_element_by_xpath("a//div[@class='description responsive']").text
        products.append(Title.strip())

    try : 
        locOldPrice = a.find_element_by_xpath("a//div[@class='size_bandi']//div[@class='old_price']//span[2]").text
        oldPrice.append(int(''.join(filter(lambda x: x.isdigit(),locOldPrice))) * 10)

        locFinalPrice = a.find_element_by_xpath("a//div[@class='size_bandi']//div[@class='price_product']//span[2]").text
        finalprice.append(int(''.join(filter(lambda x: x.isdigit(),locFinalPrice))) * 10)

    except:
        try : 
            locFinalPrice = a.find_element_by_xpath("a//div[@class='size_bandi']//div//span[2]").text
            finalprice.append(int(''.join(filter(lambda x: x.isdigit(),locFinalPrice))) * 10)
            oldPrice.append(int(''.join(filter(lambda x: x.isdigit(),locFinalPrice))) * 10)
        
        except:
            finalprice.append("ناموجود")
            oldPrice.append("ناموجود")


print(len(products))

pageN = pd.DataFrame(
{'product': products,
'oldPrice': oldPrice,
'finalprice':finalprice
})

fullList = fullList.append(pageN)


fullList['DateT'] = today
fullList['Shop'] = Shop
fullList = fullList[['DateT','Shop','product','oldPrice','finalprice']]
print(fullList)
fullList.to_excel(f'{Shop}_{today}.xlsx')

# Ready for insert to database
# data = list(zip(*[fullList[c].values.tolist() for c in fullList]))

# Close diver
driver.close()