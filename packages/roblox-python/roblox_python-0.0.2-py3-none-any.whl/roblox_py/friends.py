import httpx 

class friends:

    @staticmethod
    def user_friends(
        id:int
    ):

        url = f"https://friends.roblox.com/v1/users/{id}/friends"

        with httpx.Client() as client:
            response = client.get(url).json()

            class FriendsObject:

                def __init__(
                    self, response
                ):
                    self.response = response['data']

                def __str__(self):
                    return str(self.response)

                def isOnline(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['isOnline']
                    return jsoned 

                def all_user(
                    self
                ):
                    jsoned = []
                    for i in self.response:
                        jsoned.append(i['id'])
                    return jsoned 

                def name(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['name']
                    return jsoned 

                def displayName(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['displayName']
                    return jsoned 

                def created(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['created']
                    return jsoned 

                def externalAppDisplayName(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['externalAppDisplayName']
                    return jsoned 

                def isBanned(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['isBanned']
                    return jsoned 

                def description(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['description']
                    return jsoned 

                def friendFrequentRank(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['friendFrequentRank']
                    return jsoned 

                def friendFrequentScore(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['friendFrequentScore']
                    return jsoned 

                def isDeleted(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['isDeleted']
                    return jsoned 

                def hasVerifiedBadge(
                    self
                ):
                    jsoned = {}
                    for i in self.response:
                        jsoned[i['id']] = i['hasVerifiedBadge']
                    return jsoned 

            return FriendsObject(response)
