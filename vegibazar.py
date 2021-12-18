from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import pandas as pd
import time
import datetime



# Curret Week Number
today = datetime.date.today()
Year, Week, day_of_week = today.isocalendar()

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
    print(len(p))

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
fullList = fullList[['DateT','Shop','product','size','price']]
print(fullList)
fullList.to_excel(f'{Shop}_{today}.xlsx')

# Ready for insert to database
# data = list(zip(*[fullList[c].values.tolist() for c in fullList]))

# Close diver
driver.close()

# Insert to database
# def main():
#     InsertPriceData(data)

# if __name__ == '__main__':
#     main()
