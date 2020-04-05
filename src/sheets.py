import requests
from collections import namedtuple

API_KEY = open("api_key.txt").readline()
SHEET_ID = open("sheet_id.txt").readline()

Game = namedtuple("Game", ["winner", "losers"])

def get_results() -> [[str]]:
    parameters = {"key": API_KEY}
    return requests.get("https://sheets.googleapis.com/v4/spreadsheets/{}/values/{}".format(SHEET_ID, "A3:D999"), params = parameters).json()["values"]

def get_players() -> [str]:
    parameters = {"key": API_KEY, "majorDimension": "COLUMNS"}
    return requests.get("https://sheets.googleapis.com/v4/spreadsheets/{}/values/{}".format(SHEET_ID, "Stats!A2:A999"), params = parameters).json()["values"][0]

def get_data() -> (dict, [Game]):
    elos = {player_name: 1500 for player_name in get_players()}
    results = [Game(row[0], [row[1], row[2], row[3]]) for row in get_results()]
    return elos, results

def calculate(elos_and_results: (dict, [Game])) -> None:
    pass

def run() -> None:
    calculate(get_data())

if __name__ == "__main__":
    run()
