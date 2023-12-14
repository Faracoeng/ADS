# Tarefa A3.2 - Simulação de Rede de Filas com Omnet

Este diretório contém um projeto OMNeT++ com a implementação de uma simulação de redes de filas MM1.

## Pré-requisitos

Antes de executar este projeto, certifique-se de que você tenha instalado no SO:

- [OMNeT++ 6.0](https://doc.omnetpp.org/omnetpp/InstallGuide.pdf)

## Como Usar

1. **Criando ambiente virtual e instalar dependências**

   Execute comando a seguir:
      
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```


# Cenário

## Modelo 

O modelo de rede de filas MM1 simulado está ilustrado na figura a seguir:

![1](./figuras/modelo.png)

## Fatores

Os fatores e níveis utilizados estão descritos nas tabelas abaixo e foram configurados no arquivo [redes.ini](./redes.ini).

* Geração de requisições
  
    | Módulo  | carga 1 - 1\/[req\/s]| carga 2 - 1\/[req\/s]  |
    |:---:|:---:|:---:|
    |gen0   | 0.7  | 0.8  |  
    |gen1   | 0.9  | 1.3  | 
    |gen2   | 0.7  | 1.5  | 
    |gen3   | 0.9  | 1.7  | 

* Tempo de serviço
  
    | Módulo  | Tempo médio de serviço - 1\/[req\/s]|
    |:---:|:---:|
    |queue0   | 0.1s  | 
    |queue1   | 0.3s  | 
    |queue2   | 0.5s  |
    |queue3   | 0.2s  | 


# Resultados

<!-- 1. TODO -->