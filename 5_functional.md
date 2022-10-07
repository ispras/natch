
# 5. Функциональные возможности Natch
## 5.1. Получение поверхности атаки

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

## 5.2. Подробная трасса помеченных данных

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


