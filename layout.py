class Character:
    def __init__(self, name, color, starting_room):
        self.name = name
        self.color = color
        self.current_room = starting_room
        self.starting_room = starting_room
    
    def move_to(self, room):
        self.current_room = room


class Weapon:
    def __init__(self, name):
        self.name = name
        self.current_room = None


class Room:
    def __init__(self, name, room_type="main"):
        self.name = name
        self.room_type = room_type 
        self.rooms_connection = []
        self.characters = []
        self.weapons = []
        self.secret_passage = None
    
    def to_connection(self, room):
        
        if room not in self.rooms_connection:
            self.rooms_connection.append(room)
        if self not in room.rooms_connection:
            room.rooms_connection.append(self)
            
    def character_added(self, character):
        if character not in self.characters:
            self.characters.append(character)
    
    def character_remove(self, character):
        if character in self.characters:
            self.characters.remove(character)
    
    def add_weapon(self, weapon):
        if weapon not in self.weapons:
            self.weapons.append(weapon)
            weapon.current_room = self
    
    def remove_weapon(self, weapon):
        if weapon in self.weapons:
            self.weapons.remove(weapon)
            weapon.current_room = None


def game_characters(rooms_dict):
    return [
        Character("Miss Scarlett", "red", rooms_dict["Lounge"]),
        Character("Colonel Mustard", "yellow", rooms_dict["Dining Room"]), 
        Character("Mrs. White", "white", rooms_dict["Ballroom"]),
        Character("Reverend Green", "green", rooms_dict["Conservatory"]),
        Character("Mrs. Peacock", "blue", rooms_dict["Library"]),
        Character("Professor Plum", "purple", rooms_dict["Study"])
    ]


def game_weapons():
    return [
        Weapon("Candlestick"),
        Weapon("Dagger"), 
        Weapon("Lead Pipe"),
        Weapon("Revolver"),
        Weapon("Rope"),
        Weapon("Wrench")
    ]


def game_rooms():
    kitchen = Room("Kitchen", "main")
    ballroom = Room("Ballroom", "main")
    conservatory = Room("Conservatory", "main")
    dining_room = Room("Dining Room", "main")
    billiard_room = Room("Billiard Room", "main")
    library = Room("Library", "main")
    lounge = Room("Lounge", "main")
    hall = Room("Hall", "main")
    study = Room("Study", "main")
    
    Loung_hallway = Room("Hallway_Hall_Lounge", "hallway")
    Billiard_hallway = Room("Hallway_Hall_Billiard", "hallway")
    Study_hallway = Room("Hallway_Hall_Study", "hallway")
    Dining_Lounge_hallway = Room("Hallway_Lounge_Dining", "hallway")
    Billiard_Dining_hallway = Room("Hallway_Dining_Billiard", "hallway")
    Library_Billiard_hallway = Room("Hallway_Billiard_Library", "hallway")
    Conservatory_Library_hallyway  = Room("Hallway_Library_Conservatory", "hallway")
    Ballroom_Conservatory_hallway = Room("Hallway_Conservatory_Ballroom", "hallway")
    Kitchen_Calroom_hallway = Room("Hallway_Ballroom_Kitchen", "hallway")
    Kirchen_hallway_Dining = Room("Hallway_Kitchen_Dining", "hallway")
    Study_hallway_Library = Room("Hallway_Study_Library", "hallway")
    Ballroom_hallway_Billiard = Room("Hallway_Ballroom_Billiard", "hallway")
    
    hall.to_connection(Loung_hallway)
    hall.to_connection(Billiard_hallway)
    hall.to_connection(Study_hallway)
    
    lounge.to_connection(Loung_hallway)
    lounge.to_connection(Dining_Lounge_hallway)
    
    dining_room.to_connection(Dining_Lounge_hallway)
    dining_room.to_connection(Billiard_Dining_hallway)
    dining_room.to_connection(Kirchen_hallway_Dining)
    
    billiard_room.to_connection(Billiard_hallway)
    billiard_room.to_connection(Billiard_Dining_hallway)
    billiard_room.to_connection(Library_Billiard_hallway)
    billiard_room.to_connection(Ballroom_hallway_Billiard)
    
    library.to_connection(Library_Billiard_hallway)
    library.to_connection(Conservatory_Library_hallyway )
    library.to_connection(Study_hallway_Library)
    
    conservatory.to_connection(Conservatory_Library_hallyway )
    conservatory.to_connection(Ballroom_Conservatory_hallway)
    
    ballroom.to_connection(Ballroom_Conservatory_hallway)
    ballroom.to_connection(Kitchen_Calroom_hallway)
    ballroom.to_connection(Ballroom_hallway_Billiard)
    
    kitchen.to_connection(Kitchen_Calroom_hallway)
    kitchen.to_connection(Kirchen_hallway_Dining)
    
    study.to_connection(Study_hallway)
    study.to_connection(Study_hallway_Library)
    
    study.secret_passage = kitchen
    kitchen.secret_passage = study
    conservatory.secret_passage = lounge
    lounge.secret_passage = conservatory
    
    different_room = {
        "Kitchen": kitchen,
        "Ballroom": ballroom,
        "Conservatory": conservatory,
        "Dining Room": dining_room,
        "Billiard Room": billiard_room,
        "Library": library,
        "Lounge": lounge,
        "Hall": hall,
        "Study": study
    }
    
    all_rooms = [
        kitchen, ballroom, conservatory, dining_room, billiard_room,
        library, lounge, hall, study,
        Loung_hallway, Billiard_hallway, Study_hallway, Dining_Lounge_hallway, Billiard_Dining_hallway,
        Library_Billiard_hallway, Conservatory_Library_hallyway , Ballroom_Conservatory_hallway, Kitchen_Calroom_hallway, Kirchen_hallway_Dining,
        Study_hallway_Library, Ballroom_hallway_Billiard
    ]
    
    return all_rooms, different_room