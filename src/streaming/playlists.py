class Playlist:
    """
    Represents a user-created playlist.

    Attributes:
        playlist_id (int | str): Unique identifier.
        name (str): Playlist name.
        owner (User): Owner of the playlist.
        tracks (list[Track]): Tracks in the playlist.
    """

    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

    def add_track(self, track):
        """
        Adds a track to the playlist if not already present.

        Args:
            track (Track): Track to add.
        """
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id):
        """
        Removes a track from the playlist by its ID.

        Args:
            track_id (int | str): ID of the track to remove.
        """
        new_tracks = []

        # Rebuild list without the specified track
        for t in self.tracks:
            if t.track_id != track_id:
                new_tracks.append(t)

        self.tracks = new_tracks

    def total_duration_seconds(self):
        """
        Calculates total duration of all tracks in the playlist.

        Returns:
            int: Total duration in seconds.
        """
        total = 0

        for track in self.tracks:
            total += track.duration_seconds

        return total


class CollaborativePlaylist(Playlist):
    """
    A playlist that allows multiple contributors.

    The owner is always included as a contributor.

    Attributes:
        contributors (list[User]): Users who can modify the playlist.
    """

    def __init__(self, playlist_id, name, owner):
        super().__init__(playlist_id, name, owner)

        self.contributors = [owner]

    def add_contributor(self, user):
        """
        Adds a contributor to the playlist.

        Args:
            user (User): User to add.
        """
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user):
        """
        Removes a contributor from the playlist.

        The owner cannot be removed.

        Args:
            user (User): User to remove.
        """
        if user == self.owner:
            return

        if user in self.contributors:
            self.contributors.remove(user)