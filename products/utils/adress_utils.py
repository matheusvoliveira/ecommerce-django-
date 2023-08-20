import requests 
def cep_locater(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(url)

    if response.status_code == 200:
        adress_data = response.json()
        return adress_data
    else:
        return None
    