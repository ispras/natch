<div style="page-break-before:always;">
</div>

# <a name="natch_applications"></a> 8. Примеры использования Natch

## 8.1. Соединение нескольких эмуляторов в сеть

https://werewblog.wordpress.com/2015/12/31/create-a-virtual-network-with-qemukvm/comment-page-1/

Сконфигурировать туннель из tap-адаптеров на хосте:

```
modprobe tun tap
sudo ip link add br0 type bridge
sudo ip tuntap add dev tap0 mode tap
sudo ip tuntap add dev tap1 mode tap
sudo ip link set dev ens33 master br0
sudo ip link set dev tap0 master br0
sudo ip link set dev tap1 master br0
sudo ip link set dev br0 up
sudo ip address delete 192.168.159.131/32 dev ens33
sudo ip address delete 192.168.159.131 dev ens33
sudo ip address add 192.168.159.131/24 dev br0
sudo ip route add default via 192.168.159.2 dev br0
sudo resolvectl dns br0 192.168.159.2
```

Командная строка для запуска эмулятора:
```
qemu-system-x86_64 \
-hda ubuntu_nginx.qcow2  \
-m 4G \
-enable-kvm \
-cpu host,nx \
-monitor stdio \
-netdev tap,id=net0,ifname=tap0 \
-device e1000,netdev=net0,mac=50:54:00:00:00:43
```

Нужно придумать несколько mac-адресов для разных машин


## 8.2. Natch в режиме командной строки

При записи сценария на сервере без графической подсистемы можно использовать Natch режиме
командной строки.
Здесь описан вариант подобного использования Natch с файлом-источником помеченных данных.
При этом сам Natch ещё и помещается в Docker-контейнер.

Для выполнения примера потребуется:

