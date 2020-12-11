
# coding: utf-8

# In[7]:


import sys
from socket import *

# In[7]:
#ADDED------
#num = -4  
#END ADDED---------

remainingRecv = ''

#creates specific syntax error checks
def syntax_error(num):
    if num == -1:
        return "500 Syntax error: command unrecognized\r\n"

    if num == -2:
        return "501 Syntax error in parameters or arguments\r\n"

    if num == -3:
        return "503 Bad sequence of commands\r\n"

    if num == -4 or num == 1:
        return "250 OK\r\n"

    if num == -5:
        return "354 Start mail input; end with . on a line by itself\r\n"

# In[8]:


#check MAIL FROM:
def mail_from_cmd(l):
    if len(l) < 4:
        return -1

    if l[0:4] == 'RCPT':
        return -3
    elif l[0:4] == 'DATA':
        return -3
    elif l[0:4] != 'MAIL':
        return -1

    l = l[4:]

    #index = 4
    white = 0
    lenTest = 0

#changed
    while white >= 0:
        lenTest += 1
        #white = whitespace(l[index:index+lenTest])
        white = whitespace(l[0:lenTest])

    if lenTest == 1:
        return -1

    l = l[lenTest-1:]
#changed, changed from -1
    if len(l) < 5:
        return -2
#changed
    #if l[index:index+3] != 'TO:':
    if l[0:5] != 'FROM:':
        return -1

    #nullspace
    #changed
    l = l[5:]
    #l = l[index:]
    index = 0

    l = l.lstrip()

    #forward path and <>
    if len(l) == 0:
        #path error
        return -3

    if l[0] != '<':
        #path error
        return -3

    rightIndex = l.find('>')
    if(rightIndex == -1):
        #changed
        #return reversePath(l[index:])
        return -2

    reverse = reversePath(l[index:rightIndex+1])
    if reverse < 0:
        return reverse
    #nullspace pt 2
    l = l[rightIndex + 1:]
    index = 0

    l = l.lstrip()

    if len(l) != 0:
        return -2

    return -4


# In[9]:


#"RCPT" <whitespace> "TO:" <nullspace> <forward-path> <nullspace> <CRLF>
def rcpt_to_cmd(l):
#    return -4
    #checks if says RCPT TO:
    if len(l) < 4:
        return -1
    if l[0:4] == 'DATA':
        return -3
    elif l[0:4] == 'MAIL':
        return -3
    elif l[0:4] != "RCPT":
        return -1

    l = l[4:]

    #index = 4
    white = 0
    lenTest = 0

#changed
    while white >= 0:
        lenTest += 1
        #white = whitespace(l[index:index+lenTest])
        white = whitespace(l[0:lenTest])

    if lenTest == 1:
        return -1
#added!
 #   if lenTest > 2 and ((lenTest-1) % 4 != 0):
#        return -2

#added!
    #index = index + lenTest-1
#commented out!
    l = l[lenTest-1:]
#changed, changed from -1
    if len(l) < 3:
        return -2
#changed
    #if l[index:index+3] != 'TO:':
    if l[0:3] != 'TO:':
        return -1

    #nullspace
    #changed
    l = l[3:]
    #l = l[index:]
    index = 0

    l = l.lstrip()

    #forward path and <>
    if len(l) == 0:
        #path error
        return -3

    if l[0] != '<':
        #path error
        return -3

    #index = 0
    rightIndex = l.find('>')

    if(rightIndex == -1):
        #changed
        #return forwardPath(l)
        return -2
    #changed
    fpath = forwardPath(l[:rightIndex+1])
    #fpath = forwardPath(l[index:rightIndex+1])
    if fpath < 0:
        return fpath

    l = l[rightIndex + 1:]
    index = 0

    l = l.lstrip()

    if len(l) != 0:
        #newline error
        return -2

    return -4


# In[10]:


#"DATA" <nullspace> <CRLF>
def data_cmd(l):
    #checks DATA
    if len(l) < 4:
        return -1
    if l[0:4] == 'RCPT':
        return -3
    elif l[0:4] == 'MAIL':
        return -3
    elif l[0:4] != 'DATA':
        return -1

    #nullspace
    l = l[4:]

   # if len(l) > 1:
   #     if sp(l[0]) < 0:
   #         return -1

    l= l.lstrip()

    if len(l) > 0:
        return -2

    return -5


