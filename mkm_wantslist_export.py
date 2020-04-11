from requests_oauthlib import OAuth1Session
import json
import xmltodict
import pandas as pd

#API KEYS
cardmarket_keys = json.load(open('application_keys.json'))['cardmarket']
app_token = cardmarket_keys['app_token']
app_secret = cardmarket_keys['app_secret']
access_token = cardmarket_keys['access_token']
access_token_secret = cardmarket_keys['access_secret']

#OBTAIN ALL WANTS LIST
print("Obtaining all wants list...")
base_url = 'https://api.cardmarket.com/ws/v2.0'
url = '{}/wantslist'.format(base_url)

oauth = OAuth1Session(app_token,
                       client_secret=app_secret,
                       resource_owner_key=access_token,
                       resource_owner_secret=access_token_secret,
                       realm=url
                      )

r = oauth.get(url)
wants_list = json.loads(json.dumps(xmltodict.parse(r.text)))
wants_list_ids = [a['idWantslist'] for a in wants_list['response']['wantslist']]

wantslist_list = []
for id_ in wants_list_ids :
    url = '{}/wantslist/{}'.format(base_url,id_)
    oauth = OAuth1Session(app_token,
                       client_secret=app_secret,
                       resource_owner_key=access_token,
                       resource_owner_secret=access_token_secret,
                       realm=url
                      )
    r = oauth.get(url)
    want_list = json.loads(json.dumps(xmltodict.parse(r.text)))
    wantslist_list.append(want_list['response']['wantslist'])
    
#OBTAIN ALL CARDS RECORD
print("Obtaining all cards record...")
cards = []
base_item_url = 'https://www.cardmarket.com'
for list_ in wantslist_list:
    for item in list_['item']:
        count = item['count']
        min_condition = item['minCondition']
        product_info = item['product']
        enName = product_info['enName']
        game_name = product_info['gameName']
        rarity = product_info['rarity']
        expansion = product_info['expansionName']
        id_prod = item['idProduct']
        website = base_item_url + product_info['website']
        cards.append((id_prod,enName,expansion,rarity,min_condition,count,website,game_name))

#EXPORT TO XLSX FILE
print("Exporting...")
columns = ['id','name','expansion','rarity','min_condition','count','link','game']
result = pd.DataFrame(cards,columns=columns)
result.drop_duplicates('id',inplace=True)
result.set_index('id',inplace=True)
result.to_excel('mkm_wants_list.xlsx')
print("Done")
