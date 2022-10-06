
# 2. Основы работы с Natch

Инструмент *Natch* для определения поверхности атаки отслеживает потоки данных с помощью пометок.
Обнаруженные участки кода средствами интроспекции соотносятся с программными модулями и функциями.

*Natch* представляет собой набор плагинов для Qemu, которые инструментируют
выполняемый код и существенно замедляют работу эмулятора.
В связи с этим, анализ предлагается проводить с использованием детерминированного воспроизведения.
Детерминированное воспроизведение - это технология, которая позволяет записывать, а затем многократно воспроизводить и анализировать
сценарий работы виртуальной машины.
В нашем случае на записанный сценарий уже не будут оказывать влияния задержки от плагинов анализа,
что очень важно для корректной работы часов реального времени и при взаимодействии с сетью.

Примерный алгоритм получения поверхности атаки может выглядеть следующим образом:

*  Запуск Qemu с плагином *natch*
*  Ожидание загрузки до интересующего момента
*  Включение анализа помеченных данных (если он не был включен автоматически через конфигурационный файл)
*  Выполнение тестового сценария
*  Загрузка полученных данных в веб-интерфейс
*  Анализ и оценка результатов

# <a name="natch_config"></a> 3. Конфигурационные файлы Natch

Для работы инструмента *Natch* требуются конфигурационные файлы. Основной конфигурационный файл отдается непосредственно инструменту на вход, остальные являются источниками настроек для плагинов, входящих в состав *Natch*.

## <a name="main_config"></a> 3.1. Основной конфигурационный файл

Пример файла конфигурации приведен ниже, но пользователю может потребоваться внести в него изменения.
Содержимое файла конфигурации:

```ini
# Natch settings

# Section Version since Natch v.2.0
[Version]
version=1

[Ports]
# 6 is for tcp
ip_protocol=6
# ports are supported for tcp only yet
in=22;80;3500;5432
out=22;80;3500;5432

# threshold value for tainting. should be in decimal number system [0..255]
[Taint]
threshold=50
on=true

# section for loading modules
[Modules]
config=module_config.cfg
log=taint.log
params_log=params.log

# section for loading task_struct offsets
[Tasks]
config=task_config.ini

# section for loading custom syscall config
[Syscalls]
config=custom_x86_64.cfg

# section for enable generating graphs
[TaintedTask]
task_graph=true
module_graph=false

# section for network log. only for record
[NetLog]
on=true
log=netpackets.log

# section for add tainted files
[TaintFile]
list=file1.txt;file2.txt

# output directory for all Natch data

[OutputData]
workdir=/home/user/workdir

# section for getting coverage
[Coverage]
file=coverage.cov64
taint=true

# section for additional plugins
[Plugins]
items=bcqti,broker,addr=:5555;some_plugin

# section for tainted network packets. only for replay
[NetTaintLog]
log=tnetpackets.log
```


