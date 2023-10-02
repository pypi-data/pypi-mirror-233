import digikey
import digikey.configfile
import digikey.v3.productinformation
from digikey.v3.productinformation import KeywordSearchRequest

digikey_handler = digikey.DigikeyAPI(digikey.configfile.DigikeyJsonConfig('test_digikey.json'), is_sandbox=True)

client_id, client_secret = None, None
if digikey_handler.needs_client_id():
    client_id = input('Please enter your Digikey Client ID: ')
if digikey_handler.needs_client_secret():
    client_secret = input('Please enter your Digikey Secret ID: ')
digikey_handler.set_client_info(client_id=client_id, client_secret=client_secret)


# lookup = digikey.v3.productinformation.ProductDetails(digi_key_part_number='RMCF0805JT1K00CT-ND')
# res = digikey_handler.product_details(body=lookup)
# print(res)

# search_request = KeywordSearchRequest(keywords='CRCW080510K0FKEA', record_count=10)
# result = digikey_handler.keyword_search(body=search_request)
# print(result)


result = digikey_handler.product_details('RMCF0805JT1K00CT')
print(result)
print(result.limited_taxonomy)
