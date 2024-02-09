import os
import configparser
import json
import requests
def upload_site(site, api_key):
    with open("outputs/"+site) as f:
        products = {
            "products": json.load(f)
        }
        requests.post("https://www.arbor.eco/api/v1/products", headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer "+api_key
        }, data=json.dumps(products))
        exit()
def upload_all():
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(config.sections())
    if "ARBOR" not in config:
        raise Exception("ARBOR section not found in config.ini")
    if "API_KEY" not in config["ARBOR"]:
        raise Exception("API_KEY not found in ARBOR section of config.ini")
    api_key = config["ARBOR"]["API_KEY"]
    # List files in outputs
    # For each file, upload to Arbor
    files = os.listdir("outputs")
    for file in files:
        upload_site(file, api_key)


# {
# "title" : string ,
# "description" : string ,
# "product_url" : url ,
# "image_url" : url ,
# "category" : string ,
# "weight" : decimal ,
# "showcase" : boolean ,
# "components" : [ Component ] ,
# "manufacturing" : Manufacturing ,
# "packaging" : [ Packaging ] ,
# "accessories" : [ Accessory ] ,
# "materials" : [ Material ] ,
# }
upload_all()