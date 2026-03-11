class User:
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        total = 0

        for session in self.sessions:
            total += session.duration_listened_seconds

        return total

    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self):
        tracks = set()

        for session in self.sessions:
            tracks.add(session.track.track_id)

        return tracks

class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6

class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start=None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start

class FamilyAccountUser(PremiumUser):
    def __init__(self, user_id, name, age, subscription_start=None):
        super().__init__(user_id, name, age, subscription_start)

        self.sub_users = []

    def add_sub_user(self, sub_user):
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)

    def all_members(self):
        members = [self]

        for u in self.sub_users:
            members.append(u)

        return members

class FamilyMember(User):
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent
