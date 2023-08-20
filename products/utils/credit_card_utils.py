import requests
def credit_card_validator(cc_number):
    url = "https://card-validator.p.rapidapi.com/validate"

    payload = { "cardNumber": cc_number }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "3b7938379cmsh707de9295a7b94ep1c1e2djsn997737f0b6d6",
        "X-RapidAPI-Host": "card-validator.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('isValid') == True:
            print(result)
            return True     
        else:
            return False
    else:
        print("API request failed with status code:", response.status_code)

