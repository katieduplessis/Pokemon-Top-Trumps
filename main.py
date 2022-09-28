import random

import requests


def get_random_number():
    return random.randint(1, 151)


def get_pokemon_url(pokemon_number):
    # gets the url of a specific number Pokemon
    pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}/'
    pokemon = requests.get(pokemon_url).json()
    return pokemon


def get_pokemon_stats(pokemon_url):
    # gets the dictionary of pokemons stats list == get_pokemon_url.json()['stats']
    return {
        'name': pokemon_url['name'],
        'id': pokemon_url['id'],
        'hp': pokemon_url['stats'][0]['base_stat'],
        'attack': pokemon_url['stats'][1]['base_stat'],
        'defense': pokemon_url['stats'][2]['base_stat'],
        'special-attack': pokemon_url['stats'][3]['base_stat'],
        'special-defense': pokemon_url['stats'][4]['base_stat'],
        'speed': pokemon_url['stats'][5]['base_stat'],
    }


def display_pokemon_stats(pokemon_stats):
    # shows stats to player
    print('__________')
    print(f"Here are the stats of {pokemon_stats['name']} (ID: {pokemon_stats['id']}): ")
    print(f"1. hp: {pokemon_stats['hp']}")
    print(f"2. attack: {pokemon_stats['attack']}")
    print(f"3. defense: {pokemon_stats['defense']}")
    print(f"4. special-attack: {pokemon_stats['special-attack']}")
    print(f"5. special-defense: {pokemon_stats['special-defense']}")
    print(f"6. speed: {pokemon_stats['speed']}")
    print('__________')


def select_pokemon_stats():
    # allows player to choose one of the stats
    stats_options = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    stat_choice = input("Select stat by bullet number (1-6):")
    stat_choice = int(stat_choice)
    if stat_choice < 1 or stat_choice > 6:
        stat_choice = input("Please select correctly. You must choose a number between 1 and 6:")
        stat_choice = int(stat_choice)
    selected_stat = stats_options[stat_choice - 1]
    return selected_stat


def compare_pokemon_stats(players_stat, opponents_stat):
    # decides which player's stat is higher
    player_pokemon_higher = False
    opponent_pokemon_higher = False

    if players_stat > opponents_stat:
        player_pokemon_higher = True
    elif players_stat < opponents_stat:
        opponent_pokemon_higher = True

    return player_pokemon_higher, opponent_pokemon_higher


def update_score(player_score, opponent_score, player_wins_round, opponent_wins_round):
    # creates and updates a score-card
    if player_wins_round:
        player_score += 1
    elif opponent_wins_round:
        opponent_score += 1

    return player_score, opponent_score


def select_overall_winner(player_final_score, opponent_final_score):
    # compares overall scores and selects overall winner
    player_wins_game = False
    opponent_wins_game = False

    if player_final_score > opponent_final_score:
        player_wins_game = True
    elif player_final_score < opponent_final_score:
        opponent_wins_game = True

    return player_wins_game, opponent_wins_game


def run_round(player_chosen_username, opponent_given_username):

    players_pokemon_number = get_random_number()
    players_pokemon = get_pokemon_url(players_pokemon_number)
    players_pokemon_stats = get_pokemon_stats(players_pokemon)

    opponents_pokemon_number = get_random_number()
    while opponents_pokemon_number == players_pokemon_number:
        opponents_pokemon_number = get_random_number()
    opponents_pokemon = get_pokemon_url(opponents_pokemon_number)
    opponents_pokemon_stats = get_pokemon_stats(opponents_pokemon)

    print(f"{player_chosen_username}, your pokemon is {players_pokemon_stats['name']}")
    display_pokemon_stats(players_pokemon_stats)

    selected_stat = select_pokemon_stats()
    players_selected_stat = players_pokemon_stats[selected_stat]
    opponents_selected_stat = opponents_pokemon_stats[selected_stat]

    print(f"\n{opponent_given_username} had {opponents_pokemon_stats['name']}")
    display_pokemon_stats(opponents_pokemon_stats)

    print(
        f"{player_chosen_username}, your {players_pokemon_stats['name']}'s "
        f"{selected_stat} was {players_selected_stat} "
        f"and {opponent_given_username}'s {opponents_pokemon_stats['name']}'s "
        f"{selected_stat} was {opponents_selected_stat}"
    )
    print("Which means....")
    player_wins, opponent_wins = \
        compare_pokemon_stats(int(players_selected_stat),
                              int(opponents_selected_stat))
    if player_wins:
        print(f"{player_chosen_username}, you won this round!")
    elif opponent_wins:
        print(f"{opponent_given_username} won this round!")
    else:
        print("This round was a draw")
    print(f"\n")

    return player_wins, opponent_wins


def run_game(player_chosen_username, opponent_given_username):
    # all functions work together
    number_of_rounds = input("How many rounds do you want to play?")
    number_of_rounds = int(number_of_rounds)
    rounds_played = 0
    player_score = 0
    opponent_score = 0

    while rounds_played < number_of_rounds:
        print(f"\nThis is round {rounds_played + 1}\n")
        player_won, opponent_won = run_round(player_chosen_username, opponent_given_username)

        player_score, opponent_score = update_score(player_score, opponent_score, player_won, opponent_won)
        print("Current Score:")
        print(f"{player_chosen_username}: {player_score}")
        print(f"{opponent_given_username}: {opponent_score}")
        print(f"\n")
        rounds_played += 1

    # uses the select_overall_winner function by passing the final scores from all rounds
    player_won_game, opponent_won_game = select_overall_winner(player_score, opponent_score)

    print("And the overall winner is...\n")

    if player_won_game:
        print(f"You, {player_chosen_username}! Congratulations!!!")
    elif opponent_won_game:
        print(f"Your opponent, {opponent_given_username}... Better luck next time")
    else:
        print("No one! It was a draw. Why don't you play another round to find a winner?")
        play_another_round = input("Would you like to play another round? Print 'y' for yes or 'n' for no.")
        if play_another_round == "y":
            run_round(player_chosen_username, opponent_given_username)
        elif play_another_round == "n":
            print("Good idea, let's keep this one as a draw.")
            exit()
        else:
            exit()

    print("The final score was:")
    print(f"{player_chosen_username}: {player_score}")
    print(f"{opponent_given_username}: {opponent_score}")

    # asks player if they want to play another game
    play_another_game = input("Would you like to play again? Print 'y' for yes or 'n' for no.")
    if play_another_game == "y":
        run_game(player_chosen_username, opponent_given_username)
    elif play_another_game == "n":
        print("Okay, bye. See you around!")
        exit()
    else:
        exit()


player_username = input("What is your name?")
opponent_username = input("And what would you like your opponent to be called?")

run_game(player_username, opponent_username)

