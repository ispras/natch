<div style="page-break-before:always;">
</div>

# <a name="app_configs"></a>Приложение 2. Конфигурационные файлы Natch

Для работы инструмента *Natch* требуются конфигурационные файлы. Основной конфигурационный `natch.cfg` файл отдается непосредственно инструменту на вход,
остальные являются источниками настроек для плагинов, входящих в состав *Natch*.

Для каждого сценария также автоматически создаётся конфигурационный файл `taint.cfg`, в котором описываются правила для помеченных данных.

Ниже описаны все конфигурационные файлы, используемые *Natch*.

## <a name="main_config"></a>Основной конфигурационный файл natch.cfg

Все секции и параметры файла конфигурации приведены ниже.

```ini
# Natch settings

[Version]
version=8

# Section for path to work directory
[OutputData]
workdir=/home/user/workdir

# Section for loading task_struct offsets
[Tasks]
config=task.cfg

# Section for loading modules
[Modules]
config=module.cfg
log=taint_txt.log
params_log=params.log

# Enable network logging
[NetLog]
on=true

# Section for enabling additional plugins
[Plugins]
items=bcqti,broker,addr=:5555;some_plugin

# Section for loading custom syscall config
[Syscalls]
config=custom_x86_64.cfg
attempts=50
```

**Секция Version**

- Поле `version` -- номер версии конфигурационного файла *Natch*. Генерируется автоматически, редактирование не требуется.

**Секция OutputData**

- Поле `workdir` -- путь к директории, куда будут записываться все файлы, генерируемые инструментом.
  Внутри `workdir` будут создан каталог `output_\<scenario_name\>`, в который будут записаны файлы для анализа в графической подсистеме
  (бинарные логи, графы взаимодействия процессов и модулей, символьная информация), этот же каталог будет заархивирован.

**Секция Tasks**

