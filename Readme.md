# Instruções de Uso

Este é um projeto Python que lida com experimentos utilizando a ferramenta Imunes para criar cenários de rede. Os resultados dos experimentos são escritos em arquivos no diretório `./resultados/` e os arquivos com os gráficos no diretório `./graficos/`.

## Pré-requisitos

Antes de executar este código, certifique-se de que você tenha instalado no SO:

- Python 3.10.
- [Imunes](https://github.com/imunes/imunes)
- Usuário com acesso *root*

## Como Usar

1. **Criando ambiente virtual e instalar dependências**

   Execute comando a seguir:
      
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```

2. **Executando experimento com Cenário Padrão**

   <!-- É possível criar outro cenário pela interface do Imunes e atualizar o código presente no arquivo `gerar_dados.py` para o funcionamento correto. Atualmente, o experimento só funciona com o cenário padrão ("ads-cenario.imn"). -->

   Execute comando a seguir no terminal dentro da raiz do projeto (será solicitado a senha do usuário):
      
   ```bash
   python3 manager.py
   ```

3. **Executando análise dos dados**
   ```bash
   python3 analisar_dados.py
   ```
   
4. **Visualização de logs**


   A execução do *script* pode ser acompanhada através dos *logs* que são gerados também no arquivo `logs/log.txt`. Execute o seguinte comando em outro terminal no mesmo diretório desse projeto:

   ```bash
   tail -f -n 10 logs/log.txt
   ```