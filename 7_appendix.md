# Приложение 1. Настройка окружения для использования лицензированного Natch

Для использования лицензированной версии инструмента *Natch* необходимо иметь HASP ключ или сетевую лицензию.
При наличии ключа следует только выполнить пункт 1 из этого приложения. В случае с сетевой лицензией необходимо выполнить
все нижеописанные действия.

В качестве хостовой системы предлагается использовать Ubuntu 20.04.

Все необходимые файлы для установки и настройки будут предоставлены пользователю, а именно
пакет aksusbd_8.31-1_amd64.deb, sailor-license.ovpn и логин/пароль для подключения.

1. Установить deb пакет aksusbd_8.31-1_amd64.deb с помощью команды:

```bash
    sudo dpkg -i aksusbd_8.31-1_amd64.deb
```

2. Открыть браузер и ввести строку ``localhost:1947``

3. Откроется главная страница ``Sentinel Admin Control Center``, на которой нужно перейти в раздел ``Configuration``, в нем найти раздел ``Access to Remote License Managers``.

4. Убедиться, что в полях ``Allow Access to Remote Licenses`` и ``Broadcast Search to Remote Licenses`` стоят галочки.

5. В поле ``Remote License Search Parameters`` ввести ``license.intra.ispras.ru`` и нажать кнопку ``Submit``.

6. Создать VPN соединение.

Для этого создания VPN соединения необходимо открыть настройки операционной системы и перейти в раздел *Network*. В секции *VPN* нажать на плюсик.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/app_vpn/settings.png" width=60% height=60% alt="Настройки сети">

Появится окно для добавления новой конфигурации VPN. Нужный вариант *Import from file..*, куда следует передать входящий в поставку
файл *sailor-license.ovpn*. В предлагаемой ОС OpenVPN установлен по умолчанию.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/app_vpn/import.png" width=40% height=40% alt="Импорт настроек VPN">

После импорта файла появится окно настройки соединения, в которое необходимо вписать логин и пароль, так же входящие в поставку.
Далее осталось нажать кнопку *Add* в верхнем правом углу и конфигурация будет создана.


<img src="https://raw.githubusercontent.com/ispras/natch/main/images/app_vpn/login.png" width=40% height=40% alt="Добавление конфигурации VPN">

Осталось только включить переключатель напротив VPN и соединение будет установлено.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/app_vpn/ok.png" width=40% height=40% alt="VPN готов">

Кроме того, управлять подключением можно в трее, как показано на рисунке ниже.

<img src="https://raw.githubusercontent.com/ispras/natch/main/images/app_vpn/profit.png" width=60% height=60% alt="Подключение VPN">

После всех проделанных действий инструмент готов к использованию на вашем компьютере.


# Приложение 2. Командная строка эмулятора Qemu

Пример командной строки для запуска Qemu выглядит следующим образом:

``./qemu-system-x86_64 -hda debian.qcow2 -m 6G -monitor stdio -netdev user,id=net0 -device e1000,netdev=net0``

- ``qemu-system-x86_64``: исполняемый файл эмулятора
- ``-hda debian.qcow2``: подключение образа гостевой операционной системы
- ``-m 6G``: выделение оперативной памяти гостевой системе
- ``-monitor stdio``: подключение управляющей консоли эмулятора к терминалу
- ``-netdev user,id=net0 -device e1000,netdev=net0``: настройка сети и подключение сетевой карты модели е1000

Командная строка выше просто запускает эмулятор с заданным образом диска. Для работы Natch потребуются дополнительные опции командной строки, а именно: ::

```
-os-version Linux
-plugin <plugin_name>
```

Опция ``os-version`` настраивает *Natch* для работы с операционной системой Linux, а ``plugin`` непосредственно загружает плагин.



