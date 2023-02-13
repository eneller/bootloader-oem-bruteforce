# Unlock Huawei bootloader with brute force

## Preface

After closing the official EMUI website, which allowed you to retrieve the code to unlock the bootloader of Huawei/Honor phones, here is a python script to retrieve it by yourself.

It uses a bruteforce method based on the IMEI identifier to generate and test all unlocking codes.



## Basic instructions

### Prerequisites
- Python > 3.7 installed
- PyPI installed
- ADB and Fastboot installed (Part of android-tools)
- this repository cloned or downloaded
- USB Debugging enabled
- OEM Unlock enabled
- IMEI of your phone

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
4. Run the script after replacing IMEI_OF_YOUR_DEVICE with your IMEI. 
``` bash
python3 unlock.py IMEI_OF_YOUR_DEVICE
```


## Advanced Instructions
Some devices have a bruteforce protection, preventing trying more than five codes. In this case, you will have to invoke the script with the option attempt-limit:
```bash
python3 unlock.py --limit-attempt 5 IMEI_OF_YOUR_DEVICE
```
If you want to pause the process you can simply exit the script by pressing `CTRL+C`. Write down the last shown "Attempt no.".
   - To resume invoke the script like so: `python3 unlock.py --resume-count ATTEMPT_NO IMEI_OF_YOUR_DEVICE`
   - If you were using an attempt-limit use: `python3 unlock.py --resume-count ATTEMPT_NO --limit-attempt 5 IMEI_OF_YOUR_DEVICE`
   
Also, the repo includes an example udev rule that you can adjust to match 
your device's parameters.
You can then use it to auto-resume and pause the script upon plugging in your phone.


## FAQ & Troubleshooting

Enabling developer options in Android at your phone:
    ` Settings > System > About device ` tap _Build number_ seven times to enable developer options.

Enabling USB debugging and OEM unlock in Android:
    ` Settings > System > Developer options`

Retrieve your IMEI by either going to 
    ` Settings > System > About device `
or by dialing `*#06#` into your phone app. 

Reboot from fastboot mode by holding down your power button for ~10 seconds.

If adb and fastboot are not found, you can try manually setting their path with the flags `--adb` and `--fastboot`. All in all, the `python3 unlock.py --help` manual can always be useful.
