import socket
done = 0
s = socket.socket()
s.bind(("localhost", 5001))
s.listen(1)
c,a = s.accept()
filetodown = open("flower.png", "wb")
while done == 0:
   print("Receiving....")
   data = c.recv(1024)
   print("data is: ", data)
   #print("data[-1] is: ", data[-1])
   if data == b'0' or data == b'' or data == 0:
     print("Done Receiving.")
     done = 1
     break
   filetodown.write(data)
filetodown.close()
print("Done receiving.")
#c.send(bytes('Thank you for connecting.', 'UTF-8'))
#c.shutdown(2)
#c.close()
#s.close()
