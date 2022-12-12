# DesignGUI
Лабораторная работа №3: "Основы графического интерфейса на PyQt"

# Задание на лабораторную работу
* Реализовать приложение на PyQt с использованием представления таблиц и работы с SQL.
    - В меню две вкладки: Set connection (установить соединение с бд), Close connection (очистить все, закрыть соединение с бд).
    - По умолчанию можно сделать в QTabWidget вкладки пустыми, либо создавать их по выполнению запросов при нажатии на функциональные клавиши.
    - Сразу после успешного коннета в Tab1 устанавливается таблица, соответствующая запросу «SELECT * FROM sqlite_master».
    - Кнопка bt1 делает выборочный запрос, например, «SELECT name FROM sqlite_master», результат выводится в Tab2.
    - При выборе колонки из выпадающего списка QComboBox результат соотвествующего запроса отправляется в Tab3.
    - Кнопки bt2 и bt3 выполняют запрос по выводу таблицы в Tab4 и Tab5
* Иллюстрация пример<br><br>
![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/technical_task.png)

# Инструменты, используемые при разработке приложения
* Разработка графического приложения:
    - Python3
    - PyQt5
    - QtDesigner
* Разработка базы данных:
    - Microsoft SQL Server 2019
    - Microsoft SQL Server Managment Studio 18

# Структура решения лабораторной работы
Решение лабораторной работы состоит из двух частей:
* работа с базой данный
* работа с графическим интерфейсом

# Разработка базы данных
Для разработки базы данных использовался язык T-SQL, из MSSQL. Было разработано 2 скрипта:
* [`create table.sql`](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/database%20scripts/create%20table.sql) - производит создание таблицы, с ранее созданной базе данных.

``` sql
CREATE TABLE gui_table
(
    --пассажир
    id INT NOT NULL PRIMARY KEY, 
    фио [NVARCHAR](200) NOT NULL, 
    дата_рождения [date] NOT NULL, 
    паспорт [NVARCHAR](50) NOT NULL, 
    -- билет
    id_билета [NVARCHAR](50) NOT NULL UNIQUE,
    пункт_отправления [NVARCHAR](50) NOT NULL, 
    пункт_назначения [NVARCHAR](50) NOT NULL, 
    дата_отправления [date] NOT NULL, 
    количество_баллов [NVARCHAR](50) NOT NULL,
    вес_багажа [NVARCHAR](50) NOT NULL,
    -- параметры полета
    время_полета [NVARCHAR](50) NOT NULL, 
    самолет [NVARCHAR](50) NOT NULL
);
```

* [`bulk isert.sql`](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/database%20scripts/bulk%20isert.sql) - производит массовую вставку данных, которые были заранее подготовлены, дабы ускорить загрузку информации в базу даных.
``` sql
bulk insert gui_base.dbo.gui_table
from 'F:\output.txt'
    with
    (
	datafiletype = 'widechar',
    fieldterminator = '|',
    rowterminator = '\n'
    );
```
# Разработка графического интерфейса

