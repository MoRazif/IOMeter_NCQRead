## Example utilize API for Lecroy Analyzer Interface : Running IOMeter + Check for Read NCQ ##
## M.Razif 2018 ##

import re, os, sys, time, optparse, random, win32com.client, logging, subprocess

# Create Log Files
logging.basicConfig(filename='Lecroy.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Clear Command Line
os.system("cls")

# Open Communication with Lecroy Analyzer
Analyzer = win32com.client.Dispatch("Lecroy.SASAnalyzer")

# Get Analyzer Platform
Board = Analyzer.GetBoardPlatform()
time.sleep(1)

if Board == 34:
    analyzer_name = "Sierra M124"
if Board == 32:
    analyzer_name = "Sierra M122"
if Board == 14:
    analyzer_name = "Sierra M6-4"
if Board == 12:
    analyzer_name = "Sierra M6-2"
if Board == 11:
    analyzer_name = "Sierra M6-1"
if Board == 24:
    analyzer_name = "STX 460/STX 431"
if Board == 22:
    analyzer_name = "STX 231"


def print_all(analyzer_name):
    print analyzer_name


print_all(analyzer_name)
logging.info(analyzer_name)
time.sleep(2)


# Get Software version

def software_version():
    a = (Analyzer.GetVersion(0) & 0x0f00) >> 8
    b = (Analyzer.GetVersion(0) & 0x00ff)
    return (str(a) + "." + str(b))

log_software = "Software version is " + software_version()
print log_software
logging.info(str(log_software))

# Initilize Analyzer & Start Capturing

Analyzer.StartRecording ("C:\Users\QA-PC\Desktop\Python Combine\iometer_2s.stc")

Board = Analyzer.IsRunning(0)

if Board == 1:
    status = "Current Status : Analyzer running"

elif Board == 0:
    status = "Current Status ; Analyzer stop "

def print_status(status):
    print status

print_status(status)
logging.info(status)

# Running IO Meter
IOMeter_Start = ("IOMeter Started")
print IOMeter_Start
logging.info(IOMeter_Start)

#IOMeter Batch Files
Process = subprocess.Popen(["C:\IOMeter\IOMeter_2s.bat"], shell=True)
Process.wait()

#IOMeter Using AutoIT
#Process = subprocess.Popen(["C:\IOMeter\Run_IO_10s_Admin.exe"], shell=True)
#Process.wait()

IOMeter_End = ("IOMeter Completed & Closed")
print IOMeter_End
logging.info(IOMeter_End)

# Stop Analyzer
time.sleep(1)
Analyzer.StopRecording(0)
Board= Analyzer.IsRunning(0)

if Board == 1:
    status = "Current Status : Analyzer running"

elif Board == 0:
    status = "Current Status : Analyzer stop "

def print_status(status):
    print status

print_status(status)
logging.info(status)

# VSE Check For NCQ
status = "Running Script to check FIS 0x27 Host to Device"
print status
logging.info(status)

Trace = Analyzer.OpenFile("C:\Users\QA-PC\Desktop\Python Combine\IOMeter_10s.sts")
Result=Trace.RunVerificationScript("C:\IOMeter\Fis27_Check.sasvs")

if Result==0:
    status = "Test Failed: FIS 0x27 Host to Device detect in trace"
else:
    status = "Test Passed: No FIS 0x27 detect in trace"

print status
logging.info(status)


