import requests
from global_variables import URL


def get_info(message):
    params = {'blah': message}
    print(message)
    r = requests.get(URL, params=params) 
    print(r.text)
    if r.status_code == 200:
        return r.text
    return '404'