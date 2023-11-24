from pandas import read_csv, DataFrame
from scipy import stats
import utils, os
import matplotlib.pyplot as plt
from datetime import datetime
from gerar_dados import fatores
import argparse

column_names = ['tag','timestamp','ip_fonte','porta_fonte', 'ip_destino', 'porta_destino', 'protocolo', 'intervalo_medicao', 'id_tx', 'tx_bps']

# Função para importar dados de um arquivo CSV e retornar um DataFrame
def importar_dados(arquivo: str) -> DataFrame:
    dados = read_csv(arquivo, header=None, names=column_names)
    utils.logger.debug(dados)
    return dados

# Função para calcular intervalos de confiança para médias de dados agrupados por 'tag'
def calcular_intervalo(dados: DataFrame, confianca: str, campo: str = 'tx_bps') -> DataFrame:
    dados_agrupados = []
    for tag, group in dados.groupby('tag'):
        amostras = group[campo]

        # Calcula graus de liberdade, média e erro padrão
        graus_de_liberdade = len(amostras) - 1
        media = amostras.mean()
        erro_padrao = stats.sem(amostras)

        # Calcula o intervalo de confiança usando a distribuição t
        intervalo = stats.t.interval(confianca, graus_de_liberdade, loc=media, scale=erro_padrao)

        # Armazena os resultados em uma lista de dicionários
        dados_agrupados.append({
            'tag': tag,
            'media': media,
            'ic_min': intervalo[0],
            'ic_max': intervalo[1]
        })
    # Cria um DataFrame a partir dos dados agrupados
    frame_agrupado = DataFrame(dados_agrupados)
    return frame_agrupado

# Função para gerar gráficos a partir dos dados
def gerar_graficos(dados: DataFrame):
    # Divide as tags em prefixo e sufixo e identifica conjuntos duplicados pelo sufixo
    dados['prefixo'], dados['sufixo'] = zip(*dados['tag'].apply(separar_tag))
    conjuntos = dados[dados['sufixo'].duplicated(keep=False)]
    escalas = inserir_escalas()
    data_atual = datetime.now().strftime("%Y-%m-%d")

    for sufixo, grupo in conjuntos.groupby('sufixo'):
        mbps = 1e6  # 1 Mbps
        x_values = grupo['prefixo'].values
        y_values = grupo['media'].values
        l_values = grupo['tag'].values
        ic_min_values = grupo['ic_min'].values
        ic_max_values = grupo['ic_max'].values

        # Converte valores para Mbps
        ic_min_values /= mbps
        ic_max_values /= mbps
        y_values /= mbps

        # Define limites do eixo y para o gráfico
        y_max = max(y_values) + max(y_values) * escalas[sufixo]['max']
        y_min = min(y_values) - min(y_values) * escalas[sufixo]['min']
        y_err = [y_values - ic_min_values, ic_max_values - y_values]

        # Limpa o gráfico atual
        plt.clf()
        plt.ticklabel_format(axis='y', style='plain')

        plt.bar(x_values, y_values, label=l_values, color=['g', 'b'])    
        plt.errorbar(x_values, y_values, yerr=y_err, capsize=5, color='k', fmt='none', linewidth=2)

        # Define rótulos e título do gráfico
        plt.ylim(y_min, y_max)
        plt.xlabel('Cenário')
        plt.ylabel('Taxa média (Mbps)')
        plt.title('Comparação das médias por cenário')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        hora = datetime.now().hour
        # Cria diretório para salvar os gráficos, se não existir
        diretorio = f"graficos/{data_atual}-{hora}"
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        arquivo = f"{diretorio}/{sufixo}.png"
        plt.savefig(arquivo)

    utils.logger.info(f"Gráficos salvos em ./{diretorio}/")

# Função para separar uma tag em prefixo e sufixo
def separar_tag(tag):
    partes = tag.split('-', 1)
    prefixo = partes[0] if len(partes) > 0 else ''
    sufixo = partes[1] if len(partes) > 1 else ''
    return prefixo, sufixo

# Função para inserir escalas para diferentes conjuntos de dados
def inserir_escalas():
    escalas = {}
    # FIXME Verificar uma forma melhor de definir as escalas
    escalas[f"ber={fatores['ber'][0]}-udp={fatores['bg'][0]}"] = {'min':0.3, 'max':0.07}
    escalas[f"ber={fatores['ber'][0]}-udp={fatores['bg'][1]}"] = {'min':0.3, 'max':0.1}
    escalas[f"ber={fatores['ber'][1]}-udp={fatores['bg'][0]}"] = {'min':0.007, 'max':0.003}
    escalas[f"ber={fatores['ber'][1]}-udp={fatores['bg'][1]}"] = {'min':0.007, 'max':0.003}
    return escalas

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Processar dados de arquivo CSV e gerar gráficos.")
    parser.add_argument("-c", type=float, help="Valor de confiabilidade", default=0.99)
    parser.add_argument("arquivo_csv", help="Caminho para o arquivo CSV de entrada")
    args = parser.parse_args()

    arquivo_csv = args.arquivo_csv

    dados = importar_dados(arquivo_csv)
    resultado = calcular_intervalo(dados, confianca=args.c)
    utils.logger.info(f"\n{resultado}")
    
    gerar_graficos(resultado)
