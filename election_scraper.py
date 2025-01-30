##############################################################################
'''
election_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Jan Schuster
email: schuster.jan@seznam.cz
'''

import csv
import sys
import requests
from bs4 import BeautifulSoup

def html_checker(url_adress) -> str:
    """
    function checks if the HTML is accessible and returns its content if it is.
    """
    try:
        response = requests.get(url_adress)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        quit()
        

def get_parsed_answer(response: str) -> BeautifulSoup:
    """
    Get the parsed response to a GET request.
    """
    try:
        return BeautifulSoup(response, features="html.parser")
    except Exception as e:
        print(f"Error: {e}")
        quit() 

def get_town_code(url_adress) -> list:
    """
    Returns the town codes from the URL.
    """
    town_codes = []
    searched_tds = url_adress.find_all("td", "cislo")
    for town in searched_tds:
        town_codes.append(town.text)
    return town_codes

def get_location_name(url_adress) -> list:
    """
    returns the location names from the URL
    """
    town_locations = []
    searched_tds = url_adress.find_all("td", "overflow_name")
    for location in searched_tds:
        town_locations.append(location.text)
    return town_locations

def get_location_url(url_adress) -> list:
    """
    Extracts the URL addresses for further information about each location.  
    """
    urls = []
    searched_tds = url_adress.find_all("td", "cislo", "href")
    for url_tag in searched_tds:
        url_tag = url_tag.a["href"]
        urls.append(f"https://volby.cz/pls/ps2017nss/{url_tag}")
    return urls

def clean_the_string(word: str) -> str:
    """
    Cleans the string from unwanted characters.
    """
    if '\xa0' in word:
        word = word.replace('\xa0', ' ')
        return word
    else:
        return word

def get_registered_voters(url_adress) -> str:
    """
    returns the number of registered voters in the location
    """
    registered_voters = ''
    location_link = get_parsed_answer(html_checker(url_adress))
    registered = location_link.find_all("td", headers="sa2")
    for citizen in registered:
        citizen = citizen.text
        registered_voters = clean_the_string(citizen)
    return registered_voters

def get_envelopes(url_adress) -> str:
    """
    returns the number of envelopes in the location
    """
    voters = ''
    location_link = get_parsed_answer(html_checker(url_adress))
    envelopes = location_link.find_all("td", headers="sa3")
    for envelope in envelopes:
        envelope = envelope.text
        voters = clean_the_string(envelope)
    return voters

def get_valid_ballot_papers(url_adress) -> str:
    """
    returns the number of valid ballot papers in the location
    """
    valid_ballot_papers = ''
    location_link = get_parsed_answer(html_checker(url_adress))
    ballot_papers = location_link.find_all("td", headers="sa6")
    for ballot_paper in ballot_papers:
        ballot_paper = ballot_paper.text
        valid_ballot_papers = clean_the_string(ballot_paper)
    return valid_ballot_papers

def get_party_names(url_adress) -> list:
    """
    returns the names of the parties from the URL
    since for all the regions in the given location the parties are the same, 
    we can just take the first one
    """
    party_names = []
    location_link = get_parsed_answer(html_checker(url_adress))
    parties = location_link.find_all("td", "overflow_name")
    for party_name in parties:
        party_names.append(party_name.text)
    return party_names

def get_votes_for_each_party(url_adress) -> list:
    """
    returns the number of votes for each party in the location 
    """
    party_votes = []
    town_odkaz = get_parsed_answer(html_checker(url_adress))
    votes = town_odkaz.find_all("td", "cislo", headers=["t1sb3", "t2sb3"])
    for vote in votes:
        vote = vote.text
        vote = clean_the_string(vote)
        party_votes.append(vote)
    return party_votes

def header_generation(url) -> list:
    """
    returns header
    """
    hardcoded_headers = ['code', 'location', 'registered', 'envelopes', 'valid']
    generated_headers = get_location_url(get_parsed_answer(html_checker(url)))
    party_names = get_party_names(generated_headers[0])
    for party in party_names:
        hardcoded_headers.append(party)
    return hardcoded_headers

def data_generation(url_link: str) -> list:
    """
    returns the data in the form of a list of lists
    """
    full_data = []
    registered_voter = []
    num_of_envelopes = []
    valid_voters = []
    all_votes = []
    town_code = get_town_code(get_parsed_answer(html_checker(url_link)))
    location = get_location_name(get_parsed_answer(html_checker(url_link)))
    location_urls = get_location_url(get_parsed_answer(html_checker(url_link)))

    for location_url in location_urls:
        registered_voter.append(get_registered_voters(location_url))
        num_of_envelopes.append(get_envelopes(location_url))
        valid_voters.append(get_valid_ballot_papers(location_url))
        all_votes.append(get_votes_for_each_party(location_url))

    # zip the requested information together and transform it to list
    zip_first_bucket = zip(town_code, location, registered_voter, 
                           num_of_envelopes, valid_voters)
    list_first_values = []
    for tc, lo, re, noe, vv in zip_first_bucket:
        list_first_values.append([tc, lo, re, noe, vv])

    zip_second_bucket = zip(list_first_values, all_votes)
    for fv, av in zip_second_bucket:
        full_data.append(fv + av)
    return full_data

def check_csv_file_name(file_name: str) -> str:
    if '.csv' not in file_name:
        print("The name of the file is wrong! it must contain '.csv'.")
        quit()
    else:
        return file_name

def main(url_link, file) -> None:
    """
    combines header and data together - then stores the data in csv file
    """
    header = header_generation(url_link)    
    main_data = data_generation(url_link)

    with open(file, "w", encoding="UTF-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(main_data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("There is a wrong number of arguments.")
        quit()
    else:
        url_adress = sys.argv[1]
        output_file = sys.argv[2]
        check_csv_file_name(output_file)
        main(url_adress, output_file)
        quit()

##############################################################################