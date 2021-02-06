from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer, QTime, Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QImage, QBrush
from PyQt5.QtWidgets import QFrame, QListWidgetItem

from ui.main import Ui_MainWindow
from ui.tab_on_today import Ui_Form as CurrentDayUi
from ui.tab_on_3_days import Ui_Form as ThreeDaysUi
from ui.tab_on_5_days import Ui_Form as FiveDaysUi
from ui.list_item import Ui_Form as ListItemUi
from ui.list_item_5 import Ui_Form as ListItemUi5
from weather import WeatherManager, WeatherType
from const import available_cities, day_translate
import sys
import logging
from datetime import datetime, timedelta
from calendar import day_abbr

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# Переменная для хранения текущего выбранного города
selected_city = "Ярославль"


class TabOnToday(QtWidgets.QWidget):
    """ Виджет вкладки "На сегодня" """
    timer = QTimer()
    signal = pyqtSignal(int)

    def __init__(self, wm: WeatherManager):
        logger.debug("Initialised TabOnToday")
        super(TabOnToday, self).__init__()
        self.ui = CurrentDayUi()
        self.ui.setupUi(self)
        self.__wm = wm

        self.__init_weather_info()
        self.__init_timer()
        self.__init_cities()
        self.__set_bg_image()

        self.ui.cb_cities.currentIndexChanged.connect(self.__reload_data)

        self.ui.pb_add_city.setVisible(False)

    def __set_bg_image(self):
        """Установить задний фон"""
        palette = QPalette()
        image = QImage('src/bg.jpg')
        scaled = image.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Window, QBrush(scaled))
        self.setPalette(palette)

    def __init_cities(self):
        """Добавить доступные города в выпадающий список"""
        self.ui.cb_cities.addItems(list(available_cities.keys()))

    def __init_timer(self):
        self.timer.timeout.connect(self.__set_current_time)
        self.timer.start(1000)

    def __init_weather_info(self):
        """Получение и установка в ui данных о погоде"""
        global selected_city
        weather_date = self.__wm.get_for_city(available_cities[selected_city])
        self.ui.lbl_value_current_temp.setText(self.__format_temp(weather_date['temp']))
        self.ui.lbl_value_wind.setText(
            weather_date['wind']['duration'] + ", " + str(weather_date['wind']['speed']) + " м/с")
        self.ui.lbl_value_humidity.setText(str(weather_date['humidity']) + " %")
        self.ui.lbl_value_pressure.setText(str(int(weather_date['pressure'] * 0.75)) + " мм. рт. ст.")
        if weather_date['weather']:
            self.__set_weather_icon(weather_date['weather'][0]['icon'])
            self.ui.lbl_desc.setText(str(weather_date['weather'][0]['description']))
        else:
            logger.warning('No weather info in parsed API response')

    def __set_current_time(self):
        """Установка текущего времени"""
        current_time = QTime.currentTime()
        self.ui.lbl_current_time.setText(current_time.toString('hh:mm:ss'))

    def __set_weather_icon(self, icon_id):
        """Установить иконку погоды по ид"""
        pixmap = QtGui.QPixmap(self.__get_icon_by_id(icon_id)).scaled(85, 85, QtCore.Qt.KeepAspectRatio)
        self.ui.lbl_current_weather_icon.setPixmap(pixmap)

    def __reload_data(self):
        """Обновить данные о погоде"""
        global selected_city
        selected_city = self.ui.cb_cities.currentText()
        logger.info(selected_city)
        self.__init_weather_info()

    @staticmethod
    def __format_temp(temp):
        """Вернет форматированую строку для температуры"""
        return f'{"+" if temp > 0 else ""}{temp} \u2103'

    @staticmethod
    def __get_icon_by_id(icon_id: str):
        """Вернет путь до иконки погоды"""
        return f"src/{icon_id}@2x.png"


class CustomWidgetItem(QtWidgets.QWidget):
    """Кастомный виджет для отображения в QListWidget"""

    def __init__(self, title, temp, desc, pict_id, parent=None):
        super(CustomWidgetItem, self).__init__(parent)
        self.ui = ListItemUi()
        self.ui.setupUi(self)

        self.ui.lbl_temp.setText(temp)
        self.ui.lbl_desc.setText(desc)
        self.ui.lbl_title.setText(title)
        self.__set_weather_icon(pict_id)

    def __set_weather_icon(self, icon_id):
        """Установить иконку погоды по ид"""
        pixmap = QtGui.QPixmap(self.__get_icon_by_id(icon_id)).scaled(75, 75, QtCore.Qt.KeepAspectRatio)
        self.ui.lbl_picture.setPixmap(pixmap)

    @staticmethod
    def __get_icon_by_id(icon_id: str):
        """Вернет путь до иконки погоды"""
        return f"src/{icon_id}@2x.png"


