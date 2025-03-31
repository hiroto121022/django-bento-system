from django.db import models

class User(models.Model):
    line_id = models.CharField(max_length=100, unique=True)  # LINEのユーザーID
    name = models.CharField(max_length=100)  # ユーザー名

    def __str__(self):
        return self.name

class Cool(models.Model):
    number = models.IntegerField(unique=True)  # クール番号（例：1, 2, 3）
    start_date = models.DateField()  # クールの開始日
    end_date = models.DateField()  # クールの終了日

    def __str__(self):
        return f"{self.number}クール ({self.start_date} - {self.end_date})"

class Day(models.Model):
    cool = models.ForeignKey(Cool, on_delete=models.CASCADE)  # クールに紐づく
    date = models.DateField(unique=True)  # 日付（クール内の各日）
    is_holiday = models.BooleanField(default=False)  # 休業日かどうか

    def __str__(self):
        status = "休業日" if self.is_holiday else "営業日"
        return f"{self.date} ({status})"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザー
    day = models.ForeignKey(Day, on_delete=models.CASCADE)  # 日付
    is_present = models.BooleanField(default=True)  # ○=True, ×=False

    def __str__(self):
        return f"{self.user.name} - {self.day.date} : {'○' if self.is_present else '×'}"

class Menu(models.Model):
    number = models.IntegerField(unique=True)
    menu_image = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.number}月献立表"