- Поле `config` -- указывается имя конфигурационного файла для распознавания процессов (подробнее в пункте [Конфигурационный файл для процессов](app2_configs.md#tasks_config)).

**Секция Modules**

- Поле `config` -- указывается имя конфигурационного файла для распознавания модулей (подробнее в пункте [Конфигурационный файл для модулей](app2_configs.md#api_config)).
- Полe `log` -- содержит название файла, в который в процессе работы будет записываться подробный лог помеченных данных (подробнее в разделе [Подробная трасса помеченных данных](10_additional.md#taint_log)).
- Полe `params_log` -- содержит название файла, в который в процессе работы будет записываться лог с помеченными параметрами функций (подробнее в разделе [Получение областей помеченной памяти для функций](10_additional.md#taint_params_log)).

**Секция NetLog**

- Поле `on` -- принимает логическое значение, при установке в true данные о сетевом трафике и его содержимое сохраняются в файлы для дальнейшего анализа.

**Секция Plugins**

- Поле `items` -- через точку с запятой указываются плагины, не входящие в состав *Natch*, но которые должны быть загружены.

**Секция Syscalls**

- Поле `config` -- указывается имя конфигурационного файла для перехвата системных вызовов (подробнее в пункте [Конфигурационный файл для системных вызовов](app2_configs.md#syscalls_config)).
- Поле `attempts` -- дает возможность задать количество срабатываний системных вызовов для тюнинга. Может понадобиться уменьшить, если настройка не успевает пройти. По умолчанию 50.


## <a name="taint_config"></a>Конфигурационный файл для помеченных данных taint.cfg

Содержание файла конфигурации `taint.cfg` приведено ниже.

```ini
# Natch working mode
[Mode]
light=false

[Taint]
# Threshold value for tainting. Should be in decimal number system [1..255]
threshold=255
on=true

[Ports]
# 6 is for tcp, 17 for udp
ip_protocol=6
# ports are supported for tcp only yet
dst=22;80;3500;5432
src=22;80;3500;5432

# Section for add tainted files
[TaintFile]
list=file1.txt;file2.txt

# Section for usb traffic tainting
[USB]
on=true

# Section for enable generating graphs
[TaintedTask]
task_graph=true
module_graph=true

# Section for getting coverage
[Coverage]
file=coverage.cov64
taint=true

# Section for collecting arguments of functions
[FunctionArgs]
config=func.cfg
```

**Секция Mode**

- Поле `light` -- принимает логическое значение, при установке в true включается облегченный режим работы *Natch*,
  по умолчанию выключен (подробнее в разделе [Облегченный режим работы Natch](10_additional.md#natch_light)).

**Секция Taint**

- Поле `threshold` -- пороговое значение для отслеживания помеченных данных, задается десятеричным числом в диапазоне от 1 до 255.
  Чем больше число, тем пометка будет сильнее, то есть в поверхность атаки будут попадать минимально измененные данные.
- Поле `on` -- принимает логическое значение, при установке в true отслеживание помеченных данных будет включено при старте эмулятора.
  Если это не требуется, следует установить значение false.

Если секция `Taint` не определена, по умолчанию отслеживание помеченных данных будет выключено и пороговое значение будет установлено в 0.

**Секция Ports**

- Поле `ip_protocol` -- описывает тип протокола 4 уровня. Если не указано, пакеты по этому полю не фильтруются.
- Поле `src` -- фильтр по Source Port в заголовке TCP, порты перечисляются через точку с запятой.
- Поле `dst` -- фильтр по Destination Port в заголовке TCP, порты перечисляются через точку с запятой.

**Секция TaintFile**

- Поле `list` -- через точку с запятой могут быть перечислены имена файлов, которые требуется пометить.
  Указываются имена файлов гостевой машины в формате имя + расширение. Для надежности рекомендуется не использовать пути.
  Пометка произойдет автоматически при запуске эмулятора.

**Секция USB**

- Поле `on` -- принимает логическое значение, при установке в true будет включено отслеживание помеченных данных. Если это не требуется, следует установить значение false.

**Секция TaintedTask**

- Поле `task_graph` -- принимает логическое значение, при установке в true при завершении работы эмулятора будет создан граф задач и потоков помеченных данных.
- Поле `module_graph` -- принимает логическое значение, при установке в true при завершении работы эмулятора будет создан граф модулей и потоков помеченных данных.

**Секция Coverage**

- Поле `file` -- указывается имя файла, куда будет записана операция о покрытии кода.
- Поле `taint` -- определяет режим сбора покрытия кода (подробнее в пункте [Анализ покрытия бинарного кода](10_additional.md#functional_coverage)).

**Секция FunctionArgs**

- Поле `config` -- указывается имя конфигурационного файла, содержащее описание функций (подробнее в пункте [Получение аргументов вызываемых функций](10_additional.md#func_args)).


## <a name="api_config"></a>Конфигурационный файл для модулей module.cfg

Конфигурационный файл секции `Modules` генерируется автоматически на этапе конфигурирования *Natch*.

В редких случаях может потребоваться ручная доработка, подробная информация про этот файл в разделе [Формат списка исполняемых модулей](app3_module_cfg.md#app_module_config)


## <a name="debug_config"></a>Конфигурационный файл для управления отладочной информацией debug_info.cfg

Содержимое файла конфигурации `debug_info.cfg` представлено ниже.

```ini
# Debug Info configuration

[Version]
version=1

[Common]
# Sets max download attempts for debug information
attempts=30
mount=True
debug=False

# Section for paths to module configs
[Configs]
path=/home/user/project/module.cfg

# Section for sets DebugInfoD servers for debugging symbol search
[DebugInfoD]
# servers=['https://example1.com', 'https://example2.com']

# Section for Repository settings
[PackageAnalysis]
# Path for exporting generated list of packages needing debug information.
# WARNING: This option disables debug package loading.
# path_to_save_pkg_list=your/path/to/destonation/file

# Section for additional symbols search
[Symbols]
kernel=True
python=True
csharp=True
java=True

# Section for path to directory with debug symbols
# [UserFolder]
# path=your/path/to/directory

# Section for Containerization Tool
[ContTools]
docker_path=/var/lib/docker
# local_podman_path=/home/user/.local/share/containers
root_podman_path=/var/lib/containers/
```

Конфигуратор отладочной информации позволяет настроить способы ее получения, указать определенные сервера
или локальные пути хранения символов.

**Секция Version**

Является обязательной и содержит сверсию текущего конфигурационного файла.

**Секция Common**

Является обязательной и содержит в себе поля, которые непосредственно влияют на все этапы процесса загрузки отладочных символов.

- Поле `attempts` -- является обязательным и определяет число итераций, в ходе которых скрипт пытается получить
  доступ к различным интернет-ресурсам. В случае временной недоступности указанных ресурсов скрипт ожидает определенный
  промежуток времени перед повторной попыткой обращения к ним.

- Поле `mount` -- определяет необходимость монтирования гостевой системы и, по умолчанию, имеет значение `True`.
  В случае, если гостевой образ не может быть смонтирован по каким-либо причинам, можно запустить данный скрипт в *Лёгком режиме*,
  установив данный параметр в значение `False`. При этом дальнейший анализ ограничивается исключительно поиском отладочных символов для модулей,
  указанных в конфигурационном файле хостовой системы. Этот поиск происходит либо в пользовательской директории,
  либо с использованием сервиса `DebugInfoD`, при условии, что пользователь дал на это согласие. Указание параметра `False` препятствует
  автоматическому определению типа гостевой операционной системы. Рекомендуется указать сервера для сервиса `DebugInfoD`, соответствующие вашей операционной системе.

- Поле `debug` -- флаг включения диагностических сообщений, по умолчанию, имеет значение `False`.

**Секция Configs**

Является обязательной и включает в себя информацию о конфигурационном файле, используемом для модулей.

- Поле `path` -- является обязательным и содержит путь к конфигурационному файлу, в котором перечислены пути до модулей.


**Секция DebugInfoD**

При активации данной секции перечень доступных методов для поиска отладочных символов будет дополнен сервисом `DebugInfoD`,
если ваша гостевая ОС поддерживает его. Оставьте эту секцию закомментированной или удалите её, если этого не требуется.

- Поле `servers` -- содержит пользовательский список серверов, специфических для конкретных операционных систем.
Сервера по умолчанию установлены для операционных систем Ubuntu, Fedora, Alt и Debian. Формат поля: servers=['https://example1.com', 'https://example2.com'].


**Секция PackageAnalysis**

При активации данной секции перечень доступных методов для поиска отладочных символов будет дополнен методом
пакетного анализа гостевой операционной системы, если он был реализован для вашей гостевой ОС. На данный момент это:
Ubuntu, Fedora, Alt 10 и Alpine (работает с последними версиями пакетов). Оставьте эту секцию закомментированной или удалите её, если этого не требуется.

- Поле `path_to_save_pkg_list` -- содержит путь к файлу, в который будет экспортирован список пакетов,
требующих отладочную информацию. Одним из возможных сценариев использования этого списка является сбор указанных в нем пакетов
в гостевой операционной системе с отладочными символами, а затем повторный запуск данного скрипта.
Обратите внимание, при использовании данной опции отладочные пакеты не будут загружены этим методом.


В дополнение к описанным выше методам поиска отладочных символов, если гостевая система была смонтирована,
автоматически происходит поиск уже установленных отладочных символов в директории по умолчанию (`/usr/lib/debug`)
для всех типов гостевых операционных систем.


**Секция Symbols**

Является обязательной и содержит информацию о дополнительных символах, которые следует загружать.

- Поле `kernel` -- флаг разрешения загрузки символьной информации для ядра. При установке соответствующего флага,
скрипт позволяет выкачивать из образа ядро вместе с его символьной информацией. Если не удалось определить, какое ядро используется,
то выкачивается информация для всех ядер, найденных в каталоге `\boot`.

- Поле `python` -- флаг разрешения загрузки символьной информации для Python интерпретаторов.

- Поле `csharp` -- флаг разрешения загрузки символьной информации для C#.

- Поле `java` -- флаг разрешения загрузки символьной информации для Java.

**Секция UserFolder**

При активации данной секции перечень доступных методов для поиска отладочных символов будет дополнен поиском в директории,
указанной пользователем. Оставьте эту секцию закомментированной или удалите её, если этого не требуется.

- Поле `path` -- является обязательным и содержит путь к пользовательской директории, в которой хранятся отладочные символы.
Структура переданной директории должна соответствовать требованиям операционной системы к директории, в которую устанавливаются отладочные символы.

**Секция ContTools**

При активации данной секции будет проведен анализ не только гостевой операционной системы,
но и систем контейнеризации, которые в ней используются.

- Поле `docker_path` -- содержит путь в гостевой системе до директории с Docker,
по умолчанию это (`/var/lib/docker`). Если анализ Docker не требуется, закомментируйте это поле.

- Поле `local_podman_path` -- содержит путь в гостевой системе до директории с rootless Podman.
Учтите, что у этого поля нет значения по умолчанию. Если у вас есть контейнеры,
созданные от имени пользователя, и вы хотите их проанализировать, необходимо указать этот путь.
(пример пути: `/home/user/.local/share/containers`).
Если анализ rootless Podman не требуется, закомментируйте это поле.

- Поле `root_podman_path` -- содержит путь в гостевой системе до директории с root Podman,
по умолчанию это (`/var/lib/containers/`). Если анализ root Podman не требуется, закомментируйте это поле.


## <a name="tasks_config"></a>Конфигурационный файл для процессов task.cfg

Конфигурационный файл секции `Tasks` генерируется автоматически на этапе конфигурирования *Natch*.


## <a name="syscalls_config"></a>Конфигурационный файл для системных вызовов

Конфигурационные файлы для перехвата системных вызовов поставляются с инструментом и, как правило, подгружаются автоматически.

В редких случаях следует указывать конкретный файл, но писать самостоятельно его не нужно, лучше обратиться к разработчикам.

