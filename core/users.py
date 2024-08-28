from core.user import User
from apscheduler.schedulers.background import BackgroundScheduler
from core.controller import Controller, Collection
from core.common import getTime
from bson.json_util import dumps
import json


class Users:
    unActiveTime: int = 1000 * 60 * 10
    active: list[User] = []
    scheduler: BackgroundScheduler = BackgroundScheduler()
    controller: Controller

    def __init__(self, controller: Controller) -> None:
        self.scheduler.add_job(func=self.validateActiveUsers,
                               trigger="interval", seconds=20)

        self.scheduler.start()
        self.controller = controller

    def addNewUser(self, user: User) -> bool:
        if type(user) is not User:
            return False

        activeIndex = self.isActiveUser(user)

        if activeIndex is not None:
            self.active[activeIndex].updateTime()
            return False

        self.addUserOnDB(user.wallet)
        self.active.append(user)

        return True

    def removeUser(self, wallet: str) -> bool:
        for index, user in enumerate(self.active):
            if user.wallet == wallet:
                self.addUserTimeLog(user.wallet, user.getTotalTime())
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

    def addUserOnDB(self, wallet: str) -> None:
        if self.findUserOnDB(wallet) != None:
            return

        collection = self.controller.collection(Collection.USERS)
        collection.insert_one({"wallet": wallet, "date": getTime()})

    def findUserOnDB(self, wallet: str) -> dict | None:
        collection = self.controller.collection(Collection.USERS)
        result = collection.find_one({}, {"wallet": wallet})
        return result

    def addUserTimeLog(self, wallet: str, totalTime: int) -> None:
        # FIXME - The users who dont send the exit request will add a unactive time log on the database
        # It can be fixed reducing the unactive time but it can be dangerous in the client side because the session can ends
        # when the users is active without making actions so 10 minutes is good

        collection = self.controller.collection(Collection.TIME_LOGS)

        collection.insert_one({
            "wallet": wallet,
            "sessionTime": totalTime,
            "date": getTime()
        })

    def getTimeLogs(self) -> list[dict] | None:
        oneDay = getTime() - (1000 * 60 * 60 * 24)
        collection = self.controller.collection(Collection.TIME_LOGS)
        return [json.loads(dumps(x)) for x in collection.find({"date": {"$gte": oneDay}})]
