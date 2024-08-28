from core.common import getTime


class User:
    def __init__(self, wallet):
        time = getTime()
        self.wallet: str = wallet
        self.startTime: int = time
        self.lastUpdate: int = time

    def getTotalTime(self) -> int:
        return getTime() - self.startTime

    def getUpdatedTime(self) -> int:
        return getTime() - self.lastUpdate

    def updateTime(self):
        self.lastUpdate = getTime()
