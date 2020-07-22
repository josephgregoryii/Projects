#include <PNMreader.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>
using namespace std;

PNMreader::PNMreader(char *file){
    filename = (char *)malloc(strlen(file)+1);
    strcpy(filename,file);
}
PNMreader::~PNMreader(){
    free(filename);
}

const char *PNMreader::SourceName(){
    return "PNMreader";
}

void PNMreader::Execute() {
    FILE *f_in = fopen(filename, "rb");
    char magicNum[128];
    int width, height, maxval;

    if(f_in == NULL){
        fprintf(stderr, "Unable to open file %s", filename);
    }
    fscanf(f_in, "%s\n%d %d\n%d\n", magicNum, &width, &height, &maxval);
    unsigned char *temp = (unsigned char *)malloc(sizeof(unsigned char)*3*width*height);
    fread(temp,sizeof(unsigned char)*3, width*height, f_in);
    img.ResetSize(width,height);
    img.setBuffer(temp);
    fclose(f_in);
    free(temp);
}

