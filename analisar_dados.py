from pandas import read_csv, DataFrame, options
import numpy as npy
from scipy import stats
import utils
import matplotlib.pyplot as plt

column_names = ['tag','timestamp','ip_fonte','porta_fonte', 'ip_destino', 'porta_destino', 'protocolo', 'intervalo_medicao', 'id_tx', 'tx_bps']
confianca = 0.99

def importar_dados(arquivo: str) -> DataFrame:

    dados = read_csv(arquivo, header=None, names=column_names)
    utils.logger.debug(dados)
    return dados

def calcular_intervalo(dados: DataFrame, campo: str = 'tx_bps') -> DataFrame:
    dados_agrupados = []
    for tag, group in dados.groupby('tag'):
        amostras = group[campo]

        graus_de_liberdade = len(amostras) - 1
        media = amostras.mean()
        erro_padrao = stats.sem(amostras)
        
        intervalo = stats.t.interval(confianca, graus_de_liberdade, loc=media, scale=erro_padrao)
        
        dados_agrupados.append({
            'tag': tag,
            'media': media,
            'ic_min': intervalo[0],
            'ic_max': intervalo[1]
        })
    frame_agrupado = DataFrame(dados_agrupados)
    return frame_agrupado

def gerar_graficos(dados: DataFrame):
    dados['prefixo'], dados['sufixo'] = zip(*dados['tag'].apply(separar_tag))
    conjuntos = dados[dados['sufixo'].duplicated(keep=False)]
    escalas = inserir_escalas()

    for sufixo, grupo in conjuntos.groupby('sufixo'):
        mbps = 1e6# 1 Mbps
        x_values = grupo['prefixo'].values
        y_values = grupo['media'].values
        l_values = grupo['tag'].values
        ic_min_values = grupo['ic_min'].values
        ic_max_values = grupo['ic_max'].values

        ic_min_values /= mbps
        ic_max_values /= mbps
        y_values /= mbps # transformando em Mbps
        
        y_max = max(y_values) + max(y_values)*escalas[sufixo]['max']
        y_min = min(y_values) - min(y_values)*escalas[sufixo]['min']

        plt.clf() # limpar plot
        plt.ticklabel_format(axis='y', style='plain')
        plt.bar(x_values, y_values, label=l_values, color=['g', 'b'])
        
        y_err=[y_values - ic_min_values, ic_max_values - y_values]
        plt.errorbar(x_values, y_values, yerr=y_err, capsize=5, color='k', fmt='none', linewidth=2)

        plt.ylim(y_min, y_max)
        plt.xlabel('Cenário')
        plt.ylabel('Taxa média (Mbps)')
        plt.title('Comparação das médias por cenário')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(f"graficos/grafico-{sufixo}.png")

def separar_tag(tag):
    partes = tag.split('-', 1)
    prefixo = partes[0] if len(partes) > 0 else ''
    sufixo = partes[1] if len(partes) > 1 else ''
    return prefixo, sufixo

def inserir_escalas():
    escalas = {}
    escalas['100000-400m'] = {'min':0.3, 'max':0.07}
    escalas['100000-800m'] = {'min':0.3, 'max':0.1}
    escalas['1000000-400m'] = {'min':0.007, 'max':0.003}
    escalas['1000000-800m'] = {'min':0.007, 'max':0.003}
    return escalas

if __name__ == "__main__":
    dados = importar_dados('resultados/srv-data.csv')
    resultado = calcular_intervalo(dados)
    utils.logger.info(f"\n{resultado}")
    gerar_graficos(resultado)
