import base64
import tempfile
import os
import requests
from flask import Flask, request, jsonify
from lxml import etree
from datetime import date, datetime
from zoho_crm_contact_address_update import verify_address_with_google, update_contact_in_zoho
from createAndPrintShipment import make_pickup_request, build_soap_request_expedition_from_client_to_dentalhitec, build_soap_request_expedition_from_dentalhitec_to_client, invoke_soap_request, extract_base64_zpl_from_response, convert_base64_to_zpl, send_file_to_printer
from send_email import send_email, get_account_id

app = Flask(__name__)

# TNT service url
SERVICE_URL = "https://www.tnt.fr/service/?wsdl"

@app.route('/create_and_print_shipment', methods=['POST'])
def create_and_print_shipment():
    data = request.json
    company_name = data['company_name']
    shipper_address = data['shipper_address']
    shipper_street1 = shipper_address['street1']
    shipper_street2 = shipper_address['street2']
    shipper_city = shipper_address['city']
    shipper_zip = shipper_address['zip']
    shipper_phone_number = shipper_address['phone']
    receipt_name = data['receipt_name']
    receipt_billing_address = data['receipt_billing_address']
    receipt_street1 = receipt_billing_address['street1']
    receipt_street2 = receipt_billing_address['street2']
    receipt_city = receipt_billing_address['city']
    receipt_zip = receipt_billing_address['zip']
    shipping_date = data['shipping_date']
    zebra_api_key = data['zebra_api_key']
    zebra_tenant = data['zebra_tenant']
    printer_serial_number = data['printer_serial_number']
    user_name = data['user_name']
    user_email = data['user_email']
    tnt_account_number = data['tnt_account_number']
    tnt_account_password = data['tnt_account_password']
    tnt_account_username = data['tnt_account_username']

    receipt_name = receipt_name.replace('&', 'et')

    print("User name:", user_name);

    #print("Company Name:", company_name)
    #print("Shipper Address:")
    #print("  Street 1:", shipper_street1)
    #print("  Street 2:", shipper_street2)
    #print("  City:", shipper_city)
    #print("  Zip:", shipper_zip)
    #print("  Phone Number:", shipper_phone_number)
    #print("Receipt Name:", receipt_name)
    #print("Receipt Billing Address:")
    #print("  Street 1:", receipt_street1)
    #print("  Street 2:", receipt_street2)
    #print("  City:", receipt_city)
    #print("  Zip:", receipt_zip)
    #print("Shipping Date:", shipping_date)
    #print("Zebra API Key:", zebra_api_key)
    #print("Zebra Tenant:", zebra_tenant)
    #print("Printer Serial Number:", printer_serial_number)
    
    # If shipping_date is missing or outdated, set it to today's date
    if not shipping_date or datetime.strptime(shipping_date, "%Y-%m-%d").date() < date.today():
        shipping_date = date.today().strftime("%Y-%m-%d")

    #print("shipment date: ", shipping_date)

    soap_request = build_soap_request_expedition_from_dentalhitec_to_client(
        tnt_account_number, tnt_account_username, tnt_account_password, company_name,
        shipper_street1, shipper_street2, shipper_zip, shipper_city,
        shipper_phone_number, receipt_name, receipt_street1, receipt_street2,
        receipt_zip, receipt_city, shipping_date
    )
    #print("SOAP request", soap_request)
    headers = {
        'Content-Type': 'text/xml;charset=UTF-8'
    }

    #try:
    soap_response = invoke_soap_request(SERVICE_URL, soap_request, headers)
    #print("SOAP reponse", soap_response)
    base64_zpl = extract_base64_zpl_from_response(soap_response)
    #print("base64 zpl", base64_zpl)

    zpl_string, error = convert_base64_to_zpl(base64_zpl)
    if error:
        return jsonify({"error": error}), 500

    success, response = send_file_to_printer(zebra_api_key, zebra_tenant, printer_serial_number, zpl_string)
    if success:
        return jsonify({"message": "Shipment created and label sent to printer successfully."}), 200
    else:
        return jsonify({"error": response}), 500

    #except Exception as e:
     #   return jsonify({"error": str(e)}), 500

