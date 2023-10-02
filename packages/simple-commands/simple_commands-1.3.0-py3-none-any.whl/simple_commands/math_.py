import math

# คำนวณพื้นที่สามเหลี่ยม
def calculate_triangle_area(base, height):
    return 0.5 * base * height

# คำนวณพื้นที่สี่เหลี่ยมผืนผ้า
def calculate_rectangle_area(length, width):
    return length * width

# คำนวณพื้นที่สี่เหลี่ยมจตุรัส
def calculate_square_area(side):
    return side * side

# คำนวณพื้นที่วงกลม
def calculate_circle_area(radius):
    return math.pi * (radius ** 2)

# คำนวณความยาวเส้นรอบรูปสามเหลี่ยม
def calculate_triangle_perimeter(side1, side2, side3):
    return side1 + side2 + side3

# คำนวณความยาวเส้นรอบรูปสี่เหลี่ยมผืนผ้า
def calculate_rectangle_perimeter(length, width):
    return 2 * (length + width)

# คำนวณความยาวเส้นรอบรูปสี่เหลี่ยมจตุรัส
def calculate_square_perimeter(side):
    return 4 * side

# คำนวณความยาวเส้นรอบรูปวงกลม
def calculate_circle_circumference(radius):
    return 2 * math.pi * radius

# คำนวณปริมาตรของทรงกรวย
def calculate_cone_volume(radius, height):
    return (1/3) * math.pi * (radius ** 2) * height

# คำนวณปริมาตรของทรงกระบอก
def calculate_cylinder_volume(radius, height):
    return math.pi * (radius ** 2) * height

# คำนวณปริมาตรของทรงกระบอกออกซิเดียน
def calculate_oxygen_cylinder_volume(diameter, height):
    radius = diameter / 2
    return math.pi * (radius ** 2) * height


def tempFtoC(F):
    return (F - 32) * 5/9

def tempCtoF(C):
    return (C * 9/5) + 32

def find_area(x, z, y):
    return x * z * y

def power(num, num1):
    return num ** num1

def sigma_sum(start, end, number):
    total = 0
    for i in range(start, end + 1):
        total += number
    return total

def percentage(part, whole):
    percentage = (part/whole)*100
    return percentage, 100 - percentage 

# ฟังก์ชันคำนวณค่ารากที่สอง
def square_root(number):
    return math.sqrt(number)

# ฟังก์ชันคำนวณค่ารากที่สาม
def cube_root(number):
    return math.pow(number, 1/3)

# ฟังก์ชันคำนวณค่ายกกำลังสาม
def power_of_three(number):
    return math.pow(number, 3)

# ฟังก์ชันคำนวณค่าค่าสัมบูรณ์
def absolute_value(number):
    return abs(number)

# ฟังก์ชันตรวจสอบเลขคู่หรือเลขคี่
def is_even_or_odd(number):
    if number % 2 == 0:
        return True
    else:
        return False

# ฟังก์ชันคำนวณค่าเฉลี่ย
def average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

# ฟังก์ชันคำนวณค่ามากสุดและค่าน้อยสุด
def max_and_min(numbers):
    if len(numbers) == 0:
        return None, None
    max_value = max(numbers)
    min_value = min(numbers)
    return max_value, min_value

def repower(base, exponent):
    result = 1
    for _ in range(exponent):
        result *= base
    return f"({base}*{base}*" + "*".join([str(base) for _ in range(exponent-2)]) + f"*{base})"

def convert_storage_size(value, from_unit, to_unit):
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
    }
    if from_unit not in units or to_unit not in units:
        raise TypeError("The values from_unit, to_unit were entered incorrectly.")

    if value < 0:
        raise ValueError("Enter a value that is not 0.")

    result = (value * units[from_unit]) / units[to_unit]
    return result, to_unit

def reconvert_storage_size(value, from_unit, to_unit):
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
    }

    if from_unit not in units or to_unit not in units:
        raise TypeError("The values from_unit, to_unit were entered incorrectly.")

    if value < 0:
        raise ValueError("Enter a value that is not 0.")
    result = (value * units[from_unit]) / units[to_unit]
    return result, to_unit