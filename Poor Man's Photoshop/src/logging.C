#include <logging.h>
#include <string.h>

FILE * Logger::logger = NULL;
DataFlowException::DataFlowException(const char *type, const char *error){
    sprintf(msg, "Throwing Exception: (%s): %s ",type, error);
    Logger::LogEvent(msg);
}

void Logger::LogEvent(const char *event){
    if (logger == NULL){
        logger = fopen("mylogger.txt", "w");
    }
    //fwrite(event, sizeof(char), strlen(event), logger);
    fprintf(logger,"%s\n", event);
}

void Logger::Finalize(){
    fclose(logger);
}
