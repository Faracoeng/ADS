import subprocess, sys

try:
    client_hostname = sys.argv[1] # pc3
    router = sys.argv[2] #router1
    imn_id = sys.argv[3]
    dest_ip = sys.argv[4] #10.0.2.20 pc4

except:
    print("Necessário inserir os dados referente a simulação (hostname, router_name, imn_id e dest_ip)")
    quit()

alg = ['cubic', 'reno']
BER = ['100000', '10000000']

column_names = ['timestamp','ip_fonte','porta_fonte', 'ip_destino', 'porta_destino', 'protocolo', 'intervalo_tempo_medição', 'id_transferencia', 'taxa_transferencia_bps']

## Servidor
# sudo himage pc4@i4a11 iperf -s -y C >> server-data.csv
#cmd_iperf_server = f"sudo himage {server_hostname}@{imn_id} iperf -s -y C"



for proto in alg:
    for ber in BER:
            
        #cmd_vlink = f"sudo vlink -B {ber} -d 10000 {hostname}:{router}@{imn_id}"
        cmd_vlink = f"sudo vlink -B {ber} -d 10000 {client_hostname}:{router}@{imn_id}"
        #vlink: conexão virtual entre hosts ou roteadores simulados.
        #-B 100000: Define o valor do BER (Bit Error Rate, taxa de erro de bits).
        #-d 10000: Define o atraso (delay) da conexão para 10000 
        # pc3:router1@i4901: Formato para definir a conexão entre dois nós (host ou roteador) simulados. 
        # pc3 é o nome do primeiro nó, router1 é o nome do segundo nó e i4901 é o ID da simulação.

        print("--cmd_vlink--")
        print(cmd_vlink)
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
        cmd_iperf_client = f"sudo himage {client_hostname}@{imn_id} iperf -c {dest_ip} -b 1G -y C -Z {proto}"
        #teste_ping = f"sudo himage {hostname}@{imn_id} ping {dest_ip} >> {output_file}"
        print("--cmd_iperf_client--")
        print(cmd_iperf_client)
        #subprocess.run(cmd_iperf_client, shell=True)
        iperf_process = subprocess.Popen(cmd_iperf_client, shell=True, stdout=subprocess.PIPE)

        with open(output_file, 'a') as file:
            for line in iperf_process.stdout:
                file.write(line.decode())  # Decodifica bytes para string e escreve no arquivo

        iperf_process.wait()  # Aguarda a conclusão do processo
