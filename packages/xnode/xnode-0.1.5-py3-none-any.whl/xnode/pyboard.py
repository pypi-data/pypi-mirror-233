import sys
import time
import serial

try:
    stdout = sys.stdout.buffer
except AttributeError:
    stdout = sys.stdout

def stdout_write_bytes(b):
    b = b.replace(b"\x04", b"")
    stdout.write(b)
    stdout.flush()

class PyboardError(BaseException):
    pass

class Pyboard:
    def __init__(self, device, baudrate=115200, wait=0):  
        delayed = False

        for attempt in range(wait + 1):
            try:
                self.serial = serial.Serial(device, baudrate=baudrate, inter_byte_timeout=1)
                break
            except (OSError, IOError): 
                if wait == 0:
                    continue
                if attempt == 0:
                    sys.stdout.write('Waiting {} seconds for pyboard '.format(wait))
                    delayed = True
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()
        else:
            if delayed:
                print('')
            raise PyboardError('failed to access ' + device)
        if delayed:
            print('')

    def close(self):
        self.serial.close()

    def read_until(self, min_num_bytes, ending, timeout=10, data_consumer=None):
        data = self.serial.read(min_num_bytes)
        if data_consumer:
            data_consumer(data)
        timeout_count = 0
        while True:
            if data.endswith(ending):
                break
            elif self.serial.inWaiting() > 0:
                new_data = self.serial.read(1)
                data = data + new_data
                if data_consumer:
                    data_consumer(new_data)
                timeout_count = 0
            else:
                timeout_count += 1
                if timeout is not None and timeout_count >= 100 * timeout:
                    break
                time.sleep(0.01)
        return data

    def enter_raw_repl(self):
        self.serial.write(b'\r\x03\x03') # ctrl-C twice: interrupt any running program

        n = self.serial.inWaiting()
        while n > 0:
            self.serial.read(n)
            n = self.serial.inWaiting()

        self.serial.write(b'\r\x01') # ctrl-A: enter raw REPL
        data = self.read_until(1, b'raw REPL; CTRL-B to exit\r\n>')
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
            print(data)
            raise PyboardError('could not enter raw repl')

        self.serial.write(b'\x04') # ctrl-D: soft reset
        data = self.read_until(1, b'soft reboot\r\n')
        if not data.endswith(b'soft reboot\r\n'):
            print(data)
            raise PyboardError('could not enter raw repl')

        data = self.read_until(1, b'raw REPL; CTRL-B to exit\r\n')
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n'):
            print(data)
            raise PyboardError('could not enter raw repl')

    def exit_raw_repl(self):
        self.serial.write(b'\r\x02') # ctrl-B: enter friendly REPL

    def _follow_write(self, echo):
        import os
        
        try:
            import msvcrt
            def getkey():
                return msvcrt.getch()

            def putkey(ch):
                if ch == b'\r':
                    ch = b'\n'
                msvcrt.putch(ch)
                
        except ImportError:
            import sys, tty, termios
            def getkey():
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                return ch
            
            def putkey(ch):
                sys.stdout.write(ch)
                sys.stdout.flush()
        
        while True:
            ch = getkey()
            if ch == b'\x03': #<Ctrl>c
                os._exit(0)
            if echo:
                putkey(ch)
            self.serial.write(ch)

    def follow(self, timeout, data_consumer=None, input_stat=None):
        if input_stat[1]:
            from threading import Thread

            th = Thread(target=self._follow_write, args=(input_stat[0],))
            th.daemon = True
            th.start()
        
        data = self.read_until(1, b'\x04', timeout=timeout, data_consumer=data_consumer)
        if not data.endswith(b'\x04'):
            raise PyboardError('timeout waiting for first EOF reception')
        data = data[:-1]

        data_err = self.read_until(1, b'\x04', timeout=timeout)
        if not data_err.endswith(b'\x04'):
            raise PyboardError('timeout waiting for second EOF reception')
        data_err = data_err[:-1]

        return data, data_err

    def exec_raw_no_follow(self, command):            
        if isinstance(command, bytes):
            command_bytes = command
        else:
            command_bytes = bytes(command, encoding='utf8')

        data = self.read_until(1, b'>')
        if not data.endswith(b'>'):
            raise PyboardError('could not enter raw repl')

        for i in range(0, len(command_bytes), 256):
            self.serial.write(command_bytes[i:min(i + 256, len(command_bytes))])
            time.sleep(0.01)
        self.serial.write(b'\x04')

        data = self.serial.read(2)
        if data != b'OK':
            raise PyboardError('could not exec command')

    def exec_raw(self, command, timeout=None, data_consumer=None, input_stat=None):
        self.exec_raw_no_follow(command)
        return self.follow(timeout, data_consumer, input_stat)

    def eval(self, expression):
        ret = self.exec_('print({})'.format(expression))
        ret = ret.strip()
        return ret

    def exec_(self, command, stream_output=False, input_on=False):
        data_consumer = None
        if stream_output or input_on:
            data_consumer = stdout_write_bytes
        ret, ret_err = self.exec_raw(command, data_consumer=data_consumer, input_stat=(stream_output, input_on))
        if ret_err:
            raise PyboardError('exception', ret, ret_err)
        return ret
    
    def execfile(self, filename, stream_output=False, input_on=False):
        with open(filename, 'r+b') as f:
            pyfile = f.read()
        return self.exec_(pyfile, stream_output, input_on)
    
    def get_time(self):
        t = str(self.eval('pyb.RTC().datetime()'), encoding='utf8')[1:-1].split(', ')
        return int(t[4]) * 3600 + int(t[5]) * 60 + int(t[6])

setattr(Pyboard, "exec", Pyboard.exec_)
