PROJECT DESCRIPTION

The elections_scraper project is a tool written in Python which allows automatic 
downloading of election results information from the (https://www.volby.cz/) 
website. This tool is useful for political analysts and everybody else who 
is interested in election results data.

INSTALLATION

Clone this repository to your local environment.
Install all the libraries used in this project. For reference use
requirements.txt file

USAGE

Run the election_scraper.py script with two arguments: the election URL
and the name of the output CSV file.
The URL part MUST contain the correct url and the name of the output CSV file
MUST contain '.csv' part.
There are three examples of running the script:

python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "prostejov.csv"

python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106" "Melnik.csv" 

python election_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102" "Benesov.csv"

The example outputs: prostejov.csv, Melnik.csv and Benesov.csv 
are attached to this repository
