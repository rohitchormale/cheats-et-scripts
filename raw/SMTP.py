'''
Send message using gmail
1. create connection object
(first study if there any encryption,used by your mail client)
2. here gmail uses tls encryption
so, start tls service
3. provide login credentials
4. sendmail
5. close connection

'''
from smtplib import SMTP
import getpass #to hide password
#1 create connection object
s = SMTP('smtp.gmail.com',587) #providing smtp port

#2 starting tls service
s.starttls() #tls encryption

username=raw_input("Enter your complete email-id:")
password=getpass.getpass("Enter your password:")

#3 providing login credentials
s.login(username,password)

#creating message option
fromaddr = username
toaddr = raw_input("Enter name of receiptant:")
message = raw_input("Enter your message:")

#4. sending message
s.sendmail(fromaddr,toaddr,message)

#5 close connection
s.quit()
