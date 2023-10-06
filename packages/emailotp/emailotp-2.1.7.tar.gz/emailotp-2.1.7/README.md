
# emailotp
Email otp simplifies email integration in Python, enabling users to send emails, facilitate OTP verification,  Enhance your app's email functionality effortlessly.
## Example

```python
from emailotp import emailotp
emailotp = emailotp()
responseFromEmailOtp = emailotp.send("toemail@gmail.com")
print(responseFromEmailOtp["message"])

``` 
## -- methods

```python
emailotp = emailotp()
responseFromEmailOtp = emailotp.sendOtp("toemail@gmail.com",123456)
print(responseFromEmailOtp["message"])
   

``` 

```python
emailotp = emailotp()
responseFromEmailOtp = emailotp.sendMessage("toemail@gmail.com","title","subject","body")
print(responseFromEmailOtp["message"])

``` 

```python
emailotp = emailotp()
responseFromEmailOtp = emailotp.custom("fromemail@gmail.com","passkey","toemail@gmail.com","title","subject","body")
print(responseFromEmailOtp["message"])

``` 




##  help
```python
emailotp = emailotp()
emailotp.help()

``` 
## Authors

- [SHAIK AFRID](https://www.github.com/afriddev)



## Getting Started

For help getting started with Python, view our online
[documentation](https://docs.python.org/3/).
