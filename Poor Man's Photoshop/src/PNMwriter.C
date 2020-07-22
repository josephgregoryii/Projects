#include <PNMwriter.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void PNMwriter::Write(char *filename){
    FILE *f_out = fopen(filename, "wb");
    fprintf(f_out, "%s\n%d %d\n%d\n", "P6", input1->getWidth(),input1->getHeight(),255);
    fwrite(input1->getBuffer(), 3*sizeof(unsigned char), input1->getWidth()*input1->getHeight(), f_out);
    fclose(f_out);
}
const char * PNMwriter::SinkName(){
    return "PNMwriter";
}