При разработке графического интерфейса было реализовано несколько скриптов, рассмотрим каждый из них по подробнее.
## Генерация случайных данных
[`generate_data.py`](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/generate_data.py)<br>
Данный скрипт, содержит код, при выполнении, которого будет производиться автоматическая генерация данных, которые будут использоваться в базе данных. Скрипт содержит в себе:
* Клас генерируемых данных с конструктором и методам сохранения объекта класса в строковом представлении.
``` python
class Generated_data():
    def __init__(self, id, name, date_birth, number, id_ticket, arrival, destionation, date_arrival, count_bonus, weight, duration_fly, plane):
        self.id = id
        self.name = name
        self.date_birth = date_birth
        ...
     def result(self):
        return str(self.id) + '|' + str(self.name) + '|' + str(self.date_birth) +'|'+ str(self.number)+ '|' + str(self.id_ticket) + '|' + str(self.arrival) + '|' + str(self.destionation) + '|' + str(self.date_arrival) + '|' + str(self.count_bonus) + '|' + str(self.weight) + '|' + str(self.duration_fly) +'|'+str(self.plane) 

```
* Массивы данных, для генерации широкого набора данных, которые будут использованы в базе данных.
```python
# массив пунктов прибытия
array_destionation = [
        "Абакан", "Анапа", "Астрахань", "Белгород", "Братск", "Варандей", "Владикавказ", "Воронеж", "Екатеринбург", "Иркутск",
        "Калининград", "Кемерово", "Красноярск", "Курск", "Магадан", "Махачкала", "Москва", "Мурманск", "Нижневартовск", "Нижний Новгород",
        "Новосибирск", "Оренбург", "Остафьево", "Петрозаводск", "Псков", "Сабетта", "Санкт-Петербург", "Саратов", "Сочи", 
        "Сургут", "Томск", "Улан-Удэ", "Уфа", "Ханты-Мансийск", "Челябинск", "Чита", "Южно-Сахалинск", "Ярославль"]
# массив компаний самолетов
array_companies = [
            "Airbus", "ATR", "Saab AB", "Антонов", "ОАК",
            "Сухой", "Иркут", "Туполев", "Ильюшин", "Boeing",
            "Douglas", "Bombardier", "Embraer"
        ]
```
* Функцию генерации случайной даты
```python
def get_random_date(start, end):
    delta = end - start
    return start + timedelta(random.randint(0, delta.days))
```
* Код, обеспечивающий генерацию набора данных и его сохранение в выходной файл.

## Вспомогательный скрипт загрузки таблиц
[`help.py`](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/help.py) - в данный скрипт выненсены некоторые функции, для улучшения читаемости основного файла с описанием графического интерфейса.
* `load_name_tables` - функция, необходимая для получения имен столбцов таблицы из базы данных.
* `ld_labels` - функция, необходимая для установки имен столбцов в `QTableWidget`
* `ld_data_main_window` - функция, необходимая для загрузки данных в основное окно 
* `ld_data_add_window` - функция, необходимая для загрузки данных в дополнительное окно
* `show_message` - функция, обеспечивающая вызов сообщения "подсказки"

## Скрипты, содержащие реализцаию графического приложения
* [`untitled.ui`](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/untitled.ui) - файл генерируемый программой `QtDesigner`
* [`ui_untitled.py`](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/ui_untitled.py) - скрипт скомпилированный, на основе файла из программы `QtDesigner`, и описывающий поведение и логику работы элементов графического приложения.

## Основной скрипт программы
[`main.py`](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/main.py) - основной скрипт, производящий запуск всего приложения

# Результаты лабораторной работы

Ниже приведены скриншоты реализованного приложения.

## Внешний вид программы
### Основные компоненты программы
| Основное окно программы|Дополнительное окно программы|
|:---:|:---:|
|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/main_window.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/addition_window.png)|
### Дополнительные компоненты программы
Первое меню из бара|Второе меню из бара|Краткое окно помощи|
:---:|:---:|:---:|
|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/first_context_menu.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/second_context_menu.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/window_help.png)|


## Работа на главном окне
| Открытие соединения|Результат открытия соединения|Закрытие соединения|Результат закрытия соединения|
|:---:|:---:|:---:|:---:|
|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/open_connect.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/result_open_coonect.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/close_connect.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/close_connect_resilt.png)|

## Работа с дополнительным окном
|Работа главного окна<br>при закрытом соединении|Работа главного окна<br>при открытом соединении|Выполнение запроса<br>при открытом соединении|Выполнение запроса<br>при закрытом соединении|
|:---:|:---:|:---:|:---:|
|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/second_window_close_connect.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/second_window_open_connect.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/second_window_executed_query.png)|![фото](https://github.com/Black-Viking-63/DesignGUI/blob/main/LabWork_3/images/query_with_close_connect.png)|
