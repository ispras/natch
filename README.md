
**Natch v.2.2**

____
_В связи с переходом на новый инструмент лицензирования до окончания действия всех выданных лицензий будут поддерживаться два варианта дистрибутива. Если у вас лицензия Sentinel, то следует брать дистрибутив из одноименной папки, если вы новый пользователь Natch -- дистрибутив для вас в папке Guardant. Так же пользователям Sentinel рекомендуется переустановить окружение (aksusbd_8.51-1_amd64.deb), пакет находится в папке с дистрибутивом._
____

Natch (Network Application Tainting Can Help) - это инструмент для определения поверхности атаки, основанный на полносистемном эмуляторе Qemu.

Основная функция Natch - получение списка модулей (исполняемых файлов и динамических библиотек) и функций, используемых системой во время выполнения задачи.

Natch представляет собой набор плагинов для эмулятора Qemu.


1. [Начало работы с Natch](1_quickstart.md)

1. [Основы работы с Natch](2_natch_begin.md)

1. [Конфигурационные файлы Natch](3_configs.md)

1. [Запуск Natch](4_launch.md)

1. [Анализ поверхности атаки с помощью SNatch](5_snatch.md)

1. [Дополнительные возможности Natch](6_additional.md)

1. [Приложения](7_appendix.md)

1. [FAQ](1_quickstart.md#faq)

1. [Релизы](7_appendix.md#app_releases)


<br><br>

**Сборка PDF**

Все необходимое для сборки PDF находится в папке scripts.

При первом использовании запустить скрипт `setup.sh`.

Для непосредственно сборки запустить скрипт `generate_pdf.sh`, запускать можно из любого места, документ с именем `natch_docs.pdf` сгенерируется в месте запуска скрипта.


