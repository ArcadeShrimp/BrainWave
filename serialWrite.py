import serial
arduinoData = serial.Serial('com6',9600) #"com6" can be changed depending on which port is being used by the arduino
while(1==1):
    Number="?????"    #pass in the input of either 1 or 0
    arduinoData.write(Number.encode()) 
