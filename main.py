import pyautogui
import time
from datetime import datetime
import os
import pytesseract
from PIL import Image, ImageEnhance

# Открываем файл 'settings.txt' в текущей директории
with open('settings.txt', 'r') as file:
    # Читаем из файла
    settings_data = [file.readline().strip() for _ in range(6)]

# Периодичность (секунд) для скриншота
period = int(settings_data[5])

# Путь к Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = f"{settings_data[0]}"

# Координаты левого верхнего и правого нижнего углов области для скриншота
left_x = int(settings_data[1])
left_y = int(settings_data[2])
right_x = int(settings_data[3])
right_y = int(settings_data[4])

# Папка для сохранения скриншотов
folder_name = 'screen'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Файл для накопления распознанного текста
text_file = "db.txt"

def take_screenshot():
    # Получаем текущее время для имени файла
    current_time = datetime.now().strftime("%Y-%m-%d__%H:%M")
    hours = datetime.now().strftime("%H")
    minutes = datetime.now().strftime("%M")
    # Делаем скриншот указанной области
    screenshot = pyautogui.screenshot(region=(left_x, left_y, right_x - left_x, right_y - left_y))
    # Сохраняем скриншот в папку
    # screenshot_path = os.path.join(folder_name, f"screenshot_{current_time}.png")
    screenshot_path = os.path.join(folder_name, f"screenshot.png")
    screenshot.save(screenshot_path)
    print(f"Скриншот сохранен как {screenshot_path}")

    # Работаем с контрастностью
    start_image = Image.open(f"{screenshot_path}")
    changing_contrast = ImageEnhance.Contrast(start_image)
    contrast_image = changing_contrast.enhance(2)
    contrast_image.save(f"screen/{hours}-{minutes}_contrast.png")

    # Распознаем текст на скриншоте
    # Предыдущий:
    # recognized_text = pytesseract.image_to_string(screenshot)
    # Новый:
    # recognized_text = pytesseract.image_to_string(contrast_image, config='--psm 6 --oem 3')
    recognized_text = pytesseract.image_to_string(contrast_image, config = '-c tessedit_char_whitelist=0123456789')

    try:
        print(float(recognized_text))
        print("Распознанный текст:", recognized_text)

        # Сохраняем результат в текстовый файл
        with open(text_file, "a", encoding="utf-8") as file:
            file.write(f"{current_time} – {(recognized_text)}")
    except:
        print('NaN')

        # Сохраняем результат в текстовый файл
        with open(text_file, "a", encoding="utf-8") as file:
            file.write(f"{current_time} – NaN\n")

def main():
    print(f"Приложение запущено. Каждые {period} секунд будет делаться скриншот, а текст распознаваться и сохраняться.")
    while True:
        take_screenshot()  # Делаем скриншот и распознаем текст
        time.sleep(period)  # Ждем одну минуту

if __name__ == "__main__":
    main()