@app.route('/pickup_request', methods=['POST'])
def pickup_request():
    # Récupération des données envoyées en POST
    pickup_data = request.json

    # Récupérer les mots de passe depuis les en-têtes
    headers = request.headers
    tnt_account_number = "06301528"
    tnt_account_password = "N14GF4"
    tnt_account_username = "blanco.g@dentalhitec.com"

    # Stockage des données dans des variables individuelles
    first_name = pickup_data.get("first_name")
    last_name = pickup_data.get("last_name")
    street_address = pickup_data.get("street_address")
    address_line_2 = pickup_data.get("address_line_2")
    city = pickup_data.get("city")
    city = "GONDREVILLE"
    postal_code = pickup_data.get("postal_code")
    postal_code = "54840"
    country = pickup_data.get("country")
    email = pickup_data.get("email")
    time_added = pickup_data.get("time_added")

    print(first_name)

    # Informations d'expédition de l'entreprise (valeurs codées en dur)
    company_name = "Dentalhitec"
    company_street_address = "Rue de champ Blanc"
    company_address_line_2 = ""
    company_city = "Mazières-en-Mauges"
    company_postal_code = "49280"
    company_country = "France"
    company_email = "sargazi.h@dentalhitec.com"
    company_phone_number = "0241561616"
    
# Map the incoming data to the make_pickup_request function
    service_url = "https://www.tnt.fr/service/?wsdl"  # Replace with the actual service URL
    receiver_type = ""  # You need to determine this value
    shipping_date = "2024-08-28"  # You need to determine this value
    shipping_delay = "2"  # You need to determine this value
    notification_media = "EMAIL"  # You need to determine this value
    notification_email = email
    notify_success = "1"  # You need to determine this value
    labels_provided = "1"  # You need to determine this value
    sender_name = f"{first_name} {last_name}"
    sender_city = city
    sender_address1 = street_address
    sender_zip_code = postal_code
    sender_last_name = last_name  # Assuming the sender's last name is the same as the receiver's last name
    sender_first_name = first_name  # Assuming the sender's first name is the same as the receiver's first name
    sender_phone_number = company_phone_number
    sender_closing_time = "18:00"  # You need to determine this value
    receiver_name = company_name
    receiver_address1 = company_street_address
    receiver_zip_code = company_postal_code
    receiver_city_name = company_city
    receiver_contact_last_name = "dental"
    receiver_contact_first_name = "hitec"
    receiver_phone_number = company_phone_number  # You need to determine this value
    service_code = "..."  # You need to determine this value
    quantity = "1"  # You need to determine this value
    saturday_delivery = "0"  # You need to determine this value
    customer_reference = "..."  # You need to determine this value
    hazardous_material = "..."  # You need to determine this value

    # Call the make_pickup_request function with the mapped data
    pickup_response = make_pickup_request(
        account_username=tnt_account_username,
        account_password=tnt_account_password,
        service_url=service_url,
        account_number=tnt_account_number,
        receiver_type=receiver_type,
        shipping_date=shipping_date,
        shipping_delay=shipping_delay,
        notification_media=notification_media,
        notification_email=notification_email,
        notify_success=notify_success,
        labels_provided=labels_provided,
        sender_name=sender_name,
        sender_address1=sender_address1,
        sender_zip_code=sender_zip_code,
        sender_city=sender_city,
        sender_last_name=sender_last_name,
        sender_first_name=sender_first_name,
        sender_phone_number=sender_phone_number,
        sender_closing_time=sender_closing_time,
        receiver_name=receiver_name,
        receiver_address1=receiver_address1,
        receiver_zip_code=receiver_zip_code,
        receiver_city=receiver_city_name,
        receiver_contact_last_name=receiver_contact_last_name,
        receiver_contact_first_name=receiver_contact_first_name,
        receiver_phone_number=receiver_phone_number,
        service_code=service_code,
        quantity=quantity,
        saturday_delivery=saturday_delivery,
        customer_reference=customer_reference,
        hazardous_material=hazardous_material
    )

    print(pickup_response)
    
    return pickup_response

@app.route('/contact_address_field_update', methods=['POST'])
def handle_webhook():
    data = request.json
    address = data.get('address')
    google_api_key = data.get('google_api_key')
    
    # Verify the address with Google API
    verified_address = verify_address_with_google(address, google_api_key)

    print("verified_address:", verified_address)
    
    return jsonify(verified_address), 200
    
@app.route('/send-email', methods=['POST'])
def send_email_route():
    zoho_oauthtoken = request.form['zoho_oauthtoken']
    from_address = request.form['from_address']
    to_address = request.form['to_address']
    cc_address = request.form['cc_address']
    bcc_address = request.form['bcc_address']
    subject = request.form['subject']
    content = request.form['content']

    account_id = get_account_id(zoho_oauthtoken)
    if account_id:
        send_email(zoho_oauthtoken, account_id, from_address, to_address, cc_address, bcc_address, subject, content)
        return "Email sent successfully!"
    else:
        return "Something went wrong..."

@app.route('/')
def index():
    return "Welcome to the TNT Shipment Service"

if __name__ == '__main__':
    app.run(debug=True)
