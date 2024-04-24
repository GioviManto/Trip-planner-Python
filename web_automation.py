import sys
print(sys.path)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import requests
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from babel.dates import format_date, parse_date
from dateutil import parser
from selenium import webdriver    


def convert_to_italian_date(english_date, format='dd MMMM yyyy', locale='it_IT'):
    try:
        # Parsing of the English date with a common format
        date_object = datetime.strptime(english_date, '%d %B %Y')
    except ValueError:
        print("Unable to interpret the date:", english_date)
        return None

    # Getting the Italian translation of the weekday
    weekday_mapping = {
        'sunday': 'domenica',
        'monday': 'lunedì',
        'tuesday': 'martedì',
        'wednesday': 'mercoledì',
        'thursday': 'giovedì',
        'friday': 'venerdì',
        'saturday': 'sabato'
    }
    weekday = date_object.strftime('%A').lower()
    translate = weekday_mapping.get(weekday, weekday)

    # Formatting the date in Italian with the month in lowercase
    formatted_date = format_date(date_object, format=format, locale=locale)
    month_in_lowercase = date_object.strftime('%B').lower()
    formatted_date = formatted_date.replace(date_object.strftime('%B'), month_in_lowercase)

    # Creating the result string with Italian weekday
    result = f"{translate} {formatted_date}"
    return result

def convert_to_italian_date_b(english_date, format='dd MMMM yyyy', locale='it_IT'):
    try:
        # Parsing of the English date with a common format
        date_object = datetime.strptime(english_date, '%d %B %Y')
    except ValueError:
        print("Unable to interpret the date:", english_date)
        return None

    # Formatting the date in Italian with the month in lowercase
    formatted_date = format_date(date_object, format=format, locale=locale)
    month_in_lowercase = date_object.strftime('%B').lower()
    formatted_date = formatted_date.replace(date_object.strftime('%B'), month_in_lowercase)

    return formatted_date

def months_difference(date_string):
    current_date = datetime.now()
    date = parser.parse(date_string, dayfirst=True)
    time_difference = date - current_date
    months_difference = time_difference.days // 30
    return months_difference



def days_difference(data_str1, data_str2):
    # Converte le stringhe di data in oggetti datetime
    data1 = datetime.strptime(data_str1, '%d %B %Y')
    data2 = datetime.strptime(data_str2, '%d %B %Y')

    # Calcola la differenza tra le due date
    differenza = data2 - data1

    # Estrae il numero di giorni come risultato intero
    giorni_diff = -differenza.days

    return giorni_diff


############################################################################################################



