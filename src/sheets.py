import requests

API_KEY = open("api_key.txt").readline()
SHEET_ID = open("sheet_id.txt").readline()


def get_results() -> [[str]]:
    parameters = {"key": API_KEY}
    return requests.get("https://sheets.googleapis.com/v4/spreadsheets/{}/values/{}".format(SHEET_ID, "A2:D999"), params = parameters).json()["values"]

def get_players() -> [str]:
    parameters = {"key": API_KEY, "majorDimension": "COLUMNS"}
    return requests.get("https://sheets.googleapis.com/v4/spreadsheets/{}/values/{}".format(SHEET_ID, "Stats!A2:A999"), params = parameters).json()["values"][0]

def get_data() -> (dict, [[str]]):
    elos = {player_name: 1500 for player_name in get_players()}
    results = get_results()
    return elos, results

def calculate(elos_and_results: (dict, [[str]])) -> None:
    elos, results = elos_and_results
    for game in results:
        total_elo = sum([elos[name] for name in game])
        expected_scores = []
        for player in game:
            average_of_others = (total_elo - elos[player])/3
            expected_scores.append(1/(1 + 10**((average_of_others - elos[player])/400))) #Elo formula
        result = lambda i: 1 if i == 0 else 0
        elos[game[0]] += round(32*(1 - expected_scores[0])) #adjust winner's Elo using Elo formula
        for i, player in enumerate(game[1:]):
            elos[player] += round(32*(result(i + 1) - expected_scores[i + 1])/3)
            #losers lose 1/3 of what they should lose so that Elo is roughly conserved
    return elos

def run() -> None:
    answers = calculate(get_data())
    for k, v in sorted(answers.items(), key = lambda x: x[0]):
        print(k, "\t", v)
    
    
if __name__ == "__main__":
    run()
