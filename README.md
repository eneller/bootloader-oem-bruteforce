# Unlock Huawei bootloader with brute force

## This repository has been archived. If you are using a phone with a locked bootloader you can still try this, but it is recommended to consider paid options if available.

## Preface

After closing the official EMUI website, which allowed you to retrieve the code to unlock the bootloader of Huawei/Honor phones, here is a python script to retrieve it by yourself.

It uses a bruteforce method (optionally based on the IMEI identifier) to generate and test all unlocking codes, 
assuming the codes are only numeric - the probability of guessing an alphanumeric code within your lifetime is basically zero.
The IMEI method is the same as in scripts by [titulebolide](https://github.com/titulebolide/huawei-oem-bruteforce),[haexhub](https://github.com/titulebolide/huawei-oem-bruteforce) and [vcka](https://github.com/vcka/huawei-honor-unlock-bootloader) with the only major difference being that it actually does what it says.

The main focus here is on user-friendliness, because according to `time`, one round of `fastboot oem unlock abcdefghijklmnop` takes 0,005 seconds, while my script measures an average of 0,0076 - a factor of 1,5.
So, the performance increase of using compiled C would be noticable, but in my opinion not relevant.


## Basic instructions

### Prerequisites
- Python > 3.7 installed
- PyPI installed
- ADB and Fastboot installed (Part of android-tools)
- this repository cloned or downloaded
- USB Debugging enabled
- OEM Unlock enabled
- Optional: IMEI of your phone

### Connecting your device


1. Connect your device to the computer 

2. Once in the directory, create a virtual python environment and activate it.
You can deactivate the environment later by running `deactivate`.
``` bash
python3 -m venv .env
source .env/bin/activate
```
3. In it, install the dependencies of this script and run it. 
``` bash
python3 -m pip install -r requirements.txt
```
4. To run the script, refer to the available options:
```
Usage: unlock.py [OPTIONS]

Options:
  -r, --resume-count INTEGER   Set the attempt number at which the bruteforce
                               should resume. Defaults to 10^15 when using --imei

  -l, --limit-attempt INTEGER  Set the max number of attempt to perform before
                               rebooting. On some devices a number of 5 is
                               necessary to prevent hitting bruteforce
                               protection. Defaults to no limit.

  -f, --fastboot TEXT          Path to fastboot executable. Defaults to the
                               one in PATH in UNIX-like, fastboot.exe on
                               Windows.

  -a, --adb TEXT               Path to fastboot executable. Defaults to the
                               one in PATH in UNIX-like, adb.exe on Windows.

  --imei INTEGER               Use the IMEI generation instead of pure brute
                               force.

  --config FILE                Read configuration from FILE.

  --help                       Show this message and exit.
```


## FAQ & Troubleshooting

Enabling developer options in Android at your phone:
    ` Settings > System > About device ` tap _Build number_ seven times to enable developer options.

Enabling USB debugging and OEM unlock in Android:
    ` Settings > System > Developer options`

Retrieve your IMEI by either going to 
    ` Settings > System > About device `
or by dialing `*#06#` into your phone app. 

Reboot from fastboot mode by holding down your power button for ~10 seconds.

If adb and fastboot are not found, you can try manually setting their path with the flags `--adb` and `--fastboot`.
