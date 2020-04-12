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
    elos = {player_name: (1500, 0) for player_name in get_players()}
    results = get_results()
    return elos, results

def calculate(elos_and_results: (dict, [[str]])) -> dict:
    elos, results = elos_and_results
    for game in results:
        total_elo = sum([elos[player][0] for player in game])
        expected_scores = []
        for player in game:
            average_of_others = (total_elo - elos[player][0])/3
            expected_scores.append(1/(1 + 10**((average_of_others - elos[player][0])/400))) #Elo formula
        #expected_scores[i] stores the expected score for game[i]
        result = lambda i: 1 if i == 0 else 0
        #because data is stored so that game[0] is the winner of the game
        elo_change = lambda result, expected: round(32*(result - expected)) if result == 1 else round(32*(result - expected)/3)
        #losers lose 1/3 of what they should lose so that Elo is roughly conserved
        for i, player in enumerate(game):
            player_change = elo_change(result(i), expected_scores[i])
            elos[player] = (elos[player][0] + player_change, player_change)
        #adjust elos
        for player in elos:
            if player not in game:
                elos[player] = (elos[player][0], 0)
        #set change of players who weren't in this game to 0
    return elos

def str_of_elo_change(change: int) -> str:
    if change == 0:
        return ""
    elif change < 0:
        return "(" + str(change) + ")"
    else:
        return "(+" + str(change) + ")"

def print_elos(elos: dict) -> None:
    for k, v in sorted(elos.items(), key = lambda x: x[1], reverse = True):
        print(k, str(v[0]).rjust(15 - len(k)), str_of_elo_change(v[1]))
    print()

def run() -> None:
    print_elos(calculate(get_data()))
    
if __name__ == "__main__":
    run()
