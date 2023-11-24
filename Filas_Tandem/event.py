# Classe para representar o evento
class Event:    
    
    def __init__(self, time, action, event_type):
        self.time = time
        self.action = action
        self.event_type = event_type

    def __lt__(self, other):
        return self.time < other.time