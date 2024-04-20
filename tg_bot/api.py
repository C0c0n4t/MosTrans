import requests
from global_variables import URL


def get_info(message):
    params = {'blah': message}
    r = requests.get(URL, params=params) 
    if r.status_code == 200:
        return r.text
    return '404'