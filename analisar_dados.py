from pandas import read_csv, DataFrame
import numpy as npy
from scipy import stats
import utils

column_names = ['tag','timestamp','ip_fonte','porta_fonte', 'ip_destino', 'porta_destino', 'protocolo', 'intervalo_medicao', 'id_tx', 'tx_bps']
confianca = 0.90

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
    return DataFrame(dados_agrupados)


if __name__ == "__main__":
    dados = importar_dados('resultados/srv-data.csv')
    resultado = calcular_intervalo(dados)
    utils.logger.info(f"\n{resultado}")
