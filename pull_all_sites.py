from pull_single_site import get_bags_from_site
import json
def pull_all_sites():
    # Shopify stores
            # https://www.baggu.com/collections/reusable-bags
            # https://totebagfactory.com/collections/wholesale-tote-bags
    f = open('sites.json')
 
    # returns JSON object as 
    # a dictionary
    sites = json.load(f)
    f.close()
    total_number_of_bags = 0
    total_number_of_sites = 0
    for site in sites:
        try:
            bags = get_bags_from_site(sites[site])
            bag_output = open("outputs/"+site+".json", "w")
            bag_output.write(json.dumps(bags))
            total_number_of_bags += len(bags)
            total_number_of_sites += 1
            bag_output.close()
            
        except Exception as e:
            print("Couldn't pull", site, e)
    print("Total number of bags", total_number_of_bags, "from", total_number_of_sites, "sites")
pull_all_sites()


# "www.baggu.com": {

#         "list_url": "https://www.baggu.com/collections/reusable-bags",
#         "list_qs": {
    
#             "item": ".collection__style-view>div",
#             "link": "a"
#         },
#         "item_qs": {
#             "title": ".pt-2.text-left.text-42.font-medium.leading-none.tracking-tighter.antialiased.800:pt-0",
#             "description": [
#                 "#product-details"
#             ],
#             "image": ".grid.w-full.grid-cols-2 img"
#         }
#     },