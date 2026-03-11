from datetime import datetime, timedelta

from .users import PremiumUser, FamilyAccountUser, FamilyMember
from .playlists import CollaborativePlaylist

class StreamingPlatform:

    def __init__(self, name):
        self.name = name
        self.users = []
        self.artists = []
        self.tracks = []
        self.albums = []
        self.playlists = []
        self.sessions = []

    def add_user(self, user):
        self.users.append(user)

    def add_artist(self, artist):
        self.artists.append(artist)

    def add_track(self, track):
        self.tracks.append(track)

    def add_album(self, album):
        self.albums.append(album)

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def add_session(self, session):
        self.sessions.append(session)
        session.user.add_session(session)

    def all_users(self):
        result = []

        for user in self.users:
            result.append(user)

            if isinstance(user, FamilyAccountUser):
                for sub in user.sub_users:
                    result.append(sub)

        return result

    def total_listening_time_minutes(self, start, end):
        total_seconds = 0

        for s in self.sessions:
            if start <= s.timestamp <= end:
                total_seconds += s.duration_listened_seconds

        if total_seconds == 0:
            return 0.0

        return total_seconds / 60

    def avg_unique_tracks_per_premium_user(self, days=30):
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
        if len(self.sessions) == 0:
            return None

        track_users = {}

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

        for track in self.tracks:
            if track.track_id == most_track_id:
                return track

        return None

    def avg_session_duration_by_user_type(self):
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

            avg_minutes = (total / len(durations)) / 60

            results.append((user_type, avg_minutes))

        results.sort(key=lambda x: x[1], reverse=True)

        return results

    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        total_seconds = 0

        for user in self.all_users():
            if isinstance(user, FamilyMember) and user.age < age_threshold:
                total_seconds += user.total_listening_seconds()

        if total_seconds == 0:
            return 0.0

        return total_seconds / 60

    def top_artists_by_listening_time(self, n=3):
        artist_seconds = {}

        for s in self.sessions:
            if s.track.artist:
                artist_id = s.track.artist.artist_id

                if artist_id not in artist_seconds:
                    artist_seconds[artist_id] = 0

                artist_seconds[artist_id] += s.duration_listened_seconds

        results = []

        for artist in self.artists:
            seconds = artist_seconds.get(artist.artist_id, 0)

            if seconds > 0:
                results.append((artist, seconds / 60))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:n]

    def user_top_genre(self, user_id):
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
        result = []

        for user in self.all_users():
            listened_ids = user.unique_tracks_listened()

            completed = []

            for album in self.albums:
                album_ids = set()

                for t in album.tracks:
                    album_ids.add(t.track_id)

                if len(album_ids) > 0 and album_ids.issubset(listened_ids):
                    completed.append(album.title)

            if len(completed) > 0:
                result.append((user, completed))

        return result
