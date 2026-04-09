class ListeningSession:
    """
    Represents a listening session of a user for a specific track.

    Attributes:
        session_id (int | str): Unique session identifier.
        user (User): User who listened.
        track (Track): Track that was played.
        timestamp (datetime): When the session occurred.
        duration_listened_seconds (int): Actual listened time (not full track length).
    """

    def __init__(self, session_id, user, track, timestamp, duration_listened_seconds):
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds

    def duration_listened_minutes(self):
        """
        Converts listened duration to minutes.

        Returns:
            float: Duration in minutes.
        """
        return self.duration_listened_seconds / 60