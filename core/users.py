from core.user import User
from apscheduler.schedulers.background import BackgroundScheduler
from core.common import getTime


class Users:
    unActiveTime: int = 1000 * 60 * 2
    active: list[User] = []
    scheduler: BackgroundScheduler = BackgroundScheduler()

    def __init__(self) -> None:
        self.scheduler.add_job(func=self.validateActiveUsers,
                               trigger="interval", seconds=20)

        self.scheduler.start()

    def addNewUser(self, user: User) -> bool:
        if type(user) is not User:
            return False

        activeIndex = self.isActiveUser(user)

        if activeIndex is not None:
            self.active[activeIndex].updateTime()
            return False

        self.active.append(user)

        return True

    def removeUser(self, wallet: str) -> bool:
        for index, user in enumerate(self.active):
            if user.wallet == wallet:
                self.active.pop(index)
                return True

        return False

    def isActiveUser(self, newUser: User) -> None | int:
        for index, user in enumerate(self.active):
            if user.wallet == newUser.wallet:
                return index

        return None

    def getActiveUsersJSON(self) -> list[dict]:
        return [x.__dict__ for x in self.active]

    def validateActiveUsers(self) -> None:
        if len(self.active) == 0:
            return

        for user in self.active:
            if user.getUpdatedTime() >= self.unActiveTime:
                self.removeUser(user.wallet)
                print("Remove user by auto detection "+user.wallet+".")
