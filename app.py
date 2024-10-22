import base64
import tempfile
import os
import requests
import re
from flask import Flask, request, jsonify
from lxml import etree
from datetime import date, datetime
from zoho_crm_contact_address_update import verify_address_with_google, update_contact_in_zoho
from createAndPrintShipment import make_pickup_request, build_soap_request_expedition_from_client_to_dentalhitec, build_soap_request_expedition_from_dentalhitec_to_client, invoke_soap_request, extract_base64_zpl_from_response, convert_base64_to_zpl, send_file_to_printer
from send_email import send_email, get_account_id

app = Flask(__name__)

# TNT service url
SERVICE_URL = "https://www.tnt.fr/service/?wsdl"

# Fonction pour remplacer les caractères spéciaux
def normalize_string(value):
    if value:
        value = value.replace('œ', 'oe').replace('é', 'e').replace('ê', 'e').replace('è', 'e').replace('ô', 'o').replace('à', 'a')
        value = value.replace('&', 'et')  # Remplacer & par "et"
        value = re.sub(r'[^\w\s\-]', '', value)  # Supprimer tout autre caractère spécial sauf les lettres, chiffres, espaces et tirets
        return value.strip()  # Supprimer les espaces en début et fing
    return value

# Fonction pour formater le numéro de téléphone
def format_phone_number(phone_number):
    return re.sub(r'[^0-9+]', '', phone_number)  # Supprimer tout sauf les chiffres et le signe +

@app.route('/create_and_print_shipment', methods=['POST'])
def create_and_print_shipment():
    try:
        # Récupérer les données JSON de la requête
        data = request.json
        print("Received POST request with data:", data)  # Log les données reçues
        
        if not data:
            raise ValueError("No data received in the request.")
        
        # Normaliser les champs importants
        company_name = normalize_string(data.get('company_name'))
        shipper_address = data.get('shipper_address', {})
        shipper_street1 = normalize_string(shipper_address.get('street1'))
        shipper_street2 = normalize_string(shipper_address.get('street2'))
        shipper_city = normalize_string(shipper_address.get('city'))
        shipper_zip = shipper_address.get('zip')  # Le code postal ne nécessite pas de normalisation
        shipper_phone_number = format_phone_number(shipper_address.get('phone'))

        receipt_name = normalize_string(data.get('receipt_name'))
        receipt_billing_address = data.get('receipt_billing_address', {})
        receipt_street1 = normalize_string(receipt_billing_address.get('street1'))
        receipt_street2 = normalize_string(receipt_billing_address.get('street2'))
        receipt_city = normalize_string(receipt_billing_address.get('city'))
        receipt_zip = receipt_billing_address.get('zip')

        shipping_date = data.get('shipping_date')
        zebra_api_key = data.get('zebra_api_key')
        zebra_tenant = data.get('zebra_tenant')
        printer_serial_number = data.get('printer_serial_number')
        user_name = normalize_string(data.get('user_name'))
        user_email = data.get('user_email')
        tnt_account_number = data.get('tnt_account_number')
        tnt_account_password = data.get('tnt_account_password')
        tnt_account_username = data.get('tnt_account_username')

        print(f"Processing shipment for user {user_name} ({user_email})")

        # Validate that important fields are not missing
        if not all([company_name, shipper_street1, shipper_city, shipper_zip, receipt_name, receipt_street1]):
            raise ValueError("Some required fields are missing.")

        # Vérification de la date d'expédition
        if not shipping_date or datetime.strptime(shipping_date, "%Y-%m-%d").date() < date.today():
            shipping_date = date.today().strftime("%Y-%m-%d")
        print(f"Final shipping date: {shipping_date}")

        # Créer la requête SOAP
        soap_request = build_soap_request_expedition_from_dentalhitec_to_client(
            tnt_account_number, tnt_account_username, tnt_account_password, company_name,
            shipper_street1, shipper_street2, shipper_zip, shipper_city,
            shipper_phone_number, receipt_name, receipt_street1, receipt_street2,
            receipt_zip, receipt_city, shipping_date
        )
        print("SOAP request created successfully.")

        # Envoyer la requête SOAP
        headers = {
            'Content-Type': 'text/xml;charset=UTF-8'
        }
        soap_response = invoke_soap_request(SERVICE_URL, soap_request, headers)
        print("SOAP response received.")

        # Extraire et convertir le ZPL
        base64_zpl = extract_base64_zpl_from_response(soap_response)
        zpl_string, error = convert_base64_to_zpl(base64_zpl)

        if error:
            print(f"Error converting base64 to ZPL: {error}")
            return jsonify({"error": error}), 500
        
        print("ZPL string successfully generated.")

        # Envoyer le fichier à l'imprimante
        success, response = send_file_to_printer(zebra_api_key, zebra_tenant, printer_serial_number, zpl_string)
        
        if success:
            print("Label sent to printer successfully.")
            return jsonify({"message": "Shipment created and label sent to printer successfully."}), 200
        else:
            print(f"Error sending to printer: {response}")
            return jsonify({"error": response}), 500

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Welcome to the TNT Shipment Service"

if __name__ == '__main__':
    app.run(debug=True)
