import base64
import tempfile
import os
import requests
from lxml import etree

def clean_phone_number(phone_number):
    return phone_number.replace("+33", "0")

def build_soap_request_expedition_from_dentalhitec_to_client(account_number, account_username, account_password, company_name, 
                                                             shipper_street1, shipper_street2, shipper_zip, shipper_city, 
                                                             shipper_phone_number, receipt_name, receipt_street1, 
                                                             receipt_street2, receipt_zip, receipt_city, shipping_date):
    # Clean the phone number
    shipper_phone_number = clean_phone_number(shipper_phone_number)
    
    return f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.ws.app.tnt.fr/">
        <soapenv:Header>
            <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                <wsse:UsernameToken>
                    <wsse:Username>{account_username}</wsse:Username>
                    <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{account_password}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </soapenv:Header>
        <soapenv:Body>
            <cxf:expeditionCreation>
                <parameters>
                    <shippingDate>{shipping_date}</shippingDate>
                    <accountNumber>{account_number}</accountNumber>
                    <sender>
                        <type>ENTERPRISE</type>
                        <name>{company_name}</name>
                        <address1>{shipper_street1}</address1>
                        <address2>{shipper_street2}</address2>
                        <zipCode>{shipper_zip}</zipCode>
                        <city>{shipper_city}</city>
                        <phoneNumber>{shipper_phone_number}</phoneNumber>
                    </sender>
                    <receiver>
                        <type>ENTERPRISE</type>
                        <name>{receipt_name}</name>
                        <address1>{receipt_street1}</address1>
                        <address2>{receipt_street2}</address2>
                        <zipCode>{receipt_zip}</zipCode>
                        <city>{receipt_city}</city>
                        <contactFirstName></contactFirstName>
                        <contactLastName></contactLastName>
                        <sendNotification>1</sendNotification>
                    </receiver>
                    <serviceCode>J</serviceCode>
                    <saturdayDelivery>0</saturdayDelivery>
                    <quantity>1</quantity>
                    <parcelsRequest>
                        <parcelRequest>
                            <customerReference>CUST-REF-1</customerReference>
                            <sequenceNumber>1</sequenceNumber>
                            <weight>1.5</weight>
                        </parcelRequest>
                    </parcelsRequest>
                    <labelFormat>ZPL</labelFormat>
                </parameters>
            </cxf:expeditionCreation>
        </soapenv:Body>
    </soapenv:Envelope>
    """
# def build_soap_request_expedition_from_dentalhitec_to_client_with_pickup_request(account_number, account_username, account_password, company_name, 
#                                                              shipper_street1, shipper_street2, shipper_zip, shipper_city, 
#                                                              shipper_phone_number, receipt_name, receipt_street1, 
#                                                              receipt_street2, receipt_zip, receipt_city, shipping_date):
#     # Clean the phone number
#     shipper_phone_number = clean_phone_number(shipper_phone_number)
    
#     return f"""
#     <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.ws.app.tnt.fr/">
#         <soapenv:Header>
#             <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
#                 <wsse:UsernameToken>
#                     <wsse:Username>{account_username}</wsse:Username>
#                     <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{account_password}</wsse:Password>
#                 </wsse:UsernameToken>
#             </wsse:Security>
#         </soapenv:Header>
#         <soapenv:Body>
#             <cxf:expeditionCreation>
#                 <parameters>
#                     <shippingDate>{shipping_date}</shippingDate>
#                     <accountNumber>{account_number}</accountNumber>
#                     <sender>
#                         <type>ENTERPRISE</type>
#                         <name>{company_name}</name>
#                         <address1>{shipper_street1}</address1>
#                         <address2>{shipper_street2}</address2>
#                         <zipCode>{shipper_zip}</zipCode>
#                         <city>{shipper_city}</city>
#                         <phoneNumber>{shipper_phone_number}</phoneNumber>
#                     </sender>
#                     <receiver>
#                         <type>ENTERPRISE</type>
#                         <name>{receipt_name}</name>
#                         <address1>{receipt_street1}</address1>
#                         <address2>{receipt_street2}</address2>
#                         <zipCode>{receipt_zip}</zipCode>
#                         <city>{receipt_city}</city>
#                         <contactFirstName></contactFirstName>
#                         <contactLastName></contactLastName>
#                         <sendNotification>1</sendNotification>
#                     </receiver>
#                     <serviceCode>J</serviceCode>
#                     <saturdayDelivery>0</saturdayDelivery>
#                     <quantity>1</quantity>
#                     <parcelsRequest>
#                         <parcelRequest>
#                             <customerReference>CUST-REF-1</customerReference>
#                             <sequenceNumber>1</sequenceNumber>
#                             <weight>1.5</weight>
#                         </parcelRequest>
#                     </parcelsRequest>
#                     <labelFormat>ZPL</labelFormat>
#                 </parameters>
#             </cxf:expeditionCreation>
#         </soapenv:Body>
#     </soapenv:Envelope>
#     """
def build_soap_request_expedition_from_client_to_dentalhitec(account_number, account_username, account_password, company_name,
                                                             receipt_street1, receipt_street2, receipt_zip, receipt_city,
                                                             shipper_phone_number, shipper_street1, shipper_street2,
                                                             shipper_zip, shipper_city, shipping_date):
    # Call the other function with the parameters in the required order
    build_soap_request_expedition_from_dentalhitec_to_client(account_number, account_username, account_password, company_name,
                                                              shipper_street1, shipper_street2, shipper_zip, shipper_city,
                                                              shipper_phone_number, receipt_street1, receipt_street2,
                                                              receipt_zip, receipt_city, shipping_date)

