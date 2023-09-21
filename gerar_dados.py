import utils
import threading, time, os

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

# Fatores
fatores = {}
fatores['alg'] = ['cubic', 'reno']
fatores['ber'] = ['100000', '1000000']
fatores['bg'] = ['400m', '800m']


num_rep = 4 # FIXME configurar número de repetições
time_tx = 5 # TODO verificar se o tempo será 60s
t_sleep = 2 # tempo para aguardar entre threads
i_report = 5

# FIXME Alterei os comandos para utilizar nova estrutura de Node e Link acima.
# Também inclui o código em uma função para ser chamado do manager

def executa_experimento(imn_id: str):
    utils.create_file('resultados/cli-data.csv')
    utils.create_file('resultados/srv-data.csv')
    for rep in range(num_rep):
        for proto in fatores['alg']:
            for ber in fatores['ber']:
                for trafego_udp in fatores['bg']:
                
                    # Comandos iperf/imunes 
                    cmd_vlink = f"sudo vlink -B {ber} {link_routers.name}@{imn_id}"
                    cmd_srv_bg = f"sudo himage {pc4.name}@{imn_id} iperf -s -u -t {time_tx + (4*t_sleep)}"
                    cmd_cli_bg = f"sudo himage {pc3.name}@{imn_id} iperf -c {pc4.interfaces['eth0']} -u -t {time_tx + (3*t_sleep)} -b {trafego_udp}"
                    # cmd_srv_tcp = f"sudo himage {pc2}@{imn_id} iperf -s -e -y C -Z {proto} -t {time_tx} >> srv-data.csv"
                    # cmd_cli_tcp = f"sudo himage {pc1}@{imn_id} iperf -y -e -y C -c {pc2.interfaces['eth0']} -t {time_tx} -Z {proto} >> cli-data.csv"

                    cmd_srv_tcp = f"sudo himage {pc2.name}@{imn_id} iperf -s -e -y C -Z {proto} -t {time_tx + (2*t_sleep)}"
                    cmd_cli_tcp = f"sudo himage {pc1.name}@{imn_id} iperf -c {pc2.interfaces['eth0']} -e -y C -t {time_tx + (1*t_sleep)} -Z {proto} "
                    
                    tag_experimento = f"{proto}-{ber}-{trafego_udp}"
                    comandos = {
                        'vlink': cmd_vlink,
                        'srv-udp': cmd_srv_bg,
                        'cli-udp': cmd_cli_bg,
                        'srv-tcp': cmd_srv_tcp, 
                        'cli-tcp': cmd_cli_tcp
                    }

                    # Criar uma thread para cada comando e iniciar a execução com um atraso de 1 segundo
                    threads = []
                    resultados = {}
                    utils.logger.info(f"Iniciando experimento => repetição:{rep} - tag:{tag_experimento}")
                    try:
                        for key,cmd in comandos.items():
                            thread = threading.Thread(target=utils.executa_comando, args=(cmd, resultados, key))
                            threads.append(thread)
                            thread.start()
                            time.sleep(t_sleep)  # tempo para servidores estarem disponíveis

                        # Esperar todas as threads terminarem
                        for thread in threads:
                            thread.join()
                    except Exception as e:
                        utils.logger.error(e)
                    
                    utils.logger.info(f"Experimento Finalizado")
                    # print(resultados['srv'])
                    utils.escreve_resultado(tag_experimento, resultados)                
                    time.sleep(5)
                    os.system("reset")

