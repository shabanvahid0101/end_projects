from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
import pandas as pd
import random
import os
import arabic_reshaper
from bidi.algorithm import get_display

# تابع برای درست کردن متن فارسی
def fix_persian_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

class WordGameApp(App):
    def build(self):
        # لود فایل CSV
        try:
            self.df = pd.read_csv(os.path.join(os.path.dirname(__file__), "vocabulary-csv.csv"))
            print("ستون‌های فایل CSV:", self.df.columns.tolist())  # دیباگ: چاپ ستون‌ها
            # فیلتر کردن ردیف‌هایی که مقدار hiragana/katakana ندارن یا نامعتبرن
            self.df = self.df[self.df["hiragana/katakana"].notna() & (self.df["hiragana/katakana"].astype(str).str.strip() != "")]
            print("تعداد ردیف‌های معتبر:", len(self.df))  # دیباگ: تعداد ردیف‌های معتبر
        except FileNotFoundError:
            print("فایل CSV پیدا نشد!")
            return None

        self.score = 0  # امتیاز هر بار از 0 شروع می‌شه
        self.time_left = 1000
        self.history = []
        self.hiragana = ""

        # لود صداها
        self.correct_sound = SoundLoader.load("sounds/correct.mp3")
        self.wrong_sound = SoundLoader.load("sounds/wrong.mp3")

        # تنظیم پس‌زمینه کل اپ
        Window.clearcolor = (0.6, 0.6, 0.8, 1)  # پس‌زمینه آبی ملایم

        # چیدمان اصلی
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        # عنوان و امتیاز و زمان
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.title_label = Label(
            text=fix_persian_text("آموزش لغات به صورت تخصصی"), font_size=26, color=(0, 0, 0, 1),
            font_name="Vazir.ttf", text_size=(None, None), halign="right"
        )
        self.score_label = Label(
            text=fix_persian_text(f"امتیاز: {self.score}"), font_size=22, font_name="Vazir.ttf", color=(0, 0, 0, 1),
            text_size=(None, None), halign="right"
        )
        self.time_label = Label(
            text=fix_persian_text(f"زمان باقی‌مانده: {self.time_left}"), font_size=22, font_name="Vazir.ttf", color=(0, 0, 0, 1),
            text_size=(None, None), halign="right"
        )
        top_bar.add_widget(self.title_label)
        top_bar.add_widget(self.score_label)
        top_bar.add_widget(self.time_label)
        layout.add_widget(top_bar)

        # سوال (کانجی) با پس‌زمینه و سایه
        kanji_container = BoxLayout(size_hint=(1, 0.12))
        with kanji_container.canvas.before:
            Color(0.5, 0.5, 0.5, 0.5)  # سایه خاکستری
            self.kanji_shadow = Rectangle(pos=(kanji_container.pos[0] + 5, kanji_container.pos[1] - 5), size=kanji_container.size)
            Color(0.8, 0.5, 0.2, 1)  # رنگ قهوه‌ای ملایم
            self.kanji_rect = Rectangle(pos=kanji_container.pos, size=kanji_container.size)
        kanji_container.bind(pos=self.update_kanji_rect, size=self.update_kanji_rect)
        self.kanji_label = Label(
            text=fix_persian_text("برای شروع روی دکمه Start کلیک کنید"), font_size=40,
            color=(1, 1, 0.8, 1),
            font_name="Vazir.ttf", base_direction="ltr", text_size=(None, None), halign="center"
        )
        kanji_container.add_widget(self.kanji_label)
        layout.add_widget(kanji_container)

        # وضعیت (فارسی و انگلیسی)
        status_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.06))
        self.persian_label = Label(
            text=fix_persian_text("Persian:"), font_size=20, color=(0, 0, 0, 1),
            font_name="Vazir.ttf", text_size=(None, None), halign="right"
        )
        self.english_label = Label(
            text="English:", font_size=20, color=(0, 0, 0, 1),
            font_name="Vazir.ttf", base_direction="ltr", text_size=(None, None), halign="left"
        )
        status_bar.add_widget(self.persian_label)
        status_bar.add_widget(self.english_label)
        layout.add_widget(status_bar)

        # گزینه‌های جواب
        self.answer_grid = GridLayout(cols=2, spacing=20, size_hint=(1, 0.4))
        self.answer_buttons = []
        for i in range(4):
            btn = Button(
                text=f"answer{i+1}", font_size=28, background_color=(0.2, 0.6, 0.8, 1),
                color=(1, 1, 1, 1),
                font_name="NotoSansJP-Regular.ttf", base_direction="ltr", text_size=(None, None), halign="center"
            )
            with btn.canvas.before:
                Color(0.2, 0.6, 0.8, 1)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[10])
            btn.bind(pos=self.update_btn_rect, size=self.update_btn_rect)
            btn.bind(on_press=lambda instance, idx=i: self.score_cal(idx))
            self.answer_grid.add_widget(btn)
            self.answer_buttons.append(btn)
        layout.add_widget(self.answer_grid)

        # دکمه‌های پایین
        button_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=20)
        back_btn = Button(
            text="Back", font_size=24, background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_name="Vazir.ttf", on_press=self.back_word
        )
        with back_btn.canvas.before:
            Color(0.2, 0.7, 0.3, 1)
            back_btn.rect = RoundedRectangle(pos=back_btn.pos, size=back_btn.size, radius=[10])
        back_btn.bind(pos=self.update_btn_rect, size=self.update_btn_rect)

        self.next_btn = Button(
            text=fix_persian_text("Start"), font_size=24, background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_name="Vazir.ttf", on_press=self.change_word
        )
        with self.next_btn.canvas.before:
            Color(0.2, 0.7, 0.3, 1)
            self.next_btn.rect = RoundedRectangle(pos=self.next_btn.pos, size=self.next_btn.size, radius=[10])
        self.next_btn.bind(pos=self.update_btn_rect, size=self.update_btn_rect)

        # دکمه مرور غلط‌ها
        review_btn = Button(
            text=fix_persian_text("مرور غلط‌ها"), font_size=24, background_color=(0.7, 0.3, 0.2, 1),  # رنگ نارنجی ملایم
            color=(1, 1, 1, 1),
            font_name="Vazir.ttf", on_press=self.show_mistakes
        )
        with review_btn.canvas.before:
            Color(0.7, 0.3, 0.2, 1)
            review_btn.rect = RoundedRectangle(pos=review_btn.pos, size=review_btn.size, radius=[10])
        review_btn.bind(pos=self.update_btn_rect, size=self.update_btn_rect)

        button_bar.add_widget(back_btn)
        button_bar.add_widget(self.next_btn)
        button_bar.add_widget(review_btn)
        layout.add_widget(button_bar)

        Clock.schedule_interval(self.update_time, 1)

        return layout

    def update_btn_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def update_kanji_rect(self, instance, value):
        self.kanji_rect.pos = instance.pos
        self.kanji_rect.size = instance.size
        self.kanji_shadow.pos = (instance.pos[0] + 5, instance.pos[1] - 5)
        self.kanji_shadow.size = instance.size

    def save_mistake(self, kanji, hiragana, persian, english):
        # آموزش: ذخیره کلمه اشتباه توی فایل CSV
        mistake = pd.DataFrame([[kanji, hiragana, persian, english]], columns=["kanji", "hiragana/katakana", "persian", "english"])
        file_path = os.path.join(os.path.dirname(__file__), "mistakes.csv")  # مسیر پویا
        if os.path.exists(file_path):
            mistake.to_csv(file_path, mode='a', header=False, index=False)
        else:
            mistake.to_csv(file_path, mode='w', header=True, index=False)

    def clear_mistakes(self, instance, popup):
        # آموزش: حذف همه کلمات اشتباه
        file_path = os.path.join(os.path.dirname(__file__), "mistakes.csv")
        if os.path.exists(file_path):
            os.remove(file_path)
        popup.dismiss()
        # باز کردن دوباره پنجره برای به‌روزرسانی
        self.show_mistakes(None)

    def update_label_rect(self, instance, value):
        # تابع کمکی برای به‌روزرسانی پس‌زمینه لیبل‌ها
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def show_mistakes(self, instance):
        # آموزش: باز کردن یه پنجره جدید برای نمایش کلمات اشتباه
        try:
            mistakes_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "mistakes.csv"))
        except FileNotFoundError:
            mistakes_df = pd.DataFrame(columns=["kanji", "hiragana/katakana", "persian", "english"])

        # ساختن محتوای پنجره
        popup_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        # اضافه کردن پس‌زمینه و سایه به Popup
        with popup_layout.canvas.before:
            Color(0.5, 0.5, 0.5, 0.5)  # سایه خاکستری
            self.popup_shadow = Rectangle(pos=(popup_layout.pos[0] + 5, popup_layout.pos[1] - 5), size=popup_layout.size)
            Color(0.9, 0.9, 0.9, 1)  # پس‌زمینه خاکستری روشن
            self.popup_rect = Rectangle(pos=popup_layout.pos, size=popup_layout.size)
        popup_layout.bind(pos=self.update_popup_rect, size=self.update_popup_rect)

        grid = GridLayout(cols=4, spacing=10, size_hint_y=None, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        # اضافه کردن هدر با رنگ متمایز
        grid.add_widget(Label(
            text="Kanji", font_size=22, size_hint_y=None, height=40, color=(1, 0, 0, 1),  # زرد روشن
            font_name="NotoSansJP-Regular.ttf", halign="center", bold=True
        ))
        grid.add_widget(Label(
            text="Hiragana", font_size=22, size_hint_y=None, height=40, color=(1, 0, 0, 1),
            font_name="NotoSansJP-Regular.ttf", halign="center", bold=True
        ))
        grid.add_widget(Label(
            text=fix_persian_text("Persian"), font_size=22, size_hint_y=None, height=40, color=(1, 0, 0, 1),
            font_name="Vazir.ttf", base_direction="rtl", halign="center", bold=True
        ))
        grid.add_widget(Label(
            text="English", font_size=22, size_hint_y=None, height=40, color=(1, 0, 0, 1),
            font_name="Vazir.ttf", base_direction="ltr", halign="center", bold=True
        ))

        # اضافه کردن کلمات اشتباه با رنگ متناوب
        for idx, row in mistakes_df.iterrows():
            row_color = (0.8, 0.8, 0.8, 1) if idx % 2 == 0 else (0.7, 0.7, 0.7, 1)  # رنگ متناوب
            # لیبل برای Kanji
            kanji_label = Label(
                text=str(row["kanji"]), font_size=18, size_hint_y=None, height=40, color=(0, 0, 1, 1),
                font_name="NotoSansJP-Regular.ttf", halign="center", text_size=(None, None)
            )
            with kanji_label.canvas.before:
                Color(*row_color)
                kanji_label.rect = Rectangle(pos=kanji_label.pos, size=kanji_label.size)
            kanji_label.bind(pos=self.update_label_rect, size=self.update_label_rect)
            grid.add_widget(kanji_label)

            # لیبل برای Hiragana
            hiragana_label = Label(
                text=str(row["hiragana/katakana"]), font_size=18, size_hint_y=None, height=40, color=(0, 0, 1, 1),
                font_name="NotoSansJP-Regular.ttf", halign="center", text_size=(None, None)
            )
            with hiragana_label.canvas.before:
                Color(*row_color)
                hiragana_label.rect = Rectangle(pos=hiragana_label.pos, size=hiragana_label.size)
            hiragana_label.bind(pos=self.update_label_rect, size=self.update_label_rect)
            grid.add_widget(hiragana_label)

            # لیبل برای Persian
            persian_label = Label(
                text=fix_persian_text(str(row["persian"])), font_size=18, size_hint_y=None, height=40, color=(0, 0, 1, 1),
                font_name="Vazir.ttf", base_direction="rtl", halign="center", text_size=(None, None)
            )
            with persian_label.canvas.before:
                Color(*row_color)
                persian_label.rect = Rectangle(pos=persian_label.pos, size=persian_label.size)
            persian_label.bind(pos=self.update_label_rect, size=self.update_label_rect)
            grid.add_widget(persian_label)

            # لیبل برای English
            english_label = Label(
                text=str(row["english"]), font_size=18, size_hint_y=None, height=40, color=(0, 0, 1, 1),
                font_name="Vazir.ttf", base_direction="ltr", halign="center", text_size=(None, None)
            )
            with english_label.canvas.before:
                Color(*row_color)
                english_label.rect = Rectangle(pos=english_label.pos, size=english_label.size)
            english_label.bind(pos=self.update_label_rect, size=self.update_label_rect)
            grid.add_widget(english_label)

        popup_layout.add_widget(grid)

        # دکمه‌های پایین
        button_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        clear_btn = Button(
            text=fix_persian_text("حذف همه غلط‌ها"), font_size=20, background_color=(0.8, 0.2, 0.2, 1),  # قرمز
            color=(1, 1, 1, 1), font_name="Vazir.ttf"
        )
        clear_btn.bind(on_press=lambda x: self.clear_mistakes(x, popup))
        close_btn = Button(
            text="Close", font_size=20, background_color=(0.2, 0.7, 0.3, 1),  # سبز
            color=(1, 1, 1, 1), font_name="Vazir.ttf"
        )
        button_bar.add_widget(clear_btn)
        button_bar.add_widget(close_btn)
        popup_layout.add_widget(button_bar)

        # باز کردن پنجره
        popup = Popup(title=fix_persian_text("Mistakes"), content=popup_layout, size_hint=(0.9, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def update_popup_rect(self, instance, value):
        self.popup_rect.pos = instance.pos
        self.popup_rect.size = instance.size
        self.popup_shadow.pos = (instance.pos[0] + 5, instance.pos[1] - 5)
        self.popup_shadow.size = instance.size

    def change_word(self, instance):
        self.next_btn.text = fix_persian_text("Next")
        for btn in self.answer_buttons:
            btn.background_color = (0.2, 0.6, 0.8, 1)
            btn.color = (1, 1, 1, 1)

        try:
            random_row = self.df.sample()
            kanji = random_row["kanji"].values[0]
            self.hiragana = random_row["hiragana/katakana"].values[0]
            persian = random_row["persian"].values[0] if pd.notna(random_row["persian"].values[0]) else "None"
            english = random_row["english"].values[0] if pd.notna(random_row["english"].values[0]) else "None"
            print(f"Kanji: {kanji}, Hiragana: {self.hiragana}, Persian: {persian}, English: {english}")
        except KeyError as e:
            print(f"خطا: ستون {e} توی فایل CSV نیست!")
            return

        # آموزش: انتخاب جواب‌ها با تعداد هیراگانای مشابه و حداقل دو هیراگانای مشترک
        hiragana_length = len(self.hiragana)  # تعداد هیراگاناهای جواب اصلی
        hiragana_set = set(self.hiragana)  # تبدیل جواب اصلی به مجموعه برای پیدا کردن کاراکترهای مشترک

        # فیلتر کردن گزینه‌ها
        candidates = []
        for idx, row in self.df.iterrows():
            candidate_hiragana = row["hiragana/katakana"]
            # بررسی اینکه مقدار معتبر باشه (رشته باشه و خالی نباشه)
            if not isinstance(candidate_hiragana, str) or candidate_hiragana.strip() == "":
                print(f"ردیف {idx} مقدار نامعتبر داره: {candidate_hiragana}")  # دیباگ
                continue
            if candidate_hiragana == self.hiragana:  # گزینه نباید خودش جواب اصلی باشه
                continue
            # شرط 1: تعداد هیراگاناها باید برابر باشه
            if len(candidate_hiragana) != hiragana_length:
                continue
            # شرط 2: حداقل دو هیراگانای مشترک داشته باشه
            candidate_set = set(candidate_hiragana)
            common_hiragana = len(hiragana_set.intersection(candidate_set))
            if common_hiragana >= 2:
                candidates.append(candidate_hiragana)

        # انتخاب 3 گزینه از کاندیداها
        if len(candidates) < 3:
            print("کاندیدای کافی پیدا نشد! گزینه‌ها به‌صورت تصادفی انتخاب می‌شن.")
            answers = [row["hiragana/katakana"] for _, row in self.df.sample(3).iterrows() if isinstance(row["hiragana/katakana"], str)]
        else:
            answers = random.sample(candidates, 3)

        answers.append(self.hiragana)
        random.shuffle(answers)

        for i, btn in enumerate(self.answer_buttons):
            btn.text = answers[i]

        # انیمیشن fade-in برای تغییر سوال
        self.kanji_label.opacity = 0
        self.persian_label.opacity = 0
        self.english_label.opacity = 0
        self.kanji_label.text = f"Kanji: {kanji}"
        self.kanji_label.font_name = "NotoSansJP-Regular.ttf"
        self.persian_label.text = f"Persian: {fix_persian_text(persian)}"
        self.english_label.text = f"English: {english}"
        anim = Animation(opacity=1, duration=0.5)
        anim.start(self.kanji_label)
        anim.start(self.persian_label)
        anim.start(self.english_label)

        self.history.append({"kanji": kanji, "hiragana": self.hiragana, "persian": persian, "english": english, "answers": answers})
        if len(self.history) > 5:
            self.history.pop(0)

    def back_word(self, instance):
        if len(self.history) > 1:
            prev = self.history[-2]
            self.kanji_label.opacity = 0
            self.persian_label.opacity = 0
            self.english_label.opacity = 0
            self.kanji_label.text = f"Kanji: {prev['kanji']}"
            self.persian_label.text = f"Persian: {fix_persian_text(prev['persian'])}"
            self.english_label.text = f"English: {prev['english']}"
            anim = Animation(opacity=1, duration=0.5)
            anim.start(self.kanji_label)
            anim.start(self.persian_label)
            anim.start(self.english_label)
            for i, btn in enumerate(self.answer_buttons):
                btn.text = prev["answers"][i]

    def score_cal(self, btn_idx):
        # پیدا کردن دکمه درست
        correct_idx = None
        for i, btn in enumerate(self.answer_buttons):
            if btn.text == self.hiragana:
                correct_idx = i
                break

        # بازخورد بصری و صوتی
        if self.answer_buttons[btn_idx].text == self.hiragana:
            self.score += 1
            self.score_label.text = fix_persian_text(f"امتیاز: {self.score}")
            self.answer_buttons[btn_idx].background_color = (0, 1, 0, 1)  # سبز
            if self.correct_sound:
                self.correct_sound.play()
        else:
            self.answer_buttons[btn_idx].background_color = (1, 0, 0, 1)  # قرمز
            self.answer_buttons[correct_idx].background_color = (0, 1, 0, 1)  # سبز
            if self.wrong_sound:
                self.wrong_sound.play()
            # ذخیره کلمه اشتباه
            self.save_mistake(
                self.history[-1]["kanji"],
                self.history[-1]["hiragana"],
                self.history[-1]["persian"],
                self.history[-1]["english"]
            )

        # برگرداندن رنگ دکمه‌ها به حالت اولیه بعد از 1 ثانیه
        Clock.schedule_once(lambda dt: self.change_word(None), 1)

    def update_time(self, dt):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.text = fix_persian_text(f"زمان باقی‌مانده: {self.time_left}")
        else:
            self.time_label.text = fix_persian_text("زمان تمام شد!")

if __name__ == '__main__':
    WordGameApp().run()