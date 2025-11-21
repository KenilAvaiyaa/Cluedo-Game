import random
from layout import game_rooms, game_characters, game_weapons

class Mansion:
    def __init__(self):
        self.rooms, self.different_room = game_rooms()
        self.characters = game_characters(self.different_room)
        self.weapons = game_weapons()
        self.solution = {
            'character': random.choice(self.characters),
            'weapon': random.choice(self.weapons),
            'room': random.choice(list(self.different_room.values()))
        }
        self.give_weapons()
    
    def give_weapons(self):
        main_rooms = list(self.different_room.values())
        random.shuffle(main_rooms)
        
        for i, weapon in enumerate(self.weapons):
            room = main_rooms[i]  
            room.add_weapon(weapon)
    
    def get_room_name(self, room_name):
        for room in self.rooms:
            if room.name.lower() == room_name.lower():
                return room
        return None
    
    def get_character_name(self, character_name):
        for character in self.characters:
            if character.name.lower() == character_name.lower():
                return character
        return None
    
    def get_weapon_name(self, weapon_name):
        for weapon in self.weapons:
            if weapon.name.lower() == weapon_name.lower():
                return weapon
        return None
    
    def character_in_room(self, character, target_room):
        if not character or not target_room:
            return False
        
        if character.current_room:
            character.current_room.character_remove(character)
    
        target_room.character_added(character)
        character.move_to(target_room)
        return True
    
    def next_moves(self, current_room):
        available_rooms = []
        
        if not current_room:
            return available_rooms
        
        available_rooms.extend(current_room.rooms_connection)
        
        if current_room.secret_passage:
            available_rooms.append(current_room.secret_passage)
        
        return available_rooms
    
    def is_valid_move(self, from_room, to_room):
        if not from_room or not to_room:
            return False
        if to_room in from_room.rooms_connection:
            return True
        if from_room.secret_passage and from_room.secret_passage == to_room:
            return True
        
        return False
    
    def is_main_room(self, room):
        if hasattr(room, 'room_type'):
            return room.room_type == "main"
        return room in self.different_room.values()
    
    def display_room_info(self, room):
        if not room:
            return "Invalid room"
        
        info = f"\n=== {room.name} ===\n"
        
        if room.characters:
            char_names = [char.name for char in room.characters]
            info += f"Characters: {', '.join(char_names)}\n"
        else:
            info += "Characters: None\n"
    
        if room.weapons:
            weapon_names = [weapon.name for weapon in room.weapons]
            info += f"Weapons: {', '.join(weapon_names)}\n"
        else:
            info += "Weapons: None\n"
        
        if hasattr(room, 'room_type'):
            info += f"Room Type: {'Main Room' if room.room_type == 'main' else 'Hallway'}\n"
        else:
            info += f"Room Type: {'Main Room' if self.is_main_room(room) else 'Hallway'}\n"
        
        connected_names = [r.name for r in room.rooms_connection]
        if connected_names:
            info += f"Connected to: {', '.join(connected_names)}\n"
        
        if room.secret_passage:
            info += f"Secret passage to: {room.secret_passage.name}\n"
        
        return info
    
    def get_simple_map(self, current_room_name):
        map_lines = [
        "    [Conservatory] == [Ballroom] == [Kitchen]",
        "         |                  |           |",
        "         |                  |           |", 
        "    [Library] == [Billiard] == [Dining] == [Kitchen]",
        "         |                  |           |      |",
        "         |                  |           |      |",
        "      [Study] == [Hall] == [Lounge]     |      |",
        "         |                              |      |",
        "         └─────────── SECRET ───────────┘      |",
        "         └───────────────── SECRET ───────────┘"
        ]
    
        # Add current position indicator
        map_lines.append("")
        map_lines.append(f"Current Position: {current_room_name}")
        map_lines.append("Secret Passages: Study↔Kitchen, Conservatory↔Lounge")
    
        return "\n".join(map_lines) 