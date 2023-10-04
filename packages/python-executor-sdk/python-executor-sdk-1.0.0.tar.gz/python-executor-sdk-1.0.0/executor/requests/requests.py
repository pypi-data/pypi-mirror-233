import requests
from bs4 import BeautifulSoup as bs
from executor.utils.option import random_user_agents
def get(url, params=None, headers=None, **kwargs):
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS='ALL:@SECLEVEL=1'  # Fix [SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:997)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)  # Disable SSL error warning
    
    default_headers = {
        'User-Agent': random_user_agents()
    }
    
    if not headers:
        headers = default_headers
    else:
        for key, value in headers.items():
            default_headers[key] = value
        headers = default_headers
    if 'timeout' not in kwargs:
        timeout = 7
    
    if 'allow_redirects' not in kwargs :
        allow_redirects = False
    
    if 'verify' not in kwargs:
        verify = False
        
    return requests.get(url, params=params, headers=headers, timeout=timeout, allow_redirects=allow_redirects, verify=verify, **kwargs)
