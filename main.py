import requests
import time
import os.path

from requests import get
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as bs

# Junk Value Calculator
# Source code by UPC
# Modifications made by Thorn1000

global version
version = "1.0.0"

def jv():
    nation = input("Please enter your nation to inform NS Admin who is using this script:\n")
    
    headers = {
    "User-Agent": f"JV Calculator/{version} (github: https://github.com/Thorn1000/JV-Calc ; user:{nation}; Authenticating)"
    }
    
    try: #ripped from spyglass with Devi's permission to make sure the given nation is real
        params = {"nation": nation, "q": "influence"}
        testreq = get(
            "https://www.nationstates.net/cgi-bin/api.cgi", headers=headers, params=params
        )
        testreq.raise_for_status()
        headers = {
             "User-Agent": f"JV Calculator/{version} (github: https://github.com/Thorn1000/JV-Calc ; user:{nation})"
        }
    except HTTPError:
        print(
            "Nation not found. Be sure to input the name of a nation that actually exists."
        )  
        print(f"ERR  {nation} is not a valid nation. Terminating.")
        raise SystemExit(1)
            
    timer = int(input("How fast do you want it run in ms? \n")) #sets a sleep timer to mainatin legal rate
    if timer >= 600 :
        pass
    else :
        print('That is too fast, defaulting to 650')
        timer = 650
        
    with open('output.txt', 'r+') as f: #clears our output.txt file which is why we confirm we want to run
            f.truncate(0)

    with open("nations.txt", "r") as in_file:   #lines 48-68 were written by UPC, lines 70-73 were modified
        nations = in_file.read().strip('\n').split('\n')
        for nation in nations:
            deck_request = bs(requests.get(f"https://www.nationstates.net/cgi-bin/api.cgi?q=cards+deck;nationname={nation.lower().replace(' ', '_')}", headers=headers).text, "xml").find_all("CARD")

            jv = 0

            for card in deck_request:
                match card.CATEGORY.text:
                    case "legendary":
                        jv += 1
                    case "epic":
                        jv += 0.5
                    case "ultra-rare":
                        jv += 0.2
                    case "rare":
                        jv += 0.1
                    case "uncommon":
                        jv += 0.05
                    case "common":
                        jv += 0.01

            print(f"Nation: {nation}, JV: {round(jv,2)}")
            with open('output.txt', 'a') as output:
                output.write(f"{round(jv,2)}"+'\n')
            time.sleep(timer/1000)
            
started = True #our main function

while started:  
    input_exists = os.path.exists('nations.txt') #step 1: make sure a nation file exists
    if input_exists:
        print('Input file found') #confirmation
    else:
        print('No input file found, please create one and try again \n') #if not make one and exit
        exit()
            
    output_exists = os.path.exists('output.txt') #check for an output file
    if output_exists:
        print('Output file found') #confirmation
    else:
        with open('output.txt', 'w') as f:
            f.write('')
            print('Output file made') #makes an empty file and confirms as such
            
    #since we empty our output file every run I added a confirmation to run the code        
    answer = input("Do you want to run this code? 1 for yes and 2 for no \n")  
    if answer == "1": 
        jv()    #runs code
    elif answer == "2":
        print("Exiting...")
        exit() #exits
    else:
        print('Invalid input, try again \n')
        
