#ifndef SOURCE_330
#define SOURCE_330

#include <stdlib.h>
#include <string.h>
#include <image.h>

class Source{
	protected:
		Image  img;
        virtual void Execute() = 0;
	public:
        Source();
        ~Source();
        Image * GetOutput(void);
        virtual void Update();
        virtual const char *SourceName() = 0;
};
#endif
