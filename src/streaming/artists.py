class Artist:
    """
    Represents a music artist.

    Attributes:
        artist_id (int | str): Unique identifier.
        name (str): Artist name.
        genre (str): Primary genre of the artist.
        tracks (list[Track]): Tracks associated with the artist.
    """

    def __init__(self, artist_id, name, genre):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []

    def add_track(self, track):
        """
        Adds a track to the artist if not already present.

        Args:
            track (Track): Track to associate with the artist.
        """
        if track not in self.tracks:
            self.tracks.append(track)

    def track_count(self):
        """
        Returns the number of tracks associated with the artist.

        Returns:
            int: Number of tracks.
        """
        return len(self.tracks)