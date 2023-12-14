/*
 * generator.cc
 *
 *  Created on: Dec 14, 2022
 *      Author: omnet1
 */



// Baseado nas Anotações de
// Paolo Giaccone
//http://www.telematica.polito.it/sites/default/files/public/courses/computer-network-design/labs.pdf
/*** generator.cc ***/
#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Generator: public cSimpleModule {
private:
    cMessage *sendMsgEvent;
public:
    Generator();
    virtual ~Generator();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Generator);

Generator::Generator() {
    sendMsgEvent=NULL;
}

Generator::~Generator() {
    cancelAndDelete(sendMsgEvent);
}

void Generator::initialize() {
    // Envia a primeiro pacote
    sendMsgEvent=new cMessage("sendEvent");
    // escalona evento para enviar o próximo pacote
    scheduleAt(par("interArrivalTime"), sendMsgEvent);
}

void Generator::finish() {
}

void Generator::handleMessage(cMessage *msg) {
    cMessage *pkt;
    simtime_t departure_time;
    // Recebeu self message
    pkt = new cMessage("packet");
    // Envia pacote
    send(pkt,"out");
    // computa tempo do próximo pacote
    departure_time=simTime()+par("interArrivalTime");
    // escalona evento para enviar o próximo pacote
    scheduleAt(departure_time, sendMsgEvent);
}
