<div style="page-break-before:always;">
</div>

# <a name="begin"></a>3. Начало работы с Natch

Работа с *Natch* предполагает подготовку образа операционной системы для [QEMU](https://wiki.qemu.org/Main_Page). В [первой части](#prepare) этого раздела описаны все подготовительные действия, которые могут потребоваться перед работой непосредственно с инструментом.

Во [второй части](#natch_stepbystep) раздела представлен пошаговый разбор работы с *Natch*, а так же немного затронут инструмент *SNatch* (немного, потому что про него есть [отдельный раздел](6_snatch.md#snatch)).

**Важно!** Для ознакомления с *Natch* можно сразу переходить ко [второй части](#natch_stepbystep), все тестовые материалы подготовлены разработчиком.

## <a name="prepare"></a>3.1. Подготовительные действия

### <a name="create-qemu-env"></a>3.1.1. Подготовка виртуализованной среды в формате QEMU

Подготовка виртуализованной среды выполнения ОО в общем случае состоит из следующих последовательных шагов:

* создание образа эмулируемой операционной системы в формате диска [qcow2](https://en.wikipedia.org/wiki/Qcow) на основе базового дистрибутива ОС. Формат *qcow2* позволяет эффективно формировать снапшоты состояния файловой системы в произвольный момент выполнения виртулизованной среды функционирования;
* сборка дистрибутива ОО с требуемыми параметрами, в частности, с генерацией и сохранением отладочных символов;
* помещение собранного дистрибутива ОО в виртуализованную среду выполнения;
* подготовка команд запуска QEMU, для эмуляции аппаратной части среды функционирования, загрузку и выполнение компонентов *Natch*.

Подготовка виртуализованной среды выполнения ОО в значительной степени совпадает с подготовкой среды для анализа с помощью инструмента динамического анализа помеченных данных [Блесна](https://www.ispras.ru/technologies/blesna/) (разработчик - [ИСП РАН](https://www.ispras.ru/)), с точностью до подготовки команд запуска QEMU.

Создавать виртуализованную среду выполнения ОО рекомендуется в хостовой системе, допускающей запуск QEMU в режиме пользовательской виртуализации (ключ `-enable-kvm`) - это существенно ускорит процесс,
скорость работы в режиме аппаратной виртуализации более чем на порядок превосходит работу в режиме полносистемной эмуляции. Проверить доступность данного режима в вашей хостовой системе
(равно как и установить KVM-модули в вашу систему) можно, опираясь на следующую [статью](https://phoenixnap.com/kb/ubuntu-install-kvm), с помощью команды:
```bash
sudo kvm-ok
```

Примерный алгоритм проброса виртуализации для трехуровневого стенда: *Windows 11+AMD Процессор (хостовая ОС  рабочей станции) -> VirtualBox (хостовая ОС рабочей станции) -> ubuntu+kvm+qemu (хостовая ОС Natch) -> lubuntu (гостевая ОС)* приведён ниже.

Перед установкой KVM в гостевой ОС нужно настроить среду виртуализации VirtualBox в хостовой ОС как на рисунках ниже.

____
**ВНИМАНИЕ!**

На момент 10.10.2023 по-прежнему наблюдается проблема с тем, что VirtualBox версии 7+ (7.0.8) не позволяет корректно запускать QEMU в режиме поддержки KVM. Используйте VirtualBox версии 6.1.40 (именно эту). Наиболее актуальный тикет на данную ошибку заведён [здесь](https://www.virtualbox.org/ticket/21552), пока что без ответа.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/vbox_system.png">

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/vbox_system2.png">

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/vbox_display.png"><figcaption>_Настройки машины в VBox_</figcaption>

Перед установкой KVM необходимо определить, поддерживает ли процессор эту функцию: `egrep -c '(vmx|svm)' /proc/cpuinfo`

В результате будут следующие варианты ответа системы:

 - 0 – процессор не поддерживает функции KVM;
 - 1 и более – процессор поддерживает функции KVM.

Следующий этап – установка KVM: `sudo apt install qemu qemu-kvm libvirt-daemon libvirt-clients bridge-utils virt-manager`. Этой командой будет выполнена установка утилиты `kvm`, библиотеки `libvirt` и менеджера виртуальных машин.

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

При этом важно помнить, что анализ в любом случае необходимо выполнять без использования данного ключа, так как только полносистемная эмуляция позволяет собрать полный лог действий процессора.

#### 3.1.1.1. Подготовка хостовой системы

Рекомендации по подготовке хостовой системы приведены [здесь](9_appendix.md#app_requirements) (*для получения доступа к репозиторию сообщества ознакомьтесь с информацией в описании телеграм-канала [Орг. вопросы::Доверенная разработка](https://t.me/sdl_community)*).

Подготовим Linux-based рабочую станцию (далее - хост), поддерживающую графический режим выполнения. QEMU демонстрирует вывод эмулируемой среды выполнения в отдельном графическом окне, следовательно, нам необходим графический режим. Хост может быть реализован в формате виртуальной машины. В примерах ниже описаны действия пользователя, работающего в виртуальной машине VirtualBox (4 ядра, 8 ГБ ОЗУ)
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
Наш образ среды функционирования готов к работе, в частности, к установке в него пресобранного *с символами* прототипа объекта оценки.

#### <a name="build_prototype"></a>3.1.1.2. Сборка прототипа объекта оценки

Рекомендации по подготовке исполняемого кода приведены [здесь](9_appendix.md#app_requirements).

В общем случае к анализируемому исполняемому коду выставляется два требования:

* должна быть представлена отладочная информация в формате символов в составе исполняемых файлов, отдельно прилагаемых символов или map-файлов. Предоставление символов непосредственно в составе исполняемых файлов является основной и рекомендуемой стратегией. Natch умеет самостоятельно доставать информацию об отладочных символах из исполняемых файлов, собранных *как минимум* компиляторами *gcc* и *clang* с сохранением отладочной информации (ключ компилятора `-g`, также рекомендуется сборка без оптимизаций в режиме `-O0`). Для стандартных пакетов из наиболее популярных сборок операционных систем символы подгружаются автоматически;
* рекомендуется выполнять сборку подлежащего анализу исполняемого кода в виртуализированной среде (виртульная машина QEMU). В случае, если сборка и анализ будут выполняться в различных средах функционирования (например, сборка осуществляется на отдельном сборочном сервере), требуется обеспечить совместимость версий разделяемых динамических библиотек, в первую очередь *glibc*, из состава среды функционирования. На вашем хосте и в виртуализированной среде комплекты библиотек могут различаться.

В качестве прототипа объекта оценки рассмотрим популярную программу *wget*.
Для выполнения [*классического*](https://thoughtbot.com/blog/the-magic-behind-configure-make-make-install) подготовительного скрипта `configure`, входящего в комплект поставки *wget*, генерирующего make-файл, потребуется установить дополнительные зависимости (скрипт выведет их наименования в случае неудачного завершения), например:
```bash
sudo apt install -y gnutls-dev gnutls-bin curl make gcc g++
```
*Подсказка: поскольку мы собираем wget из исходников, потребуется комплект заголовочных файлов, доступный как раз в dev-версии пакета gnutls*

Скачаем исходные тексты *wget* из репозитория в среду функционирования:
```bash
curl -o wget-1.21.2.tar.gz  'https://ftp.gnu.org/gnu/wget/wget-1.21.2.tar.gz'
tar -xzf wget-1.21.2.tar.gz && cd wget-1.21.2
```
Скрипт `configure` запустим с ключами, устанавливающими параметры компилятора для сохранения информации об отладочных символах. После этого запустим `make` для сборки проекта.
```bash
CFLAGS='-g -O0' ./configure
make
```
#### 3.1.1.3. Перенос прототипа объекта оценки из образа ВМ на хост

Natch использует файлы объекта оценки для получения из них отладочных символов.
Чтобы выгрузить нужные файлов из виртуальной машины, можно использовать скрипт `copy_files.py`:

```bash
mkdir wget-1.21.2
sudo /usr/bin/natch/bin/natch_scripts/guest_system/copy_files.py lubuntu.qcow2 wget-1.21.2 /home/user/wget-1.21.2
```

#### 3.1.1.4. Тестирование виртуализированной среды функционирования ОО

Запускаем ВМ скриптом `run.sh` с отключенным ранее cdrom, дожидаемся загрузки ОС ВМ, авторизуемся в ОС, пробуем выполнить обращение к произвольному сетевому ресурсу с помощью собранной нами версии *wget*:
```bash
cd wget-1.21.2/src && sudo ./wget ispras.ru
```
В результате вы должны увидеть приблизительно следующую картину в графическом окне QEMU, свидетельствующую о том, что ОО корректно выполняется в среде функционирования и сетевая доступность для ВМ обеспечена:

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/check.png"><figcaption>_Пример подготовленного ОО в QEMU_</figcaption>



## <a name="natch_stepbystep"></a>3.2. Пошаговое руководство по работе с Natch

Для работы с инструментом *Natch* нужны входные данные, а именно, подготовленный образ системы с собранным в нем объектом оценки, а так же бинарные файлы самого объекта оценки.
Чтобы быстро попробовать *Natch*, разработчики подготовили образ и несколько примеров, на которых можно поэкспериментировать без лишних трудозатрат.

Предполагается, что *Natch* и зависимости уже установлены в системе, но если это не так, перейдите в раздел [Установка и настройка Natch](2_setup.md#setup_natch).

Нижеописанные действия были проделаны на примере хостовой ОС Ubuntu 20.


### 3.2.1. Получение образа и тестовых примеров

Подготовленный разработчиками [тестовый набор](https://nextcloud.ispras.ru/index.php/s/testing_2.0) включает в себя минимизированный образ гостевой операционной системы Debian (размер qcow2-образа около 1 ГБ), а также два комплекта программ (Sample1_bins и Sample2_bins), собранных с отладочными символами.

Команда для скачивания тестового комплекта с помощью *curl* выглядит так: `curl -o materials.zip 'https://nextcloud.ispras.ru/index.php/s/testing_2.0/download'`.

После скачивания обучающих материалов их следует распаковать.

Образ гоствой ОС находится в папке `Natch_testing_materials`. Учётные записи пользователей: `user/user` и `root/root`.


**Сценарий использования тестового комплекта Sample1_bins**

Программа *test_sample* читает файл *sample.txt*, в первой строке которого записан адрес Google. Он передает эту строку в качестве параметра программе *test_sample_2*. Программа *test_sample_2* "курлит гугл" в файл *curl.txt*.
В образе исполняемые файлы находятся в папке `/home/user/Sample1`, там же расположены и исходные коды.

Запуск тестового сценария:
```
cd Sample1
./test_sample
```

**Сценарий использования тестового комплекта Sample2_bins**

В ходе сценария необходимо запустить `redis-server` внутри виртуальной машины, в хостовой же системе запустить клиент `redis-cli` и отправить на сервер несколько запросов.

Команда для запуска `redis-server`:

```
redis-server --port 5555 --protected-mode no
```

Команда запуска клиентской улититы:

```
redis-cli -h localhost -p 49152
```

Утилиту `redis-cli` можно поставить в вашу систему (`sudo apt install redis-tools`), либо воспользоваться бинарным файлом `redis-cli` из тестового набора
(необходимо будет выставить права на исполнение).

Далее выполнить какие-нибудь действия, например `SET b VeryBigValue`, `GET b`. 

В тестовом образе redis установлен в систему.


### <a name="config_natch_test_image"></a>3.2.2. Настройка Natch для работы с тестовым образом ОС

Процесс настройки состоит из двух этапов -- автоматизированного (обязательный) и ручного (дополнительный, при необходимости тонкой настройки). Предназначение файлов конфигурации и их параметров описано в разделе [Конфигурационные файлы Natch](4_configs.md#natch_config_main).

#### 3.2.2.1. Автоматизированная настройка

Автоматизированная настройка выполняется [интерактивным скриптом](5_launch.md#natch_run_script) `natch_run.py`. Далее приведем вопросы скрипта и примеры ответов. Запустим скрипт:
```text
user@natch1:~/natch_quickstart$ /usr/bin/natch/bin/natch_scripts/natch_run.py Natch_testing_materials/test_image_debian.qcow2
Image: /home/user/natch_quickstart/Natch_testing_materials/test_image_debian.qcow2
OS: Linux
```
Вводим имя проекта - будет создан каталог с таким именем:
```text
Enter path to directory for project (optional): test1
Directory for project files '/home/user/natch_quickstart/test1' was created
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
На этом этапе скрипт проверит доступность утилиты natch-qemu-img, которая в дальнейшем нужна для создания оверлея для образа. В случае успеха увидим:
```text
Checking natch-qemu-img utility...
Utility natch-qemu-img is ok
```
Если что-то пошло не так, скрипт прекратит работу.

Если наш сценарий предполагает передачу помеченных данных по сети (далее мы рассматриваем в качестве основного как раз сценарий №2 -- взаимодействие с redis-сервером, слушающим tcp-порт 5555),
нам потребуется взаимодействовать с сетевыми сервисами гостевой ОС с помощью программ, запущенных на хосте. Указываем *Natch*, какой порт мы хотим опубликовать в гостевую ОС:

```text
Network option
Do you want to use ports forwarding? [Y/n] y
Do you want to taint source ports too? [Y/n] n
Write the ports you want separated by commas (e.g. 7777, 8888, etc) 5555
Your pair of ports for connecting: 5555 <=> 49152
```
Далее нам нужно указать путь к каталогу на хосте, содержащем копии бинарных файлов, размещенных в гостевой ОС. Находятся в папках `Sample1_bins` и `Sample2_bins` в тестовых материалах.
Так как будет проделан пример с redis, то следует указать путь к папке `Sample2_bins`.
Этот процесс будет выполняться параллельно, результаты увидим позже.

Следующая стадия: конфигурирование технических параметров *Natch*, требующая тестового запуска виртуальной машины. В ходе данного запуска происходит получение информации
о параметрах ядра и заполнение ini-файла. Вы можете отказаться от данного шага, в случае если этот файл уже был ранее создан для данного образа гостевой виртуальной машины --
тогда вам потребуется указать к нему путь в конфигурационном файле или скопировать этот файл в рабочую директорию.

Согласимся на создание task.cfg:

```text
Generate config file task.cfg? [Y/n] y (или просто нажмите Enter)

Now will be launch tuning. Don't close emulator
Three...
Two..
One.
Go!
Natch monitor - type 'help' for more information
Natch v.2.4
(c) 2020-2023 ISP RAS

Reading Natch config file...
Network logging enabled
[Tasks] No such file 'task.cfg'. It will be created.
Now tuning will be launched.

Tuning started. Please wait a little...
Generating config file: task.cfg
Trying to find 20 kernel-specific parameters
[01/20] Parameter - task_struct->pid            : Found
[02/20] Parameter - task_struct->comm           : Found
[03/20] Parameter - task_struct->group_leader   : Found
[04/20] Parameter - task_struct->parent         : Found
[05/20] Parameter - mount fields                : Found
[06/20] Parameter - files_struct fields         : Found
[07/20] Parameter - file->f_pos                 : Found
[08/20] Parameter - vm_area_struct size         : Found
[09/20] Parameter - vm_area_struct->vm_start    : Found
[10/20] Parameter - vm_area_struct->vm_end      : Found
[11/20] Parameter - vm_area_struct->vm_flags    : Found
[12/20] Parameter - mm->map_count               : Found
[13/20] Parameter - mm_struct fields            : Found
[14/20] Parameter - task_struct->mm             : Found
[15/20] Parameter - mm->arg_start               : Found
[16/20] Parameter - task_struct->state          : Found
[17/20] Parameter - socket struct fields        : Found
[18/20] Parameter - task_struct->exit_state     : Found
[19/20] Parameter - cred->uid                   : Found
[20/20] Parameter - task_struct->cred           : Found
Detected 43096 system events
Detected 20 of 20 kernel-specific parameters. Creating config file...

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

Далее скрипт попробует скопировать из образа системые файлы (/etc/passwd и /etc/group) для чего попросит ввести пароль администратора.
Так как на этом этапе будет происходить монтирование образа, удостоверьтесь, что в системе не работают другие виртуальные машины.

```
Users info part
[sudo] password for user: 
Mounting img - OK
Files copied from the guest system: 2
Umounting img - OK
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

─────────────────────────────── Libraries Searching Section ───────────────────────────────────────

Reading module config - OK
Searching Binary Files...                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2/2 100% 0:00:00
Searching Binary Files - OK
Searching Python Symbols - OK
Searching Java symbols - OK
Searching Kernel Symbols - OK
Searching Shared Libraries...                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 48/48 100% 0:00:01
Searching Shared Libraries - OK

───────────────────────────── Library-Debug Matching Section ──────────────────────────────────────

Method: DebugInfoD

Download debugging information - OK

Download dwz information - OK
Unmounting img - OK

───────────────────────────────────── Result Section ──────────────────────────────────────────────

Module config statistics:
In module config there were modules                               :     2
Binaries files in qcow2 found                                     :     2

Python interpreters statistics:
Python interpreters have been found                               :     OK
Added python interpreters                                         :     46
Added debugging information for python interpreters               :     46

Kernel statistics:
WARNING: Java symbols have been found                             :     NO

Kernel statistics:
Kernel symbols have been found                                    :     OK
Added kernel symbols                                              :     1
Added debugging information for kernel                            :     1

Shared library Statistics:
Added shared libraries                                            :     31
Added debugging information for shared libraries                  :     31
Added debugging information for tied files                        :     2
ld-linux-* is always skipped and isn't counted in calculations

Your config file '/home/user/natch_quickstart/test1/module.cfg' for modules was updated
```
Следом будет запущен процесс генерации базы данных символов, это займет некоторое время.
```text
Symbol info part
Reading symbols for loaded modules

Created symbol database for /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-server
Created symbol database for /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-cli
...
...
Created symbol database for /home/user/natch_quickstart/test1/libs/src/f902f8a561c3abdb9c8d8c859d4243bd8c3f928f/python3.9
Created symbol database for /home/user/natch_quickstart/test1/libs/src/cc89a8838df3652561ab61598035775fa95f8917/vmlinux-5.10.0-17-amd64
Created symbol database for /home/user/natch_quickstart/test1/libs/src/5018237bbf012b4094027fd0b96fc22a24496ea4/libpthread-2.31.so
Created symbol database for /home/user/natch_quickstart/test1/libs/src/e9d2c06479b13dd3cfa78d714d11dccf6fcbee51/libm-2.31.so
Created symbol database for /home/user/natch_quickstart/test1/libs/src/bc22349819818055008048f8001e3910ffc16dc7/libexpat.so.1.6.12
Created symbol database for /home/user/natch_quickstart/test1/libs/src/a89a9c8e4a828f47e68e2d1dafca4aae087d061d/libz.so.1.2.11
Created symbol database for /home/user/natch_quickstart/test1/libs/src/5675f6cc697d1e1fb135c65cbb0f917550fe85ac/libutil-2.31.so
Created symbol database for /home/user/natch_quickstart/test1/libs/src/118b90161526d181807818c459baee841993795b/libdl-2.31.so
Created symbol database for /home/user/natch_quickstart/test1/libs/src/2e5abcee94f3bcbed7bba094f341070a2585a2ba/libc-2.31.so

Your config file '/home/user/natch_quickstart/test1/module.cfg' for modules was updated
```

Автоматизированная настройка и создание базовых скриптов завершены успешно, всё готово к записи сценария, о чём *Natch* сообщил нам дополнительно:

```text
Configuration file natch.cfg was created.
You can edit it before using Natch.

Settings completed! Now you can launch emulator and enjoy! :)

	Natch in record mode: 'run_record.sh'
	Natch in replay mode: 'run_replay.sh'
	Qemu without Natch: 'run_qemu.sh'
```
В папке проекта появится конфигурационный файл `natch.cfg` -- его мы будем редактировать для ручной настройки, кроме того после записи сценария появится
(в соответствующей папке) еще один конфигурационный файл `taint.cfg`, который тоже можно редактировать. Также в папке проекта находится файл `natch.log` --
в нём логируются основные результаты работы программ, входящих в комплект поставки *Natch*.

#### <a name="additional_settings"></a>3.2.2.2. Дополнительная ручная настройка

Конфигурационный файл `natch.cfg` генерируется таким образом, что дополнительные опции представлены в нем в закомментированном виде.

В качестве примера ручной настройки соберем покрытие кода по базовым блокам для просмотра в *IDA Pro*. 
Для этого в конфигурационном файле `natch.cfg` предусмотрена секция `Coverage`.
Необходимо раскомментировать не только параметры секции, но и название секции в квадратных скобках.

Раскомментируем секцию `Coverage` (подробнее об предназначении секций см. пункт [Основной конфигурационный файл](4_configs.md#main_config) документации):

```ini
[Coverage]
file=coverage
taint=true
```

### <a name="record_scenario"></a>3.2.3. Запись сценария работы

Все настройки выполнены, можно переходить к записи сценария. Рассмотрим в качестве примера сценарий с redis-сервером (Sample2_bins).
Для записи сценария предусмотрен скрипт `run_record.sh`, запустим его:
```bash
user@natch1:~/natch_quickstart/test1$ ./run_record.sh
```
Скрипт запросит название сценария, введем `sample_redis`. Далее запустится эмулятор.

Введём логин и пароль учетной записи пользователя - `user/user` и запустим redis-сервер:
```
redis-server --port 5555 --protected-mode no
```

Тестово соединимся с ним из хостовой ОС чтобы убедиться, что система в комплексе работает как надо:
```text
user@natch1:~/natch_quickstart$ redis-cli -h localhost -p 49152

localhost:49152> select 0
OK
localhost:49152> set a b
OK
localhost:49152> get a
"b"
localhost:49152> exit
```
**Важное замечание**: *весь записываемый сценарий включает в себя в том числе этап загрузки ОС, но помеченные данные появятся практически в самом конце,
когда мы обратимся к redis-серверу. Соответственно, для существенного сокращения времени на сбор данных (последующее выполнение ./run_replay.sh)
нам необходимо сделать снапшот в точке, максимально приближенной к точке начала поступления помеченных данных в системе. То есть сейчас, когда от порождения
помеченных данных нас отделяет только повторное соединение с redis-сервером из хостовой ОС и повторная отправка в него уже знакомых нам команд*.

Нажмем `Ctrl+Alt+G`, выйдем в монитор QEMU (bash-терминал хостовой ОС в котором мы запустили `run_record.sh`) и выполним команду генерации снапшота:
```
savevm <name>
```
Используем имя `ready`. Сохранение состояния займёт несколько секунд, в зависимости от размера образа и производительности компьютера в целом.
```text
user@natch1:~/natch_quickstart/test1$ ./run_record.sh
Enter scenario name: sample_redis

Natch monitor - type 'help' for more information
(natch)
Natch v.2.4
(c) 2020-2023 ISP RAS

Reading Natch config file...
Network logging enabled
Config is loaded.
You can make system snapshots with the command: savevm <snapshot_name>
Network pcap log file: "/home/user/natch_quickstart/test1/sample_redis/network.pcap"
Network json log file: "/home/user/natch_quickstart/test1/sample_redis/network.json"

(natch) savevm ready
(natch)
```

После того как снапшот был сгенерирован, снова отправим какие-нибудь данные из хостовой ОС в redis-сервер. Теперь завершим работу QEMU, закрыв графическое окно эмулятора.

Сценарий работы с `redis` записан.

Теперь в папке с нашим проектом (`test1`) появилась директория с названием сценария `sample_redis`. В ней размещены логи сетевых операций, файл журнала, оверлей диска,
и, самое главное для пользователя -- конфигурационный файл помеченных данных `taint.cfg`. На данный момент все настройки по умолчанию нам подходят.

Для каждого вновь записанного сценария будет появляться своя папка с индивидуальными настройками.

### <a name="replay_scenario"></a>3.2.4. Воспроизведение сценария и сбор данных для анализа

Для воспроизведения нужно запустить скрипт `run_replay.sh`.
```text
user@natch1:~/natch_quickstart/test1/$ ./run_replay.sh
```
Скрипт может принимать два параметра: название сценария и имя снапшота. В нашем случае команда могла бы выглядеть так:
```text
user@natch1:~/natch_quickstar/test1/$ ./run_replay.sh sample_redis ready
```
Если используются параметры, то они оба являются обязательными. Однако, запускать скрипт можно без параметров, он сам или загрузит нужный сценарий (если он единственный)
или предложит выбрать из списка существующих, точно так же произойдет с выбором снапшота.

Начнём воспроизведение сценария, а точнее его фрагмента, который выполнялся после создания снапшота. Это будет несколько медленнее, чем базовое выполнение.

Через какое-то время выполнение сценария завершится, графическое окно закроется, и вы увидите сообщение наподобие приведённого ниже, свидетельствующее о том,
что интересующие нас модули гостевой ОС были распознаны успешно, и, следовательно, мы получим в отчетах корректную символьную информацию.
```text
Snapshot to load: ready
Natch monitor - type 'help' for more information
(natch) 
Natch v.2.4
(c) 2020-2023 ISP RAS

Reading Natch config file...
Network logging enabled
Task graph enabled
Module graph enabled
Taint enabled
Config is loaded.
File events binary log file /home/user/natch_quickstart/test1/output_sample_redis/files_b.log created successfully
Module binary log file /home/user/natch_quickstart/test1/output_sample_redis/log_m_b.log created successfully
Modules: started reading binaries
Modules: finished with 13 of 13 binaries for analysis
thread_monitor: identification method is set to a complex developed at isp approach
Started thread monitoring
Tasks: config file is open.
Process events binary log file /home/user/natch_quickstart/test1/output_sample_redis/log_p_b.log created successfully
Network json log file: "/home/user/natch_quickstart/test1/output_sample_redis/tnetwork.json"
Binary log file /home/user/natch_quickstart/test1/output_sample_redis/log_t_b.log created successfully
Binary call_stack log file /home/user/natch_quickstart/test1/output_sample_redis/log_cs_b.log created successfully
Detected module /home/user/natch_quickstart/test1/libs/src/cc89a8838df3652561ab61598035775fa95f8917/vmlinux-5.10.0-17-amd64 execution
Detected module /home/user/natch_quickstart/test1/libs/src/2e5abcee94f3bcbed7bba094f341070a2585a2ba/libc-2.31.so execution
Detected module /home/user/natch_quickstart/Natch_testing_materials/Sample2_bins/redis-server execution
Detected module /home/user/natch_quickstart/test1/libs/src/5018237bbf012b4094027fd0b96fc22a24496ea4/libpthread-2.31.so execution
Detected module /home/user/natch_quickstart/test1/libs/src/e9d2c06479b13dd3cfa78d714d11dccf6fcbee51/libm-2.31.so execution


=========== Statistics ===========

Tainted files             : 0
Tainted packets           : 147
Tainted processes         : 3
Tainted modules           : 3
Tainted file reads        : 0
Tainted memory accesses   : 21026

Compressing data. Please wait..

test1+sample_redis.tar.zst completed
```

Если работа системы завершилась успешно, и вы не словили, например, `core dumped` (о чём стоит немедленно сообщить в [трекер](https://gitlab.ispras.ru/natch/natch-support/-/issues) с приложением всех артефактов),
можно переходить к анализу собранных данных.

После воспроизведения сценария в папке проекта появилась директория с выходными данными `output_sample_redis` и, главное, -- архив, который необходимо передать в графическую подсистему *SNatch*.
Название архива формируется следующим образом:` <название проекта>+<название сценария>.tar.zst`. Таким образом, записывая разные сценарии, уже готовые архивы не будут перезаписаны и могут быть
использованы повторно или переданы третьим лицам.

### <a name="snatch_analysis"></a>3.2.5. Анализ с использованием SNatch

*SNatch* -- это подсистема визуализации данных и статистик, собранных при воспроизведении сценария работы под управлением *Natch*. *SNatch* реализован в формате веб-службы с браузерным интерфейсом просмотра.

В комплект поставки *SNatch* входят скрипты `snatch_start.sh` и `snatch_stop.sh` для запуска и остановки *SNatch* соответственно. Скрипт `snatch_start.sh` запускает необходимые для работы службы, а также открывает браузер с интерфейсом. В терминал, из которого был запущен скрипт, будут приходить сообщения от сервера, однако, он свободен для использования, поэтому по окончании работы из него же можно запустить скрипт `snatch_stop.sh` для остановки служб. Запускать `snatch_stop.sh` следует всегда, в противном случае процессы останутся висеть в памяти вашего компьютера до перезагрузки.

Полное руководство пользователя *SNatch* доступно в соответствующем разделе [Анализ поверхности атаки с помощью SNatch](6_snatch.md#snatch), здесь же приведем краткий обзор некоторых аналитик. 

Запустим *SNatch*:
```bash
user@natch1:~/natch_quickstart$ ./snatch/snatch_start.sh
```
Создадим проект на основе собранных данных (необходимо указывать tar.zst-архив, формируемый *Natch* в каталоге проекта по результатам выполнения `run_replay.sh`):

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_new_project.png"><figcaption>_Создание Snatch проекта_</figcaption>

Через некоторое время процесс загрузки архива завершится и станут доступны различные виды аналитик (*их число и возможности постоянно нарастают*).

Главное окно представляет динамическую визуализацию распространения помеченных данных.
Ярким цветом на каждом шаге *Timeline* выделяются сущности, взаимодействующие на данном конкретном шаге *Timeline*.

Кликнув по процессу *redis-server* мы увидим боковую панель с информацией об этом процессе. 

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_main.png"><figcaption>_Интерфейс *SNatch*_</figcaption>

На боковой панели так же находится кнопка для перехода на граф модулей, связанных с выбранным процессом.
На рисунке ниже представлен граф модулей для процесса `redis-server`.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_module_graph.png"><figcaption>_Модуль граф для redis-server_</figcaption>

Для просмотра таких аналитик, как граф вызовов и флейм граф, следует их предварительно сгенерировать, нажав на соответствующие кнопки *Generate*.

Фрагмент графа вызовов для примера с redis-server представлен на рисунке ниже. Голубым цветом выделены функции, работавшие с помеченными данными.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_callstack.png"><figcaption>_Граф вызовов_</figcaption>

Подробнее о возможностях *SNatch* написано в [соответствующем](6_snatch.md#snatch) разделе.

### 3.2.6. Просмотр сетевого трафика в Wireshark

Анализировать трафик в Wireshark можно прямо из интерфейса *SNatch* с помощью раздела *Traffic*. Здесь можно увидеть интерфейсы и сессии, клик по каждой записи будет открывать Wireshark с соответствующими данными.

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/snatch_traffic.png><figcaption>_Информация о трафике_</figcaption>

Так же можно открывать только помеченный трафик, трафик, относящийся к сценарию, а так же весь трафик с помощью соответствующих кнопок.

<img src=https://raw.githubusercontent.com/ispras/natch/main/images/quickstart/wireshark.png><figcaption>_Исследование трафика в Wireshark_</figcaption>

### 3.2.7. Изменение настроек проекта дополнительными скриптами

В рассмотренном сценарии нам не пришлось изменять конфигурационный файл сценария, потому что порт был установлен при настройке проекта. Однако, это может потребоваться.
Конфигурационный файл `taint.cfg` находится в папке со сценарием и содержит три секции: *Taint*, *Ports* и *TaintFile*. Появляется папка со сценарием, как мы уже
знаем, после записи сценария.

Попробуем записать сценарий для первого тестового примера. Запустим уже знакомый скрипт `run_record.sh`, укажем имя `sample_test`, дождемся загрузки ОС.
Для выполнения сценария следует перейти в папку `Sample1`, на этом моменте не забыть сохранить состояние машины `savevm ready`, вернуться в эмулятор и запустить программу `./test_sample`.
Дожидаемся завершения программы и работу эмулятора можно завершать.

Теперь в проекте есть еще одна папка со сценарием `sample_test`. Именно в ней находится конфигурационный файл `taint.cfg` в котором следует установить файл для пометки.
Так же мы увидим, что в наследство от первоначальной настройки остался выбранный порт. В этом сценарии отслеживание сети не требуется, закомментируем секцию *Ports* полностью.

Пометить файл *sample.txt* нужно следующим образом:

```ini
[TaintFile]
list=sample.txt
```

Казалось бы все готово к воспроизведению сценария, но при первоначальной настройке мы указывали путь только к `Sample2_bins`, значит `module.cfg` ничего не знает про бинарные файлы для
первого тестового сценария. Просто руками дописать их в конфигурационный файл не сработает, потому что необходимо еще собрать отладочную информацию для системных
библиотек, от которых зависят бинарные файлы, а так же построить символьную информацию. Это все можно сделать вручную, аккуратно вызывая ряд скриптов, входящих
в поставку *Natch*, а можно воспользоваться специальным скриптом-утилитой, которая сделает все сама.

Эта утилита называется `append_module_config.py` и находится здесь: `/usr/bin/natch/bin/natch_scripts/utils`. [Подробнее про нее тут](5_launch.md#natch_append_modules),
а сейчас рассмотрим ее работу на примере.

Потребуется указать путь к образу, а так же путь к папке с новыми модулями. Если вы находитесь не в папке проекта, то еще необходимо указать рабочую директорию.

Сейчас `module.cfg` содержит 80 записей. Запускаем утилиту:
```
/usr/bin/natch/bin/natch_scripts/utils/append_module_config.py -D Natch_testing_materials/Sample1_bins -i Natch_testing_materials/test_image_debian.qcow2
```

Скрипт спросит есть ли у вас уже загруженная информация для ядра и интерпретаторов. Если при первоначальной настройке вы не отказывались от скачивания отладочной информации, следует ответить да.
Далее для монтирования образа будет запрошен пароль администратора. Затем будут происходить действия, которые вы уже видели при первоначальной настройке проекта.

После того как скрипт отработал, мы увидим что записей в конфигурационном файле стало 82. Никаких новых системных библиотек не добавилось, только бинарные файлы нашего примера.

Теперь все готово, запустим скрипт `run_replay.sh` без параметров и увидим, что нам предлагают выбрать из двух вариантов. Выбираем `sample_test`. И снова выбор, теперь снапшота. Выбираем `ready`.

После того как эмулятор отработает увидим следующую статистику:
```
============ Statistics ============

Tainted files             : 1
Tainted packets           : 0
Tainted processes         : 9
Tainted modules           : 16
Tainted file reads        : 1
Tainted memory accesses   : 2275

```
Так же в папке с проектом появится новая директория `output_sample_test` и архив `test1+sample_test.tar.zst`.

Помимо скрипта для добавления модулей в конфигурационный файл, существует скрипт для внесения некоторых изменений в настройки проекта.
Называется он `change_settings.py` и для удобства использования копируется в папку проекта, либо его можно найти в папке `utils`, как предыдущий.
Ознакомиться с подробным описанием скрипта можно [здесь](5_launch.md#natch_change_settings).


## <a name="faq"></a>3.3. FAQ

В этом разделе собраны наиболее часто встречающиеся проблемы при работе с инструментами *Natch* и *SNatch*, раздел будет пополняться.

-----------------------------------------------------------------------------------

**Проблема**: настройка стенда происходит очень медленно

**Решение**: проверьте, используете ли вы опцию `enable-kvm` при запуске QEMU. Если вы хотите проверить включен ли KVM в уже запущенной виртуальной машине - введите в мониторе QEMU команду `info kvm`

-----------------------------------------------------------------------------------

**Проблема**: *Natch* не запускается

При запуске появляется сообщение *"Sentinel LDK Protection System: Sentinel key not found"*

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

**Проблема**: во время экспорта проекта в PDF появляется сообщение об ошибке для какого-то из заданных параметров

**Решение**: вероятнее всего, сгенерированная для данного параметра (чаще всего это относится к ресурсам) таблица оказалась слишком большой для используемой библиотеки. В таком случае рекомендуется использование предлагаемых фильтров: включить "only tainted", чтобы в отчет попали только связанные с пометками данные, и отключить "include root", чтобы оставить только пользовательские процессы.

-----------------------------------------------------------------------------------

**Проблема**: на  Alt Linux, во время создания проекта после тюнинга на этапе сборки отладочной информации, возникают ошибки `FATAL: Error create mounted folder` и `FATAL: Error delete mounted folder`

**Решение**: убедитесь в том, что учетная запись root добавлена в sudoers.

-----------------------------------------------------------------------------------

**Проблема**: в ходе анализа сценариев работы многопроцессного программного комплекса, предназначенного для работы на многоядерных (многопроцессорных) платформах, запись сценария происходит очень медленно

**Решение**: в настоящий момент и в обозримой перспективе отсутствует. Запись сценария требует запуска эмулятора QEMU в режиме полносистемной эмуляции, подразумевающем выполнение всего исполняемого кода анализируемого программного комплекса (включая код среды его функционирования - ОС, BIOS, эмулированных устройств и т. п.) в виртуальном процессоре -- программной модели процессора (эмулятор QEMU работает в данном режиме по умолчанию, в случае если не указан ключ `enable-kvm`).

Скорость выполнения исполняемого кода в режиме полносистемной эмуляции намного ниже по сравнению с выполнением на аппаратном процессоре, однако позволяет логировать любые изменения состояния виртуального процессора, оперативной памяти, а также взаимодействия с внешними по отношению к эмулированному пространству сущностями (сеть и т. п.). В том числе это позволяет записывать и в дальнейшем воспроизводить работу виртуальной машины,
сохраняя в файл случайные и недетерминированные события, меняющие состояния виртуальной машины.

Добавление возможности надежного логирования работы даже двухядерной (двухпроцессорной) системы,
требует записывать ещё и порядок обращения процессоров к памяти, чтобы избежать состояния гонки при воспроизведении.
Такой лог будет на несколько порядков больше лога однопроцессорной машины, что делает запись/воспроизведение неприменимыми при существующих объёмах
и скоростях накопителей.

Реализация данного механизма на программном уровне является фундаментальной проблемой, до сих пор не имеющей в мире эффективного решения. Некоторые попытки решить аналогичную задачу для архитектуры x86_64 делались разработчиками процессоров, в частности компанией Intel, однако во-первых они не завершились удачными конкретными решениями, во-вторых -- требовали доработки процессора за счёт внесения в него отдельного специализированного блока, отвечающего за корректное логирование всех операций доступа -- то есть создания отдельное процессорной линейки. Таким образом в настоящий момент увеличение числа ядер виртуального процессора QEMU и запись сценариев в многоядерном (многопроцессорном) режиме не представляется возможным технологически.

