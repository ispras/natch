<div style="page-break-before:always;">
</div>


# <a name="auto"></a>11. Автоматизация процессов

В этом разделе представлено API для получения информации из SNatch, а также показано как можно автоматизировать выполнение сценариев
работы *Natch* от создания проекта до получения финального PDF-отчета на примере наших тестовых сценариев.

## <a name="snatch_cicd">11.1. SNatch CI/CD

API реализовано бэкэндом SNatch, поэтому чтобы им пользоваться, необходимо запустить скрипт `snatch_run.py`, как и при браузерном использовании.

### 11.1.1. ci_create_project

- POST запрос ci_create_project для создания проекта (аналогично проекту в браузерной версии, впоследствии может открываться и из браузера).Сопровождается обязательным параметром file, и необязательными project_name и async.

Пример запроса:
```bash
curl -F "project_name=test_proj_name" -F "async=true" -F "file=@/home/snatch_traces/example.tar.zst" -X POST http://localhost:8000/ci_create_project/
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
curl -X GET -G http://localhost:8000/ci_get_status/ -d task_id=c9596e03-e007-4bac-9d81-837094d54e2b
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
curl -X GET -G http://localhost:8000/ci_get_proj_list/
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
curl -X GET -G http://localhost:8000/ci_get_content/ -d project_id=b9d7d69a-8783-464c-9f1d-5a72ac74678a -d type=callgraph
```
Параметры:

- project_id — идентификатор проекта, полученный в ответе запроса ci_create_project.
- type — тип запрашиваемого содержимого. Может принимать одно из значений:  [callgraph, interp_callgraph, resources, process_tree, files, process_info, process_timeline].

Пример ответа:
```json
{"status": "200", "content": {"graph_list": [{"pname": "gpugi", "proc": 10, "cg_array": [{"0x24e8": ... }}
```
Параметры:

- status — принимает значение "200" для корректного запроса и "400" для ошибочного.
- content — запрашиваемое содержимое в json-формате.

Пример ответа на некорректный запрос:

```json
{"status": "400", "msg": "Can not return content for provided type. Please make sure that type is one of the following: callgraph, interp_callgraph, resources, process_tree, files, process_info, process_timeline."}
```
Параметры:

- status — статус запроса, в случае ошибки всегда будет принимать значение "400".
- msg — сопроводительное сообщение об ошибке.

### 11.1.5. ci_delete_project

- POST запрос ci_delete_project для удаления проекта. Сопровождается необязательным параметром project_id, содержащим id для удаляемого проекта. Если значение id = 0 или не указано, то удалятся все проекты.

