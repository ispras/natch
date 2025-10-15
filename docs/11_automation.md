<div style="page-break-before:always;">
</div>


# <a name="auto"></a>11. Автоматизация процессов

В этом разделе представлено API для получения информации из SNatch, а также показано как можно автоматизировать выполнение сценариев
работы *Natch* от создания проекта до получения финального PDF-отчета на примере наших тестовых сценариев.

## <a name="snatch_cicd">11.1. SNatch CI/CD

API реализовано бэкэндом SNatch, поэтому чтобы им пользоваться, необходимо запустить скрипт `/usr/bin/snatch/snatch_start.sh`, как и при браузерном использовании.
Для выполнения авторизации при запросе требуется использовать ключ `-u "<login>:<password>"`, используя учетные данные созданного в веб-браузере пользователя.

### 11.1.1. ci_create_project

- POST запрос ci_create_project для создания проекта (аналогично проекту в браузерной версии, впоследствии может открываться и из браузера). Сопровождается обязательным параметром file, и необязательными project_name и async.

Пример запроса:
```bash
curl -u "<login>:<password>" -F "project_name=test_proj_name" -F "async=true" -F "file=@/home/snatch_traces/example.tar.zst" -X POST http://localhost:8000/ci_create_project/
```
Параметры:

- file —  путь к архиву, полученному от Natch
- project_name — имя для создаваемого проекта ("default_name" по умолчанию)
- async — для асинхронного создания проекта (по умолчанию False). Если установлен в True, то ответ на запрос вернется сразу и будет содержать дополнительное поле task_id для отслеживания процесса создания. В этом случае пользователь должен самостоятельно определить, в какой момент создание проекта было завершено, чтобы иметь возможность запрашивать его данные. Для состояния False процесс создания проекта будет синхронным, и ответ вернется по его завершении.

Пример ответа:
```json
{"status": "200", "project_id": "b9d7d69a-8783-464c-9f1d-5a72ac74678a", "task_id": "c9596e03-e007-4bac-9d81-837094d54e2b"}
```
Параметры:

- status — принимает значение "200" для корректного запроса и "400" для ошибочного.
- project_id — идентификатор созданного проекта, по которому можно обращаться при запросе содержимого.
- task_id — идентификатор задачи создания проекта. Возвращается, если в запросе использовался параметр "async=true". Используется для уточнения статуса задачи.

### 11.1.2. ci_get_status

- GET запрос ci_get_status для уточнения статуса задачи создания проекта при использовании асинхронного подхода. Сопровождается обязательным параметром task_id.

Пример запроса:
```bash
curl -u "<login>:<password>" -X GET -G http://localhost:8000/ci_get_status/ -d task_id=c9596e03-e007-4bac-9d81-837094d54e2b
```
Параметры:

- task_id — идентификатор задачи, полученный в ответном сообщении запроса ci_create_project.

Пример ответа:
```json
{"status": "200", "state": "SUCCESS", "result": null}
```
Параметры:

- status — принимает значение "200" для корректного запроса и "400" для ошибочного.
- state — описывает состояние выполняемой задачи, и может принимать значения ["REVOKED", "PROGRESS", ..., "SUCCESS"]. Из этих состояний наибольший интерес представляет "PROGRESS", который гласит о корректном процессе выполнения задачи, и "SUCCESS", который обозначает корректное завершение задачи.
- result — содержит сопроводительное сообщение о состоянии задачи.

### 11.1.3. ci_get_proj_list

- GET запрос ci_get_proj_list для запроса списка созданных в SNatch проектов.

Пример запроса:
```bash
curl -u "<login>:<password>" -X GET -G http://localhost:8000/ci_get_proj_list/
```

Пример ответа:

```json
{"status": "200", "proj_list": [{"title": "test_project", "proj_id": "bc5f666f-e5d4-41f8-93ce-e9b99bb5c0d1", "description": ""}]}
```
Параметры:

- status — принимает значение "200" для корректного запроса и "400" для ошибочного.
- proj_list — содержит список созданных (как с помощью автоматизации так и через пользовательский UI) проектов. Каждый элемент списка содержит следующие поля: title — имя проекта; proj_id — идентификатор проекта; description - дополнительная информация о проекте (задаётся через UI).

### 11.1.4. ci_get_content

- GET запрос ci_get_content для получения содержимого проекта. Сопровождается обязательными параметрами project_id и type.

