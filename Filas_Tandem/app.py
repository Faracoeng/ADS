#gerado com apoio do chatGPT
import heapq
import random
import math

# Parâmetros do simulador
arrival_rate = 0.5  # Taxa de chegada exponencial (lambda)
service_rate = 0.8  # Taxa de atendimento exponencial (mu)
simulation_time = 200000  # Tempo total de simulação


# Classe geradora de números randômicos

class LCG:
    def __init__(self, seed, a, c, m):
        """
        Inicializa o gerador LCG com os parâmetros fornecidos.

        Args:
            seed: Semente inicial para o gerador.
            a: Coeficiente multiplicativo.
            c: Coeficiente aditivo.
            m: Módulo.
        """
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def sample(self):
        """
        Amostra um valor da sequência de números pseudoaleatórios.

        Returns:
            Um número pseudoaleatório.
        """
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed / self.m  # Normaliza o valor para estar entre 0 e 1

# Classe para representar o evento
class Event:
    def __init__(self, time, action, event_type):
        self.time = time
        self.action = action
        self.event_type = event_type

    def __lt__(self, other):
        return self.time < other.time

# Classe para a fila
class Queue:
    def __init__(self):
        self.buffer = []  # Buffer para armazenar os eventos

    def enqueue(self, event):
        heapq.heappush(self.buffer, event)

    def dequeue(self):
        return heapq.heappop(self.buffer)

    def is_empty(self):
        return len(self.buffer) == 0

# Classe para o simulador
class Simulator:
    def __init__(self, arrival_rate, service_rate):
        self.current_time = 0
        self.event_queue = []
        self.server_idle = True
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.queue = Queue()  # Fila com buffer compartilhado
        self.queue_waiting_time = 0  # Armazena acumulado o TEMPO ESPERA FILA
        self.response_time = 0  # Armazena a acumulado o tempo de TEMPO ESPERA no Sistema
        self.num_customers_served = 0
        self.num_customers_served_from_queue = 0  
        self.LCG =  LCG(12345, 1103515245, 12345, 2**31)

    def schedule_event(self, delay, action, event_type):
        event_time = self.current_time + delay
        event = Event(event_time, action, event_type)
        heapq.heappush(self.event_queue, event)

    def exponential_random_variate(self, rate):
        #return -math.log(1.0 - random.random()) / rate
        return -math.log(1.0 - self.LCG.sample()) / rate

    def arrival_action(self):
        interarrival_time = self.exponential_random_variate(self.arrival_rate)
        self.schedule_event(interarrival_time, self.arrival_action, "Chegada")

        if self.server_idle == True :
            service_time = self.exponential_random_variate(self.service_rate)
            self.response_time += service_time
            self.schedule_event(service_time, self.departure_action, "Partida")
            self.server_idle = False
            print("Inicia serviço")
        else:
            # Adiciona o evento à fila com o tempo de chegada
            event = Event(self.current_time, None, "Chegada")
            print("Enfileira")
            self.queue.enqueue(event)

    def departure_action(self):
        self.num_customers_served += 1

        if not self.queue.is_empty():
            event = self.queue.dequeue()
            waiting_time = self.current_time - event.time
            self.queue_waiting_time += waiting_time
            print("Tempo {:.2f}: Tempo espera de cliente".format(self.queue_waiting_time))
            self.num_customers_served_from_queue += 1

            service_time = self.exponential_random_variate(self.service_rate)
            self.response_time += waiting_time + service_time

            self.schedule_event(service_time, self.departure_action, "Partida")
        else:
            self.server_idle = True

    def run(self, end_time):
        self.schedule_event(0, self.arrival_action, "Chegada")

        while self.current_time < end_time:
            if not self.event_queue:
                break

            event = heapq.heappop(self.event_queue)
            self.current_time = event.time

            if event.event_type == "Chegada":
                print("Tempo {:.2f}: Chegada de cliente".format(self.current_time))
            elif event.event_type == "Partida":
                print("Tempo {:.2f}: Partida de cliente".format(self.current_time))

            event.action()
        print("Tempo {:.2f}: Número médio de requisições no sistema no Sistema".format(self.response_time/self.current_time))
        print("Tempo {:.2f}: Total Requisicoes no Sistema".format(self.num_customers_served))
        print("Tempo {:.2f}: Vazao no Sistema".format(self.num_customers_served / simulation_time))
        print("Tempo {:.2f}: Tempo Resposta Medio no Sistema".format(self.response_time/self.num_customers_served))		



simulator = Simulator(arrival_rate, service_rate)
simulator.run(simulation_time)