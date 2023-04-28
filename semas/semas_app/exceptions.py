class UserDoesNotExists(Exception):
    def __str__(self):
        return "User does not exists"


class WrongUserOrPassword(Exception):
    def __str__(self):
        return "Wrong user or password"

class UserIsBlocked(Exception):
    def __str__(self):
        return "User is blocked"

class NoFriendRequests(Exception):
    def __str__(self):
        return "No friend requests"

class NoFriends(Exception):
    def __str__(self):
        return "No friends"

class ForumExists(Exception):
    def __str__(self):
        return "Forum exists"