def build_soap_request_pickup_request(
    account_username, account_password, shipping_date, account_number, notification_media, 
    notification_email, notify_success, labels_provided, sender_name, sender_address1, 
    sender_zip_code, sender_city, sender_last_name, sender_first_name, sender_phone_number, 
    sender_closing_time, receiver_type, receiver_name, receiver_address1, receiver_zip_code, 
    receiver_city, receiver_contact_last_name, receiver_contact_first_name, receiver_phone_number, 
    service_code, quantity, saturday_delivery, customer_reference, hazardous_material
):
    return f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.ws.app.tnt.fr/">
        <soapenv:Header>
            <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                <wsse:UsernameToken>
                    <wsse:Username>{account_username}</wsse:Username>
                    <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{account_password}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </soapenv:Header>
        <soapenv:Body>
            <cxf:pickUpRequestCreation>
                <parameters>
                    <shippingDate>{shipping_date}</shippingDate>
                    <accountNumber>{account_number}</accountNumber>
                    <notification>
                        <media>{notification_media}</media>
                        <emailAddress>{notification_email}</emailAddress>
                        <notifySuccess>{notify_success}</notifySuccess>
                    </notification>
                    <labelsProvided>{labels_provided}</labelsProvided>
                    <sender>
                        <name>{sender_name}</name>
                        <address1>{sender_address1}</address1>
                        <zipCode>{sender_zip_code}</zipCode>
                        <city>{sender_city}</city>
                        <lastName>{sender_last_name}</lastName>
                        <firstName>{sender_first_name}</firstName>
                        <phoneNumber>{sender_phone_number}</phoneNumber>
                        <closingTime>{sender_closing_time}</closingTime>
                    </sender>
                    <receiver>
                        <name>{receiver_name}</name>
                        <address1>{receiver_address1}</address1>
                        <zipCode>{receiver_zip_code}</zipCode>
                        <city>{receiver_city}</city>
                        <contactLastName>{receiver_contact_last_name}</contactLastName>
                        <contactFirstName>{receiver_contact_first_name}</contactFirstName>
                        <phoneNumber>{receiver_phone_number}</phoneNumber>
                    </receiver>
                    <serviceCode>{service_code}</serviceCode>
                    <quantity>{quantity}</quantity>
                </parameters>
            </cxf:pickUpRequestCreation>
        </soapenv:Body>
    </soapenv:Envelope>
    """



def invoke_soap_request(service_url, soap_request, headers):
    response = requests.post(service_url, data=soap_request, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
        
def extract_element_from_response(soap_response, xpath):
    try:
        # Parse the SOAP response
        root = etree.fromstring(soap_response)

        # Define namespaces
        namespaces = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            'ns1': 'http://cxf.ws.app.tnt.fr/'
        }

        # Extract element using the specified XPath
        elements = root.xpath(xpath, namespaces=namespaces)

        # Ensure we got a result
        if not elements:
            raise Exception(f"No element found at XPath '{xpath}' in the response")

        # Return the element
        return elements[0]

    except Exception as e:
        raise Exception(f"Error extracting element from SOAP response: {str(e)}")

def extract_base64_zpl_from_response(soap_response):
    xpath = '//ns1:expeditionCreationResponse//Expedition//PDFLabels/text()'
    return extract_element_from_response(soap_response, xpath)

def extract_tracking_url_from_response(soap_response):
    xpath = '//ns1:expeditionCreationResponse//Expedition//parcelResponses//trackingURL/text()'
    return extract_element_from_response(soap_response, xpath)

def make_pickup_request(account_username, account_password, service_url, account_number, receiver_type, shipping_date, 
                        shipping_delay, notification_media, notification_email, notify_success, 
                        labels_provided, sender_name, sender_address1, sender_zip_code, sender_city, 
                        sender_last_name, sender_first_name, sender_phone_number, sender_closing_time, 
                        receiver_name, receiver_address1, receiver_zip_code, receiver_city, 
                        receiver_contact_last_name, receiver_contact_first_name, receiver_phone_number, 
                        service_code, quantity, saturday_delivery, customer_reference, hazardous_material):

    # Step 1: Make the feasibility request to get the serviceCode
    feasibility_request = build_soap_feasibility_request(
        account_number=account_number,
        account_username=account_username, 
        account_password=account_password,
        receiver_zip=receiver_zip_code,
        receiver_city=receiver_city,
        receiver_type="",
        sender_zip=sender_zip_code,
        sender_city=sender_city,
        shipping_date="",
        shipping_delay=shipping_delay
    )
    print(feasibility_request)

    # Define headers for SOAP request
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    # Invoke the feasibility request
    feasibility_response = invoke_soap_request(service_url, feasibility_request, headers)
    
    # Extract serviceCode from the feasibility response (assuming it's in the response content)
    # Note: This step would require actual parsing logic depending on the structure of the SOAP response
    service_code = extract_service_code_from_response(feasibility_response)  # Placeholder function

    # Step 2: Build the pickup request SOAP envelope
    pickup_request = build_soap_request_pickup_request(
        account_username=account_username,
        account_password=account_password,
        shipping_date=shipping_date,
        account_number=account_number,
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
        receiver_type=receiver_type,
        receiver_name=receiver_name,
        receiver_address1=receiver_address1,
        receiver_zip_code=receiver_zip_code,
        receiver_city=receiver_city,
        receiver_contact_last_name=receiver_contact_last_name,
        receiver_contact_first_name=receiver_contact_first_name,
        receiver_phone_number=receiver_phone_number,
        service_code=service_code,
        quantity=quantity,
        saturday_delivery=saturday_delivery,
        customer_reference=customer_reference,
        hazardous_material=hazardous_material
    )

    print(pickup_request)

    # Step 3: Invoke the pickup request
    pickup_response = invoke_soap_request(service_url, pickup_request, headers)

    return pickup_response

# Placeholder function to simulate extraction of serviceCode from the feasibility response
def extract_service_code_from_response(feasibility_response):
    # chemin du service code
    xpath = '//ns1:feasibilityResponse//Service//serviceCode/text()'
    return extract_element_from_response(feasibility_response, xpath)


def convert_base64_to_zpl(base64_zpl):
    try:
        zpl = base64.b64decode(base64_zpl).decode('utf-8')
        return zpl, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def send_file_to_printer(api_key, tenant, printer_serial_number, zpl_string):
    try:
        url = 'https://api.zebra.com/v2/devices/printers/send'
        headers = {'apikey': api_key, 'tenant': tenant}
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_zpl_file:
            temp_zpl_file.write(zpl_string.encode('utf-8'))
            temp_zpl_file_path = temp_zpl_file.name
        with open(temp_zpl_file_path, 'rb') as file:
            files = {'zpl_file': file, 'sn': (None, printer_serial_number)}
            response = requests.post(url, headers=headers, files=files)
        os.remove(temp_zpl_file_path)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f'Failed to send file. Status code: {response.status_code}, Response: {response.text}'
    except Exception as e:
        return False, f"Error: {str(e)}"

def build_soap_feasibility_request(account_number, account_username, account_password, receiver_zip, receiver_city, receiver_type, sender_zip, sender_city, shipping_date, shipping_delay):
    # Validate that only one of shippingDate or shippingDelay is provided
    if (shipping_date and shipping_delay) or (not shipping_date and not shipping_delay):
        raise ValueError("You must provide either 'shippingDate' or 'shippingDelay', but not both.")
    
    # Create the base SOAP envelope
    envelope = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.ws.app.tnt.fr/">
        <soapenv:Header>
            <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                <wsse:UsernameToken>
                    <wsse:Username>{account_username}</wsse:Username>
                    <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{account_password}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </soapenv:Header>
       <soapenv:Body>
          <cxf:feasibility>
             <parameters>
                <accountNumber>{account_number}</accountNumber>
                <receiver>
                   <zipCode>{receiver_zip}</zipCode>
                   <city>{receiver_city}</city>
                </receiver>
                <sender>
                   <zipCode>{sender_zip}</zipCode>
                   <city>{sender_city}</city>
                </sender>"""
    
    # Add shippingDate or shippingDelay based on the provided parameters
    if shipping_date:
        envelope += f"""
                <shippingDate>{shipping_date}</shippingDate>"""
    elif shipping_delay:
        envelope += f"""
                <shippingDelay>{shipping_delay}</shippingDelay>"""

    # Close the SOAP envelope
    envelope += """
             </parameters>
          </cxf:feasibility>
       </soapenv:Body>
    </soapenv:Envelope>
    """
    
    return envelope.strip()
