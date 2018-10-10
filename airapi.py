import requests as rq
import logging as lg

unsafe_chars = ['&','?', '=']
auth = []
meta = []
strs = [
    'http://air.radiotime.com/Playing.ashx?partnerId=',
    '&partnerKey=',
    '&id=',
    '&title=',
    '&artist=',
    '&album=',
    '&commercial=true'
]

lg.basicConfig(level=lg.INFO)

def login(partner_id, partner_key, station_id):
    """authenticate the module"""
    if len(auth) == 0:
        auth.append(partner_id)
        auth.append(partner_key)
        auth.append(station_id)

def _parseResponce(x):
    list = x.split('\n')
    status = ''
    fault = ''
    for i in list:
        i = i.replace('\t', '').replace('\r', '')
        if 'fault' in i:
            fault = i.replace('<fault>', '').replace('</fault>', '')
        if 'status' in i:
            status = i.replace('<status>', '').replace('</status>', '')

    if '200' in status:
        return 200
    else:
        lg.error(f'Server responded with: {status} - {fault}')
        return f'{status}:{fault}'

def push(title, artist, album='null', comm=False):
    error = False
    for char in unsafe_chars:
        if char in title+artist+album:
            error = True
            lg.error('Invalid character')


    if len(auth) == 3 and error == False:
            payload = str(
            strs[0] + auth[0] +
            strs[1] + auth[1] +
            strs[2] + auth[2] +
            strs[3] + title +
            strs[4] + artist
            )
            if album != 'null': payload += str(strs[5] + album)
            if comm: payload += str(strs[6])

            try:
                r = rq.get(payload)
                responce = _parseResponce__(r.text)
                if responce == 200:
                    lg.info(f'Song updated to: {title} - {artist}')
            except:
                lg.error('Could not reach server')

    else: raise Exception('AIRAPI: Current session not authenticated')
