<div style="page-break-before:always;">
</div>


# <a name="app_releases"></a>Приложение 9. История релизов Natch


[**Natch v.3.0**](https://nextcloud.ispras.ru/index.php/s/BT6xeiz4ATQLqoy) (февраль 2024)

* SNatch
    * ...
* Natch
    * ...

[**Natch v.2.4**](https://nextcloud.ispras.ru/index.php/s/zxMra4pdpBRkCgd) (октябрь 2023)

* SNatch
    * Интерфейс SNatch теперь и на русском языке
    * Добавлен поиск в графах (стек вызовов, флейм граф)
    * Добавлена информация об операциях с файлами
    * Добавлена навигация по истории перемещений в боковой панели
    * Некоторые изменения интерфейса
    * Исправлен ряд багов
* Natch
    * Поддержка отладочной информации для языка Go
    * Добавлена возможность запуска Natch в облегченном режиме
    * Добавлена сборка Natch для Astra Linux 1.7.3
    * Добавлена поддержка автотюнинга для ОС семейства Windows
    * Изменения скриптов:
        * добавлен скрипт для обновления конфигурационного файла для модулей
        * выходные файлы анализа теперь в собственном каталоге, архив не перезаписывается
    * Исправлен ряд багов

[**Natch v.2.3.1**](https://nextcloud.ispras.ru/index.php/s/NALSzi9xGSaftsN) (июнь 2023)

* SNatch
    * Улучшен PDF отчет
* Natch
    * Расширен перехват системных вызовов
    * Улучшена поддержка DWARF

[**Natch v.2.3**](https://nextcloud.ispras.ru/index.php/s/natch_v.2.3) (июнь 2023)

* SNatch
    * Добавлен граф вызовов Python функций
        * реализован переход из основного графа вызовов в Python и обратно
    * Добавлена возможность получения отчетов об анализе:
        * полный отчет в формате PDF
        * сохранение графов в виде цветного или ч/б изображения
    * Добавлен раздел Файлы, отображающий участвующие в сценарии файлы с возможностью фильтрации
    * Добавлена боковая панель свойств для большинства аналитик
        * для процессов-интерпретаторов предусмотрено отображение списка выполнявшихся скриптов
    * Сохранение положения узлов графов во время и после сессии
    * Добавлена опция фильтрации во вкладках Ресурсы и Дерево процессов
    * Во вкладке Трафик добавлена фильтрация: только помеченные пакеты; пакеты, участвующие в сценарии; все пакеты
    * Во вкладку О проекте добавлена статистика помеченных данных
    * Изменения интерфейса:
        * пересмотрено главное меню
        * новая цветовая схема
        * скрывающаяся легенда для графов
        * возможность выбора цветовой схемы для флейм графа
    * Исправлен ряд багов
* Natch
    * Добавлена возможность пометки локальных соединений
    * Добавлена поддержка Python:
        * перехват вызовов Python функций
        * автоматическое скачивание интерпретатора CPython/libpython из образа
    * Добавлена поддержка маленьких исполняемых файлов в качестве объекта оценки
    * Добавлена возможность сбора корпуса данных для фаззинга выбранных функций (для аргументов простых типов)
    * Добавлена возможность фильтрации трафика по порту для протокола UDP
    * Сборки Natch теперь в виде пакетов (ubuntu20-22, debian11, alt10)
    * Улучшена работа с извлечением символов из DWARF
    * Ликвидированы файлы с текстовой поверхностью атаки (output_text)
    * Изменения скриптов:
        * добавлена удобная возможность создавать подкаталоги для записываемых сценариев
        * скачивание системных модулей доступно, даже если пользовательские не загружены
        * доработан скрипт change_settings.py
    * Исправлен ряд багов

[**Natch v.2.2**](https://nextcloud.ispras.ru/index.php/s/natch_v.2.2) (март 2023)

* SNatch
    * Добавлен раздел Ресурсы, включающий информацию о модулях, файлах и сокетах
    * Добавлен раздел Трафик:
        * списки интерфейсов и сессий
        * возможность просмотра трафика в Wireshark
    * Улучшение юзабилити. Новые возможности:
        * параллельное создание нескольких проектов
        * кнопка отмены для построения графов
        * переименовывание проектов
        * закрытие всех вкладок одной кнопкой
        * отсутствие дублирования вкладок
        * логирование работы SNatch в файл
    * Добавлена метаинформация о сценарии
    * Улучшено дерево процессов
    * Добавлен прототип интеграции со Svace
    * Добавлена генерация аннотаций для Futag
    * Исправлен ряд багов
* Natch
    * Разбор отладочной информации вынесен на этап конфигурирования
    * Добавлено скачивание отладочных символов для модуля ядра
    * Улучшено распознавание процессов и модулей
    * Визуальное отображение хода тюнинга
    * Пометка директорий, а так же файлов по заданному префиксу
    * Архиватор артефактов изменен на более быстрый
    * Добавлена статистика помеченных сущностей в результате выполнения сценария
    * Изменен скрипт natch_run.sh:
        * поддержан текстовый режим работы эмулятора
        * добавлена возможность скачивать отладочные символы
        * поддержка относительных путей для образов
    * Исправлен ряд багов


[**Natch v.2.1.1**](https://nextcloud.ispras.ru/index.php/s/natch_v.2.1.1) (декабрь 2022)

* Исправлен баг с построением графа процессов
* Улучшения в распространении помеченных данных
* Доработан раздел Modules в SNatch


[**Natch v.2.1**](https://nextcloud.ispras.ru/index.php/s/natch_v.2.1) (ноябрь 2022)

[(reserve) Natch v.2.1_ova](https://nextcloud.ispras.ru/index.php/s/natch_v.2.1_vbox)

* Обновлен графический интерфейс SNatch
    * Добавлены новые аналитики:
        * временной граф процессов
        * флейм граф процессов
        * граф помеченных модулей
        * дерево процессов
    * Улучшен граф вызовов
    * Добавлены горячие клавиши для управления визуальными элементами
    * Изменена схема БД, больше не требуется копирование модулей
* Доступно автоматическое получение отладочной информации для системных библиотек для гостевых ОС Ubuntu, Debian и Fedora
    * Добавлен скрипт для извлечения файлов из гостевой ОС
* Добавлена частичная поддержка FreeBSD
* Доработан механизм определения смещений ядерных структур
* Добавлено определение строк запуска процессов
* Исправлен ряд багов
* Скрипты для конфигурирования Natch:
    * абсолютные пути заменены на относительные (кроме образа)
    * добавлен скрипт для внесения изменений в скрипты запуска Natch
* Документация теперь доступна на github, а так же в виде PDF


[**Natch v.2.0**](https://nextcloud.ispras.ru/index.php/s/natch_v.2.0) (сентябрь 2022)

[(reserve) Natch v.2.0_ova](https://nextcloud.ispras.ru/index.php/s/natch_v.2.0_vbox)

* Представлен графический интерфейс SNatch v.1.0. Основные возможности:
    * построение графа взаимодействия процессов
        * интерактивный просмотр с помощью привязки к timeline
        * доступно четыре режима отображения сущностей
    * построение стека вызовов
* Улучшено распознавание модулей
* Добавлена поддержка сжатых секций с отладочной информацией
* Добавлена возможность фильтрации сетевых пакетов по протоколу
* Доработан скрипт для конфигурирования Natch
    * рабочая директория для проектов
    * добавлена возможность проброса портов в гостевую систему
* Запущен внешний баг-трекер


[**Natch v.1.3.2**](https://nextcloud.ispras.ru/index.php/s/natch_v.1.3.2) (июль 2022)

* Улучшение и рефакторинг механизма распознавания модулей
* Поддержка набора инструкций SSE4.2 при отслеживании помеченных данных
* Настройка Natch теперь осуществляется с помощью одного скрипта
* Выходные файлы инструмента собираются в одну директорию
* Добавлен журнал событий Natch
* Небольшие изменения в настройке и конфигурационном файле Natch


[**Natch v.1.3.1**](https://nextcloud.ispras.ru/index.php/s/natch_v.1.3.1) (май 2022)

* Исправлена ошибка сбора покрытия для Ida 7.0
* Исправлена ошибка сохранения лога для помеченных параметров функций
* Исправлена опечатка в генерируемом конфигурационном файле
* Название снапшота вынесено в начало скрипта запуска Natch в режиме воспроизведения


[**Natch v.1.3**](https://nextcloud.ispras.ru/index.php/s/natch_v.1.3) (апрель 2022)

* Добавлена поддержка отладочной информации
* Добавлена поддержка map файлов, сгенерированных компилятором gcc
* Расширен набор опций конфигурационного файла Natch:
    * добавлена возможность указывать список файлов для пометки
    * добавлена возможность загрузки дополнительных плагинов
* Добавлен скрипт для генерации конфигурационного файла для модулей
* Обновлен скрипт для генерации командных строк запуска Natch
* Обновлено ядро эмулятора Qemu до версии 6.2


[**Natch v.1.2.1**](https://nextcloud.ispras.ru/index.php/s/natch_v.1.2.1) (февраль 2022)

* Исправлена ошибка работы утилиты qemu-img в VirtualBox под Windows 10
* Исправлена ошибка с генерацией имени оверлея в скрипте для генерации командных строк
* Добавлена возможность задавать поля скрипта перед его запуском


[**Natch v.1.2**](https://nextcloud.ispras.ru/index.php/s/natch_v.1.2) (февраль 2022)

* Скрипт для генерации командных строк
* Выгрузка данных о покрытии кода в IDA Pro
* Построение графа модулей, передающих друг другу помеченные данные
* Ранжирование функций поверхности атаки по числу обращений к помеченным данным
* Исправлены дефекты в механизме распространения пометок
* Мелкие изменения в конфигурационном файле инструмента


[**Natch v.1.1**](https://nextcloud.ispras.ru/index.php/s/natch_v.1.1) (декабрь 2021)

* Возможность настраивать Natch с помощью конфигурационного файла
* Логирование входящих сетевых пакетов
* Отображение операций записи помеченных данных
* Построение графа, описывающего взаимодействие процессов
* Поддержка ELF32
* Исправление списка процессов: уничтожение завершившихся


[**Natch v.1.0**](https://nextcloud.ispras.ru/index.php/s/natch_v.1.0) (октябрь 2021)

* Пометка сетевого трафика (сетевая карта e1000)
* Пометка файлов
* Возможность задания порогового значения для пометок
* Определение модулей с исполняемым кодом в памяти виртуальной машины
* Возможность подгружать map файлы из IDA
* Получение списка процессов, модулей и функций, участвующих в обработке помеченных данных
* Получение подробной трассы по каждому обращению к помеченным данным, включающей стек вызовов функций, адрес обращения к помеченным данным и количество помеченных байтов
