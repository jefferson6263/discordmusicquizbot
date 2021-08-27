
class User: 

    def __init__(self, username, leader):

        self.username = username
        self.points = 0
        self.leader = leader
        self.guessed_artist = False
        self.guessed_song = False
        self.guessed_album = False

    def is_leader(self):

        return self.leader

    def get_guessed_artist(self):

        return self.guessed_artist
    
    def set_guessed_artist(self, bool):

        self.guessed_artist = bool

    def get_guessed_song(self):

        return self.guessed_song
    
    def set_guessed_song(self, bool):

        self.guessed_song = bool

    def get_guessed_album(self):

        return self.guessed_album
    
    def set_guessed_album(self, bool):

        self.guessed_album = bool

    def get_points(self):

        return self.points

    def add_points(self, points):

        self.points += points
