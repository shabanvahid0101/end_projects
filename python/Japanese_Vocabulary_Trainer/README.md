# Japanese Vocabulary Trainer  
**اپلیکیشن دسکتاپ آموزش لغات ژاپنی (کانجی → هیراگانا) با سیستم هوشمند مرور اشتباهات**

![demo](output.gif)


### ویژگی‌های کلیدی
- نمایش کانجی + معنی فارسی و انگلیسی  
- ۴ گزینه هیراگانا/کاتاکانا (گزینه‌های اشتباه هوشمندانه انتخاب می‌شن)  
- سیستم امتیازدهی و تایمر  
- صدا برای پاسخ درست/غلط  
- ذخیره خودکار کلمات اشتباه در `mistakes.csv`  
- پنجره مرور اشتباهات با امکان حذف همه  
- پشتیبانی کامل از فارسی (راست‌به‌چپ)  
- طراحی زیبا با انیمیشن، سایه، گوشه‌های گرد  
- دکمه Back برای برگشت به سوال قبلی  
- کاملاً آفلاین و قابل اجرا روی ویندوز/مک/لینوکس

### تکنولوژی‌های استفاده شده
- **Kivy** → فریم‌ورک GUI چندپلتفرمی پایتون
- **Pandas** → خواندن و مدیریت دیتاست لغات
- **arabic_reshaper + bidi** → نمایش صحیح فارسی
- **Kivy Animation & SoundLoader** → افکت و صدا

### ساختار فایل‌ها 
Japanese-Vocab-Trainer/
├── main.py
├── vocabulary-csv.csv          ← فایل اصلی لغات (ستون‌ها: kanji, hiragana/katakana, persian, english)
├── mistakes.csv                ← خودکار ساخته می‌شه (کلمات اشتباه)
├── Vazir.ttf                   ← فونت فارسی
├── NotoSansJP-Regular.ttf      ← فونت ژاپنی
├── sounds/
│   ├── correct.mp3
│   └── wrong.mp3
└── demo.gif                    ← پیش‌نمایش


### نصب و اجرا (خیلی ساده!)

```bash
# 1. کلون پروژه
git clone https://github.com/shabanvahid0101/top_projects.git
cd top_projects/python/Japanese_Vocabulary_Trainer

# 2. ساخت محیط مجازی (توصیه می‌شود)
python -m venv venv
venv\Scripts\activate   # ویندوز
# source venv/bin/activate  # مک/لینوکس

# 3. نصب کتابخانه‌ها
pip install kivy pandas arabic-reshaper python-bidi

# 4. اجرا
python main.py
```
فرمت فایل vocabulary-csv.csv 

kanji|hiragana/katakana|persian|english

طراحی، توسعه و دیزاین توسط وحید شعبان




