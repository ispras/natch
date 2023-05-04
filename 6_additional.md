<div style="page-break-before:always;">
</div>

# <a name="natch_additional"></a>6. Дополнительные возможности Natch
## 6.1. Получение поверхности атаки

Основным результатом работы инструмента *Natch* является поверхность атаки. Поверхность атаки представлена набором процессов, модулей и функций, которые обрабатывали помеченные данные по время выполнения тестового сценария.

Для получения поверхности атаки можно воспользоваться командой монитора ``natch_get_attack_surface <filename>``, либо завершить работу эмулятора и файлы с информацией сгенерируются автоматически.

Поверхность атаки разбита на два файла, в одном находятся модули, во втором функции. В обоих случаях сущности привязаны к процессу. К введенному пользователем имени файла добавляются соответствующие суффиксы: ``<filename>_modules.txt`` и ``<filename>_functions.txt``. Автоматически сгенерированные файлы называются *surface_modules.txt* и *surface_functions.txt*.

Фрагмент файла *surface_modules.txt*:

```text
Task docker
    Module /lib/x86_64-linux-gnu/libpthread.so.0 0x7f6bc94a4000
    Module /lib/x86_64-linux-gnu/libc.so.6 0x7f6bc92de000
Task containerd-shim
    Module 0x0
Task wget2
    Module /lib/x86_64-linux-gnu/libpsl.so.5 0x7f921b147000
    Module 0x0
    Module 0x7f921b419000
    Module files/wget2 0x55b58a293000
    Module wget2/build/lib/libwget.so.1 0x7f921b3a2000
    Module /lib/x86_64-linux-gnu/libpthread.so.0 0x7f921af77000
    Module /lib/x86_64-linux-gnu/libresolv.so.2 0x7f9219cce000
    Module /lib/x86_64-linux-gnu/libc.so.6 0x7f921adb6000
    Module /lib/x86_64-linux-gnu/libz.so.1 0x7f921b15a000
```

Фрагмент файла *surface_functions.txt*:

```text
Task docker
    Module /lib/x86_64-linux-gnu/libpthread.so.0 0x7f6bc94a4000
        Function pthread_create 0x7f6bc94ac280 43
    Module /lib/x86_64-linux-gnu/libc.so.6 0x7f6bc92de000
        Function 0x7f6bc94aa390 5
        Function 0x556426eee1b0 54
        Function 0x556426eee180 1
Task containerd-shim
    Module 0x0
        Function 0xffffffff94af9700 453
        Function 0xffffffff94c001b8 54
        Function 0xffffffff94e03000 1
Task wget2
    Module files/wget2 0x55b58a293000
        Function 0x7f921b3b1210 2
        Function process_response_header 0x55b58a2a9560 8 wget2/src/wget.c:1665
        Function prepare_file 0x55b58a2a7720 1 wget2/src/wget.c:3214
        Function _host_hash 0x55b58a2a2400 28 wget2/src/host.c:81
        Function 0x7f921b3bcbe0 4
        Function get_header 0x55b58a2a85a0 5 wget2/src/wget.c:3485
        Function my_free 0x55b58a2ad2d0 1 wget2/src/options.c:4232
        Function plugin_db_forward_downloaded_file 0x55b58a2a4510 1 wget2/src/plugin.c:556
        Function hash_iri 0x55b58a2a1880 56 wget2/src/blacklist.c:171
        Function process_response 0x55b58a2aaf40 8 wget2/src/wget.c:1980
```

Число после описания каждой функции обозначает количество ее обращений к помеченным данным.
Это позволяет выбирать функции, наиболее интенсивно задействованные в обработке данных тестового сценария.

## <a name="taint_log"></a>6.2. Подробная трасса помеченных данных

Для более детального анализа может потребоваться больше информации, которую можно получить с помощью опции конфигурационного файла *Modules/log*.

В генерируемом логе на каждое обращение к помеченной памяти формируется расширенный набор данных.

