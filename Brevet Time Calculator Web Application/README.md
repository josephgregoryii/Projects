    Brevet Time Calculator application 

    Continuous integration of mini projects

    Client:

        AJAX, jQuery, UI (Flask-Login, Flask-WTF), CSS

        Consumers using jQuery and php

    Server:

        Flask-based backend

        Storage using MongoDB (NoSQL)

    Protocols:

        HTTP, TCP/UDP, IP

    User session management

    Basic HTTP and token-based authentication

    Deployed using Docker

    Git versioning
************************************************************
Author: Joseph Gregory

Email: joeg@uoregon.edu

## build
Inside the DockerRestAPI directory, use command:
```bash
docker-compose build
docker-compose up
```

Once the web server is up and running, use port 5000 to launch the consumer program.

To reach the Brevets Calculator, use port 5002 to launch.

To reach the basic API of this program, use port 5001.

### Usage of API service:
    * "http://<host:port>/listAll" should return all open and close times in the database
    * "http://<host:port>/listOpenOnly" should return open times only
    * "http://<host:port>/listCloseOnly" should return close times only
    * "http://<host:port>/listAll/csv" should return all open and close times in CSV format
    * "http://<host:port>/listOpenOnly/csv" should return open times only in CSV format
    * "http://<host:port>/listCloseOnly/csv" should return close times only in CSV format
    * "http://<host:port>/listAll/json" should return all open and close times in JSON format
    * "http://<host:port>/listOpenOnly/json" should return open times only in JSON format
    * "http://<host:port>/listCloseOnly/json" should return close times only in JSON format
    * "http://<host:port>/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format 
    * "http://<host:port>/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format
    * "http://<host:port>/listCloseOnly/csv?top=6" should return top 5 close times only (in ascending order) in CSV format
    * "http://<host:port>/listCloseOnly/json?top=4" should return top 4 close times only (in ascending order) in JSON format

### To close the application:
```bash
control + 'c'
docker-compose down
```
