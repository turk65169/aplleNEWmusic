# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", "28334973"))
        self.API_HASH = getenv("API_HASH", "68b64929f2fb5a95e96cd21a306375f7")

        self.BOT_TOKEN = getenv("BOT_TOKEN", "8284340154:AAH07G9K1e6Lb3LbmTYm9kZj51KlYqVwses")
        self.MONGO_URL = getenv("MONGO_URL", "mongodb+srv://mongoguess:guessmongo@cluster0.zcwklzz.mongodb.net/?retryWrites=true&w=majority")

        self.LOGGER_ID = int(getenv("LOGGER_ID", "-1003695016820"))
        self.OWNER_ID = int(getenv("OWNER_ID", "6143754072"))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 500)) * 60
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 50))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 20))

        self.SESSION1 = getenv("SESSION", "AQGwW30AvuaK1wbi9SzKGppACEJL_80yOxH0WrTa_4KZGaMQJllNOflely1n6wrGzNRxArNm062ucDxGGHtYHOsltDByrPyHboDo-yzJ6omM2nZTPzsSFhy4ogIWa8np85C-19PbWYdi3zJMV_IwNJBbu4uzwUOgMA9t9Zd4wm4b0tJORa4yYRX1PXfS9fmznnfyknRD9P0AFwH0uXmFZ5qukJ_QyH1Pi5oH5BiokLEvVL2GjGqm3Fja8wZVANwzD8Fxztk5bdBo8zFXday27Ak5Wj9RGs0tGBoCaP5PhcisvqVkkwaVGMvz7X09l7-EPXOpW-K2fw7zgcbb-QkEtC8e-4QamAAAAAHtamkKAA")
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/tr_telegrammarket")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/goygoy_chat")

        def parse_bool(key: str, default: bool) -> bool:
            val = getenv(key)
            if val is None:
                return default
            return str(val).lower() in ["true", "1", "yes"]

        self.AUTO_END: bool = parse_bool("AUTO_END", False)
        self.AUTO_LEAVE: bool = parse_bool("AUTO_LEAVE", False)
        self.VIDEO_PLAY: bool = parse_bool("VIDEO_PLAY", True)
        self.COOKIES_URL = [
            url for url in getenv("COOKIES_URL", "https://batbin.me/skinneries").split(" ")
            if url and "batbin.me" in url
        ]
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://te.legra.ph/file/3e40a408286d4eda24191.jpg")
        self.PING_IMG = getenv("PING_IMG", self.DEFAULT_THUMB) or self.DEFAULT_THUMB
        self.START_IMG = getenv("START_IMG", self.DEFAULT_THUMB) or self.DEFAULT_THUMB

    def check(self):
        missing = [
            var
            for var in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID", "SESSION1"]
            if not getattr(self, var)
        ]
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