def flights(departure_date, return_date, destination, origin, budget_input, guests_num):

    try:   

        guests_number=int(guests_num)
        departure_date_it = convert_to_italian_date(departure_date)
        return_date_it = convert_to_italian_date(return_date)
        # create a new instance of the Firefox driver

        driver = webdriver.Firefox()

        # navigate to the website
        driver.get('https://www.momondo.it/')
        driver.implicitly_wait(20)
        def eliminate_cookie():
            try:
                cookie=driver.find_element(By.CSS_SELECTOR,'[class="Py0r Py0r-mod-variant-solid Py0r-mod-theme-none Py0r-mod-shape-default Py0r-mod-size-xxxsmall"]') 
                cookie.click()
            except:
                pass
        eliminate_cookie()
        driver.implicitly_wait(5)
        #close google banner
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="Finestra di dialogo Accedi con Google"]')))
        driver.switch_to.frame(iframe)
        time.sleep(2)
        try:
            banner_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Chiudi"]')))
            banner_button.click()
        except Exception as e:
            pass
        driver.switch_to.default_content()
        driver.implicitly_wait(5)
        # input origin
        clear_origin = driver.find_element(By.CSS_SELECTOR,'[class="vvTc-item-button"]')
        clear_origin.click()
        select_origin= driver.find_element(By.CSS_SELECTOR,'[aria-label="Seleziona origine"]')
        select_origin.click()
        select_origin.send_keys(origin)
        driver.implicitly_wait(5)
        origin_xpath=driver.find_element(By.XPATH,'//*[@class="JyN0-item JyN0-pres-item-mcfly"]')
        origin_xpath.click()
        # input destination
        driver.implicitly_wait(5)
        destination_field= driver.find_element(By.CSS_SELECTOR,'[aria-label="Destinazione volo"]')
        destination_field.send_keys(destination)
        destination_xpath=driver.find_element(By.XPATH, '//*[@class="JyN0-item JyN0-pres-item-mcfly"]')
        destination_xpath.click()
        driver.implicitly_wait(5)
        # input number of passengers
        if guests_number > 1:
            prova= driver.find_element(By.CSS_SELECTOR,'[class="S9tW-chevron"]')
            prova.click()
            driver.implicitly_wait(3)
            for i in range(guests_number - 1):
                driver.find_element(By.CSS_SELECTOR,'button[aria-label="Aumenta"]').click()
        # input departure date
        dep_date_field = driver.find_element(By.CSS_SELECTOR,'[class="sR_k-prefixIcon"]')
        dep_date_field.click()
        try:
            previous_month = driver.find_element(By.CSS_SELECTOR,'[aria-label="Mese precedente"]')
            previous_month.click()
            driver.implicitly_wait(5)
        except:
            pass
        try:
            find_date_d= driver.find_element(By.CSS_SELECTOR,f"[aria-label='{departure_date_it}']")
        except:
            next_month=driver.find_element(By.CSS_SELECTOR,'[aria-label="Prossimo mese"]')
            n_month_d = months_difference(departure_date)
            for x in range(n_month_d):
                next_month.click()
            driver.implicitly_wait(5)
            find_date_d= driver.find_element(By.CSS_SELECTOR,f"[aria-label='{departure_date_it}']")
        finally:
            find_date_d.click()
            
        driver.implicitly_wait(5)
        # input return date
        try:
            find_date_r= driver.find_element(By.CSS_SELECTOR, f"[aria-label='{return_date_it}']")
        except:
            next_month=driver.find_element(By.CSS_SELECTOR,'[aria-label="Prossimo mese"]')
            n_month_d = months_difference(departure_date)
            n_month_r = months_difference(return_date)
            n_month_diff = n_month_r - n_month_d
            for x in range(n_month_diff):
                next_month.click()
            find_date_r= driver.find_element(By.CSS_SELECTOR,f"[aria-label='{return_date_it}']")
        finally:
            find_date_r.click()
            search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Cerca"][type="submit"]')))
            search.click()
        
        
        eliminate_cookie()
        # all windows
        time.sleep(5)
        all_handles = driver.window_handles
        # last window
        new_window_handle = all_handles[-1]
        driver.switch_to.window(new_window_handle)
        driver.implicitly_wait(15) #problema
        # Change the URL
        current_url = driver.current_url
        driver.get(current_url+'&fs=price=-'+budget_input)
        time.sleep(5)
        '''driver.implicitly_wait(12)
        budget('&fs=price=-'+budget_input)
        time.sleep(5)'''
        eliminate_cookie()
        driver.implicitly_wait(3)
        # Find the offers
        offers = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="nrc6"]')))
        '''offers = driver.find_elements(By.CSS_SELECTOR, '[class="nrc6"]')'''
        # Print the links for the top 3 offers
        link_list=[]
        try:
            for i, offer in enumerate(offers[:3], start=1):
                driver.execute_script("arguments[0].scrollIntoView(true);", offer)
                time.sleep(3)
                link = driver.execute_script('return arguments[0].querySelector("[class=\'oVHK-fclink\']").getAttribute("href");', offer)
                link_str= f'Questo è il link {i}: https://www.momondo.it/{link}'
                link_list.append(link_str)
            return link_list
        except:
            print("There are no other available results with the entered preferences; modify them if you want to get the top three results for your flight.")
    except:
        print("We're sorry, but something went wrong with the flight booking. Please try restarting the program or change your preferences.")
    finally:
        driver.quit()


