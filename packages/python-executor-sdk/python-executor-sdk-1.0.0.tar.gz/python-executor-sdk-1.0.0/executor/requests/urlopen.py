import ssl, certifi
from urllib.request import Request, urlopen

def get(url, headers=None, **kwargs):
    context = ssl.create_default_context(cafile=certifi.where())
    context.set_ciphers('DEFAULT@SECLEVEL=1')
    request = Request(url, headers=headers, unverifiable=True, **kwargs)
    response = urlopen(request, timeout=10, context=context)