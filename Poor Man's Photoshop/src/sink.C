#include <sink.h>

Sink::Sink(){
    input1 = NULL;
    input2 = NULL;
}
Sink::~Sink(){}

void Sink::SetInput(const Image * inpt1){
    input1 = inpt1;
}

void Sink::SetInput2(const Image * inpt2){
    input2 = inpt2;
}
