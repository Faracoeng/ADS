import utils, argparse, sys
import gerar_dados as gd

# Função para iniciar um cenário
def inicia_cenario(arquivo_imunes: str = "ads-cenario.imn") -> str :
    """
    Inicia um cenário do Imunes.

    Args:
        arquivo_imunes (str, optional): O nome do arquivo de configuração do cenário. Padrão é "ads-cenario.imn".

    Returns:
        str: O identificador único do cenário iniciado.
    """
    id_cenario = utils.gera_id()
    comando = f"sudo imunes -e {id_cenario} -b {arquivo_imunes}"

    try:
        utils.logger.info(f"Iniciando Cenário")
        utils.executa_comando(comando)
        utils.logger.debug(f"Executando comando = {comando}")
        utils.logger.info(f"Cenário iniciado com sucesso")
        return id_cenario
    except Exception as error:
        utils.log.error(f"A execução do cenário falhou com o seguinte erro:\n{error}")
        sys.exit(1)

# Função para remover cenários existentes
def remove_cenarios():
    """
    Remove cenários existentes.
    """

    comando = f"sudo cleanupAll"
    try:
        utils.logger.debug(f"Removendo todos os cenários em execução")
        utils.executa_comando(comando)
    except Exception as error:
        utils.logger.error(f"A remoção do cenário falhou com o seguinte erro:\n{error}")
        sys.exit(1)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Executar experimento com cenário padrão.")
    parser.add_argument("-t", type=int, help="Tempo de transmissão em segundos", default=2)
    parser.add_argument("-n", type=int, help="Número de repetições", default=8)
    args = parser.parse_args()

    time_tx = args.t
    num_rep = args.n

    utils.logger.info(f"Cenário será executado com parâmetros:\nTempo de tx = {time_tx} min.\nNúmero de repetições = {num_rep}.\n")

    remove_cenarios()
    id_cenario = inicia_cenario()
    
    # Chame a função para executar o experimento com os argumentos fornecidos
    gd.executa_experimento(id_cenario, time_tx, num_rep)