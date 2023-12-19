from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

def get_bag_links_from_site(driver, site):
    
    bag_links = []
    paginator_next = 0
    if "list_qs" in site and "paginator_next" in site["list_qs"]:
        paginator_next = site["list_qs"]["paginator_next"]

    next_url = site["list_url"]
    while next_url is not None:
        try:
            driver.get(next_url)
            
            bags = driver.find_elements(By.CSS_SELECTOR, site["list_qs"]["item"])

            

            for bag in bags:
                bag_link = bag.find_element(By.CSS_SELECTOR, site["list_qs"]["link"])
                bag_links.append(bag_link.get_attribute("href"))

                # get bag details
                # save bag details
            next_url = None
            if paginator_next != 0 and paginator_next is not None:
                paginator_next_element = driver.find_element(By.CSS_SELECTOR, paginator_next)
                if paginator_next_element is not None:
                    
                    if paginator_next_element.tag_name.lower() == "a":
                        next_url = paginator_next_element.get_attribute("href")
                    else:
                        url_inside = paginator_next_element.find_element(By.CSS_SELECTOR, "a")
                        if url_inside is not None:
                            next_url = url_inside.get_attribute("href")
        except Exception as e:
            next_url = None
        
            
        
    return bag_links

def get_bag_details(driver, bag_link, settings):
    driver.get(bag_link)
    bag = {}
    for key in settings["item_qs"]:
        try:
            if key == "title":
                bag[key] = driver.find_element(By.CSS_SELECTOR, settings["item_qs"][key]).text
            elif key == "price":
                bag[key] = driver.find_element(By.CSS_SELECTOR, settings["item_qs"][key]).text
            elif key == "description":
                if type(settings["item_qs"][key]) == list:
                    bag[key] = ""
                    for selector in settings["item_qs"][key]:
                        bag[key] += driver.find_element(By.CSS_SELECTOR, selector).get_attribute('innerHTML')
                else:
                    bag[key] = driver.find_element(By.CSS_SELECTOR, settings["item_qs"][key][0]).get_attribute('innerHTML')
            elif key == "image":
                bag[key] = driver.find_element(By.CSS_SELECTOR, settings["item_qs"][key]).get_attribute("src")
        except Exception as e:
            exit()
            bag[key] = ""
    return bag

def pull_shopify(list_url):
    bags = []
    page = 1
    while True:
        try:
            x = requests.get(list_url+"/products.json?page="+str(page), headers={
                "Content-Type": "application/json"
            })
            if x.status_code == 200:
                products = x.json()["products"]
                for bag in products:
                    bags.append({
                        "title": bag["title"],
                        "price": bag["variants"][0]["price"],
                        "description": bag["body_html"],
                        "image": bag["images"][0]["src"] if "image" in bag and len(bag["images"]) > 0 else None
                    })
                if len(products) == 0:
                    return bags
                print("page = ", page, len(products))
                page += 1
            else:
                return bags
        except Exception as e:
            return bags
    return bags

def get_bags_from_site(settings):
    
    list_url = settings["list_url"]
    x = requests.get(list_url+".json", headers={
        "Content-Type": "application/json"
    })
    if x.status_code == 200:
        return pull_shopify(list_url)
    else:
        driver = webdriver.Chrome()
        bag_links = get_bag_links_from_site(driver, settings)
        bags = []
        for bag_link in bag_links:
            try:
                bag = get_bag_details(driver, bag_link, settings)
                bags.append(bag)
            except Exception as e:
                print("Couldn't get bag details", e)
        driver.close()
        return bags


