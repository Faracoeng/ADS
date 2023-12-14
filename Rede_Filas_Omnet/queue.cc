/*
 * queue.cc
 *
 *  Created on: Dec 14, 2022
 *      Author: omnet1
 */


// Baseado nas Anotações de
// Paolo Giaccone
//http://www.telematica.polito.it/sites/default/files/public/courses/computer-network-design/labs.pdf
/*** queue.cc ***/
#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Queue : public cSimpleModule {
private:
    // local variable
    cQueue buffer;
    cMessage *endServiceEvent;
    cMessage *currentClient;
    simtime_t service_time;
    simsignal_t queueSizeSignal;
public:
    // constructor
    Queue(); // constructor
    virtual ~Queue(); // destructor
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Queue);
Queue::Queue() {
    endServiceEvent=NULL;
}

Queue::~Queue() {
    cancelAndDelete(endServiceEvent);
}

void Queue::initialize() {
    queueSizeSignal = registerSignal("queueSizeSignal");
    endServiceEvent=new cMessage("endService");  // self message para controle do final de serviço
}

void Queue::finish() {}

void Queue::handleMessage(cMessage *msg) {
    if (msg==endServiceEvent) {       // SE MENSAGEM for final de serviço...
        send(currentClient,"out");       // envia o cliente atual para fora...
        if (!buffer.isEmpty()) {         // Se existe requisição na fila
            currentClient=(cMessage*)buffer.pop();   // retira a requsisição da fila e faz como cliente corrente
            emit(queueSizeSignal, buffer.getLength());
            service_time=par("serviceTime");
            scheduleAt(simTime()+service_time,endServiceEvent); // escalona o tempo de serviço do novo cliente
        }
    } else {                           // SE MENSAGEM for chegada de nova requisição
        if (endServiceEvent->isScheduled()) { // se o servidor estiver ocupado...
            buffer.insert(msg); //Enfileira a mensagem
            emit(queueSizeSignal, buffer.getLength());
        } else {                              // senão atende de imediato e  escalona o tempo de serviço para este cliente
            currentClient = msg;
            service_time=par("serviceTime");
            scheduleAt(simTime()+service_time,endServiceEvent);
        }
    }
}