- подготовленный разработчиком [тестовый комплект](2_quickstart.md#test_complect), включающий в себя минимизированный образ гостевой операционной системы Debian (размер qcow2-образа около 1 ГБ)
- там же [архив](https://nextcloud.ispras.ru/index.php/s/testing_2.0/download?path=%2F&files=samples.zip) с комплектом файлов с помеченными данными (sydr_0_int_overflow_1_unsigned,sydr_1_int_overflow_0_unsigned и sydr_2_int_overflow_0_unsigned).

#### 8.2.1. Подготовка образа виртуальной машины

**Важно!**

Приведённый ниже способ (тюнинг GRUB, сетевые настройки и т.д.) в вашем дистрибутиве Linux может отличаться от работающего в тестовом образе!

Необходимо скачать тестовый образ `test_image_debian.qcow2` и создать скрипт запуска `run1.sh`:

```
natch-qemu-x86_64 \
-hda test_image_debian.qcow2 \
-enable-kvm \
-m 4G \
```

Запустить скрипт `run1.sh`, залогиниться `root:root`
Установить неграфическую цель "по умолчанию": `systemctl set-default multi-user.target`

Открыть конфигурацию grub: `vim /etc/default/grub`

Изменить следующие строки (в скачанном образе эти строки уже раскомментированы):
- раскомментировать: `GRUB_TERMINAL=console`
- установить значение: `GRUB_CMDLINE_LINUX_DEFAULT="nomodeset"`

Сохранить, после этого выполнить: `update-grub`

Завершить работу: `shutdown 0`

Изменить скрипт запуска эмулятора -- отключить графический вывод используя опцию `nographic` и создать псевдографический интерфейс в терминале опцией `curses`. Управление виртуальной машиной в этом режиме работы осуществляется за счет проброса монитора QEMU на свободный порт (в данном случае - 7799) и добавления ключей `server`,`nowait`, которые  указывают QEMU прослушивать соединения и запускать виртуальную машину не дожидаясь подключения.
```
natch-qemu-x86_64 \
-hda test_image_debian.qcow2 \
-enable-kvm \
-m 4G \
-nographic \
-curses \
-monitor tcp:0.0.0.0:7799,server,nowait \
```
**Важно!**
Данные опции вставляются в Natch-скрипты записи/анализа сценариев автоматически, при указании соответствующего параметра при запуске `natch_run.py`.

#### 8.2.2. Сборка программы обработчика

Программа-обработчик представляет собой простой консольный парсер, который пытается распарсить xml-файл, подаваемый на вход в качестве первого параметра.

Запустить скрипт `run1.sh`. Залогиниться `user:user`.
Скачать папку `pugixml`:
```
git clone --depth 1 --single-branch https://github.com/zeux/pugixml
cd pugixml
```
Собрать объектный файл:
```
gcc -c -Isrc src/pugixml.cpp
```

В каталоге `pugixml` создать файл `wrapper.cpp` со следующим содержанием:
```
#include "pugixml.hpp"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
        pugi::xml_document doc;
        pugi::xml_parse_result result = doc.load_buffer((void *)data, size);
        return 0;
}

int main(int argc, char** argv)
{
        FILE *fd = fopen(argv[1], "rb");

        if (fd == NULL) return 1;
        fseek(fd, 0, SEEK_END);
        int fsize = ftell(fd);
        fseek(fd, 0, SEEK_SET);

        char* buffer = (char*) malloc(sizeof(char) * fsize);
        fread(buffer, 1, fsize, fd);
        fclose(fd);

        return LLVMFuzzerTestOneInput((const uint8_t*)buffer, fsize);
}

```

Скомпилировать цель из каталога, который находится на уровень выше содержимого каталога pugixml командой:
```
cd ..
/usr/bin/clang++ -g -O0 pugixml/src/pugixml.cpp  pugixml/wrapper.cpp  --include=unistd.h -Ipugixml/src -o target && chmod +x target
```

Завершить эмулятор можно перейдя в режим суперпользователя командой `su` и вызвав команду `systemctl poweroff`.

#### 8.2.3. Перенос объекта оценки

Далее необходимо перенести объект оценки в виртуальную машину, аналогично [пункту](2_quickstart.md#map_gen), переместить 3 сэмпла (sydr_0_int_overflow_1_unsigned, sydr_1_int_overflow_0_unsigned, sydr_2_int_overflow_0_unsigned) в папку к скомпилированному файлу.
А файл `target` нужно наоборот скопировать на хост (Например в папку **targetdir**).

Теперь стоит проверить, что программа запустится с этими сэмплами.
Запустить скрипт `run1.sh`, перейти в папку, в которой находятся 3 сэмпла и скомпилированный файл `target`, и последовательно подать сэмплы в программу-обработчик:
```
./target sydr_0_int_overflow_1_unsigned
./target sydr_1_int_overflow_0_unsigned
./target sydr_2_int_overflow_0_unsigned
```

#### 8.2.4. Создание контейнера и запуск Natch

Для настройки контейнера создадим файл `Dockerfile` со следующим содержимым:
```
FROM ubuntu:20.04

#Set Timezone or get hang during the docker build...
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update
RUN apt install -y vim git cmake make clang zlib1g-dev unzip curl python3-pip
RUN apt install -y mc
RUN apt install -y qemu-system
RUN apt install -y netcat
RUN apt install -y nano
RUN apt install -y unzip
RUN apt install -y libsdl2-2.0-0
RUN apt install -y libguestfs-tools
```
Создадим образ контейнера на основе созданного Dockerfile:
```
sudo docker build -t docker /home/user/natch_quickstart
```
Где '/home/user/natch_quickstart/' это папка, в которой находятся тестовый образ ОС и бинарные файлы Natch.

Теперь запустим созданный образ:
```
docker run -v /home/user/natch_quickstart/:/mnt/ --network=host -it --privileged docker
```

Сначала установим необходимые библиотеки для работы Python-скриптов:
```
pip3 install -r natch/bin/natch_scripts/requirements.txt
pip3 install -r natch/bin/natch_scripts/guest_system/requirements.txt
```

Дальше нужно создать с помощью Natch проект, как описано в [разделе "Начало работы"](2_quickstart.md#config_natch_test_image).

При этом ответы на некоторые вопросы будут отличаться. Нужно выбрать текстовый режим работы эмулятора:
```text
Do you want to run emulator in graphic mode? [Y/n] n
```
Не указывать опции сети:
```Network option
Do you want to use ports forwarding? [Y/n] n
```
Задать пути к копиям бинарных файлов (необходимо указать папку, в которой находится необходимый бинарный файл):
```
Modules part
Do you want to create module config? [Y/n] y
Enter path to maps dir: ./targetdir
```
После запуска natch в папке с созданным проектом необходимо раскомментировать строки "TaintFile" (строки №56, 57) и прописать имена файлов, которые требуется пометить:
```
[TaintFile]
list=/root/pugi/sydr_0_int_overflow_1_unsigned;/root/pugi/sydr_1_int_overflow_0_unsigned;/root/pugi/sydr_2_int_overflow_0_unsigned
```

Дальше нужно [записать сценарий с тестовым приложением](2_quickstart.md#record_scenario).
На этапе с созданием снэпшота необходимо на хостовой машине открыть новое окно терминала и подключиться к эмулятору:
```
nc -N 0.0.0.0 7799
```
После загрузки интерфейса управления QEMU, выполнить команду 'savevm ready'.
Открыть окно тестовой ОС и последовательно подать три сэмпла в программу-обработчик:
```
./target sydr_0_int_overflow_1_unsigned
./target sydr_1_int_overflow_0_unsigned
./target sydr_2_int_overflow_0_unsigned
```
В интерфейсе управления QEMU на хостовой машине выполнить команду 'quit'.
Дальше остаётся [воспроизвести сценарий](2_quickstart.md#replay_scenario), чтобы записать поверхность атаки,
а потом [загрузить её в SNatch](2_quickstart.md#snatch_analysis)

Если SNatch появятся диаграммы, подобные приведенным в примере ниже, то всё получилось.
<img width="722" alt="call_graph" src="https://user-images.githubusercontent.com/47216218/208419146-b524a61f-f8f1-41ff-938b-6784295a8816.png">
<img width="925" alt="flame_graph2" src="https://user-images.githubusercontent.com/47216218/208419147-0194f1e7-ba53-49d3-8cbd-aaedb33329c0.png">
