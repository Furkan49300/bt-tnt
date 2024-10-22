import requests
import json

def get_account_id(zoho_oauthtoken):
    url = "https://mail.zoho.com/api/accounts"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {zoho_oauthtoken}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        account_id = data['data'][0]['accountId']
        return account_id
    else:
        print("Something went wrong...", response.status_code)
        return None

def send_email(zoho_oauthtoken, account_id, from_address, to_address, cc_address, bcc_address, subject, content):
    url = f"https://mail.zoho.com/api/accounts/{account_id}/messages"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {zoho_oauthtoken}"
    }

    data = {
        "fromAddress": from_address,
        "toAddress": to_address,
        "ccAddress": cc_address,
        "bccAddress": bcc_address,
        "subject": subject,
        "content": content,
        "askReceipt" : "yes"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Something went wrong...", response.status_code)
