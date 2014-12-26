

'''
Read messages from inbox of gmail.

1. create connection object
(first study if there any encryption,used by your mail client)
2. provide username with connection object
3. provide password with connection object
4.Perform operations on your mailbox
    ex.
    stat() --> to get statistics
    retr() --> to retrive message
    further reading message etc.
5. close connection
'''

from poplib import POP3_SSL
import getpass #to hide password

username=raw_input("Enter your complete email-id:")
password=getpass.getpass("Enter your password:")

#1 create connection object
p=POP3_SSL('pop.gmail.com') #gmail uses SSL

#2 provide username
p.user(username)

#3 provide password
p.pass_(password)
#Here you get output '+OK Welcome'

#4 Perform necessary operations
p.stat() #shows inbox statistics
rsp,msg,siz = p.retr(1) #retriving first message in inbox
#reading message
for content in msg:
    print content

#5 close connection
p.quit()
