
# coding: utf-8

# In[7]:


import sys


# In[7]:


#creates specific syntax error checks
def syntax_error(num):
    if num == -1:
        return "500 Syntax error: command unrecognized"
    
    if num == -2:
        return "501 Syntax error in parameters or arguments"
    
    if num == -3:
        return "503 Bad sequence of commands"
    
    if num == -4:
        return "250 OK"


# In[8]:


#check MAIL FROM: 
def mail_from_cmd(l):
    if len(l) < 4:
        return -1
    if l[0:4] != 'MAIL':
        return -1
    index = 4
    lenTest = 0
    white = 0
    
    while white >= 0:
        lenTest += 1
        white = whitespace(l[index:index+lenTest]) 
        
    if lenTest == 1:
        return -1
    
    if lenTest > 2 and ((lenTest - 1) % 4 != 0):
        syntax_error0() #mail from cmd error
        return -1
    
    index = index + lenTest - 1
    
    if len(l) < (index + 5):
        return -1
    
    #checks FROM:, returns error if from is not there
    if l[index:index+5] != "FROM:":
        return -1
    index += 5
    #nullspace after from
    l = l[index + 5:]
    index = 0
    
    l = l.lstrip()
    
    if len(l) == 0:
        #path error
        return -3
    
    if l[0] != '<':
        #path error
        return -3
    
    #reverse path and <>
    index = 0
    rightIndex = l.find('>')
    if(rightIndex == -1):
        return reversePath(l[index:])
    
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
    #checks if says RCPT TO:
    if len(l) < 4:
        return -1
    if l[0:4] != "RCPT":
        return -1
    
    l = l[4:]
    
    index = 4
    white = 0
    lenTest = 0
    
    while white >= 0:
        lenTest += 1
        white = whitespace(l[0:lenTest])
        
    if lenTest == 1:
        return -1
    
    if len(l) < 3:
        return -1
    
    if l[0:3] != 'TO:':
        return -1
    
    #nullspace
    l = l[3:]
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
        return forwardPath(l)
    
    fpath = forwardPath(l[:rightIndex+1])
    
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
    
    if l[0:4] != 'DATA':
        return -1
    
    #nullspace
    l = l[4:]
    
    if len(l) > 1:
        if sp(l[0]) < 0:
            return -1
        
    l= l.lstrip()
        
    if len(l) > 0:
        return -2
    
    return -4


# In[11]:


#defines what whitespace is
def whitespace(i):
    if i == ' ' | i == '\t':
        return 1
    return 0


# In[12]:


#sp
def sp(i):
    if i == ' ' | i == '\t':
        return 1
    return 0


# In[13]:


def begin(s):
    found = false;
    length = 0
    
    while found == false and length < len(s):
        length += 1
        
        if mailbox(s[0:length]) > 0:
            found = true
            
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
        
    mailbox = s[1:]
    if mailbox(mailbox) > 0:
        #path error
        return -3
    
    mailbox = s[1:-1]
    mail = mailbox(mailbox)
    
    if mail < 0:
        if begin(mailbox):
            #path error
            return -3
        else:
            return mail
        
    if s[-1:] != '>':
        #path error
        return -3
    
    return 1 + mail + 1
        


# In[17]:


#mailbox
def mailbox(s):
    i = 0
    localPart = 0
    
    if len(s) == 0:
        #char error
        return -2
    
    while localPrt >= 0 and i < len(s):
        i += 1
        localPart = local_part(s[0:i])
        
        i -= 1
        
        if i == 0:
            #char error
            return -2
        
        if i == len(s):
            #mailbox error
            return -1
        
        if s[i] != '@':
            #mailbox error
            return -1
        
        dom = s[i+1]
        
        isDom = domain(dom)
        
        if isDom < 0:
            return isDom
        
        return i + isDom


# In[18]:


#local-part
def local_part(s):
    return string(s)


# In[19]:


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


# In[20]:


#char
def char(c):
    if special(c) > 0:
        #char error
        return -2
    
    if sp(c) > 0:
        #char error
        return -2
    
    if null(c):
        #char error
        return -2
        
    if letter(c):
        return 1
    
    if digit(c):
        return 1
    
    return 1 if (ord(c) < 128) else 0


# In[21]:


#domain
def domain(s):
    element = element(s)
    if element > 0:
        return element
    
    dot = s.find('.')
    
    if(dot < 0):
        return element
    
    ele = element(s[:dot])
    
    if ele < 0:
        return ele
    
    doma = domain(s[dot+1])
    
    if doma < 0:
        return doma
    
    return ele + 1 + doma


# In[22]:


#defines null
def null(c):
    if c == '':
        return 1
    return 0


# In[23]:


#defines nullspace (null or whitespace)
def nullspace(c):
    nul = null(c)
    if nul == 0:
        return nul
    whtspc = whitespace(c)
    if whtspc > 0:
        return whtspc
    return 0


# In[24]:


#creates newline
def CRLF(c):
    if c == '\r\n':
        return 1
    return 0


# In[25]:


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
    return 0


# In[26]:


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
    return 0


# In[27]:


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
    return 0


# In[28]:


def letterDigit(c):
    dig = digit(c)
    if dig > 0:
        return dig
    
    let = letter(c)
    if let > 0:
        return let
    
    return 0


# In[29]:


def letDigStr(s):
    if len(s) <= 1:
        return letDigStr(s)
    
    letDig = letterDigit(s[:1])
    
    if letDig < 0:
        return letDig
    
    letDigString = letDigStr(s[1:])
    
    if letDigString < 0:
        return letDigString
    
    return letDig + letDigString


# In[30]:


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


# In[31]:


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


import sys
def main():
    #sys.stdin.readline().rstrip('\n')

    sender = ''
    to = []
    message = []
    position = 0
    #.readline() ?
    
    for l in sys.stdin:
        sys.stdout.write(l)
        if position == 0:
            codeResponse1 = syntax_error(mail_from_cmd(l))
            print(codeResponse1)
            print(syntax_error(mail_from_cmd(l)))
            if codeResponse1 == "250 OK":
                position = 1
                sender = address(l)
                sys.stdout.write(codeResponse1 + '\r\n')
            else:
                sender = ''
                to = []
                message = []
                position = 0

                rcpt = syntax_error(rcpt_to_cmd(l))
                data = syntax_error(data_cmd(l))
            
                #print out syntax errors
                sys.stdout.write(syntax_error(num))
        
        elif position == 1:
            codeResponse2 = syntax_error(rcpt_to_cmd(l))
            if codeResponse2 == '250 OK':
                to.append(address(l))
                position = 2
                sys.stdout.write(codeResponse2 + '\r\n')
                
            else:
                fromC = syntax_error(data_cmd(l))
                data = syntax_error(mail_from_cmd(l))
                sender = ''
                to = []
                message = []
                position = 0
                
                #print out syntax errors
                sys.stdout.write(syntax_error(num))
       
        elif position == 2:
            codeResponse3 = syntax_error(rcpt_to_cmd(l))
            
            if codeResponse3 == '250 OK':
                to.append(address(l))
                sys.stdout.write(fromC + '\r\n')
                
            else:
                data = syntax_error(data(l))
                if data == '250 OK':
                    position = 3
                    #print out error
                    sys.stdout.write(syntax_error(num))
                else:
                    position = 0
                    sender = ''
                    to = []
                    message = []
                    fromC = syntax_error(mail_from_cmd(l))
                    
                    #print out syntax errors
                    sys.stdout.write(syntax_error(num))
                
        
        def address(l):
            left = l.find('<')
            right = l.find('>')
            return l[left+1+right]
        
        
main()

