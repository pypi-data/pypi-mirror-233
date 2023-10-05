# FcBypass
A python module to get Funcaptcha tokens from capbypass

**Create a FcBypass instance**
```python
import FcBypass
fcbypass = FcBypass.Solver(Key="ENTER_YOUR_CAPBYPASS_KEY_HERE")
```
The variable ```fcbypass``` can then be used multiple times to fetch tokens from capbypass.

# Use cases

### Signup:
```python
response = fcbypass.FunCaptchaTask(
    blob = "Submit your blob String here",
    proxy = "http://username:password@ip:port",
    Signup = True
                        )
print(response.Token)
```

### Login:
```python
response = fcbypass.FunCaptchaTask(
    blob = "Submit your blob String here",
    proxy = "http://username:password@ip:port",
    Login = True
                        )
print(response.Token)
```

### Action:
```python
response = fcbypass.FunCaptchaTask(
    blob = "Submit your blob String here",
    proxy = "http://username:password@ip:port",
    Action = True
                        )
print(response.Token)
```


Your response.Token 
