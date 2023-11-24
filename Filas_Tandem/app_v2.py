import heapq
import random
import math
from queue_event import Queue
from event import Event
from lgc import LCG

class MM1Queue:
    def __init__(self, arrival_rate, service_rate, simulator):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.simulator = simulator
        self.server_idle = True
        self.queue = Queue()
        self.queue_waiting_time = 0
        self.response_time = 0
        self.num_customers_served = 0
        self.LCG = LCG(12345, 1103515245, 12345, 2**31)

    def schedule_event(self, delay, action, event_type):
        self.simulator.schedule_event(delay, action, event_type)

    def exponential_random_variate(self, rate):
        return -math.log(1.0 - self.LCG.sample()) / rate

    def arrival_action(self):
        interarrival_time = self.exponential_random_variate(self.arrival_rate)
        self.schedule_event(interarrival_time, self.arrival_action, "Chegada")

        if self.server_idle:
            service_time = self.exponential_random_variate(self.service_rate)
            self.response_time += service_time
            self.schedule_event(service_time, self.departure_action, "Partida")
            self.server_idle = False
            print("Inicia serviço")
        else:
            event = Event(self.simulator.current_time, None, "Chegada")
            print("Enfileira")
            self.queue.enqueue(event)

    def departure_action(self):
        self.num_customers_served += 1

        if not self.queue.is_empty():
            event = self.queue.dequeue()
            waiting_time = self.simulator.current_time - event.time
            self.queue_waiting_time += waiting_time
            print("Tempo {:.2f}: Tempo espera de cliente".format(self.queue_waiting_time))
            service_time = self.exponential_random_variate(self.service_rate)
            self.response_time += waiting_time + service_time

            self.schedule_event(service_time, self.departure_action, "Partida")
        else:
            self.server_idle = True

    def run(self, end_time):
        self.schedule_event(0, self.arrival_action, "Chegada")
        while self.simulator.current_time < end_time:
            if not self.simulator.event_queue:
                break

            event = heapq.heappop(self.simulator.event_queue)
            self.simulator.current_time = event.time

            if event.event_type == "Chegada":
                print("Tempo {:.2f}: Chegada de cliente na Fila".format(self.simulator.current_time))
            elif event.event_type == "Partida":
                print("Tempo {:.2f}: Partida de cliente da Fila".format(self.simulator.current_time))

            event.action()

        print("Tempo {:.2f}: Número médio de requisições na Fila".format(self.response_time / self.simulator.current_time))
        print("Tempo {:.2f}: Total Requisições na Fila".format(self.num_customers_served))
        print("Tempo {:.2f}: Vazão na Fila".format(self.num_customers_served / end_time))
        print("Tempo {:.2f}: Tempo Médio de Resposta na Fila".format(self.response_time / self.num_customers_served))


class TandemSimulator:
    def __init__(self, arrival_rate_1, service_rate_1, arrival_rate_2, service_rate_2, simulation_time):
        self.current_time = 0
        self.event_queue = []
        self.simulation_time = simulation_time
        self.queue1 = MM1Queue(arrival_rate_1, service_rate_1, self)
        self.queue2 = MM1Queue(arrival_rate_2, service_rate_2, self)

    def schedule_event(self, delay, action, event_type):
        event_time = self.current_time + delay
        event = Event(event_time, action, event_type)
        heapq.heappush(self.event_queue, event)

    def run(self):
        self.queue1.run(self.simulation_time)
        self.queue2.run(self.simulation_time)


# Parâmetros do simulador
arrival_rate_1 = 0.3
service_rate_1 = 0.5
arrival_rate_2 = 0.4
service_rate_2 = 0.6
simulation_time = 200000

tandem_simulator = TandemSimulator(arrival_rate_1, service_rate_1, arrival_rate_2, service_rate_2, simulation_time)
tandem_simulator.run()
