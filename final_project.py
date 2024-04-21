from collections import deque


class KeyNotFoundError(Exception):
    pass


players = {
    "Vesko": {'strength': 80, "health": 91, "damage_done": 0},
    "Guri": {'strength': 56, "health": 70, "damage_done": 0},
    "Gosho": {'strength': 55, "health": 69, "damage_done": 0},
    "Rosi": {'strength': 38, "health": 73, "damage_done": 0},
    "Kalata": {'strength': 65, "health": 48, "damage_done": 0},
    "Ivcho": {'strength': 50, "health": 50, "damage_done": 0},
    "Boko": {'strength': 99, "health": 99, "damage_done": 0},
    "Sasho": {'strength': 78, "health": 80, "damage_done": 0}
}

players_damage_done = {}

removed_players = deque()


def players_strength(character):
    return players[character]["strength"]


def final_boss_strength():
    return 30


def function_if_character_choice_is_lower_for_game_over(character_choice):
    return character_choice[0].upper() + character_choice[1: 4] + " " + character_choice[5].upper() + character_choice[
                                                                                                      6:]


def character_choice_is_lower(character_choice):
    return character_choice[0].upper() + character_choice[1:]


def adding_text_to_damage_file_if_someone_is_dead_or_someone_has_written_game_over(final_boss_damage):
    with open("damage.txt", "w") as damage_file:
        for player in removed_players:
            damage_file.write(f"{player} done {players_damage_done[player]} damage.\n")
        damage_file.write(f"Final Boss has done {final_boss_damage} damage.")


def bear_func():
    final_boss_health = 500
    final_boss_damage = 0

    try:
        while True:
            character_choice = input("Choose character from our class: ").lower()

            if character_choice == "game over":
                character_choice = function_if_character_choice_is_lower_for_game_over(character_choice)

            else:
                character_choice = character_choice_is_lower(character_choice)

            if character_choice.isdigit():
                raise ValueError("Name can not be int(try again):")

            if character_choice not in players and character_choice != "Game Over":
                raise KeyNotFoundError

            if character_choice == "Game Over":
                adding_text_to_damage_file_if_someone_is_dead_or_someone_has_written_game_over(final_boss_damage)
                print("Exiting...")
                break

            if not players:
                print("Sorry you lost all of your players and boss won the game!!!")
                break

            if players[character_choice]["health"] > 0:
                players[character_choice]["health"] -= final_boss_strength()
                final_boss_damage += final_boss_strength()
                print(f"Final Boss attacked {character_choice} for {final_boss_strength()} damage")
                print(f"Current player health: {players[character_choice]['health']}")

                if players[character_choice]["health"] <= 0:
                    print(f"{character_choice} is death!")
                    removed_players.append(character_choice)
                    players.pop(character_choice)

                    while True:
                        choice = input("Do you want to continue the game(y/n): ")

                        if choice == "n":
                            print("Exiting...")
                            adding_text_to_damage_file_if_someone_is_dead_or_someone_has_written_game_over(final_boss_damage)
                            return

                        elif choice == "y":
                            break

                        else:
                            raise ValueError("Invalid choice!!Please enter y or n!")

                    continue

            if final_boss_health > 0:
                final_boss_health -= players_strength(character_choice)
                players[character_choice]["damage_done"] += players_strength(character_choice)
                print(
                    f"{character_choice} attacked the final boss for {players_strength(character_choice)}\nCurrent boss health: {final_boss_health}")

                if character_choice not in players_damage_done:
                    players_damage_done[character_choice] = players_strength(character_choice)

                elif character_choice in players_damage_done:
                    players_damage_done[character_choice] += players_strength(character_choice)

                if final_boss_health <= 0:
                    print("Final boss is dead you won the game and defeated him!!")
                    break

        if removed_players:
            print(f"Dead players: {', '.join(removed_players)}")

        else:
            print("There are no removed players this game!")

        adding_text_to_damage_file_if_someone_is_dead_or_someone_has_written_game_over(final_boss_damage)

    except KeyNotFoundError:
        adding_text_to_damage_file_if_someone_is_dead_or_someone_has_written_game_over(final_boss_damage)
        with open("damage.txt", "a") as damage_file:
            damage_file.write("\nPlease enter a valid player next time! :)")

        print("Player not found!!")