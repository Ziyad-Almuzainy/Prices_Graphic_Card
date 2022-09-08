# Import Libraries

from selenium import webdriver
from bs4 import BeautifulSoup 
from datetime import datetime
import csv
    
    
    
def get_url(search_term):
    '''Generate a url from search term'''
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')
    
    # Data Term Query to Url
    url = template.format(search_term)
    
    # Add page Query Placeholder
    url += '&page{}'
    
    
    return url

def extract_record(item):
    '''Extract & Return Data from a Single Record'''
    
    # Description & Url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    try:
        # Price & Date
        price = item.find('span',{'class' :'a-offscreen'}).text
        Price_date = datetime.today().strftime('%Y-%m-%d')
    except AttributeError:
        return
    
    
    try:
        # Rating & Reviwe
        rating = item.i.text
        review = item.find('span', {'class': 'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = ''
        review = ''
    
    result = (description, price,Price_date, rating, review)
    
    return result

def main(search_term):
    '''Run main Program Routine'''
    # startup the webdriver
    driver = webdriver.Firefox(executable_path = '/Users/ziyadalhaarbi/Documents/my project/Amazo Scrap/geckodriver')                               
    record = []   
    url = get_url(search_term)
    
    
    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div',{'data-component-type': 's-search-result'})
        
        
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
                               
    driver.close()
    
    # Save Data to csv file
    with open("/Users/ziyadalhaarbi/Documents/my project/Amazo Scrap/PricesData.csv", "w") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(['Description','Price', 'PricetDate', 'Rating', 'Review'])
        wr.writerows(records)


main('Graphics Card')