import re
import sys
import glob
import serial

from xnode.cli import cli

def main():
	sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    
	if len(sys.argv) == 2 and sys.argv[1].lower() == "scan":
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				print(port)
			except (OSError, serial.SerialException):
				pass
	else:    
		sys.exit(cli())
		
if __name__ == '__main__':
	main()