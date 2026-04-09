class Album:
    """
    Represents a music album containing multiple tracks.

    Attributes:
        album_id (int | str): Unique identifier of the album.
        title (str): Album title.
        artist (Artist): Artist who created the album.
        release_year (int): Year of release.
        tracks (list[AlbumTrack]): Tracks that belong to the album.
    """

    def __init__(self, album_id, title, artist, release_year):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track):
        """
        Adds a track to the album and assigns this album to the track.

        Tracks are automatically sorted by their track_number (expected for AlbumTrack).

        Args:
            track (AlbumTrack): Track to add.
        """
        track.album = self
        self.tracks.append(track)

        # Keep tracks ordered by track number inside the album
        self.tracks.sort(key=lambda t: t.track_number)

    def track_ids(self):
        """
        Returns a set of all track IDs in the album.

        Returns:
            set: Unique track IDs.
        """
        ids = set()

        for track in self.tracks:
            ids.add(track.track_id)

        return ids

    def duration_seconds(self):
        """
        Calculates total duration of the album.

        Returns:
            int: Total duration in seconds.
        """
        total = 0

        for track in self.tracks:
            total = total + track.duration_seconds

        return total