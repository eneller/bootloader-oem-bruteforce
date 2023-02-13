# IMPORTANT: assumes that the unlock code is numeric
import click
import click_config_file
import signal
import sys
import math
import subprocess
import time

@click.command()
@click.option('--resume-count','-r',type=int,  default=-1, help="Set the attempt number at which the bruteforce should resume in case of a stop. This number is logged by the previous run. Not necessary if running for the first time.")
@click.option('--limit-attempt', '-l',type=int, default=-1, help="Set the max number of attempt to perform before rebooting. On some devices a number of 5 is necessary to prevent hitting bruteforce protection. Don't use this option to set no limit.")
@click.option('--fastboot', '-f', default='fastboot', help="Path to fastboot executable. Defaults to the one in PATH in UNIX-like, fastboot.exe on Windows")
@click.option('--adb', '-a', default='adb', help="Path to fastboot executable. Defaults to the one in PATH in UNIX-like, adb.exe on Windows")
@click.option('--imei', type=int, default=-1, help="Use the IMEI generation instead of pure brute force")
@click_config_file.configuration_option(implicit=False, expose_value=True)
# TODO? add log file
# TODO add non-interactive delay(s) 
# TODO re-add interactive confirmation
def main(resume_count, limit_attempt, fastboot, adb, imei, config):
  increment = 1 
  if(imei!=-1):
    if (not luhn_checksum(imei)):
      print(f"{imei} is not a valid IMEI. Aborting.")
      sys.exit(1)
    increment = int(math.sqrt(imei)) * 1024
    if resume_count ==-1:
      resume_count = 1000000000000000

  if fastboot == "fastboot" and sys.platform in ('win32', 'cygwin'):
    fastboot = "fastboot.exe"
  if adb == "adb" and sys.platform in ('win32', 'cygwin'):
    adb = "adb.exe"
  
  
  subprocess.run([adb, 'devices'])
  #TODO maybe adapt to select device if multiple available=
  subprocess.run(
    [adb, 'reboot', 'bootloader']
  , stdout = subprocess.DEVNULL
  , stderr = subprocess.DEVNULL
  )
 #  register the signal handler
  signal.signal(signal.SIGINT, signal_handler)
  print('Press Ctrl+C to exit gracefully')
  
  countAttempts =0
  while(True):
    resume_count = resume_count + increment
    start_time = time.time()
    answer = subprocess.run(
      [fastboot, 'oem', 'unlock', str(resume_count).zfill(16)],
      stdout = subprocess.DEVNULL,
      stderr = subprocess.DEVNULL
    ) 
    exec_time = time.time()-start_time
    print(f"Testing code {resume_count} took {exec_time} seconds")
    countAttempts +=1

    if answer.returncode == 0:
        # could also be a different command to check unlock status
        subprocess.run([fastboot, 'getvar', 'unlocked'])
        print(f"Found Code: {resume_count}" )
        subprocess.run([fastboot, 'reboot'])
        break
    if limit_attempt != -1 and (countAttempts) % limit_attempt == 0: 
        countAttempts=0
        subprocess.run(
            [fastboot, 'reboot', 'bootloader'],
            stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL
          )








# a signal handler for interrupts
def signal_handler(sig, frame):
   #TODO handle interrupt here
  print('Press Ctrl+C again for a forced exit')
  sys.exit(0)

# calculates the luhn checksum of an imei
# used to notify the user if he has entered his imei incorrectly
def luhn_checksum(imei):
  def digits_of(n):
    return [int(d) for d in str(n)]
  digits      = [int(d) for d in str(imei)]
  oddDigits   = digits[-1::-2]
  evenDigits  = digits[-2::-2]
  checksum    = 0
  checksum    += sum(oddDigits)
  for i in evenDigits:
    checksum += sum(digits_of(i * 2))
  return (checksum % 10)==0

if __name__ == '__main__':
  main()
  
