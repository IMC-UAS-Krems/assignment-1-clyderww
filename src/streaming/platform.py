from .tracks import Song
from datetime import datetime, timedelta

from .users import PremiumUser, FamilyAccountUser, FamilyMember
from .playlists import CollaborativePlaylist

class StreamingPlatform:
    """
    Central class representing the streaming platform.

    Stores and manages all core entities such as users, tracks, albums,
    playlists, and listening sessions. Also provides analytical methods
    based on user activity.
    """

    def __init__(self, name):
        """
        Initializes the platform.

        Args:
            name (str): Name of the platform.
        """
        self.name = name
        self.users = []
        self.artists = []
        self.tracks = []
        self.albums = []
        self.playlists = []
        self.sessions = []

    def add_user(self, user):
        """Adds a user to the platform."""
        self.users.append(user)

    def add_artist(self, artist):
        """Adds an artist to the platform."""
        self.artists.append(artist)

    def add_track(self, track):
        """Adds a track to the platform."""
        self.tracks.append(track)

    def add_album(self, album):
        """Adds an album to the platform."""
        self.albums.append(album)

    def add_playlist(self, playlist):
        """Adds a playlist to the platform."""
        self.playlists.append(playlist)

    def add_session(self, session):
        """
        Adds a listening session to the platform and links it to the user.

        Args:
            session (ListeningSession): Session to add.
        """
        self.sessions.append(session)

        # Maintain bidirectional relationship (platform ↔ user)
        session.user.add_session(session)

    def all_users(self):
        """
        Returns all users including family sub-users.

        FamilyAccountUser contains additional sub-users which are included
        in the result.

        Returns:
            list[User]: All users on the platform.
        """
        result = []

        for user in self.users:
            result.append(user)

            # Include family members if user is a family account owner
            if isinstance(user, FamilyAccountUser):
                for sub in user.sub_users:
                    result.append(sub)

        return result

    def total_listening_time_minutes(self, start, end):
        """
        Calculates total listening time within a time range.

        Args:
            start (datetime): Start of the interval.
            end (datetime): End of the interval.

        Returns:
            float: Total listening time in minutes.
        """
        total_seconds = 0

        for s in self.sessions:
            if start <= s.timestamp <= end:
                total_seconds += s.duration_listened_seconds

        if total_seconds == 0:
            return 0.0

        return total_seconds / 60

    def avg_unique_tracks_per_premium_user(self, days=30):
        """
        Calculates the average number of unique tracks listened to by
        premium users within a given time window.

        Args:
            days (int): Number of days to look back.

        Returns:
            float: Average number of unique tracks per premium user.
        """
        premium_users = []

        for u in self.users:
            if isinstance(u, PremiumUser):
                premium_users.append(u)

        if len(premium_users) == 0:
            return 0.0

        cutoff = datetime.now() - timedelta(days=days)

        values = []

        for user in premium_users:
            unique_tracks = set()

            for s in user.sessions:
                if s.timestamp >= cutoff:
                    unique_tracks.add(s.track.track_id)

            values.append(len(unique_tracks))

        total = 0

        for v in values:
            total += v

        return total / len(values)

    def track_with_most_distinct_listeners(self):
        """
        Finds the track listened to by the highest number of unique users.

        Returns:
            Track | None: Most popular track or None if no sessions exist.
        """
        if len(self.sessions) == 0:
            return None

        track_users = {}

        # Map track_id → set of unique user_ids
        for s in self.sessions:
            track_id = s.track.track_id
            user_id = s.user.user_id

            if track_id not in track_users:
                track_users[track_id] = set()

            track_users[track_id].add(user_id)

        most_track_id = None
        max_count = 0

        for track_id in track_users:
            count = len(track_users[track_id])

            if count > max_count:
                max_count = count
                most_track_id = track_id

        # Find actual Track object by ID
        for track in self.tracks:
            if track.track_id == most_track_id:
                return track

        return None

    def avg_session_duration_by_user_type(self):
        """
        Calculates average session duration grouped by user type.

        Returns:
            list[tuple[str, float]]: List of (user_type, avg_seconds),
            sorted in descending order of duration.
        """
        data = {}

        for s in self.sessions:
            user_type = type(s.user).__name__

            if user_type not in data:
                data[user_type] = []

            data[user_type].append(s.duration_listened_seconds)

        results = []

        for user_type in data:
            durations = data[user_type]

            total = 0

            for d in durations:
                total += d

            avg_seconds = (total / len(durations))

            results.append((user_type, avg_seconds))

        # Sort from longest average sessions to shortest
        results.sort(key=lambda x: x[1], reverse=True)

        return results

    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        """
        Calculates total listening time for underage family members.

        Args:
            age_threshold (int): Maximum age to be considered underage.

        Returns:
            float: Total listening time in minutes.
        """
        total_seconds = 0

        for user in self.all_users():
            if isinstance(user, FamilyMember) and user.age < age_threshold:
                total_seconds += user.total_listening_seconds()

        if total_seconds == 0:
            return 0.0

        return total_seconds / 60

    def top_artists_by_listening_time(self, n=3):
        """
        Returns top N artists based on total listening time.

        Only Song instances with a non-null artist are considered.

        Args:
            n (int): Number of top artists to return.

        Returns:
            list[tuple[Artist, int]]: (artist, total_seconds).
        """
        artist_seconds = {}

        for s in self.sessions:
            if isinstance(s.track, Song) and s.track.artist:
                artist_id = s.track.artist.artist_id

                if artist_id not in artist_seconds:
                    artist_seconds[artist_id] = 0

                artist_seconds[artist_id] += s.duration_listened_seconds

        results = []

        for artist in self.artists:
            seconds = artist_seconds.get(artist.artist_id, 0)

            if seconds > 0:
                results.append((artist, seconds))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:n]

    def user_top_genre(self, user_id):
        """
        Determines the most listened genre for a given user.

        Args:
            user_id (int | str): Target user ID.

        Returns:
            tuple[str, float] | None:
                (genre, percentage of listening time) or None if no data.
        """
        user = None

        for u in self.all_users():
            if u.user_id == user_id:
                user = u
                break

        if not user or len(user.sessions) == 0:
            return None

        genre_seconds = {}

        for s in user.sessions:
            genre = s.track.genre

            if genre not in genre_seconds:
                genre_seconds[genre] = 0

            genre_seconds[genre] += s.duration_listened_seconds

        total = 0

        for g in genre_seconds:
            total += genre_seconds[g]

        if total == 0:
            return None

        top_genre = None
        max_seconds = 0

        for g in genre_seconds:
            if genre_seconds[g] > max_seconds:
                max_seconds = genre_seconds[g]
                top_genre = g

        percentage = (max_seconds / total) * 100

        return (top_genre, percentage)

    def collaborative_playlists_with_many_artists(self, threshold=3):
        """
        Finds collaborative playlists containing tracks from many artists.

        Args:
            threshold (int): Minimum number of distinct artists.

        Returns:
            list[CollaborativePlaylist]: Matching playlists.
        """
        result = []

        for playlist in self.playlists:
            if isinstance(playlist, CollaborativePlaylist):

                artists = set()

                for track in playlist.tracks:
                    if track.artist:
                        artists.add(track.artist)

                if len(artists) >= threshold:
                    result.append(playlist)

        return result

    def avg_tracks_per_playlist_type(self):
        """
        Calculates average number of tracks per playlist type.

        Returns:
            dict[str, float]: Mapping of playlist type to average size.
        """
        data = {}

        for playlist in self.playlists:
            playlist_type = type(playlist).__name__

            if playlist_type not in data:
                data[playlist_type] = []

            data[playlist_type].append(len(playlist.tracks))

        result = {}

        for playlist_type in ["Playlist", "CollaborativePlaylist"]:
            values = data.get(playlist_type, [])

            if len(values) == 0:
                result[playlist_type] = 0.0
            else:
                total = 0

                for v in values:
                    total += v

                result[playlist_type] = total / len(values)

        return result

    def users_who_completed_albums(self):
        """
        Finds users who have listened to every track of at least one album.

        Returns:
            list[tuple[User, list[str]]]:
                Each tuple contains a user and a list of completed album titles.
        """
        result = []

        for user in self.all_users():
            listened_ids = user.unique_tracks_listened()

            completed = []

            for album in self.albums:
                album_ids = set()

                for t in album.tracks:
                    album_ids.add(t.track_id)

                # Check if user listened to all tracks of the album
                if len(album_ids) > 0 and album_ids.issubset(listened_ids):
                    completed.append(album.title)

            if len(completed) > 0:
                result.append((user, completed))

        return result