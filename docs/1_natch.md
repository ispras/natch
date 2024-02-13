<div style="page-break-before:always;">
</div>

# <a name="natch_base"></a>1. Что такое Natch

*Natch* -- это инструмент для определения поверхности атаки, основанный на полносистемном эмуляторе QEMU.
*Natch* предназначен для поиска поверхности атаки (приложений, модулей, функций) в объекте оценки,
который может состоять из множества библиотек, программ, контейнеров.
Инструмент можно использовать для поиска функций для тестирования, библиотек, которые загружают
исследуемые приложения, файлов, в которые попадают заданные входные данные.

Для анализа объект оценки помещается в образ виртуальной машины (ВМ), которая запускается в эмуляторе.
Пользователь выбирает интересующие его входные данные, а *Natch* отслеживает их распространение
в виртуальной машине во время её работы. При этом фиксируется, какой код занимался обработкой этих данных.
Обнаруженные участки кода средствами интроспекции соотносятся с процессами, программными модулями и функциями.
Информация о них записывается в наборе файлов, описывающих поверхность атаки.

Файлы с поверхностью атаки загружаются в инструмент *SNatch*, входящий в поставку *Natch*,
для отображения в виде веб-страниц и генерации отчётов в pdf.

Анализ объекта оценки делится на следующие этапы:

*  Создание проекта на основе образа виртуальной машины и объекта оценки
*  Запись сценария работы объекта оценки в виртуальной машины
*  Выбор входных данных для отслеживания (файлы, сетевые подключения)
*  Воспроизведение сценария и сохранение поверхности атаки
*  Загрузка полученной поверхности атаки в *SNatch*
*  Изучение поверхности атаки с помощью интерактивных отчётов в браузере
*  Генерация отчётов в виде pdf

Шаги с записью и воспроизведением сценария необходимы по двум причинам. Первая, это борьба с замедлением виртуальной машины
во время определения поверхности атаки.
На записанный сценарий не будут влиять задержки от механизмов анализа,
что очень важно для корректной работы часов реального времени и при взаимодействии с сетью.

Вторая причина, это возможность повторять анализ уже записанного сценария, изменяя помечаемые входные данные.
Так можно многократно повторять анализ, изучая разные компоненты объекта оценки.

Установка *Natch* описана в разделе [Установка и настройка Natch](2_setup.md#setup_natch),
пошаговое руководство по работе с инструментом -- в разделе [Пошаговое руководство по работе с Natch](3_quickstart.md#natch_stepbystep),
подготовка образа исследуемой системы -- в разделе [Настройка окружения для работы с Natch](4_setup_env.md#setup_env),
анализ и оценка результатов в *SNatch* -- в разделе [Анализ поверхности атаки с помощью SNatch](8_snatch.md#snatch).

## 1.1. Возможности Natch/SNatch

* Анализ потоков помечаемых пользовательских данных (сетевых пакетов, файлов, данных из проброшенных USB-устройств) внутри виртуальной машины
* Сбор информации о процессах: командная строка, исполняемые модули, запускаемые скрипты, открываемые файлы и сокеты
* Определение процессов, запущенных в docker-контейнерах
* Сохранение сетевого трафика между виртуальной машиной и внешним миром
* Отображение потоков помеченных данных между модулями и процессами в виде графовых диаграмм
* Построение стеков вызовов для функций, обрабатывающих помеченные данные
* Получение списка работающих в каждом процессе скриптов на Python
* Построение стеков вызовов для Pythonи и Java-функций, обрабатывающих помеченные данные
* Отображение вызванных функций процессов в виде флейм-диаграмм
* Построение дерева процессов с указанием UID для каждого из них

## 1.2. Требования к объекту оценки

* Работа под 64-битной ОС на основе Linux
* Бинарные файлы ОО должны быть извлечены из образа ВМ. Для них желательно наличие отладочной информации в формате dwarf
* Python-интерпретаторы, не входящие в поставку ОС, тоже нужно извлечь из ВМ. Интерпретаторы *обязательно* должны быть с отладочной информацией

Рекомендации по подготовке объекта оценки приведены в разделе [Рекомендации по подготовке объекта оценки](21_app_oo_preparation.md#app_preparation).

## 1.3. Из чего состоит Natch

Инструмент *Natch* состоит из нескольких взаимосвязанных частей:

* Модифицированный эмулятор QEMU (расширенный механизмами анализа помеченных данных, инструментирования и поддержки плагинов)
* Набор плагинов для интроспекции виртуальных машин
* Скрипты для работы с инструментом
* Конфигурационные файлы

Интерес для пользователя представляют последние два пункта. Работа с *Natch* построена на использовании оберток над
виртуальной машиной и утилитами, чтобы максимально упростить работу с инструментом. Она начинается со скрипта
`natch_run.py`, с помощью которого создаются проекты (подробнее в разделе [Создание проекта](5_create_project.md#create_project)).

Создав проект, вы получите набор скриптов для запуска инструмента в режимах записи и воспроизвдения (подробнее в разделе
[Запись и воспроизведение сценариев](7_scenario_work.md#record_replay)), а так же главный конфигурационный файл `natch.cfg`,
содержащий основные настройки инструмента.
Вообще в *Natch* используется несколько конфигурационных файлов, ознакомиться с ними можно в разделе
[Конфигурационные файлы Natch](16_app_configs.md#app_configs) или по ходу чтения документации.



TODO:

* релиз ноутс
* пройтись-таки по рекомендациям фобоса