# In[11]:


#defines what whitespace is
def whitespace(s):
    if len(s) <= 1:
        return sp(s)
    space = sp(s[:1])
    if space < 0:
        return space
    whitesp = whitespace(s[1:])
    if whitesp < 0:
        return whitesp
    return space + whitesp


# In[12]:


#sp
def sp(c):
    if c == ' ' or c == '\t':
        return 1
    return -2


# In[13]:


def begin(s):
    found = False;
    length = 0

    while found == False and length < len(s):
        length += 1

        if mailbox(s[0:length]) > 0:
            found = True

    return found


# In[14]:


#checks reverse path
def reversePath(s):
    return path(s)


# In[15]:


#checks forward path
def forwardPath(s):
    return path(s)


# In[16]:


#path "<" <mailbox> ">"
def path(s):
    if len(s) < 1:
        #path error
        return -3
        #is this the correct error?

    if s[:1] != '<':
        #path error
        return -3

    if len(s) == 1:
        #character error
        return -2

    mailbo = s[1:]
    if mailbox(mailbo) > 0:
        #path error
        return -2

    mailbo = s[1:-1]
    mail = mailbox(mailbo)

    if mail < 0:
        if begin(mailbo):
            #path error
            return -2
        else:
            return mail

    if s[-1:] != '>':
        #path error
        return -2

    return 1 + mail + 1



# In[17]:


#mailbox
def mailbox(s):
    i = 0
    localPart = 0

    if len(s) == 0:
        #char error
        return -2

    while localPart >= 0 and i < len(s):
        i += 1
        localPart = local_part(s[0:i])

#        i -= 1
        if i == 0:
            #char error
            return -2

        if i == len(s):
            #mailbox error; trying something, changed from -1
            return -1

    i -= 1

    if s[i] != '@':
        #mailbox error; testing something changed from -1
        return -2

    dom = s[i+1:]

    isDom = domain(dom)

    if isDom < 0:
        return isDom

    return 1



#local-part
def local_part(s):
    return string(s)


#string
def string(s):
    if len(s) <= 1:
        return char(s)

    ch = char(s[:1])

    if ch < 0:
        return ch

    st = string(s[1:])

    if st < 0:
        return st
    
    return ch + st
    #return -2


#char
def char(c):
    if c == '':
        return -2

    if special(c) > 0:
        #char error
        return -2

    if sp(c) > 0:
        #char error
        return -2

    if null(c) > 0:
        #char error
        return -2

    if letter(c):
        return 1

    if digit(c):
        return 1

    return 1 if (ord(c) < 128) else 0


#domain
def domain(s):
    ele = element(s)
    if ele > 0:
        return ele

    dot = s.find('.')

    if(dot < 0):
        return ele

    stEle = element(s[:dot])

    if stEle < 0:
        return stEle

    doma = domain(s[dot+1:])

    if doma < 0:
        return doma

    return stEle + 1 + doma



#defines null
def null(c):
    if c == '':
        return 1
    return -2



#defines nullspace (null or whitespace)
def nullspace(c):
    nul = null(c)
    if nul == 0:
        return nul
    whtspc = whitespace(c)
    if whtspc > 0:
        return whtspc
    return -2



#creates newline
def CRLF(c):
    if c == '\r\n':
        return 1
    return -2



#special
def special(c):
    if c == '<':
        return 1
    if c == '>':
        return 1
    if c == '(':
        return 1
    if c == ")":
        return 1
    if c == "[":
        return 1
    if c == ']':
        return 1
    #I do not know how to declare this as a string
    if c == '\\':
        return 1
    if c == '.':
        return 1
    if c == ',':
        return 1
    if c == ';':
        return 1
    if c == ':':
        return 1
    if c == '@':
        return 1
    if c == '"':
        return 1
    if c == '?':
        return 1
    return -2



#any one of the ten digits 0 through 9
def digit(c):
    if c == '0':
        return 1
    if c == '1':
        return 1
    if c == '2':
        return 1
    if c == '3':
        return 1
    if c == '4':
        return 1
    if c == '5':
        return 1
    if c == '6':
        return 1
    if c == '7':
        return 1
    if c == '8':
        return 1
    if c == '9':
        return 1
    return -2