Фрагмент лога для одного обращения:
```text
Load:
Process name: wget2 cr3:  0x1b5a5c000
Tainted access at 00007f921af88896
Access address 0x7f921a504b08 size 8 taint 0xfcfcfcfc
icount: 21216379863
Module name: /lib/x86_64-linux-gnu/libpthread.so.0 base:  0x00007f921af77000
Call stack:
    0: 00007f921af88896 in func 00007f921b3b1c40 wget2/build/lib/libwget.so.1::.recvfrom
    1: 00007f921b3c5307 wget2/libwget/net.c:861 in func 00007f921b3b0860 wget2/build/lib/libwget.so.1::.wget_tcp_read
    2: 00007f921b3bdbda wget2/libwget/http.c:990 in func 000055b58a29f350 files/wget2::.wget_http_get_response_cb
    3: 000055b58a2ac0ec wget2/src/wget.c:4017 in func 000055b58a2ac0e0 files/wget2::http_receive_response wget2/src/wget.c:4016
    4: 000055b58a2ac654 wget2/src/wget.c:2266 in func 000055b58a2ac2b0 files/wget2::downloader_thread wget2/src/wget.c:2250
    5: 00007f921af7efa1 in func 00007f921af7eeb0 /lib/x86_64-linux-gnu/libpthread.so.0
    6: 00007f921aeaf4cd
```
Не рекомендуется включать эту опцию по умолчанию, поскольку файл получается ощутимого размера
(сотни байт на каждое обращение к помеченным данным).

## <a name="taint_params_log"></a>6.3. Получение областей помеченной памяти для функций

Инструмент позволяет получить лог вызовов функций с диапазонами адресов записанных и прочитанных помеченных данных. Для получения лога необходимо использовать опцию конфигурационного файла *Modules/params_log*. Эта опция задает имя файла, куда будет записан лог с параметрами функций.

Выходной файл содержит диапазоны адресов и типы операций, выполненных с помеченными данными (r=чтение, w=запись). Также выводится стек вызовов на момент выхода из функции.

Фрагмент выходного файла:

```text
0xffffffff82dfc6f0 vmlinux:eth_type_trans
    0xffff88800e723840 8 bytes r
    0xffff88800e72384c 2 bytes r
    enter_icount: 58799550862
    exit_icount: 58799551027
    0: ffffffff82dfc963 in func ffffffff82dfc6f0 vmlinux::eth_type_trans
    1: ffffffff827cd3b6 in func ffffffff827ccec0 vmlinux::e1000_clean_rx_irq
    2: ffffffff827d544c in func ffffffff827d4c50 vmlinux::e1000_clean
    3: ffffffff82d1ea25 in func ffffffff82d1e6c0 vmlinux::net_rx_action
    4: ffffffff83a001b0 in func ffffffff83a00000 vmlinux::__do_softirq
    5: ffffffff83800f8d
0xffffffff81232e20 vmlinux:lock_acquire
    0xffff88806d009a90 8 bytes rw
    enter_icount: 58799552881
    exit_icount: 58799554333
    0: ffffffff81232ffd in func ffffffff81232e20 vmlinux::lock_acquire
    1: ffffffff8302c830 in func ffffffff8302c670 vmlinux::inet_gro_receive
    2: ffffffff82d200cb in func ffffffff82d1f440 vmlinux::dev_gro_receive
    3: ffffffff82d22885 in func ffffffff82d22680 vmlinux::napi_gro_receive
    4: ffffffff827cd485 in func ffffffff827ccec0 vmlinux::e1000_clean_rx_irq
    5: ffffffff827d544c in func ffffffff827d4c50 vmlinux::e1000_clean
    6: ffffffff82d1ea25 in func ffffffff82d1e6c0 vmlinux::net_rx_action
    7: ffffffff83a001b0 in func ffffffff83a00000 vmlinux::__do_softirq
    8: ffffffff83800f8d
```

## 6.4. Получение графов взаимодействий процессов и модулей

*Natch* позволяет получить историю распространения помеченных данных между процессами. Каждая строка лог-файла описывает передачу данных между двумя процессами, либо между процессом и файлом.

