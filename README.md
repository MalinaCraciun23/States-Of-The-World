## States of the World
States of the World is a Python project developed for the Python programming class at UAIC.


The scope of the project is to crawl wikipedia, save useful information about all countries in the world and provide an API to access that data.

## Development
The project was developed using Python version 3.8.

#### Requirements
The libraries used are:
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc)
* [MontyDB](https://github.com/davidlatwe/montydb)
* [Flask](https://flask.palletsprojects.com/en/1.1.x)


To install the necessary requirements simply run the following command

    $ pip install -r requirements.txt
    

#### Running
To start the API run the command

    $ python wikipedia_api.py

The API will listen for requests on port 8000.

To make requests to the API you can use the client script.

    $ python Client.py
