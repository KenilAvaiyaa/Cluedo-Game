import os
import sys
from game import Game

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    banner = r"""
    The Cluedo
    ================================================
    Find who committed the murder, with which weapon, and in which room.

    IMPORTANT CLUEDO RULES:
    - every time you enter ib room, you MUST make a suggestion
    - Suggestions move the accused character and weapon to your current room. Example, Miss Scarlett Revolver 
    - You cannot make suggestions in hallways

    COMMANDS:
    move [room]              - Move to connected room (uses 1 move)
    suggest [char] [weapon]  - Make suggestion (AUTO-TRIGGERED in rooms)
    status                   - Show your current status
    map                      - Show mansion map
    help                     - Show these instructions
    end                      - End your turn
    quit                     - Exit game

    EXAMPLES:
    move "Dining Room"     
    - Move to Dining Room (will auto-trigger suggestion)
    suggest "Miss Scarlett" Revolver

    CHARACTERS (6):
    - Miss Scarlett, Colonel Mustard, Mrs. White
    - Reverend Green, Mrs. Peacock, Professor Plum

    WEAPONS (6):
    - Candlestick, Dagger, Lead Pipe, Revolver, Rope, Wrench

    ROOMS (9):
    - Kitchen, Ballroom, Conservatory, Dining Room, Billiard Room
    - Library, Lounge, Hall, Study
    """
    print(banner)


def handle_auto_suggestion(game, player):
    print(f"\nYOU ENTERED A ROOM! You must make a suggestion.")
    print("Available characters:", ", ".join([c.name for c in game.mansion.characters]))
    print("Available weapons:", ", ".join([w.name for w in game.mansion.weapons]))
    
    while True:
        suggestion_input = input("\nMake your suggestion (format: 'Character Weapon'): ").strip()
        
        if not suggestion_input:
            print("You must make a suggestion to continue.")
            continue
            
        parts = suggestion_input.split()
        if len(parts) < 2:
            print("Invalid format. Use: 'Character Weapon'")
            continue

        character_parts = []
        weapon_parts = []
        found_weapon = False
        
        weapon_keywords = ['candlestick', 'dagger', 'lead', 'revolver', 'rope', 'wrench']
        
        for part in parts:
            if not found_weapon and part.lower() in weapon_keywords:
                found_weapon = True
                weapon_parts.append(part)
            elif not found_weapon:
                character_parts.append(part)
            else:
                weapon_parts.append(part)
        
        character_name = ' '.join(character_parts)
        weapon_name = ' '.join(weapon_parts)
        
        if not character_name or not weapon_name:
            print("Please specify both character and weapon.")
            continue

        character_name = fix_character_name(character_name)
        weapon_name = fix_weapon_name(weapon_name)
        
        success, message = game.make_suggestion(player, character_name, weapon_name)
        print(f"\n{message}")
        
        if success:
            break
        else:
            print("Please try again.")


def handle_suggestion_command(game, player, command_parts):
    if len(command_parts) < 3:
        return False, "Invalid suggestion format"
    
    character_name = ""
    weapon_name = ""
    
    weapon_keywords = ['candlestick', 'dagger', 'lead', 'revolver', 'rope', 'wrench']
    
    found_weapon_index = -1
    for i, part in enumerate(command_parts[1:]):
        if part.lower() in weapon_keywords:
            found_weapon_index = i + 1
            break
    
    if found_weapon_index != -1:
        character_name = ' '.join(command_parts[1:found_weapon_index])
        weapon_name = ' '.join(command_parts[found_weapon_index:])
    else:
        if len(command_parts) >= 3:
            weapon_name = command_parts[-1]
            character_name = ' '.join(command_parts[1:-1])
        else:
            return False, "Could not parse character and weapon. Use: suggest 'Miss Scarlett' Revolver"
    
    # Fix names
    character_name = fix_character_name(character_name.strip())
    weapon_name = fix_weapon_name(weapon_name.strip())
    
    return game.make_suggestion(player, character_name, weapon_name)


def fix_character_name(name):
    name_lower = name.lower()
    
    if name_lower in ["miss scarlett", "ms scarlett", "scarlett", "miss"]:
        return "Miss Scarlett"
    elif name_lower in ["colonel mustard", "col mustard", "mustard", "colonel"]:
        return "Colonel Mustard"
    elif name_lower in ["mrs white", "mrs. white", "white", "mrs"]:
        return "Mrs. White"
    elif name_lower in ["reverend green", "mr green", "mr. green", "green", "reverend"]:
        return "Reverend Green"
    elif name_lower in ["mrs peacock", "mrs. peacock", "peacock"]:
        return "Mrs. Peacock"
    elif name_lower in ["professor plum", "prof plum", "plum", "professor"]:
        return "Professor Plum"
    
    return name


