import requests
from idvpackage.constants import *
from idvpackage.ocr_utils import fuzzy_match_fields

class Ekyc:

    def __init__(self):
        self.maps_endpoint = GOOGLE_MAPS_API_ENDPOINT
        self.api_key = API_KEY

    def address_verification(self, address):
        endpoint = self.maps_endpoint
        
        params = {
            "address": address,
            "key": self.api_key,
        }

        try:
            response = requests.get(endpoint, params=params)
            data = response.json()
            if response.status_code == 200:
                if data['status'] == 'OK':
                    for result in data['results']:
                        for address_type in result['types']:
    #                         print(result['types'])
    #                         if address_type in ['street_address', 'subpremise', 'premise']:
    #                             return "Residential", result['formatted_address'], result['types']
                            if address_type in ['food', 'restaurant', 'lodging', 'business', 'general_contractor', 'hair_care', 'health', 'spa']:
                                return True, "Commercial"
                            
                        return True, "Residential"
                    return False, "Unknown"
                else:
                    return False, None
            else:
                return False, None
        
        except Exception as e:
            return False, None
        
    def address_validation(user_input_address, utility_bill_address, address_from_other_source):
        res1 = fuzzy_match_fields(user_input_address, address_from_other_source)
        res2 = fuzzy_match_fields(user_input_address, utility_bill_address)

        if res1 or res2:
            return True
        else:
            return False
    
