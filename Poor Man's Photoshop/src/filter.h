#ifndef FILTERS_330
#define FILTERS_330

#include <stdio.h>
#include <source.h>
#include <sink.h>

class CheckSum: public Sink {
    public:
        void OutputCheckSum(char *filename);
        const char *SinkName();
};

class Color: public Source {
    protected:
        int width, height;
        unsigned char red, green, blue;
    public:
        Color(int w, int h, unsigned char r, unsigned char g, unsigned char b);
        ~Color();
        virtual void Execute();
        virtual const char *SourceName();
};

class Filter : public Source, public Sink{
    public:
        virtual void Update();
        virtual const char *FilterName() = 0;
        virtual const char *SourceName();
        virtual const char *SinkName();
};

class Shrinker : public Filter{
  public:
    virtual const char *FilterName();
    void Execute();
};

class LRCombine : public Filter
{
  public:
    virtual const char *FilterName(); 
    void Execute();
};

class TBCombine : public Filter{
  public:
    virtual const char *FilterName();
    void Execute();
};

class Blender : public Filter{
  protected:
    double factor;
  public:
    virtual const char *FilterName();
    void SetFactor(double f);
    void Execute();
};

class Grayscale: public Filter{
    public:
        virtual const char *FilterName();
        void Execute();
};
class Subtract: public Filter{
    public:
        virtual const char *FilterName();
        void Execute();
}; 
class Rotate: public Filter{
    public:
        virtual const char *FilterName();
        void Execute();
};
class Mirror: public Filter{
    public:
        virtual const char *FilterName();
        void Execute();
};
class Blur: public Filter{
    public:
        virtual const char *FilterName();
        void Execute();
};

#endif
