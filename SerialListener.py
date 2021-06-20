import serial
import logging
from datetime import datetime
import time

dataReceiveCounter=0
cannotReceiveCounter=0
receivedChecksum=0
calculatedChecksum=0

dataArray= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


logging.basicConfig(filename='./SerialReaderLog', format='%(asctime)s:%(message)s', level=logging.DEBUG)
logging.debug('------- SerialReader Started ---------')

serialPort = serial.Serial("/dev/ttyUSB0", baudrate=921600, timeout=0.1, writeTimeout=0.1)

def MCU_Read(mPort):
	readErrorCounter = 0

	while True:
		try:
			readErrorCounter+=1
			emptyCharCounter=0

			if(readErrorCounter>=2):
				break

			mReceivedData = []
			while len(mReceivedData)<10:
				mReceivedTemp = mPort.readline()

				if len(mReceivedTemp)>0:
					mReceivedData.extend(mReceivedTemp)
				else:
					emptyCharCounter+=1
					if emptyCharCounter>=1:
						print ("Port Closing")
						mPort.close()
						mPort.open()
						break

			lenm=len(mReceivedData)

			if lenm>=10:
				mPort.flushInput()
				return mReceivedData

		except Exception as err:
			logging.debug("MCU_Read error: %s", err)
			time.sleep(0.5)
			mPort.close()
			mPort.open()



while True:
	time.sleep(0.1)
	if serialPort.isOpen():
		receivedData = MCU_Read(serialPort)
		if receivedData!=None:
			if len(receivedData)==11 and receivedData[0]==42 and receivedData[10]==10:
				receivedChecksum=receivedData[9]+receivedData[8]*256+receivedData[7]*65536+receivedData[6]*16777216
				multiplier=1
				calculatedChecksum=0
				for x in range(1,6):
					calculatedChecksum += receivedData[x] * multiplier
					multiplier+=2

			if receivedChecksum == calculatedChecksum:
				dataArray[receivedData[5]]=(receivedData[4] + receivedData[3]*256 + receivedData[2]*65536 + receivedData[1]*16777216)
				now = datetime.now()
				dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
				print (round(dataArray[0],1),round(dataArray[1],1),round(dataArray[2],1),round(dataArray[3],1),round(dataArray[4],1),round(dataArray[5],1),round(dataArray[6],1),round(dataArray[7],1),round(dataArray[8],1),round(dataArray[9],1),round(dataArray[10],1),round(dataArray[11],1),round(dataArray[12],1),round(dataArray[13],1),round(dataArray[14],1))
		else:
				dataReceiveCounter+=1
				cannotReceiveCounter+=1
				if cannotReceiveCounter>10:
					cannotReceiveCounter=0
					dataArray[0] = 0
					dataArray[1] = 0
					dataArray[2] = 0
					dataArray[3] = 0
					dataArray[4] = 0
					dataArray[5] = 0
					dataArray[6] = 0
					dataArray[7] = 0
					dataArray[8] = 0
					dataArray[9] = 0
					dataArray[10] = 0
					dataArray[11] = 0
					dataArray[12] = 0
					dataArray[13] = 0
					dataArray[14] = 0
	else:
		serialPort.open()
