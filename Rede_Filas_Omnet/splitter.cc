/*
 * sink.cc
 *
 *  Created on: Dec 14, 2022
 *      Author: omnet1
 */

// Baseado nas Anotações de
// Paolo Giaccone
//http://www.telematica.polito.it/sites/default/files/public/courses/computer-network-design/labs.pdf
#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Splitter : public cSimpleModule {
protected:
    virtual void handleMessage(cMessage *msg) override;
};

Define_Module(Splitter);

void Splitter::handleMessage(cMessage *msg) {
    double prob = par("probSplit");
    double limit = par("limitDecision");
    if(prob <= limit){
        send(msg, "out", 0);
    }
    else{
        send(msg, "out", 1);
    }
}


