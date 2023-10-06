"""
------------------------------------------------------------
|               author  : shaik afrid                      |
|               github  : @afriddev                        |
|               license : MIT (shaik afrid ,2023)          |
-------------------------------------------------------------

------------- Server Post Response Format -------------------
|            fromEmail:str | None = defaultEmail            |
|            toEmail:str                                    |  
|            title:str     | None == defaultFromTitle       |
|            subject:str   | None == defaultSubject         |
|            body:str      | None == defaultBody            |
|            passkey:str   | None == None                   |
-------------------------------------------------------------

"""

#importing requests for api requests
import requests
import re
#initalizing server urls
server = "https://sendemail.cyclic.app/"
url = "https://sendemail.cyclic.app/sendEmail"
emailRegexPattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
# class with emailotp name
class emailotp:
    """
    
    help method

    """
    def help(self):
        help = """  

------------------------------------------------------------
|               author  : shaik afrid                      |
|               github  : @afriddev                        |
|               license : MIT (shaik afrid ,2023)          |
------------------------------------------------------------


-> USAGE EMAIL SENDER

  1. Initalize emailotp
  2. Initalize a method from emailotp
  3. Get output

-> Rules for usage

  4. toEmail must be initalize for sending email
  5. You cannot use password to send custom message you need to provide passkey , for more. visit : https://support.google.com/accounts/answer/13548313?hl=en
  6. If you dont fill other fileds api will automatically fill default data except toEmail

-> Examples usage

  > emailsender = emailotp()
  > responseFromEmailOtp = emailsender.send("toemail@gmail.com);
  > print(responseFromEmailOtp)

-> Methods

  > help()
  > send()
  > sendOtp()
  > sendMessage()
  > custom()
  

"""
        print(help)

    """
    
    checking server for running or 
    undermaintenance
    
    """
    def checkServer(self):
        response = requests.get(server)
        jsonResponse = response.json()["message"]
        if(jsonResponse["serverStatus"] == "running"):
            return True
        else:
            return False
    """
    
    checking email is valid or not 
    if valid return True
    ese return False
    
    """
    def checkEmail(self,email):
        if(re.fullmatch(emailRegexPattern,email)):
            return True
        else:
            return False


    """
    
    simple send method require only to email
    all are default
    
    """
    def send(self,toEmail:str):
        if(emailotp().checkEmail(toEmail)):
            if(emailotp().checkServer()):
                try:
                    response = requests.post( url,json={"toEmail": toEmail})
                    if(response.json()["message"] == "emailSendFailed"):
                        return {
                            "message":"emailSendFailed"
                            }
                    else:
                        return response.json()
            
                except:
                    return {"message":"somethingWrong"}
            else:
                return {"message":"serverUnderMaintenance"}
        else:
            return {"message":"wrongEmail"}
    """

    emailOtp method requires two params
    email 
    otp
    example 
        .sendOtp("toemail@gmail.com",123456)

    """
    def sendOtp(self,toEmail:str,otp:int):
        if(emailotp().checkEmail(toEmail)):
            if(emailotp().checkServer()):
                try:
                    response = requests.post( url,json={"toEmail": toEmail,
                    "body":"Your verification code is - {} ".format(otp)
                    })
                    if(response.json()["message"] == "emailSendFailed"):
                        return {
                            "message":"emailSendFailed"
                            }
                    else:
                        return response.json()
            
                except:
                    return {"message":"somethingWrong"}
            else:
                return {"message":"serverUnderMaintenance"}
        else:
            return {"message":"wrongEmail"}

    """
    
    sendMessage method require 4 params
    toEmail,titile,subject,body
    example
        -> .sendMessage("toemail@gmail.com","testing","emailOtp","hello world!")
    
    """
    def sendMessage(self,toEmail:str,title:str,subject:str,body:str):
        if(emailotp().checkEmail(toEmail)):
            if(emailotp().checkServer()):
                try:
                    response = requests.post( url,json={"toEmail": toEmail,
                    "title":title,
                    "subject":subject,
                    "body":body
                    })
                    if(response.json()["message"] == "emailSendFailed"):
                        return {
                            "message":"emailSendFailed"
                            }
                    else:
                        return response.json()
            
                except:
                    return {"message":"somethingWrong"}
            else:
                return {"message":"serverUnderMaintenance"}
        else:
            return {"message":"wrongEmail"}
    """
    
    sendMessage method require 6 params
    fromEmail,passkey,toEmail,titile,subject,body
    example
        -> .sendMessage("fromemail@gmail.com","16digitspasskey",
        "toemail@gmail.com",
        "testing","emailOtp","hello world!")
    
    """
    def custom(self,fromEmail:str,passkey:str,
    toEmail:str,title:str,subject:str,body:str):
        if(emailotp().checkEmail(toEmail)):
            if(emailotp().checkServer()):
                try:
                    response = requests.post( url,json={
                    "fromEmail":fromEmail,
                    "passkey":passkey,    
                    "toEmail": toEmail,
                    "title":title,
                    "subject":subject,
                    "body":body
                    })
                    if(response.json()["message"] == "emailSendFailed"):
                        return {
                            "message":"emailSendFailed"
                            }
                    else:
                        return response.json()
            
                except:
                    return {"message":"somethingWrong"}
            else:
                return {"message":"serverUnderMaintenance"}
        else:
            return {"message":"wrongEmail"}
       
"""
emailotp class successfully created

"""

