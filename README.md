# ============================================================
#  AhmedRAT - Professional Red Team Tool
#  الإصدار التجريبي | Beta Release
# ============================================================
#  All Rights Reserved © 2026-2027
#  Yemen Spam | يمن سبام
#  Developer: Mr. Ahmed Yemen | السيد احمد
#  Yemen Security Research | البحث الأمني اليمني
#  Country Code: YA 🇾🇪
#  yemenspam@gmail.com
#  https://yspa.kesug.com/
# ============================================================

# [ العربية | Arabic ]
# ------------------------------------------------------------
# الشرح الفني والميزات
# ------------------------------------------------------------

AhmedRAT هو حل متقدم ومُحكم للتحكم عن بُعد، مصمم خصيصاً
لعمليات الفريق الأحمر (Red Team) واختبار الاختراق، ويتميز
بالهندسة الدقيقة والتهرب المتقدم.

## الميزات الأساسية:

1. واجهة ثنائية اللغة:
   دعم كامل للغتين العربية والإنجليزية لضمان التوافق مع
   مختلف بيئات الهدف.

2. بنية قيادة وتحكم (C2) عبر تيليجرام:
   تعتمد على بروتوكولات تيليجرام المشفرة، مما يلغي الحاجة
   تماماً لتوجيه المنافذ (No Port Forwarding) أو استخدام
   خوادم VPS مكشوفة، ويضمن اتصالاً مستقراً ومخفياً ضمن
   حركة مرور الشبكة العادية.

3. تمويه وتخصيص متقدم:
   إمكانية حقن أيقونة مخصصة (Custom Icon) واسم حزمة
   (Package Name) ديناميكي لجعل التطبيق يبدو كبرنامج
   شرعي تماماً.

4. تحكم شامل بالجهاز:
   وصول مباشر وصامت إلى:
   - الرسائل النصية (SMS)
   - جهات الاتصال
   - سجل المكالمات
   - الموقع الجغرافي (GPS)
   - الكاميرا
   - معرض الصور
   - مقاطع الفيديو

5. مسجل المفاتيح (Keylogger):
   يعمل عبر دمج خدمة إمكانية الوصول (Accessibility Service)
   لرصد وتسجيل كل ضغطة زر يتم إدخالها على الجهاز بدقة عالية.

6. مستمع الإشعارات (Notification Listener):
   اعتراض وقراءة جميع الإشعارات الواردة من أي تطبيق في
   الوقت الفعلي (مثالي لسحب رموز التحقق OTP والرسائل
   الفورية).

7. استخراج البيانات (Exfiltration):
   سحب تلقائي ومباشر لكلمات المرور المحفوظة ومحتوى
   الحافظة (Clipboard).

## آلية البناء والاستخدام:

    chmod +x AhmedBuilder.sh
    ./AhmedBuilder.sh

أدخل:
  - Bot Token
  - Chat ID
  - App Name
  - Package Name
  - Icon Path (اختياري)

يتم تجميع وتوقيع ملف الـ APK تلقائياً وحفظه في مجلد:
  output/

## إعداد الجهاز المستهدف:

1. فتح متجر Google Play على الجهاز المستهدف.
2. الانتقال إلى: أيقونة الملف الشخصي > Play Protect > الإعدادات.
3. تعطيل خيار "فحص التطبيقات باستخدام Play Protect".
4. تثبيت ملف الـ APK المولد.
5. فتح التطبيق ومنحه كافة الأذونات المطلوبة.
6. التفعيل النهائي:
   - الإعدادات > إمكانية الوصول (Accessibility) > تفعيل Keylogger
   - الإعدادات > الإشعارات > إشعارات الجهاز والتطبيقات > تفعيل Notification Service


# ============================================================
# [ English ]
# Technical Explanation & Features
# ============================================================

AhmedRAT is a highly advanced and polished Remote Access
solution, engineered specifically for Red Team operations and
penetration testing, featuring precise architecture and
advanced evasion capabilities.

## Core Features:

1. Bilingual Interface:
   Full support for both Arabic and English to ensure seamless
   deployment across diverse target environments.

2. Telegram-based C2 Infrastructure:
   Leverages encrypted Telegram protocols, completely
   eliminating the need for Port Forwarding or exposed VPS
   servers. This guarantees a stable, stealthy connection
   masked as legitimate network traffic.

3. Advanced Camouflage & Customization:
   Dynamic injection of a Custom Icon and Package Name,
   allowing the payload to blend in perfectly as a legitimate
   application.

4. Complete Device Control:
   Direct, silent access to:
   - SMS
   - Contacts
   - Call Logs
   - GPS Location
   - Camera
   - Photos
   - Videos

5. Accessibility Keylogger:
   Utilizes the Android Accessibility Service to seamlessly
   monitor and log every keystroke entered on the device with
   high precision.

6. Notification Listener:
   Intercepts and reads all incoming notifications from any
   application in real-time (highly effective for capturing
   OTPs and instant messages).

7. Data Exfiltration:
   Automated, background extraction of saved passwords and
   Clipboard content.

## Build & Usage Mechanism:

    chmod +x AhmedBuilder.sh
    ./AhmedBuilder.sh

Input:
  - Bot Token
  - Chat ID
  - App Name
  - Package Name
  - Icon Path (optional)

The APK is automatically compiled, signed, and saved in:
  output/

## Target Device Setup:

1. Open the Google Play Store on the target Android device.
2. Navigate to: Profile Icon > Play Protect > Settings.
3. Disable "Scan apps with Play Protect".
4. Install the generated APK.
5. Open the app and grant all requested permissions.
6. Final Activation:
   - Settings > Accessibility > Enable Keylogger Service
   - Settings > Notifications > Device & app notifications >
     Enable Notification Service


# ============================================================
#  [EOF]
#  Yemen Spam | يمن سبام
#  Mr. Ahmed Yemen | ام ار احمد اليمن
#  Yemen Security Research
#  🇾🇪 YA
# ============================================================