Пример запроса:
```bash
curl -F "project_id=b9d7d69a-8783-464c-9f1d-5a72ac74678a"  -X POST http://localhost:8000/ci_delete_project/
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
Средствами `bash` и `expect` возможно автоматизировать создание проекта, запись сценария и его последующее воспроизведение,
а также создание проекта в *SNatch* и проверку его содержания. Затем при помощи `Selenium` *SNatch* запускается в браузере и генерируется PDF отчет.

Автоматизация записи сценария возможна при использовании консольных действий на Linux (через telnet) или Windows 10-11 (при использовании ssh).

**Важно!** Перед использованием автоматизации убедитесь в том, что

* *Natch* установлен и установка зависимостей была выполнена.
* *SNatch*, соответствующий установленной версии *Natch*, установлен, и `snatch_setup.sh` уже выполнялся ранее.

### 11.2.1. Реализация автоматизации

В архиве с тестовым примером (см. раздел [Получение образа и тестовых примеров](4_quickstart.md#test_suite) находится скрипт `automation.sh`,
скрипты автозаписи сценариев для тестовых примеров (`run_record_sample1.exp` и `run_record_sample2.exp`), а также Python-скрипт `snatch.py`.
Необходимо сохранить все файлы в одном каталоге и запустить скрипт `automation.sh`.

Скрипт выполняет следующие действия:

* Устанавливает требующиеся пакеты (expect, selenium и др.).
* Удаляет последний проект, созданный при автоматизированном выполнении.
* Создает новый проект в подкаталоге `autotest`. Создание нового проекта описано в разделе [Создание проекта](6_create_project.md#create_project).

Далее, для каждого из двух примеров:

* Записывает тестовый сценарий, используя скрипт `run_record_sampleX.exp`. Запись сценария вручную описана в разделе [Запись сценария](8_scenario_work.md#record).
* Выполняет воспроизведение записанного сценария. Воспроизведение сценария детально описано в разделе [Воспроизведение сценария](8_scenario_work.md#replay).

После выполнения скрипта в подкаталоге `autotest` появляются архивы `autotest+sample1.tar.zst` и `autotest+sample2.tar.zst` для дальнейшего анализа.

Затем:

* Выполняется запуск предварительно установленного *SNatch*.
* Средствами SNatch CI API (см. раздел [SNatch CI/CD](11_automation.md#snatch_cicd)) сгенерированные архивы загружаются в базу данных *SNatch* (создаются проекты).
В случае ошибки блокировки базы данных *SNatch* (возможно при высокой нагрузке), попытки создания продолжаются до тех пор, пока не происходит ее разблокировка.
* После загрузки проверяется содержимое проектов (Call Graph, Interpreter Call Graph, Resources, Process Tree, Files, Process Info, Process Timeline), и выводится статистика,
содержащая размер в байтах каждого из полученного вывода JSON.
* *SNatch* открывается в браузере, где поочередно открывается каждый проект, выполняется переход на Module Graph для активации этого графа в отчете,
а затем генерируется сам PDF отчет, который в конце сохраняется в каталоге ~/Downloads. Этими действиями управляет `snatch.py` на основе *Selenium*.

### 11.2.2. Адаптация скриптов автоматизации

Скрипты автоматизации содержат комментарии, которые помогут вам адаптировать их под свои проекты. Для этого требуются следующие действия:

#### automation.sh:

* В функции `checkRequirements` отредактируйте параметры `requirements` и `pip_requirements`, указав через пробел пакеты, которые требуется проверить/установить на хост.
* В функции `recAndReplay` измените параметр `samples`, указав через пробел названия тестовых сценариев.
* Эти названия тестовых сценариев соответствуют названиям в именах скриптов `run_record_<scenarioname>.exp`, которые также должны быть созданы.
* В функции `genTaintCfg` отредактируйте генерируемый `taint.cfg` файл (см. раздел [Конфигурационный файл для помеченных данных](17_app_configs.md#taint_config)),
в котором указываются помечаемые файлы, сокеты, протоколы, порты и т.д.

Также необходимо иметь в виду следующее:

* Скрипт ищет qcow2 образ в каталоге со скриптом. Убедитесь в том, что в каталоге только один qcow2 файл или отредактируйте параметр `qcow2Path`.
* Имя проекта `autotest` можно изменить в параметре `projName`.

#### run_record_<scenarioname>.exp:

* Отредактируйте код, начиная с `# OS login`, причем код до `# Connect from host to the VM by telnet to save a snapshot` является подготовительным и не попадет в записываемый сценарий.
Записываемый сценарий, который вы планируете в дальнейшем анализировать, должен начинаться с `# When snapshot is saved, everything is ready to record a scenario`.
Используйте любое руководство по `expect` для получения подробной информации о реализации.
* Для пробрасывания порта из хоста в образ используйте `hostfwd` параметр у `-netdev` строки запуска *Natch* (см. пример в `run_record_sample2.exp`).
* Когда сценарий записан, и ваш скрипт функционирует корректно, вы можете отключить вывод из виртуальной машины. Для этого нужно раскомментировать строку `#log_user 0`

### 11.2.3. Пример автоматической проверки

Выполните скрипт `automation.sh`. При этом появляется описание действий, выполняемых скриптом. Также определяется образ qcow2, который расположен в каталоге со скриптом:

```
ISP RAS Natch - Automation Sample.

The script automatically performs the following:
1. Installs the required packages.
2. Cleans up the previous autotest project.
3. Creates a new project (natch_run.py).
4. For both existing samples:
 ∟ Records a test scenario (run_record_*.exp).
 ∟ Replays it (run_replay.sh).
5. The generated archives are added to Snatch DB using Snatch CI API.
6. The content of the projects is tested by the available options of Snatch CI API.
7. The PDF reports for the projects are generated by Snatch via browser.
The PDF reports are saved to ~/Downloads

Image name: test_image_debian
QCOW2 image: /vms/test_image/test_image_debian.qcow2
Project dir: /vms/test_image/autotest

The script must know the Snatch directory which contains snatch_*.sh.
Warning! Installation (snatch_setup.sh) must be executed before running the further actions.
Enter path to Snatch directory: /
```

