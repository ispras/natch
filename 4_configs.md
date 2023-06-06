<div style="page-break-before:always;">
</div>

# <a name="natch_config_main"></a>4. Конфигурационные файлы Natch

Для работы инструмента *Natch* требуются конфигурационные файлы. Основной конфигурационный `natch.cfg` файл отдается непосредственно инструменту на вход, остальные являются источниками настроек для плагинов, входящих в состав *Natch*.

С версии *Natch 2.3* основной конфигурационный файл разделился на две части: с общими настройками и настройками пометок для отдельных сценариев. Второй называется *taint.cfg* и генерируется при записи сценария в соответствующем каталоге.

Ниже описаны все конфигурационные файлы, используемые *Natch*, а так же скрипты (если они существуют) для их генерации. В большинстве случаев отдельный запуск этих скриптов не потребуется, все они будут вызваны при настройке инструмента (подробнее в разделе [Использование скрипта для генерации командных строк запуска](5_launch.md#natch_run_script)).

## <a name="main_config"></a>4.1. Основной конфигурационный файл

Пример файла конфигурации приведен ниже, но пользователю может потребоваться внести в него изменения.
Содержимое файла конфигурации:

```ini
# Natch settings

# Section Version since Natch v.2.0
[Version]
version=4

# Section for path to work directory
[OutputData]
workdir=/home/user/workdir

# Section for loading task_struct offsets
[Tasks]
config=task.cfg

# Section for loading modules
[Modules]
config=module.cfg
log=taint.log
params_log=params.log

[Taint]
# Threshold value for tainting. Should be in decimal number system [0..255]
threshold=255
on=true

# Section for enable generating graphs
[TaintedTask]
task_graph=true
module_graph=false

# Enable network logging
[NetLog]
on=true

# Section for collecting arguments of functions
[FunctionArgs]
config=func.cfg

# Section for getting coverage
[Coverage]
file=coverage.cov64
taint=true

# Section for enabling additional plugins
[Plugins]
items=bcqti,broker,addr=:5555;some_plugin

# Section for loading custom syscall config
[Syscalls]
config=custom_x86_64.cfg
attempts=50
```

**Секция Version**

- Поле *version*: номер версии конфигурационного файла *Natch*. Генерируется автоматически, редактирование не требуется.

**Секция OutputData**

- Поле *workdir*: путь к директории, куда будут записываться все файлы, генерируемые инструментом.
Внутри *workdir* будут создан каталог *output*, в который будут записаны файлы для анализа в графической подсистеме (бинарные логи, графы взаимодействия процессов и модулей, символьная информация), этот же каталог будет заархивирован.

**Секция Tasks**

- Поле *config*: указывается имя конфигурационного файла для распознавания процессов (подробнее в пункте [Конфигурационный файл для процессов](4_configs.md#tasks_config)).

**Секция Modules**

- Поле *config*: указывается имя конфигурационного файла для распознавания модулей (подробнее в пункте [Конфигурационный файл для модулей](4_configs.md#api_config)).
- Полe *log*: содержит название файла, в который в процессе работы будет записываться подробный лог помеченных данных (подробнее в пункте [Подробная трасса помеченных данных](7_additional.md#taint_log)).
- Полe *params_log*: содержит название файла, в который в процессе работы будет записываться лог с помеченными параметрами функций (подробнее в пункте [Получение областей помеченной памяти для функций](7_additional.md#taint_params_log)).

**Секция Taint**

- Поле *threshold*: пороговое значение для отслеживания помеченных данных, задается десятеричным числом в диапазоне от 0 до 255. Чем больше число, тем пометка будет сильнее, то есть в поверхность атаки будут попадать минимально измененные данные.
- Поле *on*: принимает логическое значение, при установке в true отслеживание помеченных данных будет включено при старте эмулятора. Если это не требуется, следует установить значение false.

Если секция *Taint* не определена, по умолчанию отслеживание помеченных данных будет выключено и пороговое значение будет установлено в 0.

**Секция TaintedTask**

- Поле *task_graph*: принимает логическое значение, при установке в true при завершении работы эмулятора будет создан граф задач и потоков помеченных данных.
- Поле *module_graph*: принимает логическое значение, при установке в true при завершении работы эмулятора будет создан граф модулей и потоков помеченных данных.

**Секция NetLog**

- Поле *on*: принимает логическое значение, при установке в true данные о сетевом трафике и его содержимое сохраняются в файлы для дальнейшего анализа.

**Секция FunctionArgs**

- Поле *config*: указывается имя конфигурационного файла, содержащее описание функций (подробнее в пункте [Получение аргументов вызываемых функций](7_additional.md#func_args)).

**Секция Coverage**

- Поле *file*: указывается имя файла, куда будет записана операция о покрытии кода.
- Поле *taint*: определяет режим сбора покрытия кода (подробнее в пункте [Анализ покрытия бинарного кода](7_additional.md#functional_coverage)).

**Секция Plugins**

- Поле *items*: через точку с запятой указываются плагины, не входящие в состав *Natch*, но которые должны быть загружены.

**Секция Syscalls**

- Поле *config*: указывается имя конфигурационного файла для перехвата системных вызовов (подробнее в пункте [Конфигурационный файл для системных вызовов](4_configs.md#syscalls_config)).
- Поле *attempts*: дает возможность задать количество срабатываний системных вызовов для тюнинга. Может понадобиться уменьшить, если настройка не успевает пройти. По умолчанию 50.


## <a name="taint_config"></a>4.2. Конфигурационный файл для помеченных данных

Конфигурационный файл для помеченных данных генерируется при записи сценария и помещается в соответствующую директорию. Сделано это с целью сохранения настроек пометок для конкретного сценария в рамках одного проекта.

Пример файла конфигурации *taint.cfg* приведен ниже.

```ini
[Ports]
# 6 is for tcp
ip_protocol=6
# ports are supported for tcp only yet
dst=22;80;3500;5432
src=22;80;3500;5432

# Section for add tainted files
[TaintFile]
list=file1.txt;file2.txt
```

**Секция Ports**

- Поле *ip_protocol* описывает тип протокола 4 уровня. Если не указано, пакеты по этому полю не фильтруются.
- Поле *src* - фильтр по Source Port в заголовке TCP, порты перечисляются через точку с запятой.
- Поле *dst* - фильтр по Destination Port в заголовке TCP, порты перечисляются через точку с запятой.

При необходимости отслеживать трафик по всем портам, в полях *dst/src* секции *Ports* следует указать значение -1. Если хотя бы в одном поле будет -1, будет отслеживаться весь трафик.

**Секция TaintFile**

- Поле *list*: через точку с запятой могут быть перечислены имена файлов, которые требуется пометить. Указываются имена файлов гостевой машины в формате имя + расширение. Для надежности рекомендуется не использовать пути. Пометка произойдет автоматически при запуске эмулятора.

С помощью специального символа '\*' в конце имени файла можно указать множество файлов для пометки. Например, */home/\** - пометка всех файлов в каталоге home, */dev/tty\** - пометка всех данных, вводимых в каждый из терминалов (tty1, tty2 и т.д.). Если путь начинается не с корневого каталога, то он охватывает одноименные пути на разных расположениях. Например, *Pictures/1.jpg* помечает файлы и на пути */home/user/Pictures/1.jpg*, и на пути */home/root/Pictures/1.jpg*.

Если включена секция *TaintFile* без указания списка файлов, плагин *taint_file* все равно будет загружен.


## <a name="api_config"></a>4.3. Конфигурационный файл для модулей

В секции *Modules* можно указать конфигурационный файл, описывающий анализируемые исполняемые модули. *Natch* может находить загруженные модули, на которые передавалось управление, но определить их имена и функции не всегда возможно.

В этом случае можно загрузить образы интересующих модулей через конфигурационный файл.
Использование этого конфигурационного файла может понадобиться в следующих случаях:

- Для правильного определения имен бинарных файлов и их экспортируемых функций
- Для подгрузки map-файла с именами функций
- Для подгрузки дополнительных ELF-файлов с отладочной информацией (подробнее в [Приложение 3. Формат списка исполняемых модулей](8_appendix.md#module_config))

Из основного бинарного файла всегда читаются экспортируемые символы и отладочная информация,
сгенерированная компилятором при использовании ключа `-g`. Поддерживаются все современные компиляторы.
Также можно использовать map-файлы, сгенерированные с помощью IDA Pro. Это можно сделать через меню `File -> Produce file -> Create MAP File`.
В появившемся после ввода имени файла диалоге нужно выставлять галочку *Segmentation information*.

### 4.3.1. Автоматическая генерация конфигурационного файла

Конфигурационный файл со списком модулей может быть сгенерирован автоматически при помощи входящего в поставку скрипта *module_config.py* во время выполнения скрипта *natch_run.py* (подробнее в пункте [Использование скрипта для генерации командных строк запуска](5_launch.md#natch_run_script)).

Скрипт *module_config.py* принимает ряд параметров:

- Путь к директории, содержащей модули и map-файлы (обязательный).
- Путь к рабочей директории, в которую будет помещен лог работы инструмента. По умолчанию в месте запуска скрипта.
- Флаг включения диагностических сообщений.

```bash
module_config.py folder [-h] [-l] [-d]
```
Имена map-файлов и исполняемых файлов должны соответствовать друг другу: скрипт будет искать map-файлы, приписывая суффикс .map к полному имени исполняемого файла.

Пример запуска скрипта:
```bash
./module_config.py <path_to_modules>
```

### <a name="debug_info"></a>4.3.2. Автоматическая загрузка отладочной информации для разделяемых библиотек

В поставку инструмента входит скрипт `guest_system/debug_info.py`, позволяющий получить символьную информацию из системных библиотек, работавших с исследуемыми приложениями. В процессе выполнения скрипта для каждого исполняемого файла происходит поиск необходимых для него разделяемых библиотек. Для всех найденных библиотек загружается отладочная информация, если она доступна. На выходе получается новый конфигурационный файл `module.cfg`, дополненный найденными библиотеками с отладочной информацией.

При установке соответствующего флага, скрипт позволяет выкачивать из образа ядро вместе с его символьной информацией. Если не удалось определить, какое ядро используется, то выкачивается информация для всех ядер, найденных в каталоге \boot.

При необходимости анализа приложения, включающего в себя код, написанный на Python, рекомендуется установить дополнительный флаг, разрешающий загрузку символьной информации для Python интерпретаторов, используемых в анализируемом образе.

Если имеется директория, содержащая файлы отладочной информации для разделяемых библиотек, поставляемых с операционной системой, то можно включить данную директорию в скрипт, используя опцию, указанную ниже. По умолчанию, данную директорию обычно можно найти по следующему пути: /usr/lib/debug.

Скрипт принимает ряд параметров:

- Путь к конфигурационному файлу (обязательный)
- Путь к образу гостевой операционной системы (обязательный)
- Флаг включения диагностических сообщений
- Путь к директории, в которую будут сохранены разделяемые библиотеки и их отладочные символы (по умолчанию текущая)
- Флаг разрешения загрузки символьной информации для ядра
- Флаг разрешения загрузки символьной информации для Python интерпретаторов
- Путь к директории, в которой содержатся отладочная информация(.debug) для разделяемых библиотек.

```bash
debug_info.py [-h] [-d] [-s SAVE] [-k] [-i] [-dp DEBUG_PKG] cfg_path img
```

Найденные библиотеки и их отладочная информация будут помещены в папку *libs* в месте запуска скрипта, если не была указана другая локация.

Не все библиотеки могут быть обнаружены, а именно, библиотеки, загружаемые во время выполнения с помощью `dlopen` и других похожих механизмов, не могут быть определены статически, поэтому они будут пропущены.

В случае ошибки монтирования убедитесь, что не смонтированы другие образы или же не запущена виртуальная машина (например, Virtualbox).

В данный момент скрипт работает с гостевыми системами:

- Ubuntu 20.04 и выше (будет работать и с младшими версиями, но будет много пакетов без отладочной информации)
- Fedora 33 и выше
- Debian 11 и выше (версии ниже не тестировались)

Также скрипт будет работать с дистрибутивами Linux, основанных на glibc, которые поддерживают службу Debuginfod.

Пример запуска скрипта:
```bash
sudo ./debug_info.py <path_to_module_config> <path_to_system_img>
```
Обратите внимание на необходимость запуска скрипта с правами суперпользователя.


### 4.3.3. Копирование файлов из гостевой системы

При необходимости копирования файлов или же директорий из гостевой системы в хостовую, можно воспользоваться скриптом `copy_files.py` (так же находится в папке `guest_system`).

Скрипт принимает ряд параметров:

- Путь к образу гостевой операционной системы (обязательный)
- Путь к директории, в которую будут сохранены копируемые файлы (обязательный)
- Список, содержащий пути до файлов/директорий (обязательный)
- Флаг включения диагностических сообщений

```bash
copy_files.py [-h] [-d] img dest paths [paths ...]
```

При копировании директории вложенность удаляется, т.е все файлы будут скопированы в корень указанной директории.

Пример запуска скрипта:
```bash
sudo ./copy_files.py <path_to_img> <path_to_dest_folder> <list_paths_to_copy>
```
Обратите внимание на необходимость запуска скрипта с правами суперпользователя.


## <a name="tasks_config"></a>4.4. Конфигурационный файл для процессов

Конфигурационный файл секции *Tasks* генерируется автоматически на этапе конфигурирования *Natch*.

Если во время настроечного запуска индикатор прогресса зависает на одном пункте, то вероятно это связано с недостатком количества перехватываемых системных вызовов. Для решения проблемы можно попробовать запустить на гостевой системе какую-либо программу.


## <a name="syscalls_config"></a>4.5. Конфигурационный файл для системных вызовов

Конфигурационные файлы для перехвата системных вызовов поставляются с инструментом и, как правило, подгружаются автоматически.

В редких случаях следует указывать конкретный файл, но писать самостоятельно его не нужно, лучше обратиться к разработчикам.

