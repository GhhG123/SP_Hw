import requests

def check_url(url):
    try:
        response = requests.head(url)
        if response.status_code < 400:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False
