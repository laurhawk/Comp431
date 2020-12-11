"""
- how to test this program:
- copy SMTP2.py and generate_tests.py to your working directory (a directory under your home directory)
- first, generate input_0 and output_0 files by running: python3 generate_tests.py
- then, run SMTP2.py: python3 SMTP2.py < input_0 > my_output_0
- finally, compare program output (my_output_0) with expected output (output_0)
  diff shouldn't produce any output: 
        diff output_0 my_output_0
"""
import sys, re
#include Python's socket library
from socket import *
#does this need to be the same as the server or different?; server name on client side is from command line argumets as well as the serverPort
def main():
    if len(sys.argv) != 3:
        sys.stdout.write("Incorrect amount of arguments.\r\n")
        sys.exit(0)
    
#    if isinstance(sys.argv[1], str):
#        sys.stdout.write("Incorrect argument type.\r\n")
#        sys.exit(0)

#    if isinstance(sys.argv[2], int):
#        sys.stdout.write("Incorrect argument type.\r\n")
#        sys.exit(0)

serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])

#---------------------------------------------------------

#do not know where I am supposed to put the following code, adding it anyways
#initializing da socket
clientSocket = socket(AF_INET, SOCK_STREAM)
#create TCP socket to server on port 15355
try:
    clientSocket.connect((serverName, serverPort))
except:
    sys.stdout.write("Failed to connect to the server.")


#SEND GREETING
#check greeting message
greet = clientSocket.recv(1024).decode()
if greet[0:3] == '220':
    #check that the greeting is correct
    clientSocket.send(("HELO " + serverName + " \r\n").encode())
else:
    clientSocket.close()
    sys.exit(0)


#need to code the Hello hostname pleased to meet you part on the server side
#acknowledge = clientSocket.recv(1024).decode()
#clientSocket.send(greeting().encode())
#prompt from, to, subject, message, and then type there
#fromLine = input("From:")

#close = clientSocket.recv(1024).decode()
#if close[0:3] == "221 ":
#    clientSocket.close()
#sentence = input("")

#change text into a sequence of bytes before sending; the server will expect that whatever it is receving from the client is a stream of bytes
#clientSocket.send
#clientSocket.send(sentence.encode())

#receive data from server in a buffer; would never expect my sentence to be longer than 1024 bytes; if it is, the server does not have space for it
#modifiedSentence = clientSocket.recv(1024)
#print("From server:", modifiedSentence.decode())
#close = clientSocket.recv(1024).decode()
#check to make sure that it is the 221 response

#beginning of template code

def next_input_line():
    """Returns the next line from stdin and exits upon encountering EOF."""
    try:
        current_line = next(sys.stdin)
        return current_line
    except StopIteration:
        # EOF encountered
        quit_smtp()
        clientSocket.close()
        sys.exit(0)
    
def input_from():
    #prompt for "From:" field and return input line
    sys.stdout.write("From:\r\n")
    return next_input_line().strip()


def input_to():
    #prompt for "To:" field and return input line
    sys.stdout.write("To:\r\n")
    return next_input_line().strip()

def input_subject():
    #prompt for "Subject:" field and return input
    sys.stdout.write("Subject:\r\n")
    return next_input_line().strip()

def input_message():
    """
    prompt for "Message:" and return input lines as follows:
    read lines from stdin until "." is seen on a new line
    return all the lines (including the one with ".") concatenated 
    as a string (this string is considered as an email message)
    """

    sys.stdout.write("Message:\r\n")
    message = ""
    while True:
        line = next_input_line()
        message += line
        if line == ".\r\n":
            break
    return message

def input_email():
    email = {"from": "", "to": "", "subject": "", "message": ""}
    email['from'] = input_from()
    email['to'] = input_to()
    email['subject'] = input_subject()    
    email['message'] = input_message()
    return email

def send_data_to_server(data):
    
    clientSocket.send(data.encode())
    #sys.stdout.write(data)

def get_server_response_code():
    """
    return server response code (one of "250","354","500", "501") 
    if the response line is valid otherwise return "" (empty string)

    server response is simulated using standard input. If EOF is encountered,
    the program is terminated.
    """
    try:
        response = next(sys.stdin)
        sys.stdout.write(response) #echo server response

        response_code = ""
        #todo: only accept printable characters (instead of .*) 
        match = re.fullmatch("(250|354|500|501)[ \t]+.*\r\n", response)
        if match:
            response_code = match.group(1)
        
        return response_code
    except StopIteration:
        # EOF encountered  
        quit_smtp() 
        sys.exit(0)  
#         print("ok")
def send_data_to_server_and_expect_response_code(data, expected_response_code):
    """
    send the data to server and verify the response code
    if the server response code is not equal to expected_response_code
    send SMTP QUIT message to the server and exit the program.
    """
    send_data_to_server(data)
    response_code = get_server_response_code()
 #   if response_code != expected_response_code:
 #       quit_smtp()
 #       sys.exit(0) 

def quit_smtp():
    send_data_to_server("QUIT\r\n") #send quit
    close = clientSocket.recv(1024).decode() #wait for a response
    clientSocket.close() #close

def send_email(mail):
    send_data_to_server_and_expect_response_code(f"MAIL FROM: <{mail['from']}>\r\n", "250")
    send_data_to_server_and_expect_response_code(f"RCPT TO: <{mail['to']}>\r\n", "250")
    send_data_to_server_and_expect_response_code("DATA\r\n", "354")
    
    #format the message:
    message =  f"From: <{mail['from']}\r\n"
    message += f"To: <{mail['to']}>\r\n"
    message += f"Subject: {mail['subject']}\r\n"
    message += f"\r\n"
    message += f"{mail['message']}"

    #a valid message always ends with ".\r\n"
    #no need to append '\r\n' to message
    send_data_to_server_and_expect_response_code(message, "250")

    
if __name__ == "__main__":
    while True:
        email = input_email()
        send_email(email)
