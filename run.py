from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

import pandas as pd
import time
import datetime

import math



# Curret Week Number 
today = datetime.date.today()
Year, Week, day_of_week = today.isocalendar()


def Iranmood():
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
        driver.execute_script("window.scrollTo(200, document.body.scrollHeight);")
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

    pageN = pd.DataFrame(
    {'product': products,
    'oldPrice': oldPrice,
    'price':finalprice
    })

    fullList = fullList.append(pageN)


    fullList['DateT'] = today
    fullList['Shop'] = Shop
    fullList = fullList[['DateT','Shop','product','price']] #fullList[['DateT','Shop','product','oldPrice','finalprice']]

    #fullList.to_excel(f'{Shop}_{today}.xlsx')

    # Ready for insert to database
    # data = list(zip(*[fullList[c].values.tolist() for c in fullList]))

    # Close diver
    driver.close()
    return fullList


def Vegibazar():
    # Shop Name
    Shop = 'Vegibazar'

    #---------- make new driver ----------
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)


    #---------- Urls ----------
    urls=[
        'https://vegibazar.com/shop/%D9%84%D8%A8%D9%86%DB%8C%D8%A7%D8%AA-%DA%AF%DB%8C%D8%A7%D9%87%DB%8C',
        'https://vegibazar.com/shop/%D9%84%D8%A8%D9%86%DB%8C%D8%A7%D8%AA-%DA%AF%DB%8C%D8%A7%D9%87%DB%8C?page=2',
        'https://vegibazar.com/shop/%D9%84%D8%A8%D9%86%DB%8C%D8%A7%D8%AA-%DA%AF%DB%8C%D8%A7%D9%87%DB%8C?page=3',
        'https://vegibazar.com/shop/%D9%84%D8%A8%D9%86%DB%8C%D8%A7%D8%AA-%DA%AF%DB%8C%D8%A7%D9%87%DB%8C?page=4',
        'https://vegibazar.com/shop/%D9%BE%D8%B1%D9%88%D8%AA%D8%A6%DB%8C%D9%86-%DA%AF%DB%8C%D8%A7%D9%87%DB%8C',
        'https://vegibazar.com/shop/%D9%BE%D8%B1%D9%88%D8%AA%D8%A6%DB%8C%D9%86-%DA%AF%DB%8C%D8%A7%D9%87%DB%8C?page=2',
        'https://vegibazar.com/shop/%D9%BE%D8%B1%D9%88%D8%AA%D8%A6%DB%8C%D9%86-%DA%AF%DB%8C%D8%A7%D9%87%DB%8C?page=3',
        'https://vegibazar.com/shop/%D8%BA%D8%B0%D8%A7%D9%87%D8%A7%DB%8C-%D8%A2%D9%85%D8%A7%D8%AF%D9%87-%D9%88-%D9%86%DB%8C%D9%85%D9%87-%D8%A2%D9%85%D8%A7%D8%AF%D9%87',
        'https://vegibazar.com/shop/%D8%BA%D8%B0%D8%A7%D9%87%D8%A7%DB%8C-%D8%A2%D9%85%D8%A7%D8%AF%D9%87-%D9%88-%D9%86%DB%8C%D9%85%D9%87-%D8%A2%D9%85%D8%A7%D8%AF%D9%87?page=2',
        'https://vegibazar.com/shop/%D8%BA%D8%B0%D8%A7%D9%87%D8%A7%DB%8C-%D8%A2%D9%85%D8%A7%D8%AF%D9%87-%D9%88-%D9%86%DB%8C%D9%85%D9%87-%D8%A2%D9%85%D8%A7%D8%AF%D9%87?page=3',
        'https://vegibazar.com/shop/%D8%B3%D8%B3-%D9%87%D8%A7',
        'https://vegibazar.com/shop/%D8%B3%D8%B3-%D9%87%D8%A7?page=2',
        ]

    fullList = pd.DataFrame()



    for url in urls:

        #---------- Open page ----------
        driver.get(url)
        time.sleep(20)
        #---------- make empty array ----------

        products = []
        size = []
        price = []

        p = driver.find_elements_by_class_name("col-6.col-sm-4.col-xl-3.mb-15")


        for a in p:
            try : 
                locTitle = a.find_element_by_xpath("article//div[@class='store-product-image store-compact-product-image']//a")
                title = locTitle.get_attribute("title")
                products.append(title.strip())

                locSize = a.find_element_by_xpath("article//h4").text
                size.append(locSize)

                try : 
                    locPrice = a.find_element_by_xpath("article//span//span").text
                    price.append(int(''.join(filter(lambda x: x.isdigit(),locPrice))) * 10)
                    
                except:
                    price.append("ناموجود")
            except: 
                print('Products not locateable')


        pageN = pd.DataFrame(
        {'product': products,
        'size': size,
        'price':price
        })
        
        fullList = fullList.append(pageN)


    fullList['DateT'] = today
    fullList['Shop'] = Shop
    fullList =fullList[['DateT','Shop','product','price']]      ##fullList[['DateT','Shop','product','size','price']]
    #fullList.to_excel(f'{Shop}_{today}.xlsx')

    # Ready for insert to database
    # data = list(zip(*[fullList[c].values.tolist() for c in fullList]))

    # Close diver
    driver.close()
    return fullList




# Import map file 
Map = pd.read_excel('Map.xlsx')

# Concatenate 2 data 
Vegibazar = Vegibazar()
Iranmood = Iranmood()

fullList = pd.concat([Vegibazar, Iranmood], ignore_index=True)

fullList  = pd.merge(fullList,Map,how='left', on='product')

fullList = fullList[['DateT','Shop_x','product','sku','price']]

fullList.to_excel(f'{today}.xlsx')