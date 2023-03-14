<div style="page-break-before:always;">
</div>

# <a name="begin"></a>1. Начало работы с Natch

*Natch* - это инструмент для определения поверхности атаки, основанный на полносистемном эмуляторе QEMU.
С помощью этого раздела можно освоить основные принципы использования системы определения поверхности атаки [Natch](https://www.ispras.ru/technologies/natch/) (разработчик - [ИСП РАН](https://www.ispras.ru/)):

* создание виртуализованной среды выполнения объекта оценки (далее - ОО) в формате [QEMU](https://wiki.qemu.org/Main_Page/)
* запуск виртуализированной среды под контролем *Natch*
* анализ информации о движении помеченных данных в контролируемой виртуализованной среде

*Natch* поддерживает анализ только бинарного кода - таким образом анализ задействования кода интерпретируемых скриптов, а также "распространения" помеченных данных по коду интерпретируемых скриптов, возможен только в опосредованном виде - в формате анализа задействования нативных функций интерпретаторов, выполняющих указанные скрипты.

## <a name="complect"></a>1.1. Комплект поставки

Комплект поставки Natch доступен в двух форматах:

- **основной** - защищенный бинарный дистрибутив, требующий наличие аппаратного ключа (персональный "черный" ключ, сетевой "красный" ключ или иные версии ключа) с лицензией c идентификатором "6":

    [Natch v.2.2](https://nextcloud.ispras.ru/index.php/s/natch_v.2.2) 

- **резервный** - .ova-образ Ubuntu 20 для VirtualBox с предустановленным защищенным Natch, необходимым ПО (pip3, vim) и доступом к VPN-серверу, раздающему лицензии:

    Для текущей версии не предусмотрен. Прошлый релиз: [Natch v.2.1](https://nextcloud.ispras.ru/index.php/s/natch_v.2.1_vbox)


Предыдущие релизы можно найти [здесь](7_appendix.md#app_releases).

**Важно!**

В связи с переходом на новый инструмент лицензирования до окончания действия всех выданных лицензий будут поддерживаться два варианта дистрибутива. Если у вас лицензия Sentinel, то следует брать дистрибутив из одноименной папки, если вы новый пользователь *Natch* - дистрибутив для вас в папке Guardant. Так же пользователям Sentinel рекомендуется переустановить окружение (aksusbd_8.51-1_amd64.deb), пакет находится в папке с дистрибутивом.

## <a name="create-qemu-env"></a>1.2. Подготовка виртуализованной среды в формате QEMU

Подготовка виртуализованной среды выполнения ОО в общем случае состоит из следующих последовательных шагов:

* создание образа эмулируемой операционной системы в формате диска [qcow2](https://en.wikipedia.org/wiki/Qcow) на основе базового дистрибутива ОС. Формат *qcow2* позволяет эффективно формировать снэпшоты состояния файловой системы в произвольный момент выполнения виртулизованной среды функционирования;
* сборка дистрибутива ОО с требуемыми параметрами, в частности, с генерацией и сохранением отладочных символов;
* помещение собранного дистрибутива ОО в виртуализованную среду выполнения;
* подготовка команд запуска QEMU, для эмуляции аппаратной части среды функционирования, загрузку и выполнение компонентов *Natch*.

Подготовка виртуализованной среды выполнения ОО в значительной степени совпадает с подготовкой среды для анализа с помощью инструмента динамического анализа помеченных данных [Блесна](https://www.ispras.ru/technologies/blesna/) (разработчик - [ИСП РАН](https://www.ispras.ru/)), с точностью до подготовки команд запуска QEMU.

Создавать виртуализованную среду выполнения ОО **рекомендуется** в хостовой системе, допускающей запуск QEMU в режиме пользовательской виртуализации (ключ `-enable-kvm`) - это существенно ускорит процесс,
скорость работы в режиме аппаратной виртуализации более чем на порядок превосходит работу в режиме полносистемной эмуляции. Проверить доступность данного режима в вашей хостовой системе
(равно как и установить kvm-модули в вашу систему) можно опираясь на следующую [статью](https://phoenixnap.com/kb/ubuntu-install-kvm) с помощью команды:
```bash
sudo kvm-ok
```

Примерный алгоритм проброса виртуализации для трехуровневого стенда: *Windows 11+AMD Процессор (хостовая ОС  рабочей станции) -> VirtualBox (хостовая ОС рабочей станции) -> ubuntu+kvm+qemu (хостовая ОС Natch) -> lubuntu (гостевая ОС)* приведён ниже.

Перед установкой KVM в гостевой ОС нужно настроить среду виртуализации VirtualBox в хостовой ОС Natch:

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/vbox_system.png">

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/vbox_system2.png">

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/vbox_display.png"><figcaption>_Настройки машины в VBox_</figcaption>

Перед установкой KVM необходимо определить, поддерживает ли процессор эту функцию: `egrep -c '(vmx|svm)' /proc/cpuinfo`

В результате будут следующие варианты ответа системы:

 - 0 – процессор не поддерживает функции KVM;
 - 1 и более – процессор поддерживает функции KVM.

Следующий этап – установка KVM: `sudo apt install qemu qemu-kvm libvirt-daemon libvirt-clients bridge-utils virt-manager`. Этой командой выполнена установка утилиты `kvm`, библиотеки `libvirt` и менеджера виртуальных машин.

Далее необходимо добавить своего пользователя в группу `libvirt`, так как только `root` и пользователи этой группы могут использовать виртуальные машины KVM: `sudo gpasswd -a $user libvirt`

Затем необходимо убедиться, что сервис `libvirt` запущен и работает: `sudo systemctl status libvirtd`

После выполнения этой команды выполнить: `reboot`

Далее, проверка установки `kvm`: `kvm-ok`

Если вы получили ответ:

```bash
INFO: dev/kvm exists
KVM acceleration can be used
```

Значит настройка выполнена правильно, и вы молодец :) Ваша QEMU-виртуализированная гостевая ОС будет работать быстро, что позволит быстро сформировать в ней исследуемую среду.

**При этом важно помнить, что собственно анализ в любом случае необходимо выполнять без использования данного ключа**, так как только полносистемная эмуляция позволяет собрать полный лог действий процессора.

### 1.2.1. Подготовка хостовой системы

Рекомендации по подготовке хостовой системы приведены [здесь](https://gitlab.community.ispras.ru/trackers/natch/-/wikis/Natch-requirements#%D0%B0-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D0%B5-%D1%82%D1%80%D0%B5%D0%B1%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F-%D0%BA-%D1%85%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%B9-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B5) (*для получения доступа к репозиторию сообщества ознакомьтесь с информацией в описании телеграм-канала [Орг. вопросы::Доверенная разработка](https://t.me/sdl_community)*).

Подготовим Linux-based рабочую станцию (далее - хост), поддерживающую графический режим выполнения. QEMU демонстрирует вывод эмулируемой среды выполнения в отдельном графическом окне, следовательно нам необходим графический режим. Хост может быть реализован в формате виртуальной машины. В примерах ниже описаны действия пользователя, работающего в виртуальной машине VirtualBox (4 ядра, 8 ГБ ОЗУ)
с установленной ОС [Ubuntu20.04](ttps://releases.ubuntu.com/20.04/ubuntu-20.04.5-desktop-amd64.iso) (desktop-конфигурация, обновить пакеты при установке).

Установим требуемое системное ПО, в т.ч. QEMU:
```bash
sudo apt install -y curl qemu-system gcc g++
```
*Подсказка: данная инсталляция требуется не для запуска Natch, но для создания образов ВМ на произвольном хосте. Natch содержит в своём составе требуемую для работы версию QEMU, поэтому если вы планируете создавать образ ВМ на том же хосте, на котором уже установили Natch, отдельно QEMU можно не ставить*

Скачаем на хост выбранный базовый дистрибутив ОС. Лучше использовать минимальный образ -- уменьшение числа установленных служб, стартующих при запуске, сокращает нагрузку на процессор и ускоряет анализ объекта оценки в режиме полносистемной эмуляции. В нашем примере используется легковесный образ Ubuntu - [lubuntu](https://lubuntu.net/downloads/). Создадим каталог на хосте и скачаем туда дистрибутив:
```bash
cd ~ && mkdir natch_quickstart && cd natch_quickstart
curl -o lubuntu-18.04-alternate-amd64.iso  'http://cdimage.ubuntu.com/lubuntu/releases/18.04/release/lubuntu-18.04-alternate-amd64.iso'
```
Проверим, работает ли эмулятор:
```bash
qemu-system-x86_64 --version
QEMU emulator version 4.2.1 (Debian 1:4.2-3ubuntu6.19)
Copyright (c) 2003-2019 Fabrice Bellard and the QEMU Project developers
```
Для установки гостевой ОС создадим образ жесткого диска в формате `qcow2`, с именем `lubuntu.qcow2` и размером `20 ГБайт`.
```bash
qemu-img create -f qcow2 lubuntu.qcow2 20G
Formatting 'lubuntu.qcow2', fmt=qcow2 size=21474836480 cluster_size=65536 lazy_refcounts=off refcount_bits=16
ll
total 8100768
drwxrwxr-x  4 user user       4096 янв 30 20:40 ./
drwxr-xr-x 25 user user       4096 янв 30 20:40 ../
-rw-rw-r--  1 user user  751828992 янв 30 20:34 lubuntu-18.04-alternate-amd64.iso
-rw-r--r--  1 user user     196928 янв 30 20:08 lubuntu.qcow2
```
Создадим скрипт запуска нашей ВМ `run.sh`. Мы сохраняем его в виде отдельного файла, потому что позже скрипт потребуется редактировать. Для тех, кто сталкивается с синтаксисом QEMU впервые, рекомендуется ознакомиться с основными командами, описанными в официальной [документации QEMU](https://www.qemu.org/docs/master/system/invocation.html). Важным для ускорения работы виртуализированной среды qemu, за счет аппаратной [виртуализации](#create-qemu-env), является установка ключей `-enable-kvm` и `-cpu host,nx`.
```bash
qemu-system-x86_64 \
-hda lubuntu.qcow2 \
-m 4G \
-enable-kvm \
-cpu host,nx \
-monitor stdio \
-netdev user,id=net0 \
-device e1000,netdev=net0 \
-cdrom lubuntu-18.04-alternate-amd64.iso
```
Запустим скрипт:
```bash
./run.sh
```
после чего увидим графическое окно установки *lubuntu*. *lubuntu* желательно устанавливать с минимальным набором параметров для ускорения установки и уменьшения "шума" избыточных процессов и сетевых служб во время анализа.

*Подсказка: чтобы вывести курсор мыши из открытого графического окна ВМ QEMU нажмите Ctrl+Alt+G*

После завершения установки удалим из скрипта запуска `run.sh` указание подключения cdrom -- для дальнейшей работы он нам не потребуется
```bash
#-cdrom lubuntu-18.04.3-desktop-amd64.iso
```
Наш образ среды функционирования готов к работе -- в частности к установке в него пресобранного **с символами** прототипа объекта оценки.

### <a name="build_prototype"></a>1.2.2. Сборка прототипа объекта оценки

Рекомендации по подготовке исполняемого кода приведены [здесь](https://gitlab.community.ispras.ru/trackers/natch/-/wikis/Natch-requirements#%D0%B2-%D0%BF%D0%BE%D0%B4%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%BA%D0%B0-%D0%BF%D0%BE%D0%B4%D0%BB%D0%B5%D0%B6%D0%B0%D1%89%D0%B5%D0%B9-%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%D1%83-%D0%B3%D0%BE%D1%81%D1%82%D0%B5%D0%B2%D0%BE%D0%B9-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B).

В общем случае к анализируемому исполняемому коду выставляется два требования:

* должна быть представлена отладочная информация в формате символов в составе исполняемых файлов, отдельно прилагаемых символов или map-файлов. Предоставление символов непосредственно в составе исполняемых файлов является основной и рекомендуемой стратегией -- начиная с версии *Natch v.1.3* инструмент умеет самостоятельно доставать информацию об отладочных символах из исполняемых файлов, собранных *как минимум* компиляторами *gcc* и *clang* с сохранением отладочной информации (ключ компилятора `-g`, также рекомендуется сборка без оптимизаций в режиме `-O0`). Начиная с версии *Natch v.2.1* для стандартных пакетов из наиболее популярных сборок операционных систем символы подгружаются автоматически;
* **рекомендуется выполнять сборку подлежащего анализу исполняемого кода в виртуализированной среде (виртульная машина qemu).** В случае, если сборка и анализ будут выполняться в различных средах функционирования (например, сборка осуществляется на отдельном сборочном сервере), требуется обеспечить совместимость версий разделяемых динамических библиотек, в первую очередь *glibc*, из состава среды функционирования. На вашем хосте и в виртуализированной среде комплекты библиотек могут различаться.

В качестве прототипа объекта оценки рассмотрим популярную программу *wget*, сборку которой осуществим в хостовой системе (условная "сборочница") с последующим помещением собранного дистрибутива в виртуализированную гостевую среду *lubuntu*. Как было сказано выше, в тестовых сценариях **рекомендуется выполнять сборку подлежащего анализу исполняемого кода в виртуализированной среде (виртульная машина qemu).** Сборка в отдельной "сборочнице" не обязательна.

Для выполнения [*классического*](https://thoughtbot.com/blog/the-magic-behind-configure-make-make-install) подготовительного скрипта `configure`, входящего в комплект поставки *wget*, генерирующего make-файл, потребуется установить дополнительные зависимости (скрипт выведет их наименования в случае неудачного завершения), например:
```bash
sudo apt install -y gnutls-dev gnutls-bin curl make gcc g++
```
*Подсказка: поскольку мы собираем wget из исходников, потребуется комплект заголовочных файлов, доступный как раз в dev-версии пакета gnutls*

Скачаем исходные тексты *wget* из репозитория в файловую систему хоста:
```bash
curl -o wget-1.21.2.tar.gz  'https://ftp.gnu.org/gnu/wget/wget-1.21.2.tar.gz'
tar -xzf wget-1.21.2.tar.gz && cd wget-1.21.2
```
Скрипт `configure` запустим с ключами, устанавливающими параметры компилятора для сохранения информации об отладочных символах. После этого запустим `make` для сборки проекта.
```bash
CFLAGS='-g -O0' ./configure
make
```
**Важное замечание - следующие два подраздела 1.2.3 и 1.2.4 оставлены в качестве пособия для специфических случаев, когда возможность сборки исполняемого файла из исходных текстов с произвольными параметрами отсутствует, либо явно требуется получение отдельных [map-файлов](https://stackoverflow.com/questions/22199844/what-are-gcc-linker-map-files-used-for), в частности для случаев анализа ядра Linux. Генерация map-файлов не нужна для обычных тестовых сценариев анализа usermode-приложений**

### 1.2.3. *Генерация map-файлов средствами компилятора*

Выполним скрипт:
```bash
CFLAGS='-g -O0 -Xlinker -Map=output.map' ./configure && \
make
```
и проверим, что map-файлы создались:
```bash
find . -name *.map
./src/output.map
./output.map
```
Полученные map-файлы можно поместить на хосте в каталог с исполняемыми файлами *wget*. Тогда Natch будет опираться на map-файлы при символизации соответствующиех процессов.
**Важное замечание: название бинарного файла и соответствующего ему map-файла должны совпадать.**

### 1.2.4. *Генерация map-файлов сторонними инструментами*

Получение map-файлов для исполняемого файла, собранного с отладочными символами, возможно с помощью сторонних инструментов. Это может быть актуально в тех случаях, когда сборочный конвейер недоступен,
либо получение от сборочного конвейера map-файлов в поддерживаемом *Natch* формате невозможно (например, использование специфического компилятора/компоновщика). Сгенерируем map-файлы с использованием бесплатной версии дизассемблера [IDA Pro](https://hex-rays.com/ida-free/). Для этого необходимо скачать установочный комплект по указанной ссылке и возможно доустановить библиотеки Qt `apt install -y qt5-default`.

После установки IDA необходимо запустить её, открыть интересующий нас исполняемый файл (в нашем случае это `wget`)

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida_map1.png"><figcaption>_Загрузка бинарного файла в IDA Pro_</figcaption>

пройти процедуру генерации map-файла

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida_map2.png"><figcaption>_Генерация map-файла_</figcaption>

обязательным пунктом является только *Segmentation information*, остальные по желанию (хотя, например, локальные имена дизассемблера вряд ли сделают вывод понятнее).

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida_map3.png"><figcaption>_Выбор опций map-файла_</figcaption>

после чего убедиться, что map-файл появился в файловой системе

```bash
ll src | grep .map
-rw-rw-r--  1 user user  564686 фев  3 16:11 wget.map
```

### 1.2.5. Перенос прототипа объекта оценки из образа ВМ на хост (или с хоста в образ ВМ)

Чтобы поместить собранный *wget* в виртуальную машину или выкачать его из виртуальной машины на хост, воспользуемся [nbd-сервером QEMU](https://manpages.debian.org/testing/qemu-utils/qemu-nbd.8.en.html), позволяющим [смонтировать](https://gist.github.com/shamil/62935d9b456a6f9877b5) созданный ранее qcow2-диск ВМ в файловую систему хостовой ОС. Для монтирования диск не должен быть задействован (виртуальная машина должна быть выключена).

Загрузим NBD-драйвер в ядро хостовой ОС:
```bash
modprobe nbd max_part=8
```
Смонтируем наш образ диска как сетевое блочное устройство:
```bash
sudo qemu-nbd --connect=/dev/nbd0 lubuntu.qcow2
```
Определим число разделов на устройстве:
```bash
fdisk /dev/nbd0 -l
Disk /dev/nbd0: 20 GiB, 21474836480 bytes, 41943040 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xe6ea1316

Device      Boot Start      End  Sectors Size Id Type
/dev/nbd0p1 *     2048 41940991 41938944  20G 83 Linux
```
Смонтируем раздел в какой-либо каталог хостовой ОС (например, традиционно, в mnt)
```bash
sudo mount /dev/nbd0p1 /mnt/
ls /mnt
bin   dev  home        initrd.img.old  lib64       media  opt   root  sbin  swapfile  tmp  var      vmlinuz.old
boot  etc  initrd.img  lib             lost+found  mnt    proc  run   srv   sys       usr  vmlinuz
```
Поместим прототип ОО на смонтированный раздел:
```bash
sudo cp -r wget-1.21.2 /mnt/ && ls /mnt
bin   dev  home        initrd.img.old  lib64       media  opt   root  sbin  swapfile  tmp  var      vmlinuz.old
boot  etc  initrd.img  lib             lost+found  mnt    proc  run   srv   sys       usr  vmlinuz  wget-1.21.2
```
Отмонтируем диск:
```bash
sudo umount /mnt/
sudo qemu-nbd --disconnect /dev/nbd0
sudo rmmod nbd
```

### 1.2.6. Тестирование виртуализированной среды функционирования ОО

Запускаем ВМ скриптом `run.sh` с отключенным ранее cdrom, дожидаемся загрузки ОС ВМ, авторизуемся в ОС, пробуем выполнить обращение к произвольному сетевому ресурсу с помощью собранной нами версии *wget*:
```bash
cd wget-1.21.2/src && sudo ./wget ispras.ru
```
В результате вы должны увидеть приблизительно следующую картину в графическом окне QEMU, свидетельствующую о том, что ОО корректно выполняется в среде функционирования и сетевая доступность для ВМ обеспечена:

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/check.png"><figcaption>_Пример подготовленного ОО в QEMU_</figcaption>


## 1.3. Обучающие примеры

### 1.3.1. Анализ образа системы, содержащего тестовые комплекты пресобранных исполняемых файлов

Все нижеописанное проделано на примере дистрибутива, работающего под Ubuntu 20.

Для этого примера потребуется:

- рабочая станция под управлением ОС Linux (традиционно Ubuntu 20.04). Отдельная установка пакета **qemu-system** не требуется, нужная версия входит в дистрибутив *Natch*;
- актуальный [дистрибутив](#complect) Natch;
- подготовленный разработчиком [тестовый набор](https://nextcloud.ispras.ru/index.php/s/testing_2.0), включающий в себя минимизированный образ гостевой операционной системы Debian (размер qcow2-образа около 1 ГБ), а также два комплекта программ (Sample1_bins и Sample2_bins), собранных с отладочными символами.

*Сценарий использования тестового комплекта Sample1_bins*

Программа test_sample читает файл *sample.txt*, в первой строке которого записан адрес Google. Он передает эту строку в качестве параметра программе *test_sample_2*. Программа *test_sample_2* "курлит гугл" в файл *curl.txt*.

*Сценарий использования тестового комплекта Sample2_bins*

Процесс сервера redis-server следует запустить командой `redis-server --port 5555 --protected-mode no`, после чего соединиться с ним из хостовой системы клиентской утилитой `redis-cli -h localhost -p 15555` (её можно поставить например так `sudo apt install redis-tools`) и выполнить какие-нибудь действия, например `SET b VeryBigValue`.


#### 1.3.1.1. Получение образа и дистрибутива

В случае выполнении действий в подготовленной виртуальной машине, содержащей Natch, скачивание и установка бинарного комплекта не требуются.

В случае установки в формате бинарного комплекта следует скачать его и распаковать -- команда для скачивания тестового комплекта с помощью *curl* выглядит так `curl -o materials.zip 'https://nextcloud.ispras.ru/index.php/s/testing_2.0/download'`. Состав комплекта бинарной поставки в облачном хранилище включает архивы с бинарными файлами, библиотеками, SNatch и докуменатацию.

После скачивания дистрибутива и обучающих материалов их следует распаковать -- традиционно (но не обязательно, реальное размещение файлов тестовых материалов не принципиально и зависит от ваших предпочтений). После распаковки увидим следующие каталоги: `libs`, `Natch_testing_materials`, `natch_ubuntu20`, `snatch` и документацию в формате pdf.

В каталоге `libs` размещаются используемые *Natch* библиотеки (подключаются с использованием стандартного механизма [preload](https://www.baeldung.com/linux/ld_preload-trick-what-is#:~:text=The%20LD_PRELOAD%20trick%20is%20a,a%20collection%20of%20compiled%20functions.) при запуске qemu-system и иных qemu-процессов). В каталоге `natch_ubuntu20` помещаются собственно исполняемые файлы *Natch*.

Учётные записи пользователей гостевой ОС: `user/user` и `root/root`.


#### 1.3.1.2. Установка Natch и Snatch

Для работы *Natch* следует установить python-библиотеки, обеспечивающие работоспособность скриптов, а так же deb-пакеты с помощью скрипта:
```text
user@natch1:~/natch_quickstart$ ./natch_ubuntu20/bin/natch_scripts/setup_requirements.sh
```
В процессе работы скрипта потребуется пароль администратора.

Для работы *SNatch* следует запустить установочный скрипт и дождаться его успешного выполнения (сообщения об ошибках сборки некоторых python-пакетов можно игнорировать при условии того, что скрипт в целом завершается успешно):
```bash
user@natch1:~/natch_quickstart/snatch$ ./snatch_setup.sh
```
При выполнении скрипт запросит пароль для sudo.

#### 1.3.1.3. Настройка Natch для работы с тестовым образом ОС

Процесс настройки состоит из двух этапов -- автоматизированного (обязательный) и ручного (дополнительный, при необходимости тонкой настройки). Предназначение [файлов конфигурации и их параметров](3_configs.md#natch_config_main) **описано в документации**):

##### 1.3.1.3.1. Автоматизированная настройка

Автоматизированная настройка выполняется интерактивным скриптом `natch_run.py`, выводимые которым вопросы и примеры ответов на которые приведём далее. Запуск скрипта (**не забываем про необходимость прелоада библиотек**):
```text
user@natch1:~/natch_quickstart$ LD_LIBRARY_PATH=/home/user/natch_quickstart/libs/ ./natch_ubuntu20/bin/natch_scripts/natch_run.py Natch_testing_materials/test_image_debian.qcow2
Image: /home/user/natch_quickstart/Natch_testing_materials/test_image_debian.qcow2
OS: Linux
```
Вводим имя проекта - будет создан каталог с таким именем:
```text
Enter path to directory for project (optional): test1
Directory for project files '/home/user/natch_quickstart/test1' was created
Directory for output files '/home/user/natch_quickstart/test1/output' was created
```
Сколько памяти выдать гостевой виртуальной машине (постфикс указывать обязательно. G или M):
```text
Common options
Enter RAM size with suffix G or M (e.g. 4G or 256M): 4G
```
Далее можно выбрать режим работы эмулятора -- графический или текстовый. По умолчанию графический.
```text
Do you want to run emulator in graphic mode? [Y/n] y
```
На этом этапе скрипт попробует обратиться к утилите qemu-img для создания оверлея для образа. В случае успеха увидим:
```text
Now we will trying to create overlay...
Overlay created
```
Если что-то пошло не так, скрипт прекратит работу.

Если наш сценарий предполагает передачу помеченных данных по сети (далее мы рассматриваем в качестве основного как раз сценарий №2 -- взаимодействие с redis-сервером, слушающим tcp-порт 5555), нам потребуется взаимодействовать с сетевыми сервисами гостевой ОС с помощью программ, запущенных на хосте. **перехват пакетов, отправитель и получатель которых "находятся" внутри гостевой ОС (localhost <--> localhost), в настоящий момент не поддерживается**. Указываем *Natch*, какой порт мы хотим опубликовать в гостевую ОС:
```text
Network option
Do you want to use ports forwarding? [Y/n] y
Do you want to taint source ports too? [Y/n] n
Write the ports you want separated by commas (e.g. 7777, 8888, etc) 5555
Your port for connecting outside: 15555
```
Далее нам нужно указать пути к каталогам на хосте, содержащим копии бинарных файлов, размещенных в гостевой ОС -- это как раз те самые файлы (собранные с символами, или с отдельными map-файлами), которые мы получили в ходе выполнения пункта [Сборка прототипа объекта оценки](#build_prototype). 
Этот процесс будет выполняться параллельно, результаты увидим позже.

Следующая стадия - конфигурирование технических параметров *Natch*, требующая тестового запуска виртуальной машины. В ходе данного запуска выполняется получение информации о параметрах ядра и заполнение ini-файла. Вы можете отказаться от данного шага, в случае если этот файл уже был ранее создан для данного образа гостевой виртуальной машины -- тогда вам потребуется указать к нему путь, однако, в большинстве случаев вы вероятно будете создавать эти файлы с нуля:

```text
Generate config file task.cfg? [Y/n] y (или просто нажмите Enter)

Now will be launch tuning. Don't close emulator
Three...
Two..
One.
Go!
QEMU 6.2.0 monitor - type 'help' for more information
Natch v.2.2
(c) 2020-2023 ISP RAS

Reading Natch config file...
Network logging enabled
[Tasks] No such file 'task.cfg'. It will be created.
Now tuning will be launched.

Tuning started. Please wait a little...
Generating config file: task.cfg
Trying to find 19 kernel-specific parameters
[01/19] Parameter - task_struct->pid            : Found
[02/19] Parameter - task_struct->comm           : Found
[03/19] Parameter - task_struct->group_leader   : Found
[04/19] Parameter - task_struct->parent         : Found
[05/19] Parameter - mount fields                : Found
[06/19] Parameter - files_struct fields         : Found
[07/19] Parameter - vm_area_struct size         : Found
[08/19] Parameter - vm_area_struct->vm_start    : Found
[09/19] Parameter - vm_area_struct->vm_end      : Found
[10/19] Parameter - vm_area_struct->vm_flags    : Found
[11/19] Parameter - mm->map_count               : Found
[12/19] Parameter - mm_struct fields            : Found
[13/19] Parameter - task_struct->mm             : Found
[14/19] Parameter - mm->arg_start               : Found
[15/19] Parameter - task_struct->state          : Found
[16/19] Parameter - socket struct fields        : Found
[17/19] Parameter - task_struct->exit_state     : Found
[18/19] Parameter - cred->uid                   : Found
[19/19] Parameter - task_struct->cred           : Found
Detected 43298 system events
Detected 19 of 19 kernel-specific parameters. Creating config file...

Tuning completed successfully!
```
Следом появятся результаты генерации файла конфигурации для модулей.
Мы увидим подтверждение того, что все помещенные в каталог файлы найдены (в данном комплекте их 2, *Natch* ищет все ELF-файлы и соответствующие им по названию map-файлы на всю глубину вложенности каталогов):
```text
Module config is completed

Your config file module.cfg for modules was created
ELF files found: 2
Map files found: 0
```

Финальным этапом будет предложено получить отладочную информацию для загруженных модулей, модулей, которые от них зависят и для ядра.
```text
Debug info part
Do you want to get debug info for system modules? (requires sudo) [Y/n] y
```
Для более информативных результатов следует согласиться. На данном этапе потребует пароль администратора. Будет произведено монтирование образа, поиск библиотек и скачивание отладочных символов.
```text
[sudo] password for user: 
Mounting img - OK                                                                                                                                                  
Searching Binary Files...                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2/2 100% 0:00:00
Searching Shared Libraries...                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2/2 100% 0:00:00
Searching Shared Libraries - OK                                                                                                                                    
vmlinux-5.10.0-17-amd64.dbg...                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 643.2/643.2 MB 100% 0:04:39
vmlinux-5.10.0-16-amd64.dbg...                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 640.3/640.3 MB 100% 0:04:47
[KERNEL] Download debugging information - OK                                                                                                                       
libpthread-2.31.so.dbg...                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB   100% 0:00:00
libc-2.31.so.dbg...                             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.5/3.5 MB   100% 0:00:00
libm-2.31.so.dbg...                             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB   100% 0:00:00
libdl-2.31.so.dbg...                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.2/44.2 kB 100% 0:00:00
[SHARED_LIB] Download debugging information - OK                                                                                                           
Umounting img - OK                                                                                                                                         

Module config statistics:                                                                                                                                   
In module config there were modules                          :  2                                                                                           
Binaries files in qcow2 found                                :  2                                                                                           
                                                                                                                                                           
Kernel statistics:                                                                                                                                         
Kernel symbols have been found                               :  OK                                                                                         
Added kernel symbols                                         :  2                                                                                          
Added debugging information for kernel                       :  2                                                                                          

Shared library Statistics:                                                                                                                                 
Added shared libraries                                       :  4                                                                                          
Added debugging information for shared libraries             :  4                                                                                          
ld-linux-* is always skipped and isn't counted in calculations                                                                                             

Your config file '/home/user/natch_quickstart/test1/module.cfg' for modules was updated        
```
Следом будет запущен процесс генерации базы данных символов, это займет некоторое время.
```text
Symbol info part
Reading symbols for loaded modules                                                                                                                                 
Created symbol database for /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-server                                                   
Created symbol database for /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-cli                                                                                                
Created symbol database for /home/user/natch_quickstart/test1/libs/src/vmlinux-5.10.0-16-amd64                                              
Created symbol database for /home/user/natch_quickstart/test1/libs/src/vmlinux-5.10.0-17-amd64                                              
Created symbol database for /home/user/natch_quickstart/test1/libs/src/libdl-2.31.so                                                        
Created symbol database for /home/user/natch_quickstart/test1/libs/src/libc-2.31.so                                                         
Created symbol database for /home/user/natch_quickstart/test1/libs/src/libm-2.31.so                                                         
Created symbol database for /home/user/natch_quickstart/test1/libs/src/libpthread-2.31.so                                                   

Your config file '/home/user/natch_quickstart/test1//module.cfg' for modules was updated 
```

Отлично, автоматизированная настройка и создание базовых скриптов завершены успешно, всё готово к записи сценария, о чём *Natch* сообщил нам дополнительно:
```text
Configuration file '/home/user/natch_quickstart/test1/natch.cfg' was created.

Settings completed! Now you can launch emulator and enjoy! :)

	Natch in record mode with help 'run_record.sh'
	Natch in replay mode with help 'run_replay.sh'
	Qemu without Natch with help 'run_qemu.sh'
```
Обратите внимание на файл настроек `natch.cfg` -- именно его мы будем редактировать для ручной настройки, а также на файл `natch.log` - в нём логируются основные результаты работы программ, входящих в комплект поставки *Natch*.

##### <a name="additional_settings"></a>1.3.1.3.2. Дополнительная ручная настройка

Отредактируем сгенерированный основной конфигурационный файл  *Natch* `natch.cfg` в соответствии с рекомендациями. _Не забываем, что необходимо раскомментировать также названия секций в квадратных скобках, а не только сами параметры._. Раскомментируем следующие секции (подробнее об их предназначении см. пункт [Основной конфигурационный файл](3_configs.md#main_config) документации):

Пометка файла в гостевой ОС (пригодится для выполнения тестового сценария №1):
```ini
[TaintFile]
list=sample.txt
```
Сбор покрытия по базовым блокам для просмотра покрытия в *IDA Pro*:
```ini
[Coverage]
file=coverage
taint=true
```

#### 1.3.1.4. Запись сценария работы

Запустим запись интересующего нас сценария выполнения виртуальной машины:
```bash
user@natch1:~/natch_quickstart/test1$ ./run_record.sh
```
**И получим ожидаемую ошибку - забыли про прелоад :)** Выполним запуск по правилам:
```bash
user@natch1:~/natch_quickstart/test1$ LD_LIBRARY_PATH=/home/user/natch_quickstart/libs/ ./run_record.sh
```
Введём логин и пароль учетной записи пользователя - `user/user` и запустим redis-сервер:

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/redis_rec.png><figcaption>_Запуск redis-сервера_</figcaption>
Тестово соединимся с ним из хостовой ОС чтобы убедиться, что система в комплексе работает как надо:
```text
user@natch1:~/natch_quickstart$ redis-cli -h localhost -p 15555

localhost:15555> SELECT 0
OK
localhost:15555> SET a b
OK
localhost:15555> get a
"b"
localhost:15555> exit
```
**Важный момент -- весь записываемый сценарий включает в себя в том числе этап загрузки ОС -- но помеченные данные появятся практически в самом конце, когда мы обратимся к redis-серверу.** Соответственно, для существенного сокращения времени на анализ (последующее выполнение ./run_replay.sh) нам желательно и рекомендуется сделать снэпшот в точке, максимально приближенной к точке начала поступления помеченных данных в системе. То есть сейчас, когда от порождения помеченных данных нас отделяет только повторное соединение с redis-сервером из хостовой ОС и повторная отправка в него уже знакомых нам команд.

Нажмем `Ctrl+Alt+G`, выйдем в монитор QEMU (bash-терминал хостовой ОС в котором мы запустили `run_record.sh`) и выполним команду генерации снэпшота (займёт несколько секунд, в зависимости от размера образа и производительности компьютера в целом) -- с названием `ready` - **команда savevm ready**:
```text
user@natch1:~/natch_quickstart/test1$ LD_LIBRARY_PATH=/home/user/natch_quickstart/libs/ ./run_record.sh

QEMU 6.2.0 monitor - type 'help' for more information
(qemu)
Natch v.2.2
(c) 2020-2023 ISP RAS

Reading Natch config file...
Network logging enabled
Config is loaded.
You can make system snapshots with the command: savevm <snapshot_name>
Network pcap log file: "/home/user/natch_quickstart/test1/record/network.pcap"
Network json log file: "/home/user/natch_quickstart/test1/record/network.json"

(qemu) savevm ready
(qemu)
```

После того, как снэпшот был сгенерирован, снова отправим какие-нибудь данные из хостовой ОС в redis-сервер. Теперь завершим QEMU, закрыв графическое окно эмулятора.

Поздравляю, сценарий работы с redis записан!

#### 1.3.1.5. Воспроизведение сценария и сбор данных для анализа

Для воспроизведения нужно запустить скрипт `run_replay.sh`. Скрипт принимает параметр с именем снэпшота, в нашем случае команда будет выглядеть так:
```text
user@natch1:~/natch_quickstart$ LD_LIBRARY_PATH=/home/user/natch_quickstart/libs/ ./test1/run_replay.sh ready
```
Если по какой-то причине вы не хотите использовать параметр, то скрипт можно запустить без него, но при этом надо будет внести изменения в сам скрипт. Перед воспроизведением сценария следует заменить значение параметра `SNAPSHOT` на имя нашего снэпшота, например, используя редактор `vim`. По умолчанию параметр содержит строку *record*. Заменяем:
```bash
SNAPSHOT="ready"
```
Начнём воспроизведение сценария, а точнее его фрагмента, который выполнялся после создария снэпшота. Это будет приблизительно на порядок медленнее, чем базовое выполнение, вы моментально оцените пользу создания снэпшота:
```bash
user@natch1:~/natch_quickstart$ LD_LIBRARY_PATH=/home/user/natch_quickstart/libs/ ./test1/run_replay.sh
```
Если в скрипт не был передан параметр и скрипт не был отредактирован - воспроизведение начнется с начала загрузки ОС.

Через какое-то время выполнение сценария завершится, графическое окно закроется, и вы увидете сообщение наподобие приведённого ниже, свидетельствующее о том, что интересующие нас модули гостевой ОС были распознаны успешно, и, следовательно, мы получим в отчетах корректную символьную информацию.
```text
Snapshot to load: ready
QEMU 6.2.0 monitor - type 'help' for more information
(qemu) 
Natch v.2.2
(c) 2020-2023 ISP RAS

Reading Natch config file...
Network logging enabled
Task graph enabled
Module graph enabled
Taint enabled
Config is loaded.
File events binary log file /home/user/natch_quickstart/test1/output/files_b.log created successfully
Module binary log file /home/user/natch_quickstart/test1/output/log_m_b.log created successfully
Modules: started reading binaries
Modules: finished with 8 of 8 binaries for analysis
thread_monitor: identification method is set to a complex developed at isp approach
Started thread monitoring
Tasks: config file is open.
Process events binary log file /home/user/natch_quickstart/test1/output/log_p_b.log created successfully
Network json log file: "/home/user/natch_quickstart/test1/output/tnetwork.json"
Binary log file /home/user/natch_quickstart/test1/output/log_t_b.log created successfully
Binary call_stack log file /home/user/natch_quickstart/test1/output/log_cs_b.log created successfully
Tainting file: sample.txt
Detected module /home/user/natch_quickstart/test1/libs/src/vmlinux-5.10.0-17-amd64 execution
Detected module /home/user/natch_quickstart/test1/libs/src/libc-2.31.so execution
Detected module /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-server execution
Detected module /home/user/natch_quickstart/test1/libs/src/libpthread-2.31.so execution
Detected module /home/user/natch_quickstart/test1/libs/src/libm-2.31.so execution

============ Statistics ============

Tainted files count           : 1
Tainted processes count       : 3
Tainted modules count         : 5
Tainted functions count       : 231
Tainted packets count         : 149
Tainted file reading count    : 0

Compressing data. Please wait..

output.tar.zst completed
```

Если работа системы завершилась успешно, и вы не словили, например, `core dumped` (о чём стоит немедленно сообщить в [трекер](https://gitlab.community.ispras.ru/trackers/natch/-/issues) с приложением всех артефактов), можно переходить к анализу собранных данных.

Помеченный файл в данном случае это тот самый `sample.txt`, который мы пометили в `natch.cfg`, но не использовали в этом сценарии.

#### 1.3.1.6. Анализ с использованием Snatch

*SNatch* -- это подсистема визуализации данных и статистик, собранных при воспроизведении сценария работы под управлением *Natch*. *SNatch* реализован в формате веб-службы с браузерным интерфейсом просмотра.

В комплект поставки *SNatch* входят скрипты `snatch_run.sh` и `snatch_stop.sh` для запуска и остановки *SNatch* соответственно. Скрипт `snatch_run.sh` запускает необходимые для работы службы, а также открывает браузер с интерфейсом. В терминал, из которого был запущен скрипт, будут приходить сообщения от сервера, однако, он свободен для использования, поэтому по окончании работы из него же можно запустить скрипт `snatch_stop.sh` для остановки служб. Запускать `snatch_stop.sh` следует всегда, в противном случае процессы останутся висеть в памяти вашего компьютера до перезагрузки.

Запустим *SNatch*:
```bash
user@natch1:~/natch_quickstart$ ./snatch/snatch_run.sh
```
Создадим проект на основе собранных данных (необходимо указывать tar.zst-архив, формируемый *Natch* в каталоге проекта по результатам выполнения `run_replay.sh`):

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/snatch/snatch_new_proj_modal.png"><figcaption>_Создание Snatch проекта_</figcaption>

Через некоторое время процесс загрузки архива завершится и станут доступны различные виды (**их число и возможности постоянно нарастают**) аналитик, такие как просмотр стека вызовов обработки помеченных данных:

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/call_graph.png"><figcaption>_Стек вызовов_</figcaption>

а также основное окно динамической визуализации распространения помеченных данных:

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/process_graph.png"><figcaption>_Граф процессов, работавших с помеченными данными_</figcaption>

Ярким цветом на каждом шаге *Timeline* выделяются сущности, взаимодействующие на данном конкретном шаге *Timeline*.

Полное руководство пользователя *SNatch* доступно в соответствующем разделе [Графический интерфейс для анализа SNatch](5_snatch.md#snatch). 

#### 1.3.1.7. Просмотр покрытия кода в IDA Pro

С помощью плагина к *IDA Pro* можно смотреть:

* какие функции в наибольшей степени взаимодействовали с помеченными данными
* покрытие по базовым блокам функций, взаимодействовавших с помеченными данными

Анализ покрытия по базовым блокам выполняется с использованием *IDA Pro* (протестировано на версиях 7.0, 7.2), общий алгоритм действий описан в пункте [Анализ покрытия бинарного кода](6_additional.md#functional_coverage). В ходе его выполнения может потребоваться ручное сопоставление модуля, для которого собрано покрытие, с модулем, загруженным в *IDA Pro*. Наиболее явная причина -- несовпадение имён исполняемого файла и файла, распознанного *Natch*. Пример такового несовпадения приведён на рисунке ниже:

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida1.png><figcaption>_Пример несовпадения имен модулей_</figcaption>

После выполнения маппинга в представленном выше меню в ручном режиме мы увидим приблизительно следующие сведения о покрытии:

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida2.png><figcaption>_Загруженный проект_</figcaption>

Также при выборе функции можно увидеть покрытие непосредственно по ассемблерным инструкциям (голубой цвет):

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/coverage.png><figcaption>_Пример покрытия по ассемблерным инструкциям_</figcaption>

Демонстрация покрытия по декомпилированному коду в настоящий момент не поддерживается.

#### 1.3.1.8. Просмотр сетевого трафика в Wireshark

Можно открыть и изучить записанный файл сетевого трафика `wireshark output/network.pcap`:

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/wireshark.png><figcaption>_Исследование трафика в Wireshark_</figcaption>

## <a name="faq"></a>1.4. FAQ

В этом разделе собраны наиболее часто встречающиеся проблемы при работе с инструментом *Natch*, раздел будет пополняться.

-----------------------------------------------------------------------------------

**Проблема**: настройка стенда происходит очень медленно

**Решение**: проверьте, используете ли вы опцию `enable-kvm` при запуске QEMU. Если вы хотите проверить включен ли kvm в уже запущенной виртуальной машине - введите в мониторе qemu команду `info kvm`

-----------------------------------------------------------------------------------

**Проблема**: *Natch* не запускается

При запуске появляется сообщение *"Sentinel LDK Protection System: Sentinel key not found"* или *"License not found. Application terminated"*

**Решение**: проверьте наличие лицензии.

При запуске появляется сообщение вида *"./qemu-system-x86_64: error while loading shared libraries: libSDL2-2.0.so.0: cannot open shared object file: No such file or directory"*

**Решение**: проверьте не забыли ли вы сделать preload библиотек, входящих в поставку

```bash
LD_LIBRARY_PATH=<path_to_libs>/libs/
```

-----------------------------------------------------------------------------------

**Проблема**: тюнинг работает слишком долго и ничего не происходит

**Решение**: подождите (чаще всего это и есть решение). Если ОС загрузилась, а настройка все еще идет, попробуйте поделать что-то, например, позапускать программы, чтобы спровоцировать возникновение системных вызовов. В случае если вы используете экзотическую ОС и тюнинг не может быть выполнен, он завершится по таймауту и вы получите сообщение о нештатном завершении настройки. В таком случае обратитесь к разработчику.

Так же тюнинг может быть выполнен не полностью, но если все обязательные параметры были обнаружены, скрипты сформируются и инструмент будет работать.

Для удобства пользователя внизу экрана отображается счетчик событий, по которому можно ориентироваться не нужна ли системе помощь извне.

-----------------------------------------------------------------------------------

**Проблема**: поверхность атаки пустая

**Решение**: чаще всего такая ситуация возникает, если источник помеченных данных был указан неверно или если работа с помеченными данными происходила до того как состояние машины было сохранено. Проверьте:

- указали ли вы нужные порты и/или файлы в конфигурационном файле `natch.cfg`
- выполнили ли команду `savevm` до того как поработали с помеченными данными

Если все верно, а поверхность атаки пустая, возможно это баг :) Обратитесь к разработчику, пожалуйста.

-----------------------------------------------------------------------------------

**Проблема**: появилась необходимость перегенерировать `task.cfg`. Например, у вас есть проект и вы не хотите его пересоздавать, а версия конфигурационного файла `task.cfg` изменилась и *Natch* не запускается.

**Решение**: в таком случае вы можете удалить старый файл и запустить `run_replay.sh`, в результате чего будет произведена попытка выполнить тюнинг. Эта ситуация может закончиться успехом, а может и нет, если журнал слишком короткий и все параметры не успеют обнаружиться. Решений может быть несколько:

- запустите `run_replay.sh` с параметром `record`. Таким образом ОС будет загружаться с начала и шансов что все пройдет удачно больше.

Более надежные способы:

- допишите в скрипт `run_qemu.sh` строку `-plugin natch` и запустите его. Дождитесь выполнения тюнинга.
- так же можно запустить тюнинг напрямую: в скрипт `run_qemu.sh` допишите строку `-plugin tuning_introspection`. Дождитесь выполнения тюнинга.

-----------------------------------------------------------------------------------

**Проблема**: забыли название снэпшота, который указали при записи сценария.

**Решение**: вся информация о созданных снэпшотах хранится в оверлее для образа (*image_name.diff*). Получить ее можно с помощью утилиты `qemu-img`, входящей в поставку бинарных файлов инструмента. Чтобы получить список сохраненных снэпшотов нужно выполнить команду:

```bash
qemu-img snapshot -l image_name.diff
```

-----------------------------------------------------------------------------------

**Проблема**: не установился *SNatch*

**Решение**: в процессе установки могут возникать ошибки, связанные c wheel, но если в целом скрипт завершился успешно, то ничего страшного. Если не завершился, проверьте, что в названиях директорий, в которых вы находитесь, нет пробелов. Если есть, устраните проблему и перезапустите `snatch_setup.sh`.

-----------------------------------------------------------------------------------

**Проблема**: шкала прогресса "Processing surface" пропала до завершения обработки архива (например, после обновления страницы).

**Решение**: процесс обработки архива продолжается в фоне. При его завершении в консоли появится сообщение `Processing ___ is done!`

-----------------------------------------------------------------------------------

**Проблема**: Flame graph долго строится/завис.

**Решение**: процесс построения флейм графа может занять очень длительное время, более часа.

При построении флейм графа выводится прогресс. Если же ждать все равно больше не хочется, процесс построения можно прервать с помощью кнопки `Generate`, которая краснеет при наведении мыши.
