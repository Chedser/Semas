from enum import Enum


class Response(Enum):
    SUCCESS = 0
    SUCCESS = 0
    WRONG_USER_OR_PASSWORD = 2
    USER_EXISTS = 3
    UNKNOWN_ERROR = 4
    USER_IS_BLOCKED = 5

class ForumCreateResponse(Enum):
    SUCCESS = 0
    WRONG_INPUT = 1
    FORUM_EXISTS = 2
    UNKNOWN_ERROR = 3


class Sex(Enum):
    MALE = 0
    FEMALE = 1
    UNDEFINED = 2

class FriendStatus(Enum):
    UNAUTHED = 0 #Не авторизованы
    SAME_PAGE = 1 #Сидим на своей странице
    NOT_FRIEND = 2 #В друзьях нет, в заявках тоже
    CANCEL_REQUEST = 3 #Заявку отправил куки-юзер. Отменить Заявку
    DECLINE_REQUEST = 4 #Заявку отправил тот, у которого сидим. Отменить или принять заявку
    IS_FRIEND = 5 #Друзья
    UNKNOWN_ERROR = 6 #Неизвестная ошибка
