import requests
from dataclasses import dataclass
"""
Funcaptcha for Roblox!
"""

@dataclass
class RobloxKeys:
	PKEY: str
	URL: str


class KEYS_ROBLOX:
	Signup = RobloxKeys(PKEY = "A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F" ,
	                    URL = "https://www.roblox.com/?returnUrl=https%3A%2F%2Fwww.roblox.com%2Fsignup%2F")
	Login = RobloxKeys(PKEY = "476068BF-9607-4799-B53D-966BE98E2B81" , URL = "https://www.roblox.com/login")

	Action = RobloxKeys(PKEY = "63E4117F-E727-42B4-6DAA-C8448E9B137F" , URL = "https://www.roblox.com/")

class AuthenticatedSession(requests.Session):
	API_URL = "https://capbypass.com/api/createTask"

	def __init__ (self , Key, timeout=120):
		super().__init__()
		self.authentication_key = Key
		self.timeout = timeout

	def request (self , blob: str , proxy : str, PKEY_TYPE : RobloxKeys):
		payload = {
				"clientKey": self.authentication_key ,
				"task": {
					"type": "FunCaptchaTask" ,
					"websiteURL": PKEY_TYPE.URL ,
					"websitePublicKey": PKEY_TYPE.PKEY ,
					"websiteSubdomain": "roblox-api.arkoselabs.com" ,
					"data[blob]": blob ,
					"proxy": proxy
					}
				}
		if proxy is None:
			del payload['task']['proxy']
			payload[ 'task' ] = "FunCaptchaTaskProxyLess"

		# Continue with the original request method
		return super().request("POST" , AuthenticatedSession.API_URL , **{"json": payload , "timeout": self.timeout})

@dataclass
class CapBypassResponse:
	Token : str
	StatusCode: int
	Charged : bool
	Error : str = None

	def __post_init__(self):
		if self.StatusCode == 524:
			print("CapBypass Timed out before responding & you have been charged for it. Try increasing your timeout or wait until CapBypass is under less load.")

	def showError(self):
		if self.Error: print(self.Error)

	@staticmethod
	def importResponse(response):
		if response.json().get("solution") == None:
			return CapBypassResponse(
				Token = None,
				StatusCode = response.status_code,
				Charged = False
				)

		return CapBypassResponse(
			Token = response.json().get("solution" , { }).get("token" , None),
			StatusCode = response.status_code,
			Charged = True
			)
	@staticmethod
	def importError(errorType):
		return CapBypassResponse(
			Token = None,
			StatusCode = None,
			Charged = False,
			Error = errorType
			)


class fcbypass:

	def __init__ (self,
	              Key,
	              Timeout=120
	              ):
		self.session = AuthenticatedSession(Key,Timeout)

	def FunCaptchaTask (self , **kwargs):
		BLOB = kwargs.get("blob")
		if BLOB is None:
			print("You must submit a blob to solve a task!")
			return
		PROXY = kwargs.get("proxy")
		if PROXY is not None:
			if isinstance(PROXY,dict):
				if "http" in PROXY: PROXY = PROXY['http']
			elif isinstance(PROXY,str):
				if "http://" not in PROXY: PROXY = f"http://{PROXY}"

		PKEY_TYPE = None

		if kwargs.get("Signup") == True and PKEY_TYPE is None:
			PKEY_TYPE = KEYS_ROBLOX.Signup
		elif kwargs.get("Login") == True and PKEY_TYPE is None:
			PKEY_TYPE = KEYS_ROBLOX.Login
		elif kwargs.get("Action") == True and PKEY_TYPE is None:
			PKEY_TYPE = KEYS_ROBLOX.Action

		if PKEY_TYPE is None:
			print("You must enter a taskType, (Signup=True) or (Login=True) or (Action=True)")
		else:
			try:
				return CapBypassResponse.importResponse(
					self.session.request(blob = BLOB , proxy = PROXY , PKEY_TYPE = PKEY_TYPE))
			except Exception as e:
				return CapBypassResponse.importError(e)



# Example usage
if __name__ == '__main__':
	fcbypass = FcBypass(
		Key=""
		)

	result = fcbypass.FunCaptchaTask(
		blob="blobby blob goes here",
		proxy="http://user:pass@ip:port",
		Signup = True
	                        )
	print(result.Token)
