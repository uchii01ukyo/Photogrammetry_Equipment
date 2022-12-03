import requests

def get_gip_addr():
    res = requests.get('https://ifconfig.me')
    return res.text

if __name__ == '__main__':
    print('your globalip: ' + get_gip_addr())