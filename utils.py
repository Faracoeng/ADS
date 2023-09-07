import random
import string
from subprocess import CompletedProcess, CalledProcessError, run, PIPE

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
def executa_comando(cmd: str) -> CompletedProcess:
    """
    Executa um comando no shell e retorna o resultado como um objeto CompletedProcess.

    Args:
        cmd (str): O comando a ser executado.

    Returns:
        CompletedProcess: Um objeto que contém informações sobre a execução do comando.
    """
    try:
        print(f"Executando comando = {cmd}\n")
        resultado = run(cmd, shell=True, check=True, text=True, stdout=PIPE, stderr=PIPE)
        return resultado
    except CalledProcessError as error:
        raise Exception(error)