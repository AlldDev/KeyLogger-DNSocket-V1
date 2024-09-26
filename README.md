# Keylogger com Exfiltração via Servidor DNS
- **Authores:** @AlldDev, @Pmirandadev
- **Orientadores:** @bcmarini

![KeyloggerV1](https://github.com/AlldDev/KeyLogger-DNSocket-V1/blob/main/others/img/Keylogger.png)

## Projeto de Demonstração de Riscos em Cibersegurança
Este projeto é um exemplo educacional que demonstra a implementação de um keylogger que utiliza consultas DNS para exfiltrar dados capturados de um sistema alvo. **O objetivo deste projeto é puramente educativo** e visa conscientizar sobre os riscos de segurança cibernética relacionados à exfiltração de dados por canais discretos.

## 🚨 Aviso
Este código destina-se exclusivamente para fins educacionais. O uso deste projeto para atividades maliciosas ou ilegais é estritamente proibido. O propósito aqui é expor vulnerabilidades para que administradores e desenvolvedores possam mitigar tais riscos.

## 📋 Funcionalidades
- Captura de teclas digitadas no sistema alvo.
- Exfiltração de dados capturados por meio de consultas DNS.
- Comunicação discreta entre o sistema alvo e o servidor de controle via DNS.

## 🛠️ Tecnologias Utilizadas
- **Python**: Linguagem usada para a implementação do keylogger.
- **`dnslib`**: Biblioteca usada para manipular e enviar consultas DNS.
- **`pynput`**: Captura dos eventos de teclado para envio.

## 📦 Instalação

1. Clone o repositório:
```bash
https://github.com/AlldDev/KeyLogger-DNSocket-V1.git
```
2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

3. Configure um servidor DNS para monitorar e receber as consultas contendo os dados exfiltrados.
```bash
python3 server-dns.py
```

## ⚙️ Uso
Execute o keylogger no sistema alvo:
```bash
python keylogger.py
```
O keylogger irá capturar as teclas e enviar os dados como consultas DNS para o servidor DNS configurado.

No lado do servidor, monitore as requisições DNS para obter os dados exfiltrados.

## 🔐 Considerações de Segurança
Este projeto tem como objetivo mostrar a vulnerabilidade de exfiltração de dados através de canais alternativos, como o DNS. Recomenda-se que administradores e profissionais de segurança utilizem este conhecimento para fortalecer defesas de rede, implementando filtros de DNS e monitoramento de tráfego anômalo.

## ⚖️ Legalidade
Certifique-se de seguir todas as leis aplicáveis ao usar, modificar ou distribuir este código. Este projeto não deve ser utilizado para atividades mal-intencionadas e só deve ser aplicado em ambientes de teste e auditoria controlados.

## 📄 Licença
Distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
