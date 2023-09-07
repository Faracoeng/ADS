import subprocess, sys
import utils

# try:
#     client_hostname = sys.argv[1] # pc3
#     router = sys.argv[2] #router1
#     imn_id = sys.argv[3]
#     dest_ip = sys.argv[4] #10.0.2.20 pc4

# except:
#     print("Necessário inserir os dados referente a simulação (hostname, router_name, imn_id e dest_ip)")
#     quit()



#### TODO O código a seguir só funciona para o cenário incluído em ads-cenario.imn
class Node:
    """
    Classe que representa um Nodo do cenário.

    Attributes:
        name (str): O nome do nodo.
        interfaces (dict): Um dicionário de interfaces associadas ao nodo, 
        onde as chaves são os nomes das interfaces e os valores são os IPs associados a cada interface.
    """

    def __init__(self, node_name, interfaces: dict):
        self.name = node_name
        self.interfaces = interfaces
        self.links_associados = {}
class Link:
    def __init__(self, node_1: Node, node_2: Node, if_node_1: str, if_node_2: str):
        self.node_1 = node_1
        self.node_2 = node_2
        if if_node_1 in self.node_1.interfaces and if_node_2 in self.node_2.interfaces:
            self.name = f"{self.node_1.name}:{self.node_2.name}"
        else:
            ValueError("Não foi possível criar o link")

pc1 = Node(f"pc1", {"eth0":"10.0.1.20"})
pc2 = Node(f"pc2", {"eth0":"10.0.2.20"})
pc3 = Node(f"pc3", {"eth0":"10.0.3.20"})
pc4 = Node(f"pc4", {"eth0":"10.0.4.20"})

router1 = Node("router1", {"eth0":f"10.0.0.1", "eth1":f"10.0.1.1", "eth2":f"10.0.3.1"})
router2 = Node("router2", {"eth0":f"10.0.0.2", "eth1":f"10.0.2.1"," eth2":f"10.0.4.1"})

link_routers = Link(router1, router2, "eth0", "eth0")

alg = ['cubic', 'reno']
BER = ['100000', '10000000']

column_names = ['timestamp','ip_fonte','porta_fonte', 'ip_destino', 'porta_destino', 'protocolo', 'intervalo_tempo_medição', 'id_transferencia', 'taxa_transferencia_bps']

## Servidor
# sudo himage pc4@i4a11 iperf -s -y C >> server-data.csv
#cmd_iperf_server = f"sudo himage {server_hostname}@{imn_id} iperf -s -y C"


# FIXME Alterei os comandos para utilizar nova estrutura de Node e Link acima.
# Também inclui o código em uma função para ser chamado do manager

def executa_experimento(imn_id: str):
    for proto in alg:
        for ber in BER:
                
            #cmd_vlink = f"sudo vlink -B {ber} -d 10000 {hostname}:{router}@{imn_id}"
            #cmd_vlink = f"sudo vlink -B {ber} -d 10000 {client_hostname}:{router}@{imn_id}"
            print(link_routers.name)
            cmd_vlink = f"sudo vlink -B {ber} -d 10000 {link_routers.name}@{imn_id}"

            #vlink: conexão virtual entre hosts ou roteadores simulados.
            #-B 100000: Define o valor do BER (Bit Error Rate, taxa de erro de bits).
            #-d 10000: Define o atraso (delay) da conexão para 10000 
            # pc3:router1@i4901: Formato para definir a conexão entre dois nós (host ou roteador) simulados. 
            # pc3 é o nome do primeiro nó, router1 é o nome do segundo nó e i4901 é o ID da simulação.

            print("--cmd_vlink--")
            #print(cmd_vlink)
            #subprocess.run(cmd_vlink, shell=True)
            vlink_process = subprocess.Popen(cmd_vlink, shell=True)
            vlink_process.wait()  # Aguarda a conclusão do processo
        
            output_file = f"dados-{proto}-BER{ber}.csv"
            with open(output_file, 'w') as file:
                file.write('\t'.join(column_names) + '\n')
            output_file = f"dados-{proto}-BER{ber}.csv"

            #-c 10.0.4.20: Especifica o endereço IP de destino para o qual a conexão será estabelecida.
            #-b 1G: Define a taxa de transferência alvo para 1 Gigabit por segundo. 
            #-y C: Define o formato de saída do teste como formato CSV.
            #-Z cubic: Define o algoritmo de controle de congestionamento a ser usado durante o teste. 
            # cmd_iperf_client = f"sudo himage {client_hostname}@{imn_id} iperf -c {dest_ip} -b 1G -y C -Z {proto}"
            cmd_iperf_server = f"sudo himage {pc2.name}@{imn_id} iperf -s -Z {proto} -t 10 -y -e C"
            
            print("--cmd_iperf_servidor--")
            print(cmd_iperf_server)
            #subprocess.run(cmd_iperf_client, shell=True)
            iperf_process_server = subprocess.Popen(cmd_iperf_server, shell=True, stdout=subprocess.PIPE)

            with open(output_file, 'a') as file:
                for line in iperf_process_server.stdout:
                    file.write(line.decode())  # Decodifica bytes para string e escreve no arquivo

            iperf_process_server.wait()  # Aguarda a conclusão do processo

            cmd_iperf_client = f"sudo himage {pc1.name}@{imn_id} iperf -c {pc2.interfaces['eth0']} -t 10 -y C -Z {proto}"
            #teste_ping = f"sudo himage {hostname}@{imn_id} ping {dest_ip} >> {output_file}"
            print("--cmd_iperf_client--")
            print(cmd_iperf_client)
            #subprocess.run(cmd_iperf_client, shell=True)
            iperf_process_client = subprocess.Popen(cmd_iperf_client, shell=True, stdout=subprocess.PIPE)

            with open(output_file, 'a') as file:
                for line in iperf_process_client.stdout:
                    file.write(line.decode())  # Decodifica bytes para string e escreve no arquivo

            iperf_process_client.wait()  # Aguarda a conclusão do processo

