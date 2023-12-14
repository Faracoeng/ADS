//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
//
// *** mm1.ned ***
simple Generator
{
    parameters:
        volatile double interArrivalTime; // sec
        @display("i=block/source");
    gates:
        output out;
}

simple Queue
{
    parameters:
        volatile double serviceTime; // sec
        @signal[queueSizeSignal](type="int");
        @statistic[queueSize](title="Buffer Size"; source="queueSizeSignal"; record=vector,stats; interpolationmode=none);
        @display("i=block/queue");
    gates:
        input in[];
        output out;
}

simple Sink
{
    parameters:
        @display("i=block/sink");
    gates:
        input in;
}

simple Splitter
{
    parameters:
        volatile double probSplit; // controla a probabilidade das saidas do splitter
        volatile double limitDecision; // limite de probabilidade para indica saída 0 ou 1
        @display("i=block/sink");
    gates:
        input in;
        output out[];
}

network RedeFilas
{
    submodules:
        gen0: Generator {
            @display("p=327,57");
        }
        queue0: Queue {
            @display("p=269,113");
        }
        sink1: Sink {
            @display("p=42,68");
        }
        splitter0: Splitter {
            @display("p=198,113");
        }
        gen1: Generator {
            @display("p=198,29");
        }
        gen2: Generator {
            @display("p=204,228");
        }
        queue1: Queue {
            @display("p=124,68");
        }
        queue2: Queue {
            @display("p=124,164");
        }
        sink2: Sink {
            @display("p=42,164");
        }
        gen3: Generator {
            @display("p=483,96");
        }
        queue3: Queue {
            @display("p=427,164");
        }
        splitter1: Splitter {
            @display("p=355,164");
        }
    connections:
        gen0.out --> queue0.in++;
        gen1.out --> queue1.in++;
        gen2.out --> queue2.in++;
        queue0.out --> splitter0.in;
        splitter0.out++ --> queue1.in++;
        splitter0.out++ --> queue2.in++;
        queue1.out --> sink1.in;
        queue2.out --> sink2.in;



        gen3.out --> queue3.in++;
        queue3.out --> splitter1.in;
        splitter1.out++ --> queue0.in++;
        splitter1.out++ --> queue2.in++;
}
