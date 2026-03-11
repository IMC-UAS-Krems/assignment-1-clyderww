
class Playlist:
    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id):
        new_tracks = []

        for t in self.tracks:
            if t.track_id != track_id:
                new_tracks.append(t)

        self.tracks = new_tracks

    def total_duration_seconds(self):
        total = 0

        for track in self.tracks:
            total += track.duration_seconds

        return total

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner):
        super().__init__(playlist_id, name, owner)

        self.contributors = [owner]

    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user):
        if user == self.owner:
            return

        if user in self.contributors:
            self.contributors.remove(user)
