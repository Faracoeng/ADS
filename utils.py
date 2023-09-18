import random
import string
import logging, os
from subprocess import CompletedProcess, CalledProcessError, run, PIPE
from logging.handlers import RotatingFileHandler

# Configurar o logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Criar um manipulador para escrever em arquivo com rotação
file_handler = RotatingFileHandler('logs/log.txt', maxBytes=512)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
console_handler.setLevel(logging.INFO)  # Defina o nível de log para INFO

# Adicionar o manipulador de arquivo ao logger
logger.addHandler(file_handler)

# Adicionar o manipulador da saída padrão (console) apenas para mensagens INFO e superiores
logger.addHandler(console_handler)


# Função para criar identificador formado por uma cadeia de caracteres
def gera_id(qtd_digitos: int = 5) -> str:
    """
    Gera uma cadeia aleatória de caracteres alfanuméricos.

    Args:
        qtd_digitos (int, optional): O número de dígitos na cadeia gerada. Padrão é 5.

    Returns:
        str: A cadeia aleatória gerada.
    """
    caracteres = string.ascii_letters + string.digits  # Alfabeto (maiúsculas e minúsculas) + dígitos
    cadeia_aleatoria = ''.join(random.choice(caracteres) for _ in range(qtd_digitos))
    return cadeia_aleatoria

# Função para executar um comando e capturar a saída
def executa_comando(cmd: str, result: CompletedProcess = None, key: str = None):
    """
    Executa um comando no shell e retorna o resultado como um objeto CompletedProcess.

    Args:
        cmd (str): O comando a ser executado.
        result (CompletedProcess): Um objeto que contém informações sobre a execução do comando.
    """
    try:
        logger.debug(f"Executando comando = {cmd}")
        process = run(cmd, shell=True, check=True, text=True, stdout=PIPE, stderr=PIPE)
        if result is not None:
            result[key] = process
    except CalledProcessError as error:
        raise Exception(error)

# Função para escrever resultados dos comandos no arquivo
def escreve_resultado(tag: str, resultados: dict):
    """
    Executa a escrita do resultados do cliente e servidor em dois arquivos

    Args:
        tag (str): Identificador do experimento
        resultados (dict): Dicionário de objetos (CompletedProcess) com resultados da execução do comando
    """
    try:
        logger.debug(f"Escrevendo resultados nos arquivos")
        cli_file = f"resultados/cli-data.csv"
        srv_file = f"resultados/srv-data.csv"
        res_cli = resultados['cli-tcp'].stdout
        res_srv = resultados['srv-tcp'].stdout
        # FIXME Algumas vezes o resultado do client = "connect failed: Network is unreachable"
        # Verificar como tratar isso.
        logger.debug(f"dados-cliente={res_cli}")
        logger.debug(f"dados-servidor={res_srv}")
        write_line_in_file(cli_file, f"{tag},{get_last_line(res_cli)}")
        write_line_in_file(srv_file, f"{tag},{get_last_line(res_srv)}")

    except CalledProcessError as error:
        logger.error(error)
        raise Exception(error)

def get_last_line(text: str) -> str:
    if '\n' in text:
        linhas = text.splitlines()
        return f"{linhas[-1]}"
    else:
        return f"{text}"

def write_line_in_file(file_name: str, line: str):
    with open(file_name, 'a') as file:
        file.write(f"{line}\n")
        file.close()

def create_file(file_name: str):
    with open(file_name, 'w') as file:
        file.close()