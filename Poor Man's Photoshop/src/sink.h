#ifndef SINK_330
#define SINK_330

#include <image.h>
#include <stddef.h>

class Sink{
  protected:
    const Image *input1;
    const Image *input2;
  public:
    Sink();
    ~Sink();
    void SetInput(const Image *ipt1);
    void SetInput2(const Image *ipt2);
    const char *SinkName();
};
#endif
