#ifndef PNMWRITER_330
#define PNMWRITER_330

#include <sink.h>

class PNMwriter : public Sink{
public:
    void Write(char *filename);
    const char *SinkName();
};
#endif
