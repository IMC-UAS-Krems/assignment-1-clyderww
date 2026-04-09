from abc import ABC
class Track(ABC):
    """
    Base class representing any playable track on the platform.

    Attributes:
        track_id (int | str): Unique identifier.
        title (str): Track title.
        duration_seconds (int): Duration of the track.
        genre (str): Genre of the track.
        artist (Artist | None): Associated artist (if applicable).
    """

    def __init__(self, track_id, title, duration_seconds, genre, artist=None):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre
        self.artist = artist

        # Automatically link track to artist if provided
        if artist:
            artist.add_track(self)

    def duration_minutes(self):
        """
        Converts duration to minutes.

        Returns:
            float: Duration in minutes.
        """
        return self.duration_seconds / 60

    def __eq__(self, other):
        """
        Tracks are considered equal if their track_id values match.
        """
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

    def __hash__(self):
        """
        Returns a hash based on track_id, enabling usage in sets and as dict keys.
        """
        return hash(self.track_id)


class Song(Track):
    """Represents a standard music track."""
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        super().__init__(track_id, title, duration_seconds, genre, artist)


class SingleRelease(Song):
    """
    Represents a single (standalone release).

    Attributes:
        release_date (datetime | date): Release date of the single.
    """
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date


class AlbumTrack(Song):
    """
    Represents a track that belongs to an album.

    Attributes:
        track_number (int): Position in the album.
        album (Album | None): Assigned when added to an album.
    """
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = None


class Podcast(Track):
    """
    Represents a podcast episode.

    Attributes:
        host (str): Host of the podcast.
        description (str): Episode description.
    """
    def __init__(self, track_id, title, duration_seconds, genre, host, description=""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description


class InterviewEpisode(Podcast):
    """
    Podcast episode with a guest interview.

    Attributes:
        guest (str): Guest featured in the episode.
    """
    def __init__(self, track_id, title, duration_seconds, genre, host, guest, description=""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.guest = guest


class NarrativeEpisode(Podcast):
    """
    Story-driven podcast episode.

    Attributes:
        season (int): Season number.
        episode_number (int): Episode number within the season.
    """
    def __init__(self, track_id, title, duration_seconds, genre, host, season, episode_number, description=""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number


class AudiobookTrack(Track):
    """
    Represents an audiobook segment.

    Attributes:
        author (str): Author of the book.
        narrator (str): Narrator of the audiobook.
    """
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator