from .storage import loadData, saveData

POINTS = "serverPoints"
ROLL20 = "roll20Name"
SLOTS = "characterSlots"
CHARACTERS = "characters"
CONTENT = "content"


class UserData:
    def __init__(self, serverID: int, userID: int):
        self.serverID = str(serverID)
        self.userID = str(userID)
        self.data = loadData()

        # Инициализация сервера
        if self.serverID not in self.data:
            self.data[self.serverID] = {}

        # Инициализация пользователя
        if self.userID not in self.data[self.serverID]:
            self.data[self.serverID][self.userID] = {}

        # Проверка и создание всех полей
        self._ensure_field(POINTS, 0)
        self._ensure_field(ROLL20, "[Empty]")
        self._ensure_field(SLOTS, 3)
        self._ensure_field(CHARACTERS, [])
        self._ensure_field(CONTENT, {"race": [], "class": [], "spell": []})

        self._save()

    def _ensure_field(self, key, default):
        if key not in self.data[self.serverID][self.userID]:
            self.data[self.serverID][self.userID][key] = default

    def _save(self):
        saveData(self.data)

    # ==== Доступ к любым полям через словарь ====
    def __getitem__(self, key):
        return self.data[self.serverID][self.userID].get(key, None)

    def __setitem__(self, key, value):
        self.data[self.serverID][self.userID][key] = value
        self._save()

    # ==== Очки ====
    @property
    def serverPoints(self):
        return self[POINTS]

    @serverPoints.setter
    def serverPoints(self, value):
        self[POINTS] = value

    # ==== Roll20 никнейм ====
    @property
    def roll20Name(self):
        return self[ROLL20]

    @roll20Name.setter
    def roll20Name(self, value):
        self[ROLL20] = value

    # ==== Слоты персонажей ====
    @property
    def characterSlots(self):
        return self[SLOTS]

    @characterSlots.setter
    def characterSlots(self, value):
        self[SLOTS] = value

    # ==== Персонажи ====
    @property
    def characters(self):
        return self[CHARACTERS]

    @characters.setter
    def characters(self, value):
        self[CHARACTERS] = value

    @property
    def content(self):
        return self[CONTENT]

    @content.setter
    def content(self, value):
        self[CONTENT] = value
