#include <logging.h>
#include <source.h>

Image * Source::GetOutput(){
  return &img;
}

Source::Source() {
    img.setSource(this);
}

Source::~Source() { }

void Source::Update(){
    char msg[1024];
    sprintf(msg, "%s: about to execute", SourceName());
    Logger::LogEvent(msg);
    Execute();
    sprintf(msg, "%s: done executing", SourceName());
    Logger::LogEvent(msg);
}
