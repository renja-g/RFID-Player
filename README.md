# RFID-Player

# Devlog
- [25.06.2024](##25.06.2024)

## 25.06.2024
![image](https://github.com/renja-g/RFID-Player/assets/76645494/4093736f-4aae-4558-82d7-10dd5297f489)
Right now I want to first figure out how to make the setup easy, assuming that the software is on the pi, but is not connected to a network.
My current idea is:
1. Let the pi create an access point.
2. Use a phone to connect to the access point.
3. The phone opens the captive portal that has a list of available networks.
4. The user selects a network and enters in the password.
5. The Pi connects to the selected network.
