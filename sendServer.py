import socket

host, port = "127.0.0.1", 25001
dataX = 30
dataY = 6
dataZ = 0
running = True

prompt = "What would you like to do?\nS = Change size\nP = Change Postion\n>>"
posPrompt = "Postion: Which way would you like to go?\n(X, Y, or Z)\n>>"
sizPrompt = "Size: Which operation would you like to do?\n(A = add, S = subtract, M = multiply, D = divide)\n>>"

# SOCK_STREAM means TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendData(X, Y, Z, type):
        data = str(type) + ',' + str(X) + ',' + str(Y) + ',' +  str(Z)
        sock.sendall(data.encode("utf-8"))
        response = sock.recv(1024).decode("utf-8")
        print (response)

try:
    # Connect to the server and send the data
    sock.connect((host, port))
    while (running):
        inp = str(input(prompt))

        if(inp.lower().__eq__('s')):
              inp = str(input(sizPrompt))
              match inp.lower():
                    case 'a':
                          magnitude = int(input("How much are we adding by?\n(Enter a number)\n>>"))
                          sendData(inp, magnitude, 0, 's')
                    case 's':
                          magnitude = int(input("How much are we subtracting by?\n(Enter a number)\n>>"))
                          sendData(inp, magnitude, 0, 's')
                    case 'm':
                          magnitude = int(input("How much are we multiplying by?\n(Enter a number)\n>>"))
                          sendData(inp, magnitude, 0, 's')
                    case 'd':
                          magnitude = int(input("How much are we dividing by?\n(Enter a number)\n>>"))
                          if(magnitude == 0):
                                print("You cannot divide by zero!")
                          else:
                                sendData(inp, magnitude, 0, 's')
                    case _:
                          print("This data is incorrect!")

        elif(inp.lower().__eq__('p')):
                inp = input(posPrompt)
                match inp.lower():
                        case 'x':
                             inp = int(input("X: How many in this direction?\n>>"))
                             dataX = dataX + inp
                        case 'y':
                             inp = int(input("Y: How many in this direction?\n>>"))
                             dataY = dataY + inp
                        case 'z':
                             inp = int(input("Z: How many in this direction?\n>>"))
                             dataZ = dataZ + inp
                sendData(dataX, dataY, dataZ, 'p')
        else:
              print("This data was incorrect. Try again!\n\n\n")

        inp = str(input("Again?(y/n)"))
        if(inp.lower().__eq__('n')):
            running = False

finally:
    sock.close()