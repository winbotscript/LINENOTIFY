import requests

class LineNotify:
    def __init__(self, token):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'notify-bot.line.me',
            'Referer': 'https://notify-bot.line.me/my/'
        }
        self.token = token

    def sendNotify(self, message):
        return self.session.post('https://notify-api.line.me/api/notify', headers={**self.headers, **{'Authorization': 'Bearer %s' % (self.token)}}, params={'message': message}).json()

    def revokeToken(self):
        return self.session.post('https://notify-api.line.me/api/revoke', headers={**self.headers, **{'Authorization': 'Bearer %s' % (self.token)}}).json()
        
class LineNotifyPersonal:
    def __init__(self, token, SESSION):
        self.token = token
        self.session = requests.session()
        for key, value in {'XSRF-TOKEN': token, 'SESSION': SESSION}.items():
            self.session.cookies.set_cookie(requests.cookies.create_cookie(key, value))

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'notify-bot.line.me',
            'Referer': 'https://notify-bot.line.me/my/'
        }

    def groupList(self, page=1):
        return self.session.get('https://notify-bot.line.me/api/groupList', headers=self.headers, params={'page': page}).json()

    def issuePersonalAcessToken(self, description, targetMid, targetType="GROUP"):
        data = {
            "action": "issuePersonalAcessToken",
            "description": description,
            "targetType": targetType,
            "targetMid": targetMid,
            "_csrf": self.token
        }
        return self.session.post('https://notify-bot.line.me/my/personalAccessToken', headers=self.headers, data=data).json()

    def createLineNotify(self, name, groupName):
        mid = [group['mid'] for group in self.groupList()['results'] if group['name'] == groupName]
        if not mid:
            raise Exception('can\' find group name')
        return LineNotify(self.issuePersonalAcessToken(name, mid[0])['token'])

if __name__ == '__main__':
    client = LineNotifyPersonal('140c9ad5-xxxx-xxxx-xxxx-ce97d5434ff3', 'YzQxODQ3NDgtNGIyNS00OWFkLThiYzQtZDAxYzg1NDkzN2E3')
    HelloWorld = client.createLineNotify('HelloWorld', 'RESEARCH')
    print(HelloWorld.sendNotify(HelloWorld.token))
    print(HelloWorld.revokeToken())