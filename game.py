import random
from mansion import Mansion


class Player:
    
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.position = character.current_room
        self.cards = []
        self.must_suggest = False 
    
    @property
    def current_room(self):
        return self.position


class Game:
    
    def __init__(self, gamePlayers):
        self.mansion = Mansion()
        self.players = []
        self.current_player_index = 0
        self.game_over = False
        self.turn_count = 0
        self.remain_moves = 0
        
        if gamePlayers < 3 or gamePlayers > 6:
            raise ValueError("Players must be between 3 and 6")
        self._create_players(gamePlayers)
        self._distribute_cards()
        
        print(f"\nThis game has {gamePlayers} players")
        print("Cards distributed sucessfully")
    
    def _create_players(self, gamePlayers):
        available_characters = self.mansion.characters[:gamePlayers]
        
        for i in range(gamePlayers):
            player_name = f"Player {i+1}"
            player = Player(player_name, available_characters[i])
            self.players.append(player)
    
    def _distribute_cards(self):
        all_cards = []
        solution_char = self.mansion.solution['character'].name
        for char in self.mansion.characters:
            if char.name != solution_char:
                all_cards.append(char.name)
        
        solution_weapon = self.mansion.solution['weapon'].name
        for weapon in self.mansion.weapons:
            if weapon.name != solution_weapon:
                all_cards.append(weapon.name)
    
        solution_room = self.mansion.solution['room'].name
        room_names = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", 
                     "Billiard Room", "Library", "Lounge", "Hall", "Study"]
        for room_name in room_names:
            if room_name != solution_room:
                all_cards.append(room_name)
        
        random.shuffle(all_cards)
        
        gamePlayers = len(self.players)
        cards_per_player = len(all_cards) // gamePlayers
        extra_cards = len(all_cards) % gamePlayers
        
        card_index = 0
        for i, player in enumerate(self.players):
            num_cards = cards_per_player + (1 if i < extra_cards else 0)
            player.cards = all_cards[card_index:card_index + num_cards]
            card_index += num_cards
            
            print(f"{player.name} received {len(player.cards)} cards: {', '.join(player.cards)}")
    
    def roll_dice(self):
        return random.randint(1, 6)
    
    def start_turn(self):
        dice_roll = self.roll_dice()
        self.remain_moves = dice_roll
        return dice_roll
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.turn_count += 1
        self.remain_moves = 0
        
        # Reset suggestion flag for new player
        current_player = self.get_current_player()
        current_player.must_suggest = False
    
    def move_player(self, player, target_room_name):
        if self.remain_moves <= 0:
            return False, "your turn is over", False
        
        current_room = player.position
        target_room = self.mansion.get_room_name(target_room_name)
        
        if not target_room:
            return False, f"Room '{target_room_name}' not found.", False
        
        if not self.mansion.is_valid_move(current_room, target_room):
            return False, f"Cannot move to {target_room_name} from {current_room.name}.", False
        
        player.position = target_room
        
        used_secret_passage = False
        if (current_room.secret_passage and 
            current_room.secret_passage.name == target_room_name):
            message = f"Used secret passage to {target_room_name}!"
            used_secret_passage = True
        else:
            self.remain_moves -= 1
            message = f"Moved to {target_room_name}. Moves remaining: {self.remain_moves}"
        
        requires_suggestion = False
        if self.mansion.is_main_room(target_room): 
            player.must_suggest = True
            requires_suggestion = True
            message += f"\nYou entered {target_room_name}! Now first make a suggestion."
        
        return True, message, requires_suggestion
    
    def make_suggestion(self, player, character_name, weapon_name):
        current_room = player.position
        
        if not self.mansion.is_main_room(current_room):
            return False, "\make suggestions in main rooms, not hallways."
    
        character = self.mansion.get_character_name(character_name)
        if not character:
            available_chars = [c.name for c in self.mansion.characters]
            return False, f"Character '{character_name}' not found. Available: {', '.join(available_chars)}"
        
        weapon = self.mansion.get_weapon_name(weapon_name)
        if not weapon:
            available_weapons = [w.name for w in self.mansion.weapons]
            return False, f"Weapon '{weapon_name}' not found. Available: {', '.join(available_weapons)}"
    
        character_moved = False
        if character.current_room != current_room:
            self.mansion.character_in_room(character, current_room)
            character_moved = True
            char_move_msg = f"Moved {character.name} to {current_room.name}. "
        else:
            char_move_msg = f"{character.name} is already here. "
    
        weapon_moved = False
        if weapon.current_room != current_room:
            if weapon.current_room:
                weapon.current_room.remove_weapon(weapon)
            current_room.add_weapon(weapon)
            weapon_moved = True
            weapon_move_msg = f"Moved {weapon.name} to {current_room.name}."
        else:
            weapon_move_msg = f"{weapon.name} is already here."
        
        player.must_suggest = False
        
        message = f"SUGGESTION: {character.name} with {weapon.name} in {current_room.name}\n"
        message += f"RESULT: {char_move_msg}{weapon_move_msg}"
        
        return True, message
    
    def get_available_moves(self, player):
        available_rooms = self.mansion.next_moves(player.position)
        return [room.name for room in available_rooms]
    
    def display_player_status(self, player):
        status = f"\n=== {player.name} ({player.character.name}) ===\n"
        status += f"Position: {player.position.name}\n"
        status += f"Moves remaining: {self.remain_moves}\n"
        
        if player.must_suggest:
            status += "YOU MUST MAKE A SUGGESTION (entered a room)\n"
        
        status += f"Your cards: {', '.join(player.cards)}\n"
        
        # Current room info
        status += self.mansion.display_room_info(player.position)
        
        # Available moves
        available_moves = self.get_available_moves(player)
        status += f"\nAvailable moves: {', '.join(available_moves)}\n"
        
        return status
    
    def display_game_state(self):
        state = f"\n=== Game State (Turn {self.turn_count + 1}) ===\n"
        state += f"Current player: {self.get_current_player().name}\n"
        state += f"Total players: {len(self.players)}\n"
        state += f"Players: {', '.join([p.name for p in self.players])}\n"
        return state