def fix_weapon_name(name):
    name_lower = name.lower()
    
    if name_lower in ["candlestick", "candle"]:
        return "Candlestick"
    elif name_lower == "dagger":
        return "Dagger"
    elif name_lower in ["lead", "pipe", "lead pipe"]:
        return "Lead Pipe"
    elif name_lower in ["revolver", "gun"]:
        return "Revolver"
    elif name_lower == "rope":
        return "Rope"
    elif name_lower == "wrench":
        return "Wrench"
    
    return name


def main():
    clear_screen()
    print_banner()

    while True:
        try:
            gamePlayers = int(input("\nAdd no of players (3-6): "))
            if 3 <= gamePlayers <= 6:
                break
            else:
                print("Please enter a number between 3 and 6.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGame cancelled.")
            return
    try:
        game = Game(gamePlayers)
        print(f"\nStarting positions:")
        for player in game.players:
            print(f"  {player.name} ({player.character.name}) starts in {player.character.starting_room.name}")
        
        print(f"\nWeapon locations:")
        weapon_locations = {}
        for room in game.mansion.rooms:
            if room.weapons and game.mansion.is_main_room(room):
                for weapon in room.weapons:
                    weapon_locations[weapon.name] = room.name
        
        for weapon_name, room_name in weapon_locations.items():
            print(f"{weapon_name}: {room_name}")
        
        print("\nREMEMBER: When you enter a room, you MUST make a suggestion!")
        input("\nPress Enter to start the game...")
        
    except Exception as e:
        print(f"Error initializing game: {e}")
        return
    
    while not game.game_over:
        clear_screen()
        current_player = game.get_current_player()
        
        print_banner()
        print(game.display_game_state())
        
        if game.remain_moves == 0 and not current_player.must_suggest:
            print(f"\n {current_player.name}'s turn - Rolling dice...")
            input("Press Enter to roll dice...")
            dice_roll = game.start_turn()
            print(f"You rolled a {dice_roll}! You have {game.remain_moves} moves.")
            input("Press Enter to continue...")
            continue 
        
        print(game.display_player_status(current_player))
        
        if current_player.must_suggest:
            handle_auto_suggestion(game, current_player)
            input("\nPress Enter to continue...")
            continue
        
        try:
            command = input("\nEnter command: ").strip()
            if not command:
                continue
                
            command_lower = command.lower()
            command_parts = command.split()
            
            if command_lower == "quit":
                if input("Are you sure you want to quit? (y/n): ").lower() == 'y':
                    print("Thanks for playing Cluedo!")
                    break
            
            elif command_lower == "help":
                print_instructions()
                input("\nPress Enter to continue...")
            
            elif command_lower == "status":
                input("\nPress Enter to continue...")
            
            elif command_lower == "map":
                print("\n" + game.mansion.get_simple_map(current_player.position.name))
                input("\nPress Enter to continue...")
            
            elif command_lower == "end":
                if current_player.must_suggest:
                    print("You cannot end your turn without making a suggestion! You entered a room.")
                    input("Press Enter to continue...")
                    continue
                    
                if game.remain_moves > 0:
                    print(f"You ended your turn with {game.remain_moves} moves remaining.")
                else:
                    print("You ended your turn.")
                    
                game.next_turn()
                print(f"\nTurn passed to {game.get_current_player().name}")
                input("Press Enter to continue...")
            
            elif command_lower.startswith("move "):
                if game.remain_moves <= 0:
                    print("No moves remaining. You need to end your turn.")
                    input("Press Enter to continue...")
                    continue
                
                target_room = ' '.join(command_parts[1:])
                success, message, requires_suggestion = game.move_player(current_player, target_room)
                print(f"\n{message}")
                
                if success and requires_suggestion:
                    input("\nPress Enter to make your suggestion...")
                
                elif success:
                    input("\nPress Enter to continue...")
                
            elif command_lower.startswith("suggest "):
                if not game.mansion.is_main_room(current_player.position):
                    print("You can only make suggestions when in a main room, not a hallway.")
                    input("Press Enter to continue...")
                    continue
                    
                success, message = handle_suggestion_command(game, current_player, command_parts)
                print(f"\n{message}")
                input("\nPress Enter to continue...")
            
            else:
                print("Invalid command. Type 'help' for available commands.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\nGame interrupted.")
            break
        except Exception as e:
            print(f"Error: {e}")
            input("Press Enter to continue...")
    
    print("\nGame over! Thanks for playing Cluedo Part 1!")


if __name__ == "__main__":
    main()