import requests

import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def verify_address_with_google(address, google_api_key):
    GOOGLE_API_URL = "https://addressvalidation.googleapis.com/v1:validateAddress"

    if address["Mailing_Country"].lower() == "france":
        address["Mailing_Country"] = "FR"
    
    # Prepare the request payload
    payload = {
        "address": {
            "revision": 0,
            "regionCode":address["Mailing_Country"],
            "postalCode": address['Mailing_Zip'],
            "locality": address['Mailing_City'],
            "addressLines": [
                address['Mailing_Street']
            ],
            "recipients": [],
            "organization": ""
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Make the request to Google's Address Validation API
    response = requests.post(GOOGLE_API_URL, headers=headers, params={'key': google_api_key}, json=payload)
    print("Google API response:", response.text)
    
    if response.status_code == 200:
        result = response.json()
        if 'result' in result and 'address' in result['result']:
            address = result['result']['address']
            postal_address = address.get('postalAddress', {})
            
            verified_address = {
                'Mailing_Street': postal_address.get('addressLines', [''])[0],
                'Mailing_City': postal_address.get('locality', ''),
                'Mailing_Zip': postal_address.get('postalCode', ''),
                'Mailing_Country': postal_address.get('regionCode', '')
            }
            return verified_address
    return address  # Return the original address if validation fails


def update_contact_in_zoho(contact_id, verified_address, zoho_token):
    ZOHO_API_URL = f"https://www.zohoapis.com/crm/v6/Contacts/{contact_id}"
    headers = {
        'Authorization': f'Zoho-oauthtoken {zoho_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "data": [
            {
                "Contacts - ID Contact": contact_id,
                "Contacts - Addresse Complète": verified_address
            }
        ]
    }
    response = requests.patch(ZOHO_API_URL, json=payload, headers=headers)
    return response.json()