class TabOnThreeDays(QtWidgets.QWidget):
    """ Виджет вкладки "На 3 дня" """

    def __init__(self, wm: WeatherManager):
        logger.debug("Initialised TabOnThreeDays")
        super(TabOnThreeDays, self).__init__()
        self.ui = ThreeDaysUi()
        self.ui.setupUi(self)
        self.__wm = wm
        self.__current_city = None

        self.__set_bg_image()
        self.__init_weather_info()

        self.__set_style_sheet()

    def __set_bg_image(self):
        """Установить задний фон"""
        palette = QPalette()
        image = QImage('src/bg.jpg')
        scaled = image.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Window, QBrush(scaled))
        self.setPalette(palette)

    def __set_style_sheet(self):
        """Добавить стили к элементам"""
        # Прозрачный фон для ListView
        self.ui.lw_day_1.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.ui.lw_day_2.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.ui.lw_day_3.setStyleSheet("background-color: rgba(0,0,0,0)")

    def __init_weather_info(self):
        global selected_city
        logger.info(selected_city)
        weather_data = self.__wm.get_for_city(available_cities[selected_city], WeatherType.PREDICT, 3)
        self.__current_city = selected_city
        logger.debug(len(weather_data.items()))
        for i, value in enumerate(
                sorted(weather_data.items(), key=lambda item: datetime.strptime(item[0], "%Y-%m-%d").date())):
            self.__set_text_by_widget_name(f"lbl_day_{i + 1}", value[0] + " " + day_translate[
                day_abbr[datetime.strptime(value[0], "%Y-%m-%d").weekday()].lower()])
            self.__fill_data_list_widget_by_name(f"lw_day_{i + 1}", value[1]['list'])

    def __fill_data_list_widget_by_name(self, name, data):
        """Заполнит List Widget"""
        try:
            lw = getattr(self.ui, name)
        except Exception as ex:
            logger.error(str(ex))
            return
        for weather_obj in data:
            weather_text = self.__get_list_item_elms(weather_obj)
            custom_widget = CustomWidgetItem(*weather_text)
            list_widget = QListWidgetItem()
            lw.addItem(list_widget)
            lw.setItemWidget(list_widget, custom_widget)
            list_widget.setSizeHint(custom_widget.sizeHint())
            # пустой item в качестве разделителея
            lw.addItem("")

    def __set_text_by_widget_name(self, lbl_name, text):
        """Установит текст в Widget по его названию"""
        try:
            lbl = getattr(self.ui, lbl_name)
            lbl.setText(text)
        except Exception as ex:
            logger.error(str(ex))

    @staticmethod
    def __get_list_item_elms(weather_obj):
        """Сформирует кортеж параметров для вывода в ListWidgetItem"""
        time_ = datetime.strptime(weather_obj['time'], "%H:%M:%S")
        time_str = f"{time_.time().strftime('%H:%M')} - {(time_ + timedelta(hours=3)).strftime('%H:%M')}\n"
        temp_str = f"Температура {weather_obj['temp']} \u2103\n"
        weather_str = ""
        icon = ""
        if weather_obj['weather']:
            weather_str = f"{weather_obj['weather'][0]['description'].capitalize()}"
            icon = weather_obj['weather'][0]['icon']

        return time_str, temp_str, weather_str, icon

    def update(self):
        """Обновить данные"""
        global selected_city
        if self.__current_city == selected_city:
            logger.info("TabOnThreeDays updating not necessary")
            return
        logger.info("TabOnThreeDays updated")
        self.clear()
        self.__init_weather_info()

    def clear(self):
        """Очистка List Widget"""
        logger.info("cleanup List Widgets TabOnThreeDays")
        self.ui.lw_day_1.clear()
        self.ui.lw_day_2.clear()
        self.ui.lw_day_3.clear()


