class Artist:
    def __init__(self, artist_id, name, genre):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []

    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)

    def track_count(self):
        return len(self.tracks)
