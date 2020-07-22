#include <filter.h>
#include <logging.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void Filter::Update() {
    char msg[128];
    if(input1 != NULL){
        sprintf(msg, "%s: about to update input1", FilterName());
        Logger::LogEvent(msg);
        input1->Update();
        sprintf(msg, "%s: done updating input1", FilterName());
        Logger::LogEvent(msg);
    }
    if(input2 != NULL){
        sprintf(msg, "%s: about to update input2",FilterName());
        Logger::LogEvent(msg);
        input2->Update();
        sprintf(msg, "%s: done updating input2",FilterName());
        Logger::LogEvent(msg);
    }
    
    sprintf(msg, "%s: about to execute", FilterName());
    Logger::LogEvent(msg);
    Execute();
    sprintf(msg, "%s: done executing", FilterName());
    Logger::LogEvent(msg);
}

const char *Shrinker::FilterName(){
    return "Shrinker";
}
const char *LRCombine::FilterName(){
    return "LRCombine";
}
const char *TBCombine::FilterName(){
    return "TBCombine";
}
const char *Blender::FilterName(){
    return "Blender";
}
const char *CheckSum::SinkName() {
    return "CheckSum";
}
const char *Color::SourceName(){
    return "Color";
}
const char *Grayscale::FilterName(){
    return "Grayscale";
}
const char *Subtract::FilterName(){
    return "Subtract";
}
const char *Rotate::FilterName(){
    return "Subtract";
}
const char *Mirror::FilterName(){
    return "Mirror";
}
const char *Blur::FilterName(){
    return "Blur";
}

const char *Filter::SourceName(){ return FilterName(); }
const char *Filter::SinkName()  { return FilterName(); }

void CheckSum::OutputCheckSum(char *filename){
    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!", SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    int width  = input1->getWidth();
    int height = input1->getHeight();
    int red   = 0;
    int green = 0;
    int blue  = 0;
    FILE *f = fopen(filename, "w");
    for(int i = 0; i<height; i++){
        for(int j = 0; j < width; j++){
            int index = 3*(i*width + j);
            red   += input1->getBuffer()[index];
            green += input1->getBuffer()[index+1];
            blue  += input1->getBuffer()[index+2];

            red   %= 256;
            green %= 256;
            blue  %= 256;
        }
    }
    fprintf(f, "CHECKSUM: %d, %d, %d\n", red, green, blue);
    fclose(f);
}

void Shrinker::Execute() {

    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!", SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    int width = input1->getWidth();
    int height = input1->getHeight();
    int halfWidth = width/2;
    int halfHeight = height/2;
    img.ResetSize(halfWidth, halfHeight);
    
    unsigned char * temp = (unsigned char *) malloc(halfWidth*halfHeight*3);
    
    for(int i=0; i<halfHeight; i++) {
        for(int j=0; j<halfWidth; j++) {
            int in = 3*(i*2*width+j*2);
            int out = 3*(i*halfWidth+j);
            temp[out] = input1->getBuffer()[in];
            temp[out+1] = input1->getBuffer()[in+1];
            temp[out+2] = input1->getBuffer()[in+2];
        }
    }
    
    img.setBuffer(temp);
    free(temp);
}

void LRCombine::Execute() {

    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!",SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    if (input2 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input2!",SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    int width1 = input1->getWidth();
    int height1 = input1->getHeight();
    int width2 = input2->getWidth();
    int height2 = input2->getHeight();
    int outWidth = width1+width2;
    int outHeight = (height1+height2)/2;

    if (height1 != height2){
        char msg[1024];
        sprintf(msg, "%s: heights must match: %d, %d", SinkName(), height1, height2);
        DataFlowException e(SinkName(),msg);
            throw e;
    }
    
    img.ResetSize(outWidth, outHeight);

    
    unsigned char * temp = (unsigned char *) malloc(outWidth*outHeight*3);
    
    for(int i=0; i < width1; i++) {
        for(int j=0; j < outHeight; j++) {
            int out = (j*outWidth+i)*3;
            int in = (j*width1+i)*3;
            temp[out] = input1->getBuffer()[in];
            temp[out + 1] = input1->getBuffer()[in + 1];
            temp[out + 2] = input1->getBuffer()[in + 2];
        }
    }
    
    for(int i=0; i < width2; i++) {
        for(int j=0; j < outHeight; j++) {
            int in2 = (j*width2+i)*3;
            int out = (j*outWidth+width1+i)*3;
            temp[out] = input2->getBuffer()[in2];
            temp[out + 1] = input2->getBuffer()[in2 + 1];
            temp[out + 2] = input2->getBuffer()[in2 + 2];
        }
    }
    
    img.setBuffer(temp);
    
    free(temp);
}