На данном этапе требуется ввести полный путь к директории *SNatch*.
По нажатии Enter появляется запрос sudo. После ввода пароля следует установка требующихся компонент.
Затем появляется запрос sudo для создания проекта, после чего запускается создание проекта в `natch_run.py`:

```
spawn /usr/bin/natch/bin/natch_scripts/natch_run.py /vms/test_image/test_image_debian.qcow2

Image: /vms/test_image/test_image_debian.qcow2
OS: Linux

Attention! To successfully create a project you will need a root password

Enter path to directory for project (optional): autotest
Directory for project files /vms/test_image/autotest was created

Checking natch-qemu-img utility...
Utility natch-qemu-img is ok

Common options
Enter RAM size with suffix G or M (e.g. 4G or 256M): 4G
Do you want to run emulator in graphic mode? [Y/n] Y

Network option
Do you want to use ports forwarding? [Y/n] N

Modules part
Do you want to create module config? [Y/n] Y
Enter path to binaries dir: .

Debug info part
Do you want to get debug info for system modules? [Y/n] Y

Generate config file task.cfg? (recommended) [Y/n] Y

Waiting for module config generating
Module config is completed

Your config file module.cfg for modules was created
ELF files found: 4
Map files found: 0

The steps above require a root password

[sudo] password for user:
Mounting img - OK
Files copied from the guest system: 2
Umounting img - OK
Mounting img - OK

...

Settings completed! Now you can launch emulator and enjoy! :)

	Natch in record mode: 'run_record.sh'
	Natch in replay mode: 'run_replay.sh'
	Qemu without Natch: 'run_qemu.sh'
```

По завершении работы `natch_run.py` для виртуальной машины создается diff файл:
```
Formatting '/vms/test_image/autotest/sample1/test_image_debian.diff', fmt=qcow2 cluster_size=65536 extended_l2=off compression_type=zlib size=21474836480 backing_file=/vms/test_image/test_image_debian.qcow2 backing_fmt=qcow2 lazy_refcounts=off refcount_bits=16
```

Следом появляется сообщение ```Recording a sample1 scenario...```. На этом этапе запускается скрипт `run_record_sample1.exp`.
Этот скрипт загружает виртуальную машину и автоматически записывается тестовый сценарий для первого примера.


По завершении работы expect-скрипта активность возвращается к `automation.sh` и возникает сообщение ```Replaying the sample1 scenario...```, а затем:

```
Natch monitor - type 'help' for more information
(natch)
Natch_v.3.0
(c) 2020-2024 ISP RAS

Reading Natch config file...
Natch is working in NORMAL mode

Network logging enabled
Task graph enabled
Module graph enabled
Taint enabled
Config is loaded.
File monitor storage /vms/test_image/autotest/output_sample1/filemon.log created successfully
Module binary log file /vms/test_image/autotest/output_sample1/log_m_b.log created successfully
Modules: started reading binaries
Modules: finished with 82 of 82 binaries for analysis
thread_monitor: identification method is set to a complex developed at isp approach
Started thread monitoring
Tasks: config file is open.
Network json log file: "/vms/test_image/autotest/output_sample1/tnetwork.json"
Taint log storage file /vms/test_image/autotest/output_sample1/taint.log created successfully
Binary call_stack log file /vms/test_image/autotest/output_sample1/log_cs_b.log created successfully
Tainting file: curl.txt
Detected module /vms/test_image/autotest/libs/54ce98cf6f65914636ace17148725666/vmlinux-5.10.0-17-amd64 execution
Detected module /vms/test_image/autotest/libs/9b8f02224b6497f2fd72ebf18d1949a3/libc-2.31.so execution
Detected module /vms/test_image/Sample1_bins/test_sample execution
Detected module /vms/test_image/Sample1_bins/test_sample_2 execution
File /home/user/Sample1/curl.txt is opened, handle = 0x0000000000000003
File /home/user/Sample1/curl.txt is opened, handle = 0x0000000000000001
Detected module /vms/test_image/autotest/libs/2e93e13b373621a7d3aaddacd6701fa8/libssl.so.1.1 execution
Detected module /vms/test_image/autotest/libs/6841efca9a812a58ac478ca5f8233952/libpthread-2.31.so execution
Detected module /vms/test_image/autotest/libs/cb5e1aed69e5825344104409380618b7/libffi.so.7.1.0 execution
Detected module /vms/test_image/autotest/libs/37c74ba908b7557fdc1301b97e4599e2/libkeyutils.so.1.9 execution
Detected module /vms/test_image/autotest/libs/5ca6b88c0086c158c365ccdaee252ea7/libdl-2.31.so execution
Detected module /vms/test_image/autotest/libs/c321937f4b7676d21947a671f6512a9f/libresolv-2.31.so execution
Detected module /vms/test_image/autotest/libs/d861ebb9591e1df1a976daed3647b3da/libkrb5support.so.0.1 execution
Detected module /vms/test_image/autotest/libs/66c3bc8b77614fd5412317f9b504eca0/libcom_err.so.2.1 execution
Detected module /vms/test_image/autotest/libs/fe8eadb6d18a039846578f3c06ff4de7/libk5crypto.so.3.1 execution
Detected module /vms/test_image/autotest/libs/b39a79b8f3c07df3c91e50a2fb8ed970/libkrb5.so.3.3 execution
Detected module /vms/test_image/autotest/libs/4f9f1f95098b2baaba560f5e1ff6f9a3/libgssapi_krb5.so.2.2 execution
Detected module /vms/test_image/autotest/libs/83c9488ccb57383a628a199f9e7b17cb/libcrypto.so.1.1 execution
Detected module /vms/test_image/autotest/libs/8e12a00fd2769b5130e11cf3a773289f/libz.so.1.2.11 execution
Detected module /vms/test_image/autotest/libs/855da59f8deb05d1edb1391aa41a5545/libdb-5.3.so execution
File /home/user/Sample1/curl.txt is opened, handle = 0x0000000000000001

============ Statistics ============

Tainted files             : 1
Tainted packets           : 20
Tainted processes         : 3
Tainted modules           : 3
Tainted file reads        : 0
Tainted memory accesses   : 33166


Compressing data. Please wait..

autotest+sample1.tar.zst completed
```

Далее последние шаги, начиная с создания diff файла, повторяются снова для второго примера. По завершении процедуры для обоих примеров появляется сообщение:

```
These are the archives we will test in Snatch:
/vms/test_image/autotest/autotest+sample1.tar.zst
/vms/test_image/autotest/autotest+sample2.tar.zst
```


Затем запускается *SNatch*, сгенерированные архивы добавляются в него и проходят проверку:

```
Snatch started.
Creating a project sample1
The project sample1 has been created.
Checking content...
   ∟ callgraph size: 194862 bytes
   ∟ interp_callgraph size: 0 bytes
   ∟ resources size: 4643 bytes
   ∟ process_tree size: 2729 bytes
   ∟ files size: 6752 bytes
   ∟ process_info size: 6902 bytes
   ∟ process_timeline size: 8942 bytes
The content check for the project sample1 has been finished.
Creating a project sample2
The project sample2 has been created.
Checking content...
   ∟ callgraph size: 194434 bytes
   ∟ interp_callgraph size: 0 bytes
   ∟ resources size: 3546 bytes
   ∟ process_tree size: 1298 bytes
   ∟ files size: 2485 bytes
   ∟ process_info size: 3099 bytes
   ∟ process_timeline size: 4071 bytes
The content check for the project sample2 has been finished.
```

После чего запускается `snatch.py`. Он открывает браузер, открывается проект, выполняется переход на Module Graph для его активации, а затем генерируется и сохраняется PDF отчет.
Действия повторяются для второго проекта.

```
[WDM] - Downloading: 19.9kB [00:00, 11.2MB/s]
[WDM] - Downloading: 100%|███████████████████████████████████████████████| 3.10M/3.10M [00:00<00:00, 7.11MB/s]
Snatch opened in browser.
Report /home/user/Downloads/report-sample1-24-1-2024.pdf (342.62 KB) has been generated.
Report /home/user/Downloads/report-sample2-24-1-2024.pdf (414.53 KB) has been generated.
```

В результате в каталоге Downloads мы получили PDF отчеты для двух тестовых приложений.

Следует обратить особое внимание, что автоматизация намеренно не очищает базу данных уже загруженных ранее проектов в *SNatch*,
так что, если вы ранее уже загружали свои проекты в него, они не пропадут. Более того, для них также будут сгенерированы отчеты.


