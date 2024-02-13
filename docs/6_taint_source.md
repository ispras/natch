<div style="page-break-before:always;">
</div>

# <a name="taint_source"></a>6. Определение источников пометки

Одной из важных особенностей *Natch* является возможность пометки данных и отслеживания их
продвижения по системе. На данный момент можно помечать файлы, сеть (в том числе и локальную),
трафик от USB устройств. Способы пометки описаны ниже, воспользоваться ими пользователю нужно
после того, как создан проект и записан сценарий работы с объектом оценки. Про запись
сценария подробно в разделе [Запись сценария](7_scenario_work.md#record),
или коротко в разделе [Запись сценария работы](3_quickstart.md#record_scenario)
пошагового руководства по работе с *Natch*.

## 6.1. Пометка файлов

*Natch* может помечать отдельные файлы в гостевой системе, в расчет берутся операции чтения и отображения в память.

Пометка файлов осуществляется в [конфигурационном файле помеченных данных](16_app_configs.md#taint_config) в секции *[TaintFile]*.
В секции присутствует параметр *list*, куда можно записать список файлов для пометки.

Если файлов больше одного, их необходимо разделять точкой с запятой без пробелов.

Пример:

```ini
[TaintFile]
list=sample.txt;hello.txt
```

С помощью символа '\*' в конце имени файла можно указать множество файлов для пометки.
Например, */home/\** -- пометка всех файлов в каталоге home, */dev/tty\** - пометка всех данных,
вводимых в каждый из терминалов (tty1, tty2 и т.д.). Если путь начинается не с корневого каталога,
то он охватывает одноименные пути на разных расположениях. Например, *Pictures/1.jpg* помечает файлы
и на пути */home/user/Pictures/1.jpg*, и на пути */home/root/Pictures/1.jpg*.

Исполняемые файлы помечаться таким способом не будут, так как они не открываются для чтения пользовательским кодом, а отображаются
прямо в адресное пространство ядерными функциями.
Аналогично не будет детектироваться работа драйвера жесткого диска с местом хранения заданного файла.


## 6.2. Пометка входящих сетевых пакетов

*Natch* способен помечать весь сетевой трафик, который приходит в виртуальную машину извне.
Пометка полностью локального трафика на данный момент осуществляется через пометку сокетов (подробнее в разделе [Пометка сокетов](6_taint_source.md#taint_sockets)).

Для управления пометкой пакетов используется секция *[Ports]* конфигурационного файла `taint.cfg`
(подробнее в разделе [Конфигурационный файл для помеченных данных](16_app_configs.md#taint_config) секция *Ports*).

Пакеты помечаются целиком, вместе с заголовком второго уровня.
Для пометки можно фильтровать пакеты по протоколу 3 уровня или по выбранным портам,
если используются протоколы TCP или UDP. Список портов можно посмотреть в [википедии](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers).

Возможны следующие варианты работы:

* Помечать все входные пакеты. ip_protocol=-1 + (dst=-1 или src=-1)
* Помечать все UDP-пакеты. ip_protocol=17 + (dst=-1 или src=-1)
* Помечать все TCP-пакеты. ip_protocol=6 + (dst=-1 или src=-1)
* Помечать все HTTP-пакеты от внешнего веб-сервера. ip_protocol=6 + src=80
* Помечать все SNMP-пакеты к внутреннему серверу. ip_protocol=17 + dst=161
* Помечать все ICMP-пакеты. ip_protocol=1
* Помечать другие IP-пакеты, относящиеся к выбранному протоколу 3 уровня. ip_protocol=*x*, где *x* можно взять из [таблицы](https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers)

При необходимости отслеживать трафик по всем портам, в полях *dst/src* секции *[Ports]* следует указать значение -1. Если хотя бы в одном поле будет -1, будет отслеживаться весь трафик.

## <a name="taint_sockets"></a>6.3. Пометка сокетов

На данный момент поддерживается только для Linux.

В *Natch* реализована возможность пометки локальных сокетов. Для этого используется поле *list* (то же что и для пометки файлов) в секции *TaintFile*
конфигурационного файла помеченных данных. Чтобы помечать сокеты, следует указать название нужного протокола в качестве имени файла.
Поддерживаются следующие варианты: *TCP*, *UDP*, *TCPv6*, *UDPv6*, *UNIX*. Это имена, которые присваиваются файлам сокетов самим ядром Linux.

По умолчанию будет выполняться пометка всех сокетов указанного протокола. Предусмотрела возможность фильтрации с помощью следующего синтаксиса:

```
<socket_name>|parameters;
```

Параметры следует указывать в определенном виде.

Для сетевых сокетов указывается ip адрес в традиционной форме записи IPv4 или IPv6
(например, 127.0.0.1 и ::FFFF:10.0.2.2). Через пробел опционально указывается порт сокета.
Подразумевается, что эти адрес и порт относятся к месту назначения, с которым данный сокет взаимодействует.
Пометка по параметрам "слушающих" сокетов на текущий момент не реализована, поэтому при необходимости помечать сокеты,
создаваемые сервером для каждого клиента, необходимо указать выдаваемые им системой номера портов.

Для UNIX сокетов после вертикальной черты указывается соответствующее их адресу имя файла или уникальная строка.
Указать для пометки конкретный безымянный UNIX сокет на текущий момент не представляется возможным.

Ниже приведены примеры, указываемых имен файлов:

```text
TCPv6                          # пометка всех tcpv6 сокетов
UDPv6|2a00:1450:4010:c0b::71 0 # пометка udpv6 сокета по ip адресу и порту
UDP|127.0.0.1                  # пометка udp сокетов по ip адресу
TCP|173.194.220.105 80         # пометка tcp сокетов по ip адресу и порту
UNIX|server123.sock            # пометка unix сокетов по имени
```

Пример секции *TaintFile* с указанными сокетами:

```ini
[TaintFile]
list=TCP|173.194.220.105 80;UDP|127.0.0.1;UNIX|server123.sock;UDPv6|2a00:1450:4010:c0f::69
```

## 6.4. Пометка USB трафика

В *Natch* есть возможность помечать пакеты от USB устройств, но чтобы этим воспользоваться,
необходимо подготовить хостовую ОС для проброса USB устройства в гостевую систему и внести изменения в скрипты запуска *Natch*.

Для проброса USB устройств в виртуальную машину потребуется сделать ряд действий:

* В хостовой системе создать файл /lib/udev/rules.d/90-udev.rules с содержимым:

```bash
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0666"
```
* Выполнить команды:

```bash
sudo udevadm control --reload
sudo udevadm trigger
```

Так же помимо обычной настройки конфигурационных файлов, в этом случае требуется внести изменения
в скрипты запуска инструмента. На данный момент, это необходимо делать вручную.

Для работы с USB устройством в скрипты `run_record.sh` и `run_replay.sh` в конфигурацию запуска виртуальной машины необходимо добавить строку:
```
-usb -device usb-ehci,id=ehci -device usb-host,hostbus=X,hostaddr=Y,bus=ehci.0
```
Где вместо `X` и `Y` у параметров `hostbus` и `hostaddr` соответственно нужно указать параметры реального USB устройства, которое будет проброшено в
виртуальную машину.

Узнать эти параметры можно с помощью команды `lsusb`.

Пример вывода команды:
```
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 059: ID 05ac:12a8 Apple, Inc. iPhone5/5C/5S/6
Bus 001 Device 056: ID 0951:1665 Kingston Technology Digital DataTraveler SE9 64GB
Bus 001 Device 055: ID 05e3:0608 Genesys Logic, Inc. Hub
```

В этом выводе параметр `Bus` это `hostbus`, а `Device` -- `hostaddr`.

Если мы хотим пробросить флешку Kingston из представленного вывода, то командная строка будет выглядеть следующим образом:
```
-usb -device usb-ehci,id=ehci -device usb-host,hostbus=1,hostaddr=56,bus=ehci.0
```

Строка будет одинаковой как для режима записи, так и для воспроизведения, однако, в режиме воспроизведения устройство не будет подключено, поэтому
при переподключении устройства или его отсутствии нет необходимости править параметры.

После того как сценарий был записан, необходимо раскомментировать (или добавить) в `taint.cfg` секцию `USB`:
```
[USB]
on=true
```