void TBCombine::Execute() {
    
    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!",SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    if (input2 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input2!",SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    int width1 = input1->getWidth();
    int height1 = input1->getHeight();
    int width2 = input2->getWidth();
    int height2 = input2->getHeight();
    int outHeight = height1+height2;
    int outWidth = (width1+width2)/2;

    if (width1 != width2){
        char msg[1024];
        sprintf(msg, "%s: widths must match: %d, %d", SinkName(), width1, width2);
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    img.ResetSize(outWidth, outHeight);
    
    unsigned char * temp = (unsigned char *) malloc(outHeight*outWidth*3);
    
    for(int i=0; i < outWidth; i++) {
        for(int j=0; j < height1; j++) {
            int out = (j*outWidth+i)*3;
            int in = (j*width1+i)*3;
            temp[out] = input1->getBuffer()[in];
            temp[out + 1] = input1->getBuffer()[in + 1];
            temp[out + 2] = input1->getBuffer()[in + 2];
        }
    }
    
    for(int i=0; i < outWidth; i++) {
        for(int j=0; j < height2; j++) {
            int in2 = (j*width2+i)*3;
            int out = ((j+height1)*outWidth+i)*3;
            temp[out] = input2->getBuffer()[in2];
            temp[out + 1] = input2->getBuffer()[in2 + 1];
            temp[out + 2] = input2->getBuffer()[in2 + 2];
        }
    }
    
    img.setBuffer(temp);
    free(temp);
}
void Blender::SetFactor(double f){factor = f;}
void Blender::Execute() {
    
    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!",SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    if (input2 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input2!",SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    int width1 = input1->getWidth();
    int height1 = input1->getHeight();
    int width2 = input2->getWidth();
    int height2 = input2->getHeight();
    
    int outHeight = (height1+height2)/2;
    int outWidth = (width1+width2)/2;

    if (height1 != height2 || width1 != width2){
        char msg[1024];
        sprintf(msg, "%s: image size must match: %d x %d, %d x %d",SinkName(), width1, height1, width2, height2);
        DataFlowException e(SinkName(),msg);
        throw e;
    }

    if (factor > 1.0){
        char msg[1024];
        sprintf(msg, "%s: Invalid factor for Blender: %f", SinkName(), factor);
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    img.ResetSize(outWidth, outHeight);

    
    unsigned char * temp = (unsigned char *) malloc(outHeight*outWidth*3);
    
    for(int i=0; i < outWidth; i++) {
        for(int j=0; j < outHeight; j++) {
            int index = (j*outWidth+i)*3;
            temp[index] = input1->getBuffer()[index]*factor + input2->getBuffer()[index]*(1-factor);
            temp[index + 1] = input1->getBuffer()[index + 1]*factor + input2->getBuffer()[index + 1]*(1-factor);
            temp[index + 2] = input1->getBuffer()[index + 2]*factor + input2->getBuffer()[index + 2]*(1-factor);
        }
    }
    
    img.setBuffer(temp);
    free(temp);
}

Color::~Color(){}
Color::Color(int w, int h, unsigned char r, unsigned char g, unsigned char b){
    width  = w;
    height = h;
    red = r;
    green = g;
    blue = b;
    img.ResetSize(width,height);
}

void Color::Execute(){
    unsigned char *temp = (unsigned char *) malloc(width*height*3);

    for (int i = 0; i<height; i++){
        for (int j = 0; j<width; j++){
            int index = 3*(i*width+j);
            temp[index]   = red;
            temp[index+1] = green;
            temp[index+2] = blue;
        }
    }
    img.setBuffer(temp);
    free(temp);
}
void Grayscale::Execute(){
    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!", SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    int width = input1->getWidth();
    int height = input1->getHeight();
    int outHeight = (height+height)/2;
    int outWidth = (width+width)/2;
    
    unsigned char * temp = (unsigned char *) malloc(outWidth*outHeight*3);
    
    for(int i=0; i<outHeight; i++) {
        for(int j=0; j<outWidth; j++) {
            int index = 3*(i*width+j);
            temp[index]   = input1->getBuffer()[index]/5 + input1->getBuffer()[index+1]/2 + input1->getBuffer()[index+2]/4;
            temp[index+1] = input1->getBuffer()[index]/5 + input1->getBuffer()[index+1]/2 + input1->getBuffer()[index+2]/4;
            temp[index+2] = input1->getBuffer()[index]/5 + input1->getBuffer()[index+1]/2 + input1->getBuffer()[index+2]/4;
        }
    }
    img.ResetSize(outWidth,outHeight);
    img.setBuffer(temp);
    free(temp);
}

void Subtract::Execute(){
    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!",SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    if (input2 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input2!",SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    int width1 = input1->getWidth();
    int height1 = input1->getHeight();
    int width2 = input2->getWidth();
    int height2 = input2->getHeight();
    
    int outHeight = (height1+height2)/2;
    int outWidth = (width1+width2)/2;

    if (height1 != height2 || width1 != width2){
        char msg[1024];
        sprintf(msg, "%s: image size must match: %d x %d, %d x %d",SinkName(), width1, height1, width2, height2);
        DataFlowException e(SinkName(),msg);
        throw e;
    }

    unsigned char * temp = (unsigned char *) malloc(outWidth*outHeight*3);

    for (int i = 0; i<outHeight; i++){
        for(int j = 0; j<outWidth; j++){
            int index = 3*(i*outWidth+j);
            if (input1->getBuffer()[index] > input2->getBuffer()[index]){
                temp[index] = input1->getBuffer()[index] - input2->getBuffer()[index];
            }
            else{
                temp[index] = 0;
            }
            if (input1->getBuffer()[index+1] > input2->getBuffer()[index+1]){
                temp[index+1] = input1->getBuffer()[index+1] - input2->getBuffer()[index+1];
            }
            else{
                temp[index+1] = 0;
            }
            if (input1->getBuffer()[index+2] > input2->getBuffer()[index+2]){
                temp[index+2] = input1->getBuffer()[index+2] - input2->getBuffer()[index+2];
            }
            else{
                temp[index+2] = 0;
            }
        }
    }
    img.ResetSize(outWidth,outHeight);
    img.setBuffer(temp);
    free(temp);
}

void Rotate::Execute(){
    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!", SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    int width = input1->getWidth();
    int height = input1->getHeight();
    unsigned char * temp = (unsigned char *) malloc(width*height*3);

    for(int i = 0; i<width; i++){
        for(int j = 0; j<height; j++){
            int in  = 3*(j*width+i);
            int out = 3*(i*height+(height-j-1));
            temp[out]   = input1->getBuffer()[in];
            temp[out+1] = input1->getBuffer()[in+1];
            temp[out+2] = input1->getBuffer()[in+2];
        }
    }
    img.ResetSize(height,width);
    img.setBuffer(temp);
    free(temp);
}
void Mirror::Execute(){
    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!", SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    int width = input1->getWidth();
    int height = input1->getHeight();
    
    unsigned char *temp = (unsigned char *)malloc(width*height*3);

    for(int i = 0; i<height; i++){
        for(int j = 0; j<width; j++){
            int in  = 3*(i*width+j);
            int out = 3*(i*width+(width-j-1));
            temp[out] = input1->getBuffer()[in];
            temp[out+1] = input1->getBuffer()[in+1];
            temp[out+2] = input1->getBuffer()[in+2];
        }
    }
    img.ResetSize(width,height);
    img.setBuffer(temp);
    free(temp);
}

void Blur::Execute(){
    
    if (input1 == NULL){
        char msg[1024];
        sprintf(msg, "%s: no input1!", SinkName());
        DataFlowException e(SinkName(), msg);
        throw e;
    }
    
    int width = input1->getWidth();
    int height = input1->getHeight();
    
    unsigned char * temp = (unsigned char *) malloc(width*height*3);

    for(int i = 0; i<height; i++){
        for(int j = 0; j<width; j++){
            int index  = 3*(i*width+j);
            if (i == 0 || j == 0){
                temp[index] = input1->getBuffer()[index];
                temp[index+1] = input1->getBuffer()[index+1];
                temp[index+2] = input1->getBuffer()[index+2];
            }
            else if (i == height-1 || j == width-1){
                temp[index] = input1->getBuffer()[index];
                temp[index+1] = input1->getBuffer()[index+1];
                temp[index+2] = input1->getBuffer()[index+2];
            }
            else{
            temp[index]   = input1->getBuffer()[3*((i-1)*width+(j-1))]/8 + \
                            input1->getBuffer()[3*((i)  *width+(j-1))]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j-1))]/8 + \
                            input1->getBuffer()[3*((i-1)*width+(j))  ]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j))  ]/8 + \
                            input1->getBuffer()[3*((i-1)*width+(j+1))]/8 + \
                            input1->getBuffer()[3*((i)  *width+(j+1))]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j+1))]/8;

            temp[index+1] = input1->getBuffer()[3*((i-1)*width+(j-1))+1]/8 + \
                            input1->getBuffer()[3*((i)  *width+(j-1))+1]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j-1))+1]/8 + \
                            input1->getBuffer()[3*((i-1)*width+(j))  +1]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j))  +1]/8 + \
                            input1->getBuffer()[3*((i-1)*width+(j+1))+1]/8 + \
                            input1->getBuffer()[3*((i)  *width+(j+1))+1]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j+1))+1]/8;

            temp[index+2] = input1->getBuffer()[3*((i-1)*width+(j-1))+2]/8 + \
                            input1->getBuffer()[3*((i)  *width+(j-1))+2]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j-1))+2]/8 + \
                            input1->getBuffer()[3*((i-1)*width+(j))  +2]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j))  +2]/8 + \
                            input1->getBuffer()[3*((i-1)*width+(j+1))+2]/8 + \
                            input1->getBuffer()[3*((i)  *width+(j+1))+2]/8 + \
                            input1->getBuffer()[3*((i+1)*width+(j+1))+2]/8;
            }
        }
    }
    img.ResetSize(width,height);
    img.setBuffer(temp);
    free(temp);
}
