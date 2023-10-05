xnode is a CLI tool for the zigbee mote (xnode) running in micropython.
  
### Find serial port
```sh
xnode scan
```

### Initialize XNode (with zigbee) file system
```sh
xnode -pcom3 format b
```
> com3 is the port number found by scan

### Install Pop library on XNode
```sh
xnode -pcom3 put lib
xnode -pcom3 ls /flash/lib
```
> The Pop library (pop.py, etc.) must be included in the lib folder of the current path.

### Executes the PC's MicroPython script by sequentially passing it to the XNode
```sh
xnode -p com3 run app.py
```
> Wait for serial output until the script finishes

**Additional Options**
   - -n: Does not wait for serial output, so it appears as if the program has terminated on the PC side.
     - Script continues to run on XNode
     - Used to check data output serially from XNode with other tools (PuTTY, smon, etc.)
   - -i: Passes PC keyboard input to the script running on XNode via serial.
     - The script running on XNode must implement a syntax for reading data from serial.
     - Displays the pressed key in the terminal window (Echo on)
   - -ni (or -n -i): Same as -i, but does not display the pressed key in the terminal window (Echo off)

### Install and run the MicroPython script on XNode
```sh
xnode -p com3 put app.py main.py
xnode -p com3 ls
```
> app.py is the name of the script written on the PC, main.py is the name to be installed on XNode
> Automatically runs /flash/main.py if it exists when XNode starts

### Delete XNode file
```sh
xnode -p com3 rm main.py
xnode -p com3 ls
```

### Run visualization tool
```sh
xmon
```
> Visualize sensor data output in CSV format