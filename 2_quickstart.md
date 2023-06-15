<div style="page-break-before:always;">
</div>

# <a name="begin"></a>2. Начало работы с Natch

*Natch* - это инструмент для определения поверхности атаки, основанный на полносистемном эмуляторе QEMU.
С помощью этого раздела можно освоить основные принципы использования системы определения поверхности атаки [Natch](https://www.ispras.ru/technologies/natch/) (разработчик - [ИСП РАН](https://www.ispras.ru/)):

* создание виртуализованной среды выполнения объекта оценки (далее - ОО) в формате [QEMU](https://wiki.qemu.org/Main_Page)
* запуск виртуализированной среды под контролем *Natch*
* анализ информации о движении помеченных данных в контролируемой виртуализованной среде

## <a name="complect"></a>2.1. Комплект поставки Natch

С версии *Natch 2.3* инструмент распространяется в виде пакета для следующих операционных систем:

* Ubuntu20
* Ubuntu22
* Debian11
* Alt10

В пакете представлен защищенный бинарный дистрибутив, требующий наличия аппаратного ключа (персональный "черный" ключ, сетевой "красный" ключ или иные версии ключа) с лицензией c идентификатором "6".

Дистрибутив доступен по ссылке [Natch v.2.3](https://nextcloud.ispras.ru/index.php/s/natch_v.2.3)

Предыдущие релизы можно найти [здесь](9_appendix.md#app_releases).

Установка *Natch* описана в разделе [Установка Natch](3_setup.md#setup_natch).

## <a name="create-qemu-env"></a>2.2. Подготовка виртуализованной среды в формате QEMU

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

Перед установкой KVM в гостевой ОС нужно настроить среду виртуализации VirtualBox в хостовой ОС:

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

____
**ВНИМАНИЕ!**

На момент 08.05.2023 по-прежнему наблюдается проблема с тем, что VirtualBox версии 7+ (7.0.8) не позволяет корректно запускать qemu в режиме поддержки kvm. Используйте VirtualBox версии 6. Наиболее актуальный тикет на данную ошибку заведён [здесь](https://www.virtualbox.org/ticket/21552), пока что без ответа.


### 2.2.1. Подготовка хостовой системы

Рекомендации по подготовке хостовой системы приведены [здесь](9_appendix.md#app_requirements) (*для получения доступа к репозиторию сообщества ознакомьтесь с информацией в описании телеграм-канала [Орг. вопросы::Доверенная разработка](https://t.me/sdl_community)*).

Подготовим Linux-based рабочую станцию (далее - хост), поддерживающую графический режим выполнения. QEMU демонстрирует вывод эмулируемой среды выполнения в отдельном графическом окне, следовательно нам необходим графический режим. Хост может быть реализован в формате виртуальной машины. В примерах ниже описаны действия пользователя, работающего в виртуальной машине VirtualBox (4 ядра, 8 ГБ ОЗУ)
с установленной ОС [Ubuntu20.04](ttps://releases.ubuntu.com/20.04/ubuntu-20.04.5-desktop-amd64.iso) (desktop-конфигурация, обновить пакеты при установке).

Установим требуемое системное ПО, в т.ч. QEMU:
```bash
sudo apt install -y curl qemu-system gcc g++
```
*Подсказка: данная инсталляция требуется не для запуска Natch, но для создания образов ВМ на произвольном хосте. Natch содержит в своём составе требуемую для работы версию QEMU, поэтому если вы планируете создавать образ ВМ на том же хосте, на котором уже установили Natch, отдельно QEMU можно не ставить.*

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
Создадим скрипт запуска нашей ВМ `run.sh`. Мы сохраняем его в виде отдельного файла, потому что позже скрипт потребуется редактировать. Для тех, кто сталкивается с синтаксисом QEMU впервые, рекомендуется ознакомиться с основными командами, описанными в официальной [документации QEMU](https://www.qemu.org/docs/master/system/invocation.html). Важным для ускорения работы виртуализированной среды QEMU, за счет аппаратной [виртуализации](#create-qemu-env), является установка ключей `-enable-kvm` и `-cpu host,nx`.
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
Наш образ среды функционирования готов к работе, в частности, к установке в него пресобранного **с символами** прототипа объекта оценки.

### <a name="build_prototype"></a>2.2.2. Сборка прототипа объекта оценки

Рекомендации по подготовке исполняемого кода приведены [здесь](9_appendix.md#app_requirements).

В общем случае к анализируемому исполняемому коду выставляется два требования:

* должна быть представлена отладочная информация в формате символов в составе исполняемых файлов, отдельно прилагаемых символов или map-файлов. Предоставление символов непосредственно в составе исполняемых файлов является основной и рекомендуемой стратегией -- начиная с версии *Natch v.1.3* инструмент умеет самостоятельно доставать информацию об отладочных символах из исполняемых файлов, собранных *как минимум* компиляторами *gcc* и *clang* с сохранением отладочной информации (ключ компилятора `-g`, также рекомендуется сборка без оптимизаций в режиме `-O0`). Начиная с версии *Natch v.2.1* для стандартных пакетов из наиболее популярных сборок операционных систем символы подгружаются автоматически;
* **рекомендуется выполнять сборку подлежащего анализу исполняемого кода в виртуализированной среде (виртульная машина QEMU).** В случае, если сборка и анализ будут выполняться в различных средах функционирования (например, сборка осуществляется на отдельном сборочном сервере), требуется обеспечить совместимость версий разделяемых динамических библиотек, в первую очередь *glibc*, из состава среды функционирования. На вашем хосте и в виртуализированной среде комплекты библиотек могут различаться.

В качестве прототипа объекта оценки рассмотрим популярную программу *wget*, сборку которой осуществим в хостовой системе (условная "сборочница") с последующим помещением собранного дистрибутива в виртуализированную гостевую среду *lubuntu*. Как было сказано выше, в тестовых сценариях **рекомендуется выполнять сборку подлежащего анализу исполняемого кода в виртуализированной среде (виртульная машина QEMU).** Сборка в отдельной "сборочнице" не обязательна.

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
**Важное замечание: следующие два подраздела (*Генерация map-файлов средствами компилятора* и *Генерация map-файлов сторонними инструментами*) представлены в качестве пособия для специфических случаев, когда возможность сборки исполняемого файла из исходных текстов с произвольными параметрами отсутствует, либо явно требуется получение отдельных [map-файлов](https://stackoverflow.com/questions/22199844/what-are-gcc-linker-map-files-used-for), в частности для случаев анализа ядра Linux. Генерация map-файлов не нужна для обычных тестовых сценариев анализа usermode-приложений.**

### <a name="map_gen"></a>2.2.3. Генерация map-файлов средствами компилятора

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

### 2.2.4. Генерация map-файлов сторонними инструментами

Получение map-файлов для исполняемого файла возможно с помощью сторонних инструментов. Это может быть актуально в тех случаях, когда сборочный конвейер недоступен,
либо получение от сборочного конвейера map-файлов в поддерживаемом *Natch* формате невозможно (например, использование специфического компилятора/компоновщика). Сгенерируем map-файлы с использованием бесплатной версии дизассемблера [IDA Pro](https://hex-rays.com/ida-free/). Для этого необходимо скачать установочный комплект по указанной ссылке и возможно доустановить библиотеки Qt `apt install -y qt5-default`.

После установки IDA необходимо запустить её, открыть интересующий нас исполняемый файл (в нашем случае это `wget`).

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida_map1.png"><figcaption>_Загрузка бинарного файла в IDA Pro_</figcaption>

Пройти процедуру генерации map-файла.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida_map2.png"><figcaption>_Генерация map-файла_</figcaption>

Обязательным пунктом является только *Segmentation information*, остальные по желанию (хотя, например, локальные имена дизассемблера вряд ли сделают вывод понятнее).

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida_map3.png"><figcaption>_Выбор опций map-файла_</figcaption>

После чего убедиться, что map-файл появился в файловой системе:

```bash
ll src | grep .map
-rw-rw-r--  1 user user  564686 фев  3 16:11 wget.map
```

### 2.2.5. Перенос прототипа объекта оценки из образа ВМ на хост (или с хоста в образ ВМ)

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

### 2.2.6. Тестирование виртуализированной среды функционирования ОО

Запускаем ВМ скриптом `run.sh` с отключенным ранее cdrom, дожидаемся загрузки ОС ВМ, авторизуемся в ОС, пробуем выполнить обращение к произвольному сетевому ресурсу с помощью собранной нами версии *wget*:
```bash
cd wget-1.21.2/src && sudo ./wget ispras.ru
```
В результате вы должны увидеть приблизительно следующую картину в графическом окне QEMU, свидетельствующую о том, что ОО корректно выполняется в среде функционирования и сетевая доступность для ВМ обеспечена:

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/check.png"><figcaption>_Пример подготовленного ОО в QEMU_</figcaption>


## 2.3. Обучающие примеры

### <a name="test_complect"></a>2.3.1. Анализ образа системы, содержащего тестовые комплекты пресобранных исполняемых файлов

**Все нижеописанное описано и проделано на примере дистрибутива, работающего под Ubuntu 20.**

Для этого примера потребуется:

- рабочая станция под управлением ОС Linux (традиционно Ubuntu 20.04). Отдельная установка пакета **qemu-system** не требуется, нужная версия входит в дистрибутив *Natch*;
- актуальный [дистрибутив](#complect) *Natch*;
- подготовленный разработчиком [тестовый набор](https://nextcloud.ispras.ru/index.php/s/testing_2.0), включающий в себя минимизированный образ гостевой операционной системы Debian (размер qcow2-образа около 1 ГБ), а также два комплекта программ (Sample1_bins и Sample2_bins), собранных с отладочными символами.

*Сценарий использования тестового комплекта Sample1_bins*

Программа *test_sample* читает файл *sample.txt*, в первой строке которого записан адрес Google. Он передает эту строку в качестве параметра программе *test_sample_2*. Программа *test_sample_2* "курлит гугл" в файл *curl.txt*.
В образе исполняемые файлы находятся в папке `/home/user/Sample1`, там же расположены и исходные коды.

Запуск тестового сценария: 
```
cd Sample1
./test_sample
```

*Сценарий использования тестового комплекта Sample2_bins*

Процесс сервера redis-server следует запустить командой `redis-server --port 5555 --protected-mode no`, после чего соединиться с ним из хостовой системы клиентской утилитой `redis-cli -h localhost -p 15555` (её можно поставить например так `sudo apt install redis-tools`) и выполнить какие-нибудь действия, например `SET b VeryBigValue`. В образе redis установлен в систему.


#### 2.3.1.1. Получение образа и дистрибутива

Команда для скачивания тестового комплекта с помощью *curl* выглядит так `curl -o materials.zip 'https://nextcloud.ispras.ru/index.php/s/testing_2.0/download'`. 

Состав комплекта поставки *Natch* в облачном хранилище включает deb-пакет Natch, SNatch и докуменатацию.

После скачивания дистрибутива и обучающих материалов их следует распаковать.

В папке `Natch_testing_materials` находится образ гоствой ОС. Учётные записи пользователей: `user/user` и `root/root`.


#### <a name="setup_natchSnatch"></a>2.3.1.2. Установка Natch и Snatch

Установка *Natch* описана в разделе [Установка Natch](3_setup.md#setup_natch).

Для устaновки *SNatch* следует запустить скрипт *snatch_setup.sh*, который находится в папке snatch, и дождаться его успешного выполнения:
```bash
user@natch1:~/natch_quickstart/snatch$ ./snatch_setup.sh
```
При выполнении скрипт запросит пароль администратора.


#### <a name="config_natch_test_image"></a>2.3.1.3. Настройка Natch для работы с тестовым образом ОС

Процесс настройки состоит из двух этапов -- автоматизированного (обязательный) и ручного (дополнительный, при необходимости тонкой настройки). Предназначение [файлов конфигурации и их параметров](4_configs.md#natch_config_main) **описано в документации**):

##### 2.3.1.3.1. Автоматизированная настройка

Автоматизированная настройка выполняется интерактивным скриптом `natch_run.py`. Далее приведем вопросы скрипта и примеры ответов. Запустим скрипт:
```text
user@natch1:~/natch_quickstart$ ./natch_ubuntu20/bin/natch_scripts/natch_run.py Natch_testing_materials/test_image_debian.qcow2
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
На этом этапе скрипт проверит доступность утилиты natch-qemu-img, которая в адльнейшем нужна для создания оверлея для образа. В случае успеха увидим:
```text
Checking natch-qemu-img utility...
Utility natch-qemu-img is ok
```
Если что-то пошло не так, скрипт прекратит работу.

Если наш сценарий предполагает передачу помеченных данных по сети (далее мы рассматриваем в качестве основного как раз сценарий №2 -- взаимодействие с redis-сервером, слушающим tcp-порт 5555), нам потребуется взаимодействовать с сетевыми сервисами гостевой ОС с помощью программ, запущенных на хосте. Указываем *Natch*, какой порт мы хотим опубликовать в гостевую ОС:
<!---
**перехват пакетов, отправитель и получатель которых "находятся" внутри гостевой ОС (localhost - localhost), в настоящий момент не поддерживается**
-->

```text
Network option
Do you want to use ports forwarding? [Y/n] y
Do you want to taint source ports too? [Y/n] n
Write the ports you want separated by commas (e.g. 7777, 8888, etc) 5555
Your port for connecting outside: 15555
```
Далее нам нужно указать пути к каталогам на хосте, содержащим копии бинарных файлов, размещенных в гостевой ОС -- это как раз те самые файлы (собранные с символами, или с отдельными map-файлами), которые мы получили в ходе выполнения пункта [Сборка прототипа объекта оценки](#build_prototype). 
Этот процесс будет выполняться параллельно, результаты увидим позже.

Следующая стадия: конфигурирование технических параметров *Natch*, требующая тестового запуска виртуальной машины. В ходе данного запуска выполняется получение информации о параметрах ядра и заполнение ini-файла. Вы можете отказаться от данного шага, в случае если этот файл уже был ранее создан для данного образа гостевой виртуальной машины -- тогда вам потребуется указать к нему путь, однако, в большинстве случаев вы вероятно будете создавать эти файлы с нуля:

```text
Generate config file task.cfg? [Y/n] y (или просто нажмите Enter)

Now will be launch tuning. Don't close emulator
Three...
Two..
One.
Go!
Natch monitor - type 'help' for more information
Natch v.2.3
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

Финальным этапом будет предложено получить отладочную информацию для загруженных модулей, модулей, которые от них зависят, для ядра и установленных интерпретаторов.
```text
Debug info part
Do you want to get debug info for system modules? (requires sudo) [Y/n] y
```
Для более информативных результатов следует согласиться. На данном этапе потребуется пароль администратора. Будет произведено монтирование образа, поиск библиотек и скачивание отладочных символов.
```text
[sudo] password for user:
Mounting img - OK
Reading module config - OK

Searching Binary Files...                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2/2 100% 0:00:00
python3.9.dbg...                                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.2/8.2 MB 100% 0:00:01
[PYTHON] Download debugging information - OK

[PYTHON_TIED] Download debugging information - OK
vmlinux-5.10.0-17-amd64.dbg...                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 643.2/643.2 MB 100% 0:04:39
[KERNEL] Download debugging information - OK

[KERNEL_TIED] Download debugging information - OK
Searching Shared Libraries...                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2/2 100% 0:00:00
Searching Shared Libraries - OK
libz.so.1.2.11.dbg...                           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 109.8/109.8 kB 100% 0:00:00
libexpat.so.1.6.12.dbg...                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 167.0/167.0 kB 100% 0:00:00
libdl-2.31.so.dbg...                            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.2/44.2 kB   100% 0:00:00
libpthread-2.31.so.dbg...                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB     100% 0:00:00
libc-2.31.so.dbg...                             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.5/3.5 MB     100% 0:00:00
libm-2.31.so.dbg...                             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB     100% 0:00:00
libutil-2.31.so.dbg...                          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.1/11.0 kB   100% 0:00:00
[SHARED_LIB] Download debugging information - OK

[SHARED_LIB_TIED] Download debugging information - OK
Umounting img - OK


Module config statistics:
In module config there were modules                          : 2
Binaries files in qcow2 found                                : 2

Python interpreters statistics:
Python interpreters have been found                          : OK
Added python interpreters                                    : 1
Added debugging information for python interpreters          : 1

Kernel statistics:
Kernel symbols have been found                               : OK
Added kernel symbols                                         : 1
Added debugging information for kernel                       : 1

Shared library Statistics:
Added shared libraries                                       : 7
Added debugging information for shared libraries             : 7
Added debugging information for tied files                   : 0
ld-linux-* is always skipped and isn't counted in calculations

Your config file '/home/user/natch_quickstart/test1/module.cfg' for modules was updated
```
Следом будет запущен процесс генерации базы данных символов, это займет некоторое время.
```text
Symbol info part
Reading symbols for loaded modules

Created symbol database for /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-server
Created symbol database for /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-cli
Created symbol database for /home/user/natch_quickstart/test1/libs/src/f902f8a561c3abdb9c8d8c859d4243bd8c3f928f/python3.9
Created symbol database for /home/user/natch_quickstart/test1/libs/src/cc89a8838df3652561ab61598035775fa95f8917/vmlinux-5.10.0-17-amd64
Created symbol database for /home/user/natch_quickstart/test1/libs/src/5018237bbf012b4094027fd0b96fc22a24496ea4/libpthread-2.31.so
Created symbol database for /home/user/natch_quickstart/test1/libs/src/e9d2c06479b13dd3cfa78d714d11dccf6fcbee51/libm-2.31.so
Created symbol database for /home/user/natch_quickstart/test1/libs/src/bc22349819818055008048f8001e3910ffc16dc7/libexpat.so.1.6.12
Created symbol database for /home/user/natch_quickstart/test1/libs/src/a89a9c8e4a828f47e68e2d1dafca4aae087d061d/libz.so.1.2.11
Created symbol database for /home/user/natch_quickstart/test1/libs/src/5675f6cc697d1e1fb135c65cbb0f917550fe85ac/libutil-2.31.so
Created symbol database for /home/user/natch_quickstart/test1/libs/src/118b90161526d181807818c459baee841993795b/libdl-2.31.so
Created symbol database for /home/user/natch_quickstart/test1/libs/src/2e5abcee94f3bcbed7bba094f341070a2585a2ba/libc-2.31.so

Your config file '/home/user/natch_quickstart/test1//module.cfg' for modules was updated
```

Отлично, автоматизированная настройка и создание базовых скриптов завершены успешно, всё готово к записи сценария, о чём *Natch* сообщил нам дополнительно:
```text
Configuration file natch.cfg was created.
You can edit it before using Natch.

Settings completed! Now you can launch emulator and enjoy! :)

	Natch in record mode: 'run_record.sh'
	Natch in replay mode: 'run_replay.sh'
	Qemu without Natch: 'run_qemu.sh'
```
В папке проекта появится файл настроек `natch.cfg` -- его мы будем редактировать для ручной настройки, кроме того после записи сценария появится еще один файл настроек `taint.cfg`, который тоже надо будет редактировать. Также в папке проекта находится файл `natch.log` -- в нём логируются основные результаты работы программ, входящих в комплект поставки *Natch*.

##### <a name="additional_settings"></a>2.3.1.3.2. Дополнительная ручная настройка

Отредактируем основной конфигурационный файл *Natch* `natch.cfg` в соответствии с рекомендациями. _Не забываем, что необходимо раскомментировать также названия секций в квадратных скобках, а не только сами параметры._. Раскомментируем следующую секцию (подробнее об предназначении секций см. пункт [Основной конфигурационный файл](4_configs.md#main_config) документации):

Сбор покрытия по базовым блокам для просмотра покрытия в *IDA Pro*:
```ini
[Coverage]
file=coverage
taint=true
```

#### <a name="record_scenario"></a>2.3.1.4. Запись сценария работы

Запустим запись интересующего нас сценария выполнения виртуальной машины:
```bash
user@natch1:~/natch_quickstart/test1$ ./run_record.sh
```
Скрипт запросит название сценария, введем `sample_redis`. Далее запустится эмулятор.

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
**Важный момент -- весь записываемый сценарий включает в себя в том числе этап загрузки ОС -- но помеченные данные появятся практически в самом конце, когда мы обратимся к redis-серверу.** Соответственно, для существенного сокращения времени на анализ (последующее выполнение ./run_replay.sh) нам желательно и рекомендуется сделать снапшот в точке, максимально приближенной к точке начала поступления помеченных данных в системе. То есть сейчас, когда от порождения помеченных данных нас отделяет только повторное соединение с redis-сервером из хостовой ОС и повторная отправка в него уже знакомых нам команд.

Нажмем `Ctrl+Alt+G`, выйдем в монитор QEMU (bash-терминал хостовой ОС в котором мы запустили `run_record.sh`) и выполним команду генерации снапшота:
```
savevm <name>
```
Используем имя `ready`. Сохранение состояния займёт несколько секунд, в зависимости от размера образа и производительности компьютера в целом.
```text
user@natch1:~/natch_quickstart/test1$ ./run_record.sh

Natch monitor - type 'help' for more information
(natch)
Natch v.2.3
(c) 2020-2023 ISP RAS

Reading Natch config file...
Network logging enabled
Config is loaded.
You can make system snapshots with the command: savevm <snapshot_name>
Network pcap log file: "/home/user/natch_quickstart/test1/record/network.pcap"
Network json log file: "/home/user/natch_quickstart/test1/record/network.json"

(natch) savevm ready
(natch)
```

После того как снапшот был сгенерирован, снова отправим какие-нибудь данные из хостовой ОС в redis-сервер. Теперь завершим работу QEMU, закрыв графическое окно эмулятора.

Сценарий работы с redis записан.

#### <a name="replay_scenario"></a>2.3.1.5. Воспроизведение сценария и сбор данных для анализа

Для воспроизведения нужно запустить скрипт `run_replay.sh`.
```text
user@natch1:~/natch_quickstart/test1/$ ./run_replay.sh
```
Скрипт может принимать два параметра: название сценария и имя снапшота. В нашем случае команда могла бы выглядеть так:
```text
user@natch1:~/natch_quickstar/test1/t$ ./run_replay.sh sample_redis ready
```
Если используются параметры, то они оба являются обязательными. Однако, запускать скрипт можно без параметров, он сам или загрузит нужный сценарий (если он единственный) или предложит выбрать из списка существующих, точно
так же произойдет с выбором снапшота.

Начнём воспроизведение сценария, а точнее его фрагмента, который выполнялся после создания снапшота. Это будет несколько медленнее, чем базовое выполнение.

Через какое-то время выполнение сценария завершится, графическое окно закроется, и вы увидите сообщение наподобие приведённого ниже, свидетельствующее о том, что интересующие нас модули гостевой ОС были распознаны успешно, и, следовательно, мы получим в отчетах корректную символьную информацию.
```text
Snapshot to load: ready
Natch monitor - type 'help' for more information
(natch) 
Natch v.2.3
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
Modules: finished with 13 of 13 binaries for analysis
thread_monitor: identification method is set to a complex developed at isp approach
Started thread monitoring
Tasks: config file is open.
Process events binary log file /home/user/natch_quickstart/test1/output/log_p_b.log created successfully
Network json log file: "/home/user/natch_quickstart/test1/output/tnetwork.json"
Binary log file /home/user/natch_quickstart/test1/output/log_t_b.log created successfully
Binary call_stack log file /home/user/natch_quickstart/test1/output/log_cs_b.log created successfully
Detected module /home/user/natch_quickstart/test1/libs/src/vmlinux-5.10.0-17-amd64 execution
Detected module /home/user/natch_quickstart/test1/libs/src/libc-2.31.so execution
Detected module /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-server execution
Detected module /home/user/natch_quickstart/test1/libs/src/libpthread-2.31.so execution
Detected module /home/user/natch_quickstart/test1/libs/src/libm-2.31.so execution

=========== Statistics ===========

Tainted files             : 0
Tainted packets           : 151
Tainted processes         : 3
Tainted modules           : 3
Tainted file reads        : 0
Tainted memory accesses   : 21838

Compressing data. Please wait..

output.tar.zst completed
```

Если работа системы завершилась успешно, и вы не словили, например, `core dumped` (о чём стоит немедленно сообщить в [трекер](https://gitlab.ispras.ru/natch/natch-support/-/issues) с приложением всех артефактов), можно переходить к анализу собранных данных.

В этом сценарии нам не пришлось изменять конфигурационный файл сценария, потому что порт был установлен при настройке проекта. Однако, это может потребоваться. Конфигурационный файл `taint.cfg` находится в папке
со сценарием и содержит всего две секции: **Ports** и **TaintFile**.

Если бы мы выполняли первый тестовый сценарий (бинарный файл test_samle), нам следовало бы пометить файл *sample.txt* следующим образом:

```ini
[TaintFile]
list=sample.txt
```

#### <a name="snatch_analysis"></a>2.3.1.6. Анализ с использованием Snatch

*SNatch* -- это подсистема визуализации данных и статистик, собранных при воспроизведении сценария работы под управлением *Natch*. *SNatch* реализован в формате веб-службы с браузерным интерфейсом просмотра.

В комплект поставки *SNatch* входят скрипты `snatch_start.sh` и `snatch_stop.sh` для запуска и остановки *SNatch* соответственно. Скрипт `snatch_start.sh` запускает необходимые для работы службы, а также открывает браузер с интерфейсом. В терминал, из которого был запущен скрипт, будут приходить сообщения от сервера, однако, он свободен для использования, поэтому по окончании работы из него же можно запустить скрипт `snatch_stop.sh` для остановки служб. Запускать `snatch_stop.sh` следует всегда, в противном случае процессы останутся висеть в памяти вашего компьютера до перезагрузки.

Полное руководство пользователя *SNatch* доступно в соответствующем разделе [Анализ поверхности атаки с помощью SNatch](6_snatch.md#snatch). 

Запустим *SNatch*:
```bash
user@natch1:~/natch_quickstart$ ./snatch/snatch_start.sh
```
Создадим проект на основе собранных данных (необходимо указывать tar.zst-архив, формируемый *Natch* в каталоге проекта по результатам выполнения `run_replay.sh`):

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/snatch/snatch_new_proj_modal.png"><figcaption>_Создание Snatch проекта_</figcaption>

Через некоторое время процесс загрузки архива завершится и станут доступны различные виды аналитик (**их число и возможности постоянно нарастают**).

После загрузки архива *SNatch* выглядит следующим образом:

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_main.png"><figcaption>_Интерфейс *SNatch*_</figcaption>

Главное окно представляет динамическую визуализацию распространения помеченных данных. Ярким цветом на каждом шаге *Timeline* выделяются сущности, взаимодействующие на данном конкретном шаге *Timeline*.

Дважды кликнув по процессу *redis-server* мы перейдем на граф модулей, связанных с выбранным процессом.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_module_graph.png"><figcaption>_Модуль граф для redis-server_</figcaption>

Для просмотра таких аналитик, как граф вызовов и флейм граф, следует их предварительно сгенерировать, нажав на соответствующие кнопки *Generate*.

Фрагмент графа вызовов для примера с redis-server представлен на рисунке ниже. Голубым цветом выделены функции, работавшие с помеченными данными.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_callstack.png"><figcaption>_Граф вызовов_</figcaption>

Подробнее о возможностях *SNatch* написано в [соответствующем](6_snatch.md#snatch) разделе.

#### 2.3.1.7. Просмотр покрытия кода в IDA Pro

С помощью плагина к *IDA Pro* можно смотреть:

* какие функции в наибольшей степени взаимодействовали с помеченными данными
* покрытие по базовым блокам функций, взаимодействовавших с помеченными данными

Анализ покрытия по базовым блокам выполняется с использованием *IDA Pro* (протестировано на версиях 7.0, 7.2), общий алгоритм действий описан в пункте [Анализ покрытия бинарного кода](7_additional.md#functional_coverage). В ходе его выполнения может потребоваться ручное сопоставление модуля, для которого собрано покрытие, с модулем, загруженным в *IDA Pro*. Наиболее явная причина -- несовпадение имён исполняемого файла и файла, распознанного *Natch*. Пример такового несовпадения приведён на рисунке ниже:

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida1.png><figcaption>_Пример несовпадения имен модулей_</figcaption>

После выполнения маппинга в представленном выше меню в ручном режиме мы увидим приблизительно следующие сведения о покрытии:

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/ida2.png><figcaption>_Загруженный проект_</figcaption>

Также при выборе функции можно увидеть покрытие непосредственно по ассемблерным инструкциям (голубой цвет):

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/coverage.png><figcaption>_Пример покрытия по ассемблерным инструкциям_</figcaption>

Демонстрация покрытия по декомпилированному коду в настоящий момент не поддерживается.

#### 2.3.1.8. Просмотр сетевого трафика в Wireshark

Анализировать трафик в Wireshark можно прямо из интерфейса *SNatch* с помощью раздела *Traffic*. Здесь можно увидеть интерфейсы и сессии, клик по каждой записи будет открывать Wireshark с соответствующими данными.

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_traffic.png><figcaption>_Информация о трафике_</figcaption>

Так же можно открывать весь .pcap файл с помощью соответствующей кнопки.

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/wireshark.png><figcaption>_Исследование трафика в Wireshark_</figcaption>


## <a name="faq"></a>2.4. FAQ

В этом разделе собраны наиболее часто встречающиеся проблемы при работе с инструментом *Natch*, раздел будет пополняться.

-----------------------------------------------------------------------------------

**Проблема**: настройка стенда происходит очень медленно

**Решение**: проверьте, используете ли вы опцию `enable-kvm` при запуске QEMU. Если вы хотите проверить включен ли kvm в уже запущенной виртуальной машине - введите в мониторе QEMU команду `info kvm`

-----------------------------------------------------------------------------------

**Проблема**: *Natch* не запускается

При запуске появляется сообщение *"Sentinel LDK Protection System: Sentinel key not found"* или *"License not found. Application terminated"*

**Решение**: проверьте наличие лицензии.

-----------------------------------------------------------------------------------

**Проблема**: тюнинг работает слишком долго и ничего не происходит

**Решение**: подождите (чаще всего это и есть решение). Если ОС загрузилась, а настройка все еще идет, попробуйте поделать что-то, например, позапускать программы, чтобы спровоцировать возникновение системных вызовов. В случае если вы используете экзотическую ОС и тюнинг не может быть выполнен, он завершится по таймауту и вы получите сообщение о нештатном завершении настройки. В таком случае обратитесь к разработчику.

Так же тюнинг может быть выполнен не полностью, но если все обязательные параметры были обнаружены, скрипты сформируются и инструмент будет работать.

Для удобства пользователя внизу экрана отображается счетчик событий, по которому можно ориентироваться не нужна ли системе помощь извне.

-----------------------------------------------------------------------------------

**Проблема**: статистика помеченных данных показывает нули

**Решение**: чаще всего такая ситуация возникает, если источник помеченных данных был указан неверно или если работа с помеченными данными происходила до того как состояние машины было сохранено. Проверьте:

- указали ли вы нужные порты и/или файлы в конфигурационном файле `taint.cfg`
- выполнили ли команду `savevm` до того как поработали с помеченными данными

Если все верно, а статистика нулевая, возможно это баг :) Обратитесь к разработчику, пожалуйста.

-----------------------------------------------------------------------------------

**Проблема**: появилась необходимость перегенерировать `task.cfg`. Например, у вас есть проект и вы не хотите его пересоздавать, а версия конфигурационного файла `task.cfg` изменилась и *Natch* не запускается

**Решение**: в таком случае вы можете удалить старый файл и запустить `run_replay.sh`, в результате чего будет произведена попытка выполнить тюнинг. Эта ситуация может закончиться успехом, а может и нет, если журнал слишком короткий и все параметры не успеют обнаружиться. Решений может быть несколько:

- запустите `run_replay.sh` с параметрами `<scenario_name> init`. Таким образом ОС будет загружаться с начала и шансов что все пройдет удачно больше.

Более надежные способы:

- допишите в скрипт `run_qemu.sh` строку `-plugin natch` и запустите его. Дождитесь выполнения тюнинга.
- так же можно запустить тюнинг напрямую: в скрипт `run_qemu.sh` допишите строку `-plugin tuning_introspection`. Дождитесь выполнения тюнинга.

-----------------------------------------------------------------------------------

**Проблема**: забыли название снапшота, который указали при записи сценария

**Решение**: вся информация о созданных снапшотах хранится в оверлее для образа (*image_name.diff*). Получить ее можно с помощью утилиты `natch-qemu-img`, входящей в поставку бинарных файлов инструмента. Чтобы получить список сохраненных снапшотов, нужно выполнить команду:

```bash
natch-qemu-img snapshot -l image_name.diff
```

-----------------------------------------------------------------------------------

**Проблема**: не установился *SNatch*

**Решение**: проверьте, что в названиях директорий, в которых вы находитесь, нет пробелов. Если есть, устраните проблему и перезапустите `snatch_setup.sh`.

-----------------------------------------------------------------------------------

**Проблема**: шкала прогресса "Processing surface" пропала до завершения обработки архива (например, после обновления страницы).

**Решение**: процесс обработки архива продолжается в фоне. При его завершении в консоли появится сообщение `Processing ___ is done!`

-----------------------------------------------------------------------------------

**Проблема**: Flame graph долго строится/завис

**Решение**: процесс построения флейм графа может занять очень длительное время, более часа.

При построении флейм графа выводится прогресс. Если же ждать все равно больше не хочется, процесс построения можно прервать с помощью кнопки `Generate`, которая краснеет при наведении мыши.

-----------------------------------------------------------------------------------

**Проблема**: на  Alt Linux, во время создания проекта после тюнинга на этапе сборки отладочной информации, возникают ошибки `FATAL: Error create mounted folder` и `FATAL: Error delete mounted folder`

**Решение**: убедитесь в том, что учетная запись root добавлена в sudoers.