class CustomWidgetItem5(QtWidgets.QWidget):
    """Кастомный виджет для отображения в QListWidget"""

    def __init__(self, date, morning, morning_temp, morning_icon, day, day_temp, day_icon, evening, evening_temp,
                 evening_icon, min_temp, max_temp, all_data=None, parent=None):
        super(CustomWidgetItem5, self).__init__(parent)
        self.ui = ListItemUi5()
        self.ui.setupUi(self)

        self.__all_data = all_data

        self.ui.lbl_date.setText(date)
        if morning:
            self.ui.lbl_morning.setText("Утром " + "{:5.2f}".format(morning_temp) + " \u2103, " + morning)
            pixmap = QtGui.QPixmap(self.__get_icon_by_id(morning_icon)).scaled(60, 60, QtCore.Qt.KeepAspectRatio)
            self.ui.lbl_morning_icon.setPixmap(pixmap)

        if day:
            self.ui.lbl_day.setText("Днем " + "{:5.2f}".format(day_temp) + " \u2103, " + day)
            pixmap = QtGui.QPixmap(self.__get_icon_by_id(day_icon)).scaled(60, 60, QtCore.Qt.KeepAspectRatio)
            self.ui.lbl_day_icon.setPixmap(pixmap)

        if evening:
            self.ui.lbl_evening.setText("Вечером " + "{:5.2f}".format(evening_temp) + " \u2103, " + evening)
            pixmap = QtGui.QPixmap(self.__get_icon_by_id(evening_icon)).scaled(60, 60, QtCore.Qt.KeepAspectRatio)
            self.ui.lbl_evening_icon.setPixmap(pixmap)

        self.ui.lbl_min_temp.setText("Минимальная за день " + min_temp + " \u2103")
        self.ui.lbl_max_temp.setText("Максимальная за день " + max_temp + " \u2103")

    @staticmethod
    def __get_icon_by_id(icon_id: str):
        """Вернет путь до иконки погоды"""
        return f"src/{icon_id}@2x.png"


class TabOnFiveDays(QtWidgets.QWidget):
    """ Виджет вкладки "На 5 дней" """

    def __init__(self, wm: WeatherManager):
        logger.debug("Initialised TabOnFiveDays")
        super(TabOnFiveDays, self).__init__()
        self.ui = FiveDaysUi()
        self.ui.setupUi(self)

        self.__wm = wm
        self.__current_city = None
        now = datetime.now()
        self.ui.lbl_current_date.setText(
            "Сегодня " + now.strftime("%Y-%m-%d") + " " + day_translate[day_abbr[now.weekday()].lower()])

        self.ui.lw_days_weather_list.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.__set_bg_image()
        self.__init_weather_info()

    def __init_weather_info(self):
        """Получить и заполнить на ui данные о погоде"""
        global selected_city
        logger.info(selected_city)
        weather_data = self.__wm.get_for_city(available_cities[selected_city], WeatherType.PREDICT, 5)
        self.__current_city = selected_city
        self.__fill_data_list_widget(weather_data)

    def __fill_data_list_widget(self, weather_data):
        for date, weather_obj in weather_data.items():
            data = self.__get_list_item_elms(weather_obj)
            custom_widget = CustomWidgetItem5(date, *data, weather_obj)
            list_widget = QListWidgetItem()
            self.ui.lw_days_weather_list.addItem(list_widget)
            self.ui.lw_days_weather_list.setItemWidget(list_widget, custom_widget)
            list_widget.setSizeHint(custom_widget.sizeHint())

    @staticmethod
    def __get_list_item_elms(weather_obj):
        """Получить кортеж для заполения List Item"""
        morning = weather_obj["main_weather"]["morning"]["description"]
        morning_temp = weather_obj["main_weather"]["morning"]["temp"]
        morning_icon = weather_obj["main_weather"]["morning"]["icon"]
        day = weather_obj["main_weather"]["day"]["description"]
        day_temp = weather_obj["main_weather"]["day"]["temp"]
        day_icon = weather_obj["main_weather"]["day"]["icon"]
        evening = weather_obj["main_weather"]["evening"]["description"]
        evening_temp = weather_obj["main_weather"]["evening"]["temp"]
        evening_icon = weather_obj["main_weather"]["evening"]["icon"]
        min_temp_str = str(weather_obj["min_temp"])
        max_temp_str = str(weather_obj["max_temp"])
        return (
            morning, morning_temp, morning_icon, day, day_temp, day_icon, evening, evening_temp, evening_icon,
            min_temp_str, max_temp_str)

    def __set_bg_image(self):
        """Установить задний фон"""
        palette = QPalette()
        image = QImage('src/bg.jpg')
        scaled = image.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Window, QBrush(scaled))
        self.setPalette(palette)

    def update(self):
        """Обновить данные"""
        global selected_city
        if self.__current_city == selected_city:
            logger.info("TabOnThreeDays updating not necessary")
            return
        logger.info("TabOnFiveDays updated")
        self.clear()
        self.__init_weather_info()

    def clear(self):
        """Очистить List Widget"""
        logger.info("cleanup List Widget TabOnFiveDays")
        self.ui.lw_days_weather_list.clear()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.wm = WeatherManager()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Погода")
        self.setFixedSize(650, 470)
        self.ui.tabs_weather.addTab(TabOnToday(self.wm), "На сегодня")
        self.ui.tabs_weather.addTab(TabOnThreeDays(self.wm), "На 3 дня")
        self.ui.tabs_weather.addTab(TabOnFiveDays(self.wm), "На 5 дней")
        # Обновить вкладки при смене
        self.ui.tabs_weather.currentChanged.connect(lambda i: self.ui.tabs_weather.widget(i).update())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