#<letter> any one of the 52 alphabetic characters A through Z in upper case and a through z in lower case
def letter(c):
    if c.lower() == 'a':
        return 1
    if c.lower() == 'b':
        return 1
    if c.lower() == 'c':
        return 1
    if c.lower() == 'd':
        return 1
    if c.lower() == 'e':
        return 1
    if c.lower() == 'f':
        return 1
    if c.lower() == 'g':
        return 1
    if c.lower() == 'h':
        return 1
    if c.lower() == 'i':
        return 1
    if c.lower() == 'j':
        return 1
    if c.lower() == 'k':
        return 1
    if c.lower() == 'l':
        return 1
    if c.lower() == 'm':
        return 1
    if c.lower() == 'n':
        return 1
    if c.lower() == 'o':
        return 1
    if c.lower() == 'p':
        return 1
    if c.lower() == 'q':
        return 1
    if c.lower() == 'r':
        return 1
    if c.lower() == 's':
        return 1
    if c.lower() == 't':
        return 1
    if c.lower() == 'u':
        return 1
    if c.lower() == 'v':
        return 1
    if c.lower() == 'w':
        return 1
    if c.lower() == 'x':
        return 1
    if c.lower() == 'y':
        return 1
    if c.lower() == 'z':
        return 1
    return -2


def letterDigit(c):
    dig = digit(c)
    if dig > 0:
        return dig

    let = letter(c)
    if let > 0:
        return let

    #added for letterdigithyphen
    if c == '-':
        return 1

    if c == '_':
        return 1

    return -2



def letDigStr(s):
    if len(s) <= 1:
        return letterDigit(s)

    letDig = letterDigit(s[:1])

    if letDig < 0:
        return letDig

    letDigString = letDigStr(s[1:])

    if letDigString < 0:
        return letDigString

    return letDig + letDigString


#<letter> <let-dig-str>
def name(s):
    #if the length of the string is 0, return the letter
    if len(s) == 0:
        return letter(s)
    #if the length of the string is 1, return the letter/digit
    if len(s) == 1:
        return letDigStr(s[1:])
    #let = the string at index through one
    let = letter(s[:1])

    #letdigstri = the string at index after one
    letDigStri = letDigStr(s[1:])

    #if letter less than 0, return letter
    if let < 0:
        return let
    #if letdigstri less than 0, return
    if letDigStri < 0:
        return letDigStri

    #return combination of both
    return let + letDigStri


#<letter> | <name>
def element(s):
    let = letter(s)

    if len(s) <= 1:
        return let

    if let > 0:
        return let

    nam = name(s)

    if nam > 0:
        return nam

    return nam


# In[34]:
def check_for_dot(l):
    #print(repr(l))
    #if len(l) != 2:
    #    return -1

    if l == '.\r\n' or l == '.':
        return -4

    return -1

def address(l):
    left = l.find('<')
    right = l.find('>')
    return l[left+1:right]



def contents(sEmail, tEmail, content):
   # print(f"s={sender}, t={to}, m={message}")
    #messag = sEmail
    messag = ''
    #for tos in tEmail:
    #    messag += 'RCPT TO: <' +  tos + '>\r\n'
    for frag in content:
        messag += frag
    for tos in tEmail:
        #tos.index should give me domain from @ to closing brace
        #make sure that forward directory exists mkdir forward 
        #with open('forward/<' +tos[tos.index('@'):tos.index('>')] + '>', 'a') as f:
        with open('forward/' +tos[tos.find('@'):], 'a') as f:
            f.write(messag)   


def recv(connectionSocket):
    global remainingRecv # = connectionSocket.recv(1024).decode()

    while "\r\n" not in remainingRecv:
        remainingRecv = connectionSocket.recv(1024).decode()

    l = remainingRecv[0:remainingRecv.find("\r\n")+2]
    remainingRecv = remainingRecv[remainingRecv.find("\r\n")+2:]

    return l

#def 
#global buffer initialized to empty string
#took that through carriage return newline
#add a single receipt chunk to that buffer
#split at that point, return first chunk