Для определения взаимодействий *Natch* выделяет дополнительную теневую память объемом в два раза больше, чем объем основной памяти, выделенной гостевой системе. В эту память для каждого физического адреса записывается идентификатор процесса, который последним записал помеченные данные на этот адрес. Взаимодействие определяется, когда процесс читает помеченные данные из ячейки памяти, записанной другим процессом. Взаимодействия также имеют веса, соответствующие количеству передаваемых данных. Однако следует отметить, что случаи, когда процесс читает 100 байт другого
процесса и когда читает 1 байт 100 раз, имеют один и тот же вес.

Также *Natch* умеет определять некоторые интерфейсы передачи данных. По системным вызовам отслеживаются взаимодействия процессов с файлами и сокетами. Через структуры ядра определяются области разделяемой и приватной памяти.

Для включения функции построения графов используется секция *TaintedTask* в основном конфигурационном файле. Опция *task_graph* отвечает за граф процессов, опция *module_graph* за граф модулей. Граф модулей строится теми же методами, что и граф процессов. Заметим, что включение обеих опций одновременно приведет к значительному увеличению объема потребления памяти. Результаты записываются соответственно в файлы *task_graph.json* и *module_graph.json* при завершении работы эмулятора.

Выходной файл на верхнем уровне представляет собой список ребер графа. У каждого ребра есть поля *source*, *destination* и *score*. Первые два описывают узлы, между которыми происходит передача помеченных данных. Поле *score* содержит количество передаваемых байт между процессами. Если граф строился во время воспроизведения, то для каждого ребра присутствует поле *icount*, которое описывает диапазон времени, в которое происходила передача данных. У некоторых ребер присутствует поле *extra*, которое содержит описание способа передачи данных. Описание способа передачи состоит из одного поля *type*, которое может принимать значения *shared-memory* для передач через разделяемую память и *private-memory* для передач через приватную память (Например, передача данных от родительского процесса к дочернему во время вызова fork). Описание узла графа имеет поле *type*, описывающее тип узла. Если узел является источником помеченных данных, то его описание содержит поле *taint_source* в значении *true*. Далее идет описание каждого типа узлов графа и его параметров:

* *file* - обычный файл. Поле *name* содержит полное имя файла.
* *tcp*, *udp*, *tcpv6*, *udpv6* - сетевые сокеты TCP и UDP для IPv4 и IPv6 соответственно. Поля ip и port содержат соответственно ip адрес и порт сокета.
* *unix* - unix сокет. Поле *name* содержит имя файла из параметров сокета, либо строку *pair + число*, если сокет не имеет имени файла (Создан системным вызовом *socketpair*)
* *netlink* - netlink сокет. Поле *name* содержит индивидуальный адрес сокета netlink.
* *socket* - остальные виды сокетов. Поле *name* содержит название типа сокета. Наличие такого узла в графе говорит о том, что обработка параметров данного типа сокетов в настоящее время не реализована.
* *pipe* - неименованный канал. Поле *name* содержит строку *pair + число*.
* *network* - сеть, источник помеченных данных. Поле *protocol* описывает номер ip протокола в сетевых пакетах. Поле *port_in* описывает входящий порт, поле *port_out* исходящий порт.
* *user-process* - пользовательский процесс. Поле proc содержит уникальный id процесса.
* *kernel-process* - процесс ядра. Поля совпадают с *user-process*.
* *module* - модуль (Только для *module_graph*). Поле *name* содержит имя модуля, поле *address* - адрес модуля.
* *kernel* - ядро в *module_graph*. При наличии отладочных символов поле *name* содержит имя исполняемого файла ядра.

Пример выходного файла:

