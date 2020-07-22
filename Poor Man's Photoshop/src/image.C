#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <image.h>
#include <source.h>

void Image::Update() const {
    source->Update();
}

Image::Image(void) {
    height = 0;
    width = 0;
    buffer = NULL;
}

Image::Image(int wid, int hei, unsigned char *buff) {
    width = wid;
    height = hei;
    buffer = (unsigned char *) malloc(3*height*width);
    memcpy(buffer, buff, 3*height*width);;
}

Image::Image(const Image &img) {
    buffer = (unsigned char *) malloc(3*height*width);
    height = img.height;
    width = img.width;
    memcpy(buffer, img.buffer, 3*height*width);
}

void Image::ResetSize(int w, int h) {
    width = w;
    height = h;
}

void Image::setBuffer(unsigned char *buff) {
    if (buffer == NULL) {
        buffer = (unsigned char *) malloc(3*width*height);
    }
    memcpy(buffer, buff, 3*height*width);
}

void Image::setSource(Source *s) {
    if (s != NULL) {
        source = s;
    }
}

int Image::getWidth() const {
    return width;
}

int Image::getHeight() const {
    return height;
}

unsigned char* Image::getBuffer() const {
    return  buffer;
}
