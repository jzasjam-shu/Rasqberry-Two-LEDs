# Rasqberry-Two-LEDs
Code for the LED display on he Rasqberry Two

Instructions to run at startup a per: https://forums.raspberrypi.com/viewtopic.php?t=347485

1. `nano ~/.bashrc`

2. Add `python3 /full/path/to/leds.py`

---

Alternatively, using crontab as per https://raspberrytips.com/autostart-a-program-on-boot/

1. Create/update `start_leds.sh`

```
#!/bin/bash

python3 /full/path/to/leds.py
```

2. Make the start_leds.py executable `sudo chmod +x start_leds.sh`

2. `crontab -e` and select 'nano'

3. Add `@reboot /full/path/to/start_leds.py`
