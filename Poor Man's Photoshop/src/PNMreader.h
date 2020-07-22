#include <source.h>

class PNMreader : public Source {
protected:
    char *filename;
public:
    PNMreader(char *file);
    ~PNMreader();
    virtual const char *SourceName();
    virtual void Execute();
};