```text
{"icount": {"start": 13557580656, "final": 13557582746}, "source": {"port": 80, "ip": "172.217.168.228", "type": "tcp", "id": 219}, "destination": {"proc": 20, "type": "user-process"}, "score": 1642},
{"icount": {"start": 14161961429, "final": 14161966494}, "source": {"proc": 20, "type": "user-process"}, "destination": {"name": "/home/nat/bin/scripts/index.html", "type": "file", "id": 2035}, "score": 2058},
{"icount": {"start": 14161961429, "final": 14161966494}, "source": {"name": "/home/nat/bin/scripts/index.html", "type": "file", "id": 2035}, "destination": {"proc": 196, "type": "user-process"}, "score": 2048},
{"icount": {"start": 14167892352, "final": 14167896186}, "extra": {"type": "shared-memory"}, "source": {"proc": 196, "type": "user-process"}, "destination": {"proc": 198, "type": "user-process"}, "score": 100},
```

## <a name="functional_coverage"></a>6.5. Анализ покрытия бинарного кода

Плагин *coverage* используется для сбора покрытия исполняемого кода.

Опции плагина:

- *file*
Задаёт название файла, куда будут записываться данные о покрытии кода (по умолчанию *coverage.cov64*)
- *taint*
Переключает режимы сбора покрытия. При установке в true, сбор ведётся только для помеченных данных. Иначе, для всех выполненных базовых блоков (ББ), которые относятся к какому-либо модулю (данный плагин не собирает покрытия для ББ, которые не относятся ни к одному модулю).

Пример командной строки для сбора покрытия всех выполненных ББ в режиме воспроизведения выглядит следующим образом: 

```text
./qemu-system-x86_64 -m 4G \
-monitor stdio \
-os-version Linux \
-drive file=debian10_w_gui.diff,if=none,id=img-direct \
-drive driver=blkreplay,if=none,image=img-direct,id=img-blkreplay \
-device ide-hd,drive=img-blkreplay \
-netdev user,id=net0 \
-device e1000,netdev=net0 \
-object filter-replay,id=replay,netdev=net0 \
-icount shift=5,rr=replay,rrfile=replay.bin,rrsnapshot=snap \
-plugin natch,config=natch.cfg \
-plugin coverage,taint=false \
```

Для удобного анализа выходного файла можно воспользоваться скриптом *coverage.py*, который раскрашивает выполненный код в IDA Pro и выводит таблицу с покрытием функций. На данный момент скрипт протестирован и гарантированно работает на версиях 7.2 и 7.6, теоретически и на тех, что между ними.

Чтобы использовать скрипт *coverage.py*, необходимо:

1. Открыть интересующий двоичный файл в IDA Pro.
2. Для совпадения адресов в Qemu и IDA Pro необходимо выполнить Rebase (Edit -> Segments -> Rebase program). Рекомендуется использовать адрес начала модуля.
3. Импортировать скрипт в окно File -> Script Command.
4. Убедиться, что выбран язык сценариев Python.
5. Нажать "Выполнить" и выбрать файл с покрытием в формате *.cov64*.
6. В появившемся окне выбрать интересующие процессы.


## 6.6. Получение аргументов вызываемых функций.

Один из способов получения начальных данных для функции при фаззинге - это использование данных, полученных в результате выполнения приложения. Если вы знаете, какие функции вам нужно протестировать, то можно сразу запустить Natch с раскомментированной секцией *[FunctionArgs]* в основном конфигурационном файле и указать путь к конфигурационному файлу с именами интересующих функций. При этом, для минимизации замедления, в секции, относящейся к тейнту, необходимо поставить параметр *on* в значение *false*. Если вы не знаете, какие функции вам нужны, то сначала запустите Natch для получения функций, которые работали с помеченными данными, а затем использовать их в качестве интересующих функций при повторном запуске.

В результате работы в директорию *output* будет сохранен файл *args_info.json*, содержащий результирующую информацию об аргументах в формате JSON.

Пример конфигурационного файла для функций с именами: test_1 и test_2:

```
[Func1]
name=test_1

[Func2]
name=test_2
```
В настоящее время, реализована поддержка только простых типов аргументов:

* Целочисленные значения.
* Строки (char *), заканчивающиеся нулевым терминатором.

Если встречается аргумент, не соответствующий этим требованиям, то он и все последующие аргументы не будут проанализированы.