Пример запроса:
```bash
curl -u "<login>:<password>" -X GET -G http://localhost:8000/ci_get_content/ -d project_id=b9d7d69a-8783-464c-9f1d-5a72ac74678a -d type=callgraph
```
Параметры:

- project_id — идентификатор проекта, полученный в ответе запроса ci_create_project.
- type — тип запрашиваемого содержимого. Может принимать одно из значений:  [callgraph, interp_callgraph, resources, process_tree, files, process_info, process_timeline, attack_surface].

Пример ответа:
```json
{"status": "200", "content": {"graph_list": [{"pname": "gpugi", "proc": 10, "cg_array": [{"0x24e8": ... }}
```
Параметры:

- status — принимает значение "200" для корректного запроса и "400" для ошибочного.
- content — запрашиваемое содержимое в json-формате.

Пример ответа на некорректный запрос:

```json
{"status": "400", "msg": "Can not return content for provided type. Please make sure that type is one of the following: callgraph, interp_callgraph, resources, process_tree, files, process_info, process_timeline, attack_surface."}
```
Параметры:

- status — статус запроса, в случае ошибки всегда будет принимать значение "400".
- msg — сопроводительное сообщение об ошибке.

### 11.1.5. ci_delete_project

- POST запрос ci_delete_project для удаления проекта. Сопровождается необязательным параметром project_id, содержащим id для удаляемого проекта. Если значение id = 0 или не указано, то удалятся все проекты.

Пример запроса:
```bash
curl -u "<login>:<password>" -F "project_id=b9d7d69a-8783-464c-9f1d-5a72ac74678a"  -X POST http://localhost:8000/ci_delete_project/
```
Параметры:

- project_id — идентификатор проекта (по умолчанию отсутствует и в этом сценарии удаляет все проекты)
Пример ответа:
```json
{"status": "200", "project_id": "project_id=b9d7d69a-8783-464c-9f1d-5a72ac74678a"}
```
Параметры:

- status — принимает значение "200" для корректного запроса и "400" для ошибочного.
- project_id — идентификатор удаленного проекта.



## <a name="automation"></a>11.2. Автоматизированное выполнение

После обновления *Natch* ранее записанные сценарии могут не работать. Перезапись тестовых сценариев может быть достаточно трудоёмка.
Здесь на помощь приходит автоматизация. Также она будет полезна при необходимости встраивания *Natch* в CI/CD.
Средствами `bash` и `expect` возможно автоматизировать создание проекта, запись сценария и его последующее воспроизведение, а с помощью `python` - создание проекта в *SNatch* и проверку его содержания. Затем при помощи `Selenium` *SNatch* запускается в браузере и генерируется PDF отчет.

Автоматизация записи сценария возможна при использовании консольных действий на Linux (через telnet) или Windows 10-11 (при использовании ssh).

**Важно!** Перед использованием автоматизации убедитесь в том, что

* *Natch* установлен и установка зависимостей была выполнена.
* *SNatch*, соответствующий установленной версии *Natch*, установлен. Для Alt и РЕД ОС также должно быть выполнено конфигурирование и первый запуск.

### 11.2.1. Реализация автоматизации