def main():
    #begin code from slideshow
    #do I hard code the Port number?; No, obtained from command line arguments

#GET HOSTNAME FOR THE GREETING AND CLOSING MESSAGE

    serverPort = int(sys.argv[1])
    #serverPort = int(sys.argv[0])
    #serverPort = 15355
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #create TCP welcoming socket
    try:
        serverSocket.bind(('',serverPort))
        #server begins listening for incoming TCP requests
        serverSocket.listen(1)
        #print "220 comp431-1sp20.cs.unc.edu"
        while True:
            #server waits on accept() for incoming requests, a new socket is created on return socket to server on port 15355

            #print "220 comp431-1sp20.cs.unc.edu"
            greeting = "220 " + gethostname() + "\r\n"#comp431-1sp20.cs.unc.edu " # + getHostName()
            #echo?
            #print(greeting)
            connectionSocket, addr = serverSocket.accept()
            connectionSocket.send(greeting.encode())
            #read bytes from socket

            #HELOreceived = False

            #while not HELOreceived:
            sentence = recv(connectionSocket)
    #        sentence = connectionSocket.recv(1024).decode()
       #    print(f"Server read {sentence} while waiting for HELO")
            #echo
            #changed and took end away? 
            print(sentence, end = '')
            
            if sentence == "HELO " + gethostname() + "\r\n":
                #print("acknowledging connection")
                acknowledge = "250 Hello " + gethostname() + " pleased to meet you\r\n"
                connectionSocket.send(acknowledge.encode())
                #echo?; client prints this
                #print(acknowledge)

            #capitalizedSentence = sentence.upper()
            #connectionSocket.send(ca10pitalizedSentence.encode())
            #close connection to this client (but not the welcoming socket)
#           connectionSocket.close()
        #end code from slideshow
        #sys.stdin.readline().rstrip('\n')
            QUITreceived = False;
            num = -4
            sender = ''
            to = []
            message = []
            position = 0
            #.readline() ?
            #l = connectionSocket.recv(1024).decode()
            #print(l)
            while not QUITreceived:
            #if QUITreceived == False:
                #print("in this loop")
                #it is only printing l one time, needs to print each time
                l = recv(connectionSocket)
                #l = connectionSocket.recv(1024).decode()

