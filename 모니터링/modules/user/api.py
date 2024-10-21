import requests
import modules.user.utils as utils

from info import Info

URI = Info.baseURL_API
AUTH_URL =Info.AUTH_URL



class Api_SH():
    def __init__(self):

        # self.URL = url
        self.get_jwt()

    def _getUserInfo(self) ->dict:
        return Info.UserInfo
    
    def get_jwt(self):
        response = requests.post(AUTH_URL, self._getUserInfo() )
        res = response.json()
        self.refresh = res['refresh']
        self.access = res['access']
        utils.pprint(res)


        # tokenSplit = self.access.split('.')
        # print (base64.b64decode(tokenSplit[1]) )
        # decode = json.loads((base64.b64decode(tokenSplit[1])).decode('utf-8'))
        # print (decode)

    def getlist(self, url):
        header = {
                'Authorization'  : 'JWT '+ self.access

        }
        response = requests.get( URI+url, headers=header)
        utils.pprint(response.json())
        return response.json()
        
    def patch(self, url, data):
        header = {
                'Authorization'  : 'JWT '+ self.access

        }
        response = requests.patch(url=URI+url, data=data, headers=header )
        # print (response)
        return response.json()

# api= Api_SH(AUTH_URL)
# api.get_jwt()
# result = api.getlist(URI+ 'api/users/users/?page_size=0')
# print ( result )
# print ( len(result))