############################################################################################################
     
 
def hotels(budget_input_hotel, guests_num, departure_date, return_date, destination, n_days):
    try:    
        
        def budget_nightly():
            budget_hotel_nightly = int(budget_input_hotel)/n_days
            budget_final = int(budget_hotel_nightly)
            return str(budget_final)
        
        guests_number=int(guests_num)
        
        departure_date_it = convert_to_italian_date_b(departure_date)
        return_date_it = convert_to_italian_date_b(return_date)

        # create a new instance of the Google Chrome driver
        driver = webdriver.Firefox()
        driver.maximize_window()
        
        driver.get('https://www.booking.com/')
               
        iframe = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//iframe[@title="Finestra di dialogo Accedi con Google"]')))
        driver.switch_to.frame(iframe)
        time.sleep(2)
        try:
            banner_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Chiudi"]')))
            banner_button.click()
        except Exception as e:
            pass
        driver.switch_to.default_content()
        driver.implicitly_wait(5)        

        def eliminate_cookie():
            try:
                cookie=driver.find_element(By.CSS_SELECTOR,'#onetrust-reject-all-handler') 
                cookie.click()
            except:
                pass
        eliminate_cookie()

        driver.implicitly_wait(3) 
        
        def eliminate_login():
            try:
                login = driver.find_element(By.CSS_SELECTOR, '.f4552b6561 > span:nth-child(1) > span:nth-child(1) > svg:nth-child(1) > path:nth-child(1)')
                login.click()
            except:
                pass
        eliminate_login()    

        driver.implicitly_wait(3)
        destination_field= driver.find_element(By.CSS_SELECTOR,'[aria-label="Dove vuoi andare?"]')
        destination_field.send_keys(destination)
        time.sleep(2)
        destination_xpath=driver.find_element(By.XPATH, '//*[@id="autocomplete-result-0"]')
        destination_xpath.click()    
        driver.implicitly_wait(2)
          
        try:
            find_date_d = driver.find_element(By.CSS_SELECTOR,f"[aria-label='{departure_date_it}']")
        except:
            next_month=driver.find_element(By.CSS_SELECTOR,'.f4552b6561 > span:nth-child(1) > span:nth-child(1)')
            n_month_d = months_difference(departure_date)
            for x in range(n_month_d):
                next_month.click()
                
            find_date_d = driver.find_element(By.CSS_SELECTOR,f"[aria-label='{departure_date_it}']")
        finally:
            find_date_d.click()       
        
        try:
            find_date_r= driver.find_element(By.CSS_SELECTOR, f"[aria-label='{return_date_it}']")
        except:
            next_month=driver.find_element(By.CSS_SELECTOR,'button.ebbedaf8ac:nth-child(2)')
            n_month_d = months_difference(departure_date)
            n_month_r = months_difference(return_date)
            n_month_diff = n_month_r - n_month_d
            for x in range(n_month_diff):
                next_month.click()
            find_date_r= driver.find_element(By.CSS_SELECTOR,f"[aria-label='{return_date_it}']")
        finally:
            find_date_r.click()
        
        def click_search():
            search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.a4c1805887')))
            search.click()           
        def guests_botton_up():
            guests_botton_up = driver.find_element(By.CSS_SELECTOR,'div.a7a72174b8:nth-child(1) > div:nth-child(3) > button:nth-child(3)')
            guests_botton_up.click()
        
        guests_field = driver.find_element(By.CSS_SELECTOR,'button.ebbedaf8ac:nth-child(1)')
        guests_field.click()
        
        if guests_number == 2:
            time.sleep(2)
            click_search()
            
        elif guests_number == 1:
            guest_button_minus = driver.find_element(By.CSS_SELECTOR, 'button.bb803d8689:nth-child(1)')
            guest_button_minus.click()
            time.sleep(2)
            click_search()
        
        else:
            for i in range(guests_number - 2):
                guests_botton_up()
            time.sleep(2)
            click_search()
            
        time.sleep(4)
        eliminate_login()
          
        current_url = driver.current_url
        driver.get(current_url+'&nflt=price%3DEUR-min-'+budget_nightly()+'-1')
        driver.implicitly_wait(5)
    
        time.sleep(5)
        link_list=[]        

        selectors = [
            'div.c82435a4b8:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)',
            'div.c82435a4b8:nth-child(10) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)',
            'div.c82435a4b8:nth-child(12) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)',
        ]

        # Ciclo for per estrarre e stampare i link
        try:
            for i, selector in enumerate(selectors, start=1):
                link_element = driver.find_element(By.CSS_SELECTOR, selector)
                link = link_element.get_attribute("href")
                link_str= f'Questo è il link {i}: {link}'
                link_list.append(link_str)
            return link_list

        except IndexError:
            print("There are no available results with the entered preferences.")

    except:
        print("We're sorry, but something went wrong with the hotel reservation. Please try restarting the program or change your preferences.")
    finally:
        driver.quit()


###########################################################################################################

