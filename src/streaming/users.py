class User:
    """
    Base class representing a platform user.

    Attributes:
        user_id (int | str): Unique identifier.
        name (str): User name.
        age (int): User age.
        sessions (list[ListeningSession]): Listening history.
    """

    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        """
        Adds a listening session to the user.

        Args:
            session (ListeningSession): Session to add.
        """
        self.sessions.append(session)

    def total_listening_seconds(self):
        """
        Calculates total listening time in seconds.

        Returns:
            int: Total seconds listened.
        """
        total = 0

        for session in self.sessions:
            total += session.duration_listened_seconds

        return total

    def total_listening_minutes(self):
        """
        Calculates total listening time in minutes.

        Returns:
            float: Total minutes listened.
        """
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self):
        """
        Returns unique track IDs listened by the user.

        Returns:
            set: Set of track IDs.
        """
        tracks = set()

        for session in self.sessions:
            tracks.add(session.track.track_id)

        return tracks


class FreeUser(User):
    """
    Represents a free-tier user with limitations.
    """
    MAX_SKIPS_PER_HOUR = 6


class PremiumUser(User):
    """
    Represents a premium user.

    Attributes:
        subscription_start (datetime | None): Subscription start date.
    """

    def __init__(self, user_id, name, age, subscription_start=None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    """
    Represents a family account owner with sub-users.

    Attributes:
        sub_users (list[FamilyMember]): Linked family members.
    """

    def __init__(self, user_id, name, age, subscription_start=None):
        super().__init__(user_id, name, age, subscription_start)

        self.sub_users = []

    def add_sub_user(self, sub_user):
        """
        Adds a family member to the account.

        Args:
            sub_user (FamilyMember): User to add.
        """
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)

    def all_members(self):
        """
        Returns all users in the family account including the owner.

        Returns:
            list[User]: Owner and all sub-users.
        """
        members = [self]

        for u in self.sub_users:
            members.append(u)

        return members


class FamilyMember(User):
    """
    Represents a sub-user within a family account.

    Attributes:
        parent (FamilyAccountUser): Parent account.
    """

    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent