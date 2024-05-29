import json
import requests
from datetime import datetime

def refreshToken():
    def citeste_configurare(file_path):
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    config = citeste_configurare('config.json')
    appData = config['dateFirma']

    def refresh_token(client_id, client_secret, refresh_token, config_file_path):
        token_url = 'https://logincert.anaf.ro/anaf-oauth2/v1/token'
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post(token_url, data=payload)
        
        if response.status_code == 200:
            new_token_data = response.json()
            new_token = new_token_data['access_token']
            new_refresh_token = new_token_data['refresh_token']
            save_tokens_to_config(new_token, new_refresh_token, config_file_path)
            return new_token, new_refresh_token
        else:
            print("Nu s-a putut actualiza token-ul.")
            return None, None

    def save_tokens_to_config(new_token, new_refresh_token, config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
        
        config_data["dateFirma"]["header"] = f"Bearer {new_token}"
        config_data["dateFirma"]["refresh_token"] = new_refresh_token
        config_data["dateFirma"]["data_token"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(config_file_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

    # Exemplu de folosire:
    client_id = appData['client_id']
    client_secret = appData['client_secret']
    refresh_token_value = appData['refresh_token_value']

    config_file_path = 'config.json'

    new_token, new_refresh_token = refresh_token(client_id, client_secret, refresh_token_value, config_file_path)
    if new_token:
        print("Token-ul nou:", new_token)
        print("Refresh token-ul nou:", new_refresh_token)
    print("a rulat REFRESH TOKEN")
# refreshToken()