def activities(destination,n_days):
    driver = webdriver.Firefox()
    def get_text_from_html(html_content):
        html_content = driver.page_source  
        soup = BeautifulSoup(html_content, 'html.parser')

            # Trova l'elemento div con la classe specifica
        div_elements = soup.findAll('div', class_='XfVdV o AIbhI')
        texts = []
        for div_element in div_elements:
        # Trova tutti gli elementi span con la classe specifica all'interno dell'elemento div
            span_elements = div_element.find_all('span', class_='vAUKO')
        # Ottieni il testo dai primi 3 elementi span o da tutti gli elementi disponibili
            span_texts = [span.text.strip() for span in span_elements]
        # Aggiungi il testo dell'elemento div alla lista solo se ci sono elementi span
            if span_texts:
                texts.append([div_element.text.strip()])
        return texts

    def click_element_by_css_selector(driver, css_selector):
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            element.click()

    def get_html():
        
        html_content = driver.page_source
        return html_content

    url = 'https://www.tripadvisor.it/'

    # Imposta il tempo di attesa implicito a 5 secondi
    driver.implicitly_wait(5)

    # Accedi al sito TripAdvisor
    driver.get(url)

    # Accetta i cookie
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        ).click()
    except Exception as e:
        pass

    # Esegui la ricerca
    try:
        input_ricerca = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )
        input_ricerca.send_keys(destination)
    except Exception as e:
        pass

    try:
        elemento_chiudi = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'TvD9Pc-Bz112c'))
        )
        elemento_chiudi.click()
        
    except Exception as e:
        pass

    # Clicca sull'elemento "Cose da fare"
    try:
        elemento_cose_da_fare = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="GzJDZ w z _S _F Wc Wh Q B- _G"]'))
        )
        elemento_cose_da_fare.click()
        
    except Exception as e:
        pass

    try:
        elemento_chiudi = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'TvD9Pc-Bz112c'))
        )
        elemento_chiudi.click()
        
    except Exception as e:
        pass

    try:
        elemento_categorie = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.rmyCe._G.B-.z._S.c.Wc.wSSLS.jWkoZ.QHaGY'))
        )
        elemento_categorie.click()
    except Exception as e:
        pass

    window_handles = driver.window_handles
    new_window_handle = window_handles[-1]
    driver.switch_to.window(new_window_handle)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
        ).click()
    except Exception as e:
        pass

    def click_element_by_class(driver, class_name):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'div.{class_name}'))
            )
            element.click()
            print(f"Clicked element with class name: {class_name}")
        except Exception:
            print('uywfduwfed')


    x=get_html()
    culture=get_text_from_html(x)

    click_element_by_css_selector(driver,"#filter-navbar > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > a:nth-child(1) > div:nth-child(1)"
    )
    time.sleep(10)
    y=get_html()
    while y==x:
        y=get_html()

    new_window_handle = window_handles[-1]
    driver.switch_to.window(new_window_handle)
    food=get_text_from_html(y)
    click_element_by_css_selector(driver,"div.XDHza:nth-child(9) > a:nth-child(1) > div:nth-child(1)")
    time.sleep(10)
    z=get_html()
    while z==y:
        z=get_html()
    new_window_handle = window_handles[-1]
    driver.switch_to.window(new_window_handle)
    shopping=get_text_from_html(z)
    click_element_by_css_selector(driver,'.Dgygn > div:nth-child(1)')
    time.sleep(10)
    k=get_html()
    while k==z:
        k=get_html()
    new_window_handle = window_handles[-1]
    driver.switch_to.window(new_window_handle)
    tour=get_text_from_html(k)


    b=[culture,food,shopping,tour]
    r=['culture','food','shopping','tour']
    fin_list=[]
    weights={'culture':0.25,'food':0.25,'shopping':0.25,'tour':0.25}
    tot_activities=4*n_days

    for enne in b:
        for i in r:
            if len(enne)<(weights[i]*tot_activities):
                for x in random.sample(enne,round(weights[i]*tot_activities)):
                    fin_list.append(x)
            else:
                for x in enne:
                    fin_list.append(x)

    ultimate_list=random.sample(fin_list,len(fin_list))
    final=[]
    driver.quit()

    for i in range(0,n_days):
        a=[]
        for x in range(0,4):
            a.append(ultimate_list.pop(x))
        final.append(a)

    return final