В архиве с тестовым примером (см. раздел [Получение образа и тестовых примеров](4_launch_test_samples.md#test_suite) находится скрипт `automation.sh`,
шаблоны записи сценариев для тестовых примеров (`run_record_sample1.exp` и `run_record_sample2.exp`), а также Python-скрипты в каталоге `snatch` и вспомогательный скрипт `wait4release.sh`.
Необходимо сохранить все файлы в одном каталоге и запустить скрипт `automation.sh`.

Скрипт выполняет следующие действия:

* Устанавливает требующиеся пакеты (expect, selenium и др.).
* Удаляет последний проект, созданный при автоматизированном выполнении.
* Создает новый проект в подкаталоге `autotest`. Создание нового проекта описано в разделе [Создание проекта](6_create_project.md#create_project).

Далее, для каждого из двух примеров:

* Модифицирует конфигурационный файл qemu_opts.ini, содержащий настройки QEMU.
* На основе шаблона записи сценария создает expect скрипт `record_sampleX.exp` для записи тестового сценария.
* Используя созданный скрипт, записывает тестовый сценарий. Запись сценария вручную описана в разделе [Запись сценария](8_scenario_work.md#record).
* Обновляет конфигурационный файл taint.cfg для пометки данных, которые необходимо отслеживать.
* Выполняет воспроизведение записанного сценария. Воспроизведение сценария детально описано в разделе [Воспроизведение сценария](8_scenario_work.md#replay).
* Вспомогательный скрипт `wait4release.sh` используется для ожидания завершения работы natch и проверки используемого для диагностики порта.
* Выполняет распаковку поверхности атаки. Описание используемой команды смотрите в пункте [natch coverage](3_natch_cmd.md#natch_cmd_coverage)

После выполнения скрипта в подкаталоге `autotest` появляются архивы `autotest+sample1.tar.zst` и `autotest+sample2.tar.zst` для дальнейшего анализа.

Затем:

* Выполняется запуск предварительно установленного *SNatch*.
* *SNatch* открывается в браузере, выполняется создание учетной записи, а затем вход с использованием этой учетной записи.
* Средствами SNatch CI API (см. раздел [SNatch CI/CD](11_automation.md#snatch_cicd)) сгенерированные архивы загружаются в базу данных *SNatch* (создаются проекты).
* После загрузки проверяются различные аналитики содержимого проектов: Call Graph, Interpreter Call Graph, Resources, Process Tree, Files, Process Info, Process Timeline. Также выводится краткая информация, содержащая размер в байтах каждого из полученного вывода JSON и начало блока данных.
* *SNatch* открывается в браузере, где поочередно открывается каждый проект, выполняется переход на Module Graph для активации этого графа в отчете,
а затем генерируется сам PDF отчет, который в конце сохраняется в каталоге ~/Downloads. Этими действиями управляет `snatch.py` на основе *Selenium*.

### 11.2.2. Адаптация скриптов автоматизации

Скрипты автоматизации содержат комментарии, которые помогут вам адаптировать их под свои проекты. Для этого требуются следующие действия:

#### automation.sh:

* В функции `introAndPrompts` в параметре `path2binaries` указывается путь к бинарным файлам. В `place4binaries` указывается `h` в случае расположения бинарных файлов на хосте, `g` - на гостевом образе (виртуальной машине).
* В функции `checkRequirements` отредактируйте параметры `requirements` и `pip_requirements`, указав через пробел пакеты, которые требуется проверить/установить на хост.
* В функции `createProject` можно добавить дополнительные параметры для запуска `natch create` в параметре `natchRun`.
* В функции `recAndReplay` измените параметр `samples`, указав через пробел названия тестовых сценариев.
* Эти названия тестовых сценариев соответствуют названиям в именах скриптов `run_record_<scenarioname>.exp`, которые также должны быть созданы.
* В функции `preRecordConfiguration` отредактируйте путь к `rootFS`, а также перенправляемые порты в `forwPorts`.
* В функции `preReplayConfiguration` отредактируйте генерируемый `taint.cfg` файл (см. раздел [Конфигурационный файл для помеченных данных](app2_configs.md#taint_config)),
в котором указываются помечаемые файлы, сокеты, протоколы, порты и т.д.

Также необходимо иметь в виду следующее:

* Скрипт ищет qcow2 образ в каталоге со скриптом. Убедитесь в том, что в каталоге только один qcow2 файл или отредактируйте параметр `qcow2Path`.
* Имя проекта `autotest` можно изменить в параметре `projName`.

#### run_record_<scenarioname>.exp:

* Отредактируйте код, начиная с `# OS login`, причем код до `# Connect from host to the VM by telnet to save a snapshot` является подготовительным и не попадет в записываемый сценарий.
Записываемый сценарий, который вы планируете в дальнейшем анализировать, должен начинаться с `# When snapshot is saved, everything is ready to record a scenario`.
Используйте любое руководство по `expect` для получения подробной информации о реализации.
* Для пробрасывания порта из хоста в образ используйте `hostfwd` параметр у `-netdev` строки запуска *Natch* (см. пример в `run_record_sample2.exp`).
* Когда сценарий записан, и ваш скрипт функционирует корректно, вы можете отключить вывод из виртуальной машины. Для этого нужно раскомментировать строку `#log_user 0`, которая добавляется в создаваемый скрипт записи сценария в функции `preRecordConfiguration` скрипта `automation.sh`.

#### snatch/snatch.py:

* Отредактировать название и путь к файлу лога можно в строке `logfile =`
* По умолчанию, тесты запускаются в Firefox. Можно использовать Chrome, для этого нужно заменить значение FF на CHROME в строке `useBrowser =`


### 11.2.3. Пример автоматической проверки

Выполните скрипт `automation.sh`. При этом появляется описание действий, выполняемых скриптом. Также определяется образ qcow2, который расположен в каталоге со скриптом:

```
ISP RAS Natch - Automation Sample

It automatically performs the following:
1. Installs the required packages (only for the first time).
2. Cleans up the previous autotest project.
3. Creates a new project (natch create).
4. For both existing samples:
 ∟ Prepares a required configuration (qemu_opts.ini, an expect script for making the record).
 ∟ Records a predefined scenario (natch record).
 ∟ Configuring the tainting (taint.cfg).
 ∟ Replays the recorded scenario (natch replay).
 ∟ Extracts coverage (natch extract coverage).
5. Opens Snatch to create an account and try login.
6. The generated archives are added to Snatch DB using Snatch CI API.
7. The content of the projects is tested by the available options of Snatch CI API.
8. The PDF reports for the projects are generated by Snatch via browser and saved to Downloads directory

Image name:     test_image_debian
QCOW2 image:    /vms/test_image/test_image_debian.qcow2
Project dir:    /vms/test_image/autotest
Modules dir:    /home/user (on guest)

```
По запросу требуется ввести пароль суперпользователя. После этого начнется поиск и установка требующихся пакетов. Пароль сохраняется в файл sudo.pwd в текущую директорию, и в дальнейшем запрашиваться не будет. После ввода пароля следует установка требующихся компонент.
Затем запускается создание проекта командой `natch create`:

```
spawn natch create autotest /vms/test_image/test_image_debian.qcow2
Directory for project files /vms/test_image/autotest was created
OS: Linux

Image: /vms/test_image/test_image_debian.qcow2

-> Attention! To create a project you will need a root password


Checking natch-qemu-img utility...
Utility natch-qemu-img is ok

-> Attention! Some options need to mount your image
Do you agree to mount image? [Y/n] Y

Common options
Enter RAM size with suffix G or M (e.g. 4G or 256M): 4G
Select mode you want to run emulator: graphic [G/g] (default), text [T/t] or vnc [V/v]

Network option
Do you want to use port forwarding? [Y/n] N

Modules part
Do you want to create module config? [Y/n] Y
Select way to point directory with modules - from HOST [H/h] system (default) or GUEST [G/g] system: g
Enter path to binaries dir in guest system (or 'exit' to skip): /home/user

Debug info part
Do you want to get debug info for system modules? [Y/n] Y
Do you want to set additional parameters? (many questions) [y/N] N

Generate config file task.cfg? (recommended) [Y/n] Y

The steps above require a root password

[sudo] password for user:
Mounting Image - OK

[Copying files to host system...]
Status: Found: 2
Umounting Image - OK


──────────────────────── Module Configuration Section ────────────────────────


Mounting Image - OK

[Parsing received folder...]
Status: Found: 2279

[Searching Debugging Information...]
Status: Found: 2 | Skipped: 5

USER statistics:
Images have been found                                            :     OK
Added images                                                      :     7
Added debugging information                                       :     2
Added tied information                                            :     0


ld-linux-* is always skipped and is not counted in calculations
Your config file module.cfg was created
Umounting Image - OK
Mounting Image - OK

...

Your config file '/vms/test_image/autotest/module.cfg' for modules was updated

Configuration file natch.cfg was created.
You can edit it before using Natch.

Settings completed! Now you can launch Natch and enjoy! :)


File 'settings_autotest.ini' was saved here: /vms/test_image
You can use it for creating other projects

Checking the projects completeness...
/vms/test_image/autotest/natch.cfg                 +
/vms/test_image/autotest/qemu_opts.ini             +
/vms/test_image/autotest/service_info.ini          +
/vms/test_image/autotest/module.cfg                +
Everything is fine!

```

Следом появляется сообщение о создании архивной копии qemu_opts.ini. В одном проекте мы будем записывать
два независимых сценария, и поэтому хотим начинать настройку опций QEMU с чистого конфигурационного файла,
сгенерированного при создании проекта.

Далее создается скрипт записи:

```
Created the record script /vms/test_image/autotest/record_sample1.exp
```

После чего стартует запись сценария: ```Recording a sample1 scenario...```. На этом этапе запускается скрипт `record_sample1.exp`.
Этот скрипт загружает виртуальную машину и автоматически записывается тестовый сценарий для первого примера.


По завершении работы expect-скрипта активность возвращается к `automation.sh` и появляется сообщение о том, что была выполнена настройка `taint.cfg`:

```
taint.cfg: set tainting sample.txt
```


Затем запускается воспроизведение записанного сценария:

```
Replaying the sample1 scenario...
spawn natch replay -s sample1 -S autosave

Natch_v.3.4
(c) 2020-2025 ISP RAS

Waiting for the icount 13142751405 to be reached...
Start icount 13142751405 has been reached
Reading Natch config file...
Checking config file '/vms/test_image/autotest/module.cfg'...
Natch is working in NORMAL mode

Network logging enabled
Task graph enabled
Module graph enabled
Taint enabled
Config is loaded.
File monitor storage /vms/test_image/autotest/output_sample1/filemon.log created successfully
Module binary log file /vms/test_image/autotest/output_sample1/log_m_b.log created successfully
Modules: started reading binaries
Modules: finished with 87 of 87 binaries for analysis
thread_monitor: identification method is set to a complex developed at isp approach
Started thread monitoring
Tasks: config file is open.
Network json log file: "/vms/test_image/autotest/output_sample1/tnetwork.json"
Taint log storage file /vms/test_image/autotest/output_sample1/taint.log created successfully
Binary call_stack log file /vms/test_image/autotest/output_sample1/log_cs_b.log created successfully
Tainting file: sample.txt
(natch) Detected module /vms/test_image/autotest/debug_info/guest_system/lib/54ce98cf6f65914636ace1714872566n
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/126d561af479fb6bad3ace2334af40f1/libc-2n
./test_sample
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/0b0c82f0b1cea7f0db918daf79e6f5b6/test_sn
I am a just function
res = 47270
value is even
I am a just function
Address for curl: www.google.com
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/7e29edbe29acf0ed4457899b90f65de5/test_sn
File /home/user/Sample1/sample.txt is opened, handle = 0x0000000000000003
File /home/user/Sample1/sample.txt is opened, handle = 0x0000000000000001
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/cb5e1aed69e5825344104409380618b7/libffin
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/855da59f8deb05d1edb1391aa41a5545/libdb-n
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/2e93e13b373621a7d3aaddacd6701fa8/libssln
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/791f890164e45876863a379f3cc80d7d/libpthn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/37c74ba908b7557fdc1301b97e4599e2/libkeyn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/380061e32442beddc07979d12fc4a1e8/libdl-n
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/d9e8cb528c03d87895f5af76e7da7341/libresn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/d861ebb9591e1df1a976daed3647b3da/libkrbn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/66c3bc8b77614fd5412317f9b504eca0/libcomn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/fe8eadb6d18a039846578f3c06ff4de7/libk5cn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/b39a79b8f3c07df3c91e50a2fb8ed970/libkrbn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/4f9f1f95098b2baaba560f5e1ff6f9a3/libgssn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/83c9488ccb57383a628a199f9e7b17cb/libcryn
Detected module /vms/test_image/autotest/debug_info/guest_system/lib/8e12a00fd2769b5130e11cf3a773289f/libz.sn
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0File /home/user/Sample1/sample.txt is ope1
100 23962    0 23962    0     0   164k      0 --:--:-- --:--:-- --:--:--  164k
result file: sample.txt
user@debian:~/Sample1$
============ Statistics ============

Tainted files             : 1
Tainted packets           : 21
Tainted processes         : 3
Tainted modules           : 3
Tainted file reads        : 0
Tainted memory accesses   : 37518

====================================


Compressing data. Please wait..

autotest+sample1.tar.zst completed
```

После чего выполняется поиск поверхности атаки, результаты которого добавляются в созданный архив:

```
Extract coverage for sample1
spawn natch coverage extract -s sample1
[sudo] password for user:
Mounting Image - OK

[Reading Module Config...]
Status: Found: 7

[Searching Images By Numbers...]
Progress:    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7/7 100% 0:00:00
Status: Found: 7

[Parsing Cov64 Modules...]
Status: Found: 43 | Skipped: 40

[Parsing Cov64 BBs...]
Progress:    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45462/45462 100% 0:00:00
Status: Found: 45462

[Parsing VmiDbs...]
Progress:    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7/7 100% 0:00:01
Status: Found: 7

[Filling Info For Images...]
WARNING: Image ../debug_info/guest_system/lib/80f502f2064bc93c4c673ace7eed5208/redis-check-rdb: Coverage for was not
found!
WARNING: Image ../debug_info/guest_system/lib/6ec6d8037c4dfc1ea5e9fbae56d98d33/redis-benchmark: Coverage for was not
found!
WARNING: Image ../debug_info/guest_system/lib/4e4fc92774670e5c02c60d937d19688c/redis-cli: Coverage for was not found!
WARNING: Image ../debug_info/guest_system/lib/260ebb825b267c3f6d01a8840240299c/lua: Coverage for was not found!
WARNING: Image ../debug_info/guest_system/lib/68b38b1fc4ba765d9cdf4e68f0332e38/luac: Coverage for was not found!
Progress:    ━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2/7  29% 0:00:00
Status: Found: 2 | Skipped: 5

[Generating Lcov...]
Status: Found: 2
Umounting Image - OK
Found 2 entries.
Found common filename prefix "/vms/test_image/autotest/output_sample1/source_files/home/user"
Generating output.
Processing file Sample1/test_sample_2.c
  lines=11 hit=11 functions=2 hit=2
Processing file Sample1/test_sample.c
  lines=41 hit=38 functions=6 hit=6
Overall coverage rate:
  lines......: 94.2% (49 of 52 lines)
  functions......: 100.0% (8 of 8 functions)

Compressing data. Please wait..

Archive autotest+sample1.tar.zst updated!

```


Далее скрипт возвращает нам сгенерированный при создании проекта qemu_opts.ini, включает перенаправление порта,
требующееся для второго сценария, и шаги, начиная с создания скрипта записи, повторяются снова для второго примера.
По завершении процедуры для обоих примеров появляется сообщение:

```
Snatch started.
```

После чего запускается `snatch.py`. Он открывает *SNatch* в браузере, выполняется регистрация учетной записи с произвольным именем пользователя и паролем. Учетные данные выводятся в консоль и записываются в файл `snatch.creds`, в лог и отчет. Браузер закрывается. 

Сгенерированные архивы загружаются в Snatch и проходят проверку:

```
INFO [upload:30] Uploading /vms/_test/autotest/autotest+sample1.tar.zst to Snatch
INFO [upload:53] Upload OK, project_id: 07c497e0-4c2c-472e-8d34-2fbab688ad52
INFO [upload:89] Obtained the callgraph data:
Length: 229950 bytes
Data: [{"pname": "swapper/0", "proc": 1, "cg_array": [{"0x2c95f4": {"children": [{"0x2c91c0": {"children":...
WARNING [upload:85] interp_callgraph data is blank
INFO [upload:89] Obtained the resources data:
Length: 17165 bytes
Data: [{"resources": {"modules": [{"name": "/boot/vmlinuz-5.10.0-17-amd64", "taint": False, "symbolless": ...
INFO [upload:89] Obtained the process_tree data:
Length: 2699 bytes
Data: {"name": ".", "children": [{"proc": 0, "name": "unknown", "children": [], "uids": [], "pid": 0, "arg...
INFO [upload:89] Obtained the files data:
Length: 10002 bytes
Data: [{"name": "/dev/ttyS0", "tainted": 1, "list": [{"proc": 15, "name": "curl", "uids": [{"uid": 1000, "...
INFO [upload:89] Obtained the process_info data:
Length: 6062 bytes
Data: {"processes": {"0": {"proc": 0, "name": "unknown", "parents": "", "cont_name": "", "root": 0, "taint...
INFO [upload:89] Obtained the process_timeline data:
Length: 8711 bytes
Data: {"0": [{"name": "unknown", "start": 0, "end": 1, "root": 0, "tainted": 0, "info": {"name": "unknown"...
INFO [upload:89] Obtained the attack_surface data:
Length: 9169 bytes
Data: [{"files": [], "name": "test_sample", "proc": 7, "tag": "", "root": 0, "tainted": 1, "binaries": [{"...

```

Снова запускается *SNatch* в браузере, открывается первый проект, выполняется переход на `Process Graph`, потом на `Module Graph` для их активации, а затем генерируется и сохраняется PDF отчет.
Действия повторяются для второго проекта.

```
Snatch opened in browser.
Report /home/user/Downloads/report-sample2-16-10-2024.pdf (417.7 KB) has been generated.
Report /home/user/Downloads/report-sample1-16-10-2024.pdf (364.14 KB) has been generated.
```

В результате в каталоге Downloads мы получаем PDF отчеты для двух тестовых приложений.

Следует обратить особое внимание, что автоматизация намеренно не очищает базу данных уже загруженных ранее проектов в *SNatch*, так что, если вы ранее уже загружали свои проекты в него, они не пропадут. Более того, для них также будут сгенерированы отчеты.
