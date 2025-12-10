import tkinter as tk

class human:
    def __init__(self,height,weight):
        self.BMI = weight / (height/100)**2
    def value(self):
        return round(self.BMI,2)
    def is_fat(self):
        if self.BMI < 18.5:
            return '痩せ型'
        elif self.BMI < 25:
            return '普通体重'
        elif self.BMI < 30:
            return '肥満(1度)'
        elif self.BMI < 35:
            return '肥満(2度)'
        elif self.BMI < 40:
            return '肥満(3度)'
        else:
            return '肥満(4度)'

if __name__ == '__main__':
    
    body = human(int(input('please insert your height: ')),int(input('please insert your weight: ')))
    print('BMI:',body.value())
    print('判定:',body.is_fat())