#                print(f"received: {repr(l)}")

                print(l, end = '')
                if l == "QUIT\r\n":
                    QUITreceived = True
                    #connectionSocket.close()

                else:
                #for l in sys.stdin:
                    #sys.stdout.write(l)
                    if position == 0:
                        num = mail_from_cmd(l)
                        codeResponse1 = syntax_error(num)
                        # print(syntax_error(mail_from_cmd(l)))
                        if codeResponse1 == '250 OK\r\n':
                            position = 1
                            sender = address(l)
                            message.append(l) 
                            QUITreceived = False
                            #print(f"sender set to {sender}")
                            connectionSocket.send(codeResponse1.encode())
                            #sys.stdout.write(codeResponse1)
                        else:
                            """sender = ''
                            to = []
                            message = []"""
                            position = 1
                            QUITreceived = False
                            rcpt = syntax_error(rcpt_to_cmd(l))
                            data = syntax_error(data_cmd(l))

                            #print out syntax errors
                            connectionSocket.send(codeResponse1.encode())
                            #sys.stdout.write(syntax_error(num))

                    elif position == 1:
                        #added
                        if l[0:4] == 'MAIL':
                            #position = 0
                            num = mail_from_cmd(l)
                            #print(num)
                            if num == -4:
                                position = 1
                                message.append(l)
                                sender = address(l)
                                QUITreceived = False
                                connectionSocket.send(syntax_error(num).encode())
                                #sys.stdout.write(syntax_error(num))
                            else:
                                """sender = ''
                                to = []
                                message = []"""
                                position = 1
                                connectionSocket.send(syntax_error(num).encode())
                                #sys.stdout.write(syntax_error(num))

                            continue
                        #end of added
                        num = rcpt_to_cmd(l)
                        codeResponse2 = syntax_error(num)
                        if codeResponse2 == '250 OK\r\n':
                            message.append(l)
                            to.append(address(l))
                            position = 2
                            QUITreceived = False
                            connectionSocket.send(codeResponse2.encode())
                            #sys.stdout.write(codeResponse2)

                        else:
                            fromC = syntax_error(data_cmd(l))
                            data = syntax_error(mail_from_cmd(l))
                            """sender = ''
                            to = []
                            message = []"""
                            position = 2
                            QUITreceived = False
                                #print out syntax errors; bad sequence of commands being printed here
                            connectionSocket.send(codeResponse2.encode())
                                #sys.stdout.write(syntax_error(num))

                    elif position == 2:
                        #added
                        #additional thought
                        if l[0:4] == 'MAIL':
                            num = mail_from_cmd(l)
                            if num == -4:
                                position = 1
                                message.append(l)
                                sender = address(l)
                                QUITreceived = False
                                connectionSocket.send(syntax_error(num).encode())
                                #sys.stdout.write(syntax_error(num))
                            else:
                                """sender = ''
                                to = []
                                message = []"""
                                position = 1
                                QUITreceived = False
                                connectionSocket.send(syntax_error(num).encode())
                                #sys.stdout.write(syntax_error(num))
                            continue
                            #end additional thought

                        if l[0:4] == 'RCPT':
                            num = rcpt_to_cmd(l)
                            if syntax_error(num) == '250 OK\r\n':
                                to.append(address(l))
                                message.append(l)
                                QUITreceived = False
                                position = 2 #changed from 2
                    #            print(l)
                                connectionSocket.send(syntax_error(num).encode())
                                #sys.stdout.write(syntax_error(num))
                            else:
                                """sender = ''
                                to = []
                                message = []"""
                                position = 2 #changed from 2
                                QUITreceived = False
                                connectionSocket.send(syntax_error(num).encode())
                                #sys.stdout.write(syntax_error(num))
                            continue
                        #end added

                        num = rcpt_to_cmd(l)
                        codeResponse3 = syntax_error(num)
                        if codeResponse3 == '250 OK\r\n':
                            to.append(address(l))
                            message.append(l)
                            QUITreceived = False
                            #sys.stdout.write(fromC)
                            connectionSocket.send(fromC.encode())
                        else:
                            num = data_cmd(l)
                            data = syntax_error(num)
                            if data == '250 OK\r\n' or data == '354 Start mail input; end with . on a line by itself\r\n':
                                position = 3
                                message.append(l)
                                QUITreceived = False
                                #print out error
                                connectionSocket.send(syntax_error(num).encode())
                                #sys.stdout.write(syntax_error(num))
                            else:
                                position = 3
                                """sender = ''
                                to = []
                                message = []"""
                                QUITreceived = False
                                connectionSocket.send(syntax_error(num).encode())
                                fromC = syntax_error(mail_from_cmd(l))
                    #print out syntax errors; the 503 bad sequence is being printed in this else block
                    #sys.stdout.write(syntax_error(num))

                    elif position == 3:
                        if l == "DATA\r\n":
                            message.append(l)
                            QUITreceived = False
                            #what should it write out here???
                            #sys.stdout.write('354 Start mail input; end with a . on a line by itself \r\n')
           
                        num = check_for_dot(l)
                        codeResponse4 = syntax_error(num)
 #                       print(codeResponse4)
                        #if num != -4:
                        message.append(l)
                        #hardcode
                        #connectionSocket.send(syntax_error(-4).encode())
                        if '.\r\n' in l:
                        #if l == ".\r\n":
                        #if num == -4:
                            contents(sender, to, message)
                            QUITreceived = False
                            connectionSocket.send(syntax_error(-4).encode())
                            #sys.stdout.write(syntax_error(num))
                            position = 0
                            sender = ''
                            to = []
                            message= []
                #terminate the program if the server encounters a non-protocol error from which it cannot recover
                    else:
                        sys.stderr.write("Cannot recover from this error. Connection closing."+'\r\n')
                        connectionSocket.close()

            closingMessage = "221 " + gethostname() + " closing connection\r\n"
            #print(closingMessage)
            connectionSocket.send(closingMessage.encode())
            # print(f"s={sender}, t={to}, m={message}")
            #close connection to this client (but not the welcoming socket) 
            connectionSocket.close()

    except OSError:
        print("Port number already in use.")
main()

