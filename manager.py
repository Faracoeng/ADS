import utils
import sys
import gerar_dados_integrado as gd

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
        print(f"Iniciando Cenário")
        utils.executa_comando(comando)
        print(f"Cenário iniciado com sucesso")
        return id_cenario
    except Exception as error:
        print(f"A execução do cenário falhou com o seguinte erro:\n{error}")
        sys.exit(1)

# Função para remover cenários existentes
def remove_cenarios():
    """
    Remove cenários existentes.
    """

    comando = f"sudo cleanupAll"
    try:
        print(f"Removendo todos os cenários em execução")
        utils.executa_comando(comando)
    except Exception as error:
        print(f"A remoção do cenário falhou com o seguinte erro:\n{error}")
        sys.exit(1)

if __name__ == "__main__":
    remove_cenarios()
    id_cenario = inicia_cenario()
    gd.executa_experimento(id_cenario)
