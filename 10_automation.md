<div style="page-break-before:always;">
</div>


# <a name="auto"></a>10. Автоматизация процессов

В этом разделе представлено API для получения информации из SNatch, а также показано как можно автоматизировать выполнение сценариев
работы *Natch* от создания проекта до получения финального PDF-отчета на примере наших тестовых сценариев.

## 10.1. SNatch CI/CD

API реализовано бэкэндом SNatch, поэтому чтобы им пользоваться, необходимо запустить скрипт `snatch_run.py`, как и при браузерном использовании.

### 10.1.1. ci_create_project

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

### 10.1.2. ci_get_status

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

### 10.1.3. ci_get_proj_list

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

### 10.1.4. ci_get_content

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

### 10.1.5. ci_delete_project

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






## <a name="automation"></a>10.2. Автоматизированное выполнение

После обновления Natch ранее записанные сценарии могут не работать. Перезапись тестовых сценариев может быть достаточно трудоёмка. Здесь на помощь приходит автоматизация. Также она будет полезна при необходимости встраивания Natch в CI/CD.
Средствами bash и expect возможно автоматизировать создание проекта, запись сценария и его последующее воспроизведение, а также создание проекта в Snatch и проверку его содержания. Затем при помощи Selenium Snatch запускается в браузере и генерируется PDF отчет.

**Важно!** Автоматизация записи сценария возможна при использовании консольных действий на Linux (через telnet) или Windows 10-11 (при использовании ssh).

#### Реализация автоматизации

В архиве с тестовым примером (см. раздел [Получение образа и тестовых примеров](#test_sample)) находится скрипт automation.sh, скрипты автозаписи сценариев для тестовых примеров (run_record_sample1.exp и run_record_sample2.exp), а также python-скрипт snatch.py. Необходимо сохранить все файлы в одном каталоге, и запустить скрипт automation.sh. Он выполняет следующие действия:

* Проверяет наличие требующихся пакетов (expect, redis-tools, selenium), и устанавливает их в случае отсутствия.
* Удаляет последний проект, созданный при автоматизированном выполнении.
* Создает новый проект в подкаталоге `autotest`. Создание нового проекта описано в разделе [Автоматизированная настройка](#autoconfig).

Далее, для каждого из двух примеров
* Записывает тестовый сценарий, используя скрипт run_record_sampleX.exp. Запись сценария вручную [описана в разделе Запись сценария работы](#record_scenario)
* Выполняет воспроизведение записанного сценария с целью получения объекта анализа. Воспроизведение сценария детально описано в разделе [Воспроизведение сценария и сбор данных для анализа](#replay_scenario).

После выполнения в подкаталоге `autotest` появляются архивы autotest+sample1.tar.zst и autotest+sample2.tar.zst для дальнейшего анализа.

Затем
* Выполняется запуск предварительно установленного Snatch.
* Средствами Snatch CI API (см. раздел [CI/CD](6_snatch.md#66-cicd)) сгенерированные архивы загружаются в базу данных Snatch (создаются проекты).
В случае ошибки блокировки базы данных Snatch (возможно при высокой нагрузке), попытки создания продолжаются до тех пор, пока не происходит ее разблокировка.
* После загрузки проверяется содержание проектов (Call Graph, Interpreter Call Graph, Resources, Process Tree, Files, Process Info, Process Timeline), и выводится статистика, содержащая размер в байтах каждого из полученного вывода JSON.
* Snatch открывается в браузере (Firefox), где поочередно открывается каждый проект, выполняется переход на Module Graph для активации этого графа в отчете, а затем генерируется сам PDF отчет, который в конце сохраняется в каталоге ~/Downloads. Этими действиями управляет snatch.py на основе Selenium. 

#### Адаптация скриптов автоматизации

Скрипты автоматизации содержат комментарии, которые помогут вам адаптировать их под свои проекты. Для этого требуются следующие действия:
automation.sh:

* В функции `checkRequirements` отредактируйте параметры requirements и pip_requirements, указав через пробел пакеты, которые требуется проверить/предложить установить на хост.
* В функции `recAndReplay` можно изменить параметр samples, указав через пробел названия тестовых сценариев.
* Эти названия тестовых сценариев соответствуют названиям в именах скриптов `run_record_<scenarioname>.exp`
* В функции `genTaintCfg` можно отредактировать генерируемый taint.cfg файл (см. раздел [Конфигурационный файл для помеченных данных](4_configs.md#taint_config)), в котором указываются помечаемые файлы, сокеты, протоколы и порты.

Также необходимо иметь в виду следующее:

* Скрипт ищет qcow2 образ в каталоге со скриптом. Убедитесь в том, что в каталоге только один qcow2 файл или отредактируйте параметр `qcow2Path`.
* Имя проекта `autotest` можно изменить в параметре `projName`

run_record_<scenarioname>.exp
* Отредактируйте код, начиная с `# OS login`, причем код до `# Connect from host to the VM by telnet to save a snapshot` является подготовительным и не попадет в записываемый сценарий. Записываемый сценарий, который вы планируете в дальнейшем анализировать, должен начинаться с `# When snapshot is saved, everything is ready to record a scenario`. Используйте любое руководство по expect для получения подробной информации о реализации.
* Для пробрасывания порта из хоста в образ используйте hostfwd параметр у -netdev строки запуска natch (см. пример в run_record_sample2.exp).
* Когда сценарий записан, и ваш скрипт функционирует корректно, вы можете отключить вывод из виртуальной машины. Для этого нужно раскомментировать строку `#log_user 0`

#### Пример автоматической проверки

Выполните скрипт automation.sh.
```bash
#!/bin/bash

introAndPrompts()
{

	echo "ISP RAS Natch - Automation Sample."; echo
	echo "The script automatically performs the following:"
	echo "1. Checks requirements and install the absent packages."
	echo "2. Cleans up the previous autotest project."
	echo "3. Creates a new project (natch_run.py)."
	echo "4. For both existing samples:"
	echo " ∟ Records a test scenario (run_record_*.exp)."
	echo " ∟ Replays it (run_replay.sh)."
	echo "5. The generated archives are added to Snatch DB using Snatch CI API."
	echo "6. The content of the projects is tested by the available options of Snatch CI API."
	echo "7. The PDF reports for the projects are generated by Snatch via browser."; 
	echo "The PDF reports are saved to ~/Downloads"; echo

	# Looking for a qcow2 image in the directory
	qcow2Path=`find . -type f -name "*.qcow2" -exec realpath {} \;`
	imageName=`basename $qcow2Path | grep -o -P '(?<=).*(?=.qcow2)'`
	vmPath=`dirname $qcow2Path`

	projName="autotest"
	projPath="$scriptDir/$projName"

	echo "Image name: $imageName"
	echo "QCOW2 image: $qcow2Path"
	echo "Project dir: $projPath"; echo

	read -p "Press any key to continue."

	checkRequirements

	echo; echo "The script must know the Snatch directory which contains snatch_*.sh."
	echo "Warning! Installation (snatch_setup.sh) must be executed before running the further actions."
	read -p "Enter path to Snatch directory: " -i "/" -e snatchPath; echo

	$snatchPath/snatch_stop.sh

	rm -rf "$projPath"

	# Expect scripts must be executable like bash scripts
	chmod +x $scriptDir/*.exp

}

# Provides validation for the required packages and install if anything is missed
checkRequirements()
{

	# The list of required packages
	requirements="expect redis-tools"

	# For every required package
	for requiredPackage in $requirements
	do
		# Depending on OS (for Alt Linux)
		if [[ $osName == "ALT Workstation" ]]; then
			# Check the required package
			checkInst=`rpm -q $requiredPackage`

			# If the package was already installed, the output starts from its name
			if [[ "$checkInst" != "$requiredPackage"* ]]; then
				sudo apt-get install -y $requiredPackage
			fi

		# For other OS distributions
		else
			# In Russian locale (tested on Astra Linux) the text "ok installed" also appears in English
			checkInst=`dpkg -s $requiredPackage | grep "ok installed"`

			if [ ! -n "$checkInst" ]; then
				sudo apt-get install -y $requiredPackage
			fi
		fi
	done

	pip3_requirements="selenium"

	# Check the required package
	checkInst=`pip3 list --disable-pip-version-check | grep $pip3_requirements`

	if [[ -z  "$checkInst" ]]; then
		pip3 install $pip3_requirements
	fi

}

# Automation creates a project using natch_run.py
createProject()
{

	echo "Creating the project requires sudo privileges."

	readSudoPassword

	/usr/bin/expect -c '
						set timeout -1

	#					log_user 0
						log_file -noappend /tmp/natchtestprojgen.log

						spawn /usr/bin/natch/bin/natch_scripts/natch_run.py '"$qcow2Path"'
						set nrID "$spawn_id"

						expect "Enter path to directory for project (optional): "
						send "'"$projName"'\n"

						expect "Enter RAM size with suffix G or M (e.g. 4G or 256M): "
						send "4G\n"

						expect "Do you want to run emulator in graphic mode? "
						send "Y\n"

						# we will forward ports in another way later
						expect "Do you want to use ports forwarding? "
						send "N\n"

						expect "Do you want to create module config? "
						send "Y\n"

						expect "Enter path to binaries dir: "
						send '".\n"'

						expect "Do you want to get debug info for system modules? " 
						send "Y\n"; 

						expect "Generate config file task.cfg? (recommended) "
						send "Y\n"

						expect {
							"Do you want to see module config log? " { 
								send "N\n"; 

								expect { 
									" password for " { send -i nrID "'"$sudoPwd"'\n" } 
									" пароль для " { send -i nrID "'"$sudoPwd"'\n" } 
								} 
							}

							" password for " { 
								send -i nrID "'"$sudoPwd"'\n";
							}
						
							
							" пароль для " { 
								send -i nrID "'"$sudoPwd"'\n";
							}
						}

						expect -i nrID "Settings completed"
	'

}

readSudoPassword() 
{

    read -s -p "[sudo] password for $USER: " sudoPwd
    until (echo $sudoPwd | sudo -S echo '' 2>/dev/null)
    do
        echo -e '\nSorry, try again.'
        read -s -p "[sudo] password for $USER: " sudoPwd
    done

}

recAndReplay()
{

	# The list of samples
	samples="sample1 sample2"

	# For every sample
	for sample in $samples
	do
		mkdir $projPath/$sample

		# Generate a taint.cfg file containing the taint settings
		genTaintCfg

		# Create a diff file
		/usr/bin/natch/bin/natch-qemu-img create -f qcow2 -b "$qcow2Path" -F qcow2 "$projPath/$sample/$imageName.diff"
		
		echo "Recording a $sample scenario..."
		"$scriptDir/run_record_$sample.exp" "$vmPath" "$projPath" "$sample" "$imageName"

		sleep 5

		echo "Replaying the $sample scenario..."
		cd "$projPath"
		"./run_replay.sh" "$sample" "autosave"
		cd - > /dev/null
	done

	archives=`ls $projPath/*.tar.zst`
	echo -e "These are the archives we will test in Snatch:\n$archives"

}

genTaintCfg()
{

	echo -e "[TaintFile]" >> "$projPath/$sample/taint.cfg"
	echo -e "list=curl.txt" >> "$projPath/$sample/taint.cfg"

	echo -e "[Taint]" >> "$projPath/$sample/taint.cfg"
	echo -e "threshold=255" >> "$projPath/$sample/taint.cfg"
	echo -e "on=true" >> "$projPath/$sample/taint.cfg"

	echo -e "[Ports]" >> "$projPath/$sample/taint.cfg"
	echo -e "dst=-1" >> "$projPath/$sample/taint.cfg"
	echo -e "src=-1" >> "$projPath/$sample/taint.cfg"
	echo -e "ip_protocol=6" >> "$projPath/$sample/taint.cfg"

}

snatchTesting()
{

	snatchStart
	snatchAPI
	python3 ./snatch.py

}

snatchStart()
{

	$snatchPath/snatch_start.sh no-autorun-browser > /dev/null 2>&1

	# Workaround for rabbitmq on Alt Linux
	if [[ $osName == *"Alt"* ]]; then
		/usr/bin/expect -c '
			set timeout -1

			spawn sudo systemctl start rabbitmq

			expect ":"
			send "'"$sudoPwd"'\n"

			expect eof
		'    
	fi

	# Waiting for Snatch to be started
	isDone=0
	while [[ $isDone -eq 0 ]]; do
		if grep -q "ready." "$snatchPath/snatch.log"; then
			echo "Snatch started."
			isDone=1
		else
			sleep 1
		fi
	done

}

snatchAPI()
{

	for archive in $archives
	do

		finished=false
		attempt=1

		while [[ "$finished" == false ]]
		do

			# Grab the project name from the archive name
			projName=`basename $archive | grep -o -P '(?<=\+).*(?=.tar)'`

			echo "Creating a project $projName"

			# Creating the project
			createdProject=`curl -s -F "project_name=$projName" -F "async=false" -F "file=@$archive" -X POST http://localhost:8000/ci_create_project/`

			sleep 1				# to avoid the DB lockout

			# Obtain its status
			state=`echo $createdProject | grep -o -P '(?<="status": ").*(?=",)'`

			# If there was an error
			if [[ $state == '400' ]]; then

				# Grab the error text
				error=`echo $createdProject | grep -o -P '(?<="msg": ").*(?="})'`

				# in case of the "database is locked" we will try again and again
				if [[ "$error" == "database is locked" ]]; then
					echo "Attempt #$attempt. Database is currently locked, will try again in a minute."
					sleep 60
					attempt=$((attempt+1))

				else
					echo "Creating a project $projName resulted in the error: $error"
					finished=true
				fi

			# If no errors
			elif [[ $state == '200' ]]; then
				
				echo "The project $projName has been created."

				# Obtain the project ID
				projectID=`echo $createdProject | grep -o -P '(?<="project_id": ").*(?="})'`

				echo "Checking content..."
				check_content callgraph
				check_content interp_callgraph
				check_content resources
				check_content process_tree
				check_content files
				check_content process_info
				check_content process_timeline

				echo "The content check for the project $projName has been finished."
				finished=true

			fi

		done

	done	

}

# Function for checking the content
# $1 is the passed type of check
check_content()
{

	content=`curl -s -X GET -G http://localhost:8000/ci_get_content/ -d project_id=$projectID -d type=$1`
	content=`echo $content | grep -o -P '(?<="content": {).*(?=")'`

	sleep 1				# to avoid the DB lockout

	# Won't display the content but will display the size
	contentSize=${#content}
	echo "   ∟ $1 size: $contentSize bytes"

	i=$((i+1))
}

#########################

# Current directory
scriptDir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# OS distribution
osName=`grep '^NAME' /etc/os-release | grep -o '".*"' | sed 's/"//g'`

introAndPrompts
createProject
recAndReplay
snatchTesting
```

При этом появляется описание действий, выполняемых скриптом. Также определяется образ qcow2, который расположен в каталоге со скриптом:
```
ISP RAS Natch - Automation Sample.

The script automatically performs the following:
1. Checks requirements and install the absent packages.
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

Press any key to continue.
```

По нажатии любой кнопки вначале появляется запрос sudo. После ввода пароля следует проверка требующихся компонент, которые устанавливаются в случае отсутствия.

Далее появляется сообщение:
```
The script must know the Snatch directory which contains snatch_*.sh.
Warning! Installation (snatch_setup.sh) must be executed before running the further actions.
Enter path to Snatch directory: /
```

Требуется ввести полный путь к директории Snatch. 
**Важно!** Убедитесь, что snatch_setup.sh уже выполнялся ранее.

После ввода пути возникает сообщение ```Creating the project requires sudo privileges``` и может потребоваться ввести пароль sudo заново, после чего запускается создание проекта в natch_run.py:
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

[sudo] password for gteys: 
Mounting img - OK                                                                                             
Files copied from the guest system: 2                                                                         
Umounting img - OK                                                                                            
Mounting img - OK                                                                                             


──────────────────────────────────────── Libraries Searching Section ─────────────────────────────────────────


Reading module config - OK                                                                                    
Searching Binary Files...                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4/4 100% 0:00:00
Searching Binary Files - OK                                                                                   
Searching Kernel Symbols - OK                                                                                 
Searching Python Symbols - OK                                                                                 
Searching Java symbols - OK                                                                                   
Searching Shared Libraries...                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 50/50 100% 0:00:01
Searching Shared Libraries - OK                                                                               


─────────────────────────────────────── Library-Debug Matching Section ───────────────────────────────────────


Method: Search For Installed Debug Symbols                                                                    
Getting debug information from default locat... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  0/78   0% 0:00:00
Search For Installed Debug Symbols - OK                                                                       
Method: DebugInfoD                                                                                            
[DebuginfoD]: Searching debugging information...                                                              

[DebuginfoD]: Download debugging information - OK                                                             
[DebuginfoD]: Searching tieddebug information...                                                              

[DebuginfoD]: Download tieddebug information - OK                                                             
Umounting img - OK                                                                                            


─────────────────────────────────────────────── Result Section ───────────────────────────────────────────────


Module config statistics:                                                                                     
In module config there were modules                               :     4                                     
Binaries files in qcow2 found                                     :     4                                     
                                                                                                              
Python statistics:                                                                                            
Python symbols have been found                                    :     OK                                    
Added Python symbols                                              :     46                                    
Added debugging information for Python                            :     46                                    
                                                                                                              
Java statistics:                                                                                              
WARNING: Java symbols have been found                             :     NO                                    
                                                                                                              
Kernel statistics:                                                                                            
Kernel symbols have been found                                    :     OK                                    
Added Kernel symbols                                              :     1                                     
Added debugging information for Kernel                            :     1                                     
                                                                                                              
Shared library Statistics:                                                                                    
Added shared libraries                                            :     31                                    
Added debugging information for shared libraries                  :     31                                    
Added debugging information for tied files                        :     2                                     
ld-linux-* is always skipped and isn't counted in calculations                                                
                                                                                                              
Your config file '/vms/test_image/autotest/module.cfg' for modules was updated            
```

Через пару минут появляется окно Natch, проходит тюнинг, а затем создание базы символьной информации:
```
Tuning process will be started soon. Please, do not close the emulator
Three...
Two..
One.
Go!
Natch monitor - type 'help' for more information
(natch) 
Natch_v.2.4_work-8103-g2ae3f27bbb
(c) 2020-2023 ISP RAS

Reading Natch config file...
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
Detected 42766 system events
Detected 20 of 20 kernel-specific parameters. Creating config file...

Tuning completed successfully!

Symbol info part
Reading symbols for loaded modules                                                                            
Created symbol database for /vms/test_image/Sample2_bins/redis-cli                        
Created symbol database for /vms/test_image/Sample2_bins/redis-server                     
Created symbol database for /vms/test_image/Sample1_bins/test_sample                      
Created symbol database for /vms/test_image/Sample1_bins/test_sample_2                    
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/54ce98cf6f65914636ace17148725666/vmlinux-5.10.0-17-amd64    
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/eed19130c94a3a667d8ce347f88776ec/_queue.cpython-39-x86_64-linux-gnu.so                                                                                                    
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/ed8680738e7177e62f490b7f961ec056/audioop.cpython-39-x86_64-linux-gnu.so                                                                                                   
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/f36724732f33c9099e41968c0213a2f6/termios.cpython-39-x86_64-linux-gnu.so                                                                                                   
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/e1e62ad1ca37ffa79b8d1a267d7c85dd/_xxtestfuzz.cpython-39-x86_64-linux-gnu.so                                                                                               
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/67da82f5773d2cf96693129ac374f3c1/_zoneinfo.cpython-39-x86_64-linux-gnu.so                                                                                                 
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/888024fc34fffc4d1ac95add43b5f310/_testinternalcapi.cpython-39-x86_64-linux-gnu.so                                                                                         
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/383caaebe71f739bb75a83b5c4ff07c6/_posixshmem.cpython-39-x86_64-linux-gnu.so                                                                                               
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/0ec5955dddd26dc7a91667eb36e16b86/_lzma.cpython-39-x86_64-linux-gnu.so                                                                                                     
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/5b9b79d678f0d4c1828ff5d100d3774c/_codecs_iso2022.cpython-39-x86_64-linux-gnu.so                                                                                           
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/aee386fd7820c661ad8e704bc1635a58/_multiprocessing.cpython-39-x86_64-linux-gnu.so                                                                                          
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/04dbf3567b07ef68049c4593c1965c1f/_codecs_tw.cpython-39-x86_64-linux-gnu.so                                                                                                
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/2c44d8f9652d3e049393706808f3660a/_dbm.cpython-39-x86_64-linux-gnu.so                                                                                                      
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/7db6b1296d730aa62372b17ae88913f4/_curses.cpython-39-x86_64-linux-gnu.so                                                                                                   
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/76738a48bcb763647f5556bb73e9d380/_codecs_jp.cpython-39-x86_64-linux-gnu.so                                                                                                
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/ea4508b0f4d55e69f36e225475932feb/_testbuffer.cpython-39-x86_64-linux-gnu.so                                                                                               
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/bd1f84b536a4461b194016c860664de2/_opcode.cpython-39-x86_64-linux-gnu.so                                                                                                   
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/841c4462971ec21bba603eeaf2b5c555/_multibytecodec.cpython-39-x86_64-linux-gnu.so                                                                                           
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/19ac77ce1c5e1fbe0c28127a4be1b71e/_codecs_cn.cpython-39-x86_64-linux-gnu.so                                                                                                
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/f879047d8d1f6f872351765820037dd2/_bz2.cpython-39-x86_64-linux-gnu.so                                                                                                      
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/bdaa61ac6c76855ae36bcd53259976f8/_sqlite3.cpython-39-x86_64-linux-gnu.so                                                                                                  
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/4b6a8db66faa09206d9234e9cf3021de/python3.9                  
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/c6945f4d2e79386790f4d194976b4a76/_hashlib.cpython-39-x86_64-linux-gnu.so                                                                                                  
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/71342849b738edcaa7d480a27b4632a9/_asyncio.cpython-39-x86_64-linux-gnu.so                                                                                                  
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/08ba69183e66bd88f76895949745a4af/_testmultiphase.cpython-39-x86_64-linux-gnu.so                                                                                           
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/90a94574fe18e77602202ed442c540b2/xxlimited.cpython-39-x86_64-linux-gnu.so                                                                                                 
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/84e35244db894c62c2879dbac35d68b6/_xxsubinterpreters.cpython-39-x86_64-linux-gnu.so                                                                                        
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/d69445d05d65e1a242ce652b820e75a3/_testcapi.cpython-39-x86_64-linux-gnu.so                                                                                                 
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/1f370f45ae02f961220a4814d4abd9cc/nis.cpython-39-x86_64-linux-gnu.so                                                                                                       
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/94937b512919cda50a24f61e3a144da4/resource.cpython-39-x86_64-linux-gnu.so                                                                                                  
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/18cd6afe460c8426ab1049958f1f04e1/_ctypes_test.cpython-39-x86_64-linux-gnu.so                                                                                              
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/caca0e629f8ad54127cc082e21189731/_decimal.cpython-39-x86_64-linux-gnu.so                                                                                                  
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/474a704a55eb2427025d92747e841959/_crypt.cpython-39-x86_64-linux-gnu.so                                                                                                    
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/66e5a0cc6f3b3dc750587f05464ffbe0/_testimportmultiple.cpython-39-x86_64-linux-gnu.so                                                                                       
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/4ec8e956625a0cd776c7060c7c4dd7de/_codecs_hk.cpython-39-x86_64-linux-gnu.so                                                                                                
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/c7202c836366bd6706d0bd09e2b6fb3d/_curses_panel.cpython-39-x86_64-linux-gnu.so                                                                                             
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/0c6fa7fca2772bf9e781525d06dd73a1/_ssl.cpython-39-x86_64-linux-gnu.so                                                                                                      
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/a3eb1e0675288741a9e5df3b8034f63b/_lsprof.cpython-39-x86_64-linux-gnu.so                                                                                                   
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/6566ceeba0809f3b1026deaf453ed917/_uuid.cpython-39-x86_64-linux-gnu.so                                                                                                     
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/a398b2fafd9b8f2fa8d310b4342332d7/mmap.cpython-39-x86_64-linux-gnu.so                                                                                                      
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/7d9d945cf69fa3f06716e03be929d6b4/_ctypes.cpython-39-x86_64-linux-gnu.so                                                                                                   
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/1b3c372cab4e9232c7ea2647f2fba24b/ossaudiodev.cpython-39-x86_64-linux-gnu.so                                                                                               
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/b4877771881ff44c8b640df1584e95e8/_json.cpython-39-x86_64-linux-gnu.so                                                                                                     
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/08c50faa2fac0d3aec139058335fa2fd/parser.cpython-39-x86_64-linux-gnu.so                                                                                                    
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/cf527be5d3db1d7ac7c37ec2623c1eb3/_codecs_kr.cpython-39-x86_64-linux-gnu.so                                                                                                
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/51b3d5f432bec89b175d0b14f660a7a5/readline.cpython-39-x86_64-linux-gnu.so                                                                                                  
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/0fa5d0ec4d61d93e307c7070a650b221/_contextvars.cpython-39-x86_64-linux-gnu.so                                                                                              
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/9b8f02224b6497f2fd72ebf18d1949a3/libc-2.31.so               
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/9d20d3847422d29c8fec65a5b44a2ef2/libm-2.31.so               
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/6841efca9a812a58ac478ca5f8233952/libpthread-2.31.so         
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/dda624224ccc71f136d0d31c837b6be6/librt-2.31.so              
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/6d00aae5aa9005f3320fd78d8cc17c20/liblzma.so.5.2.5           
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/5ca6b88c0086c158c365ccdaee252ea7/libdl-2.31.so              
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/855da59f8deb05d1edb1391aa41a5545/libdb-5.3.so               
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/c3de0b3ee5a60484e1c9965f4de7adbd/libtinfo.so.6.2            
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/5b631ba18c08ab580859eeb7a95337b3/libncursesw.so.6.2         
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/8fac8f3edb2ea0da11863f8fb7cb5158/libbz2.so.1.0.4            
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/64345961ae5d3add53341adb0511f82d/libsqlite3.so.0.8.6        
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/8e12a00fd2769b5130e11cf3a773289f/libz.so.1.2.11             
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/7dbb06b0b34d7e54523f00c0703af051/libexpat.so.1.6.12         
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/acf3efc768da6720019c8820473b96b8/libutil-2.31.so            
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/83c9488ccb57383a628a199f9e7b17cb/libcrypto.so.1.1           
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/a515e1a63090ec10e0a8ca7d7c93b021/libnsl.so.2.0.1            
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/2e0b356ad89a7566022fcbd2ed362bcc/libtirpc.so.3.0.0          
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/4f9f1f95098b2baaba560f5e1ff6f9a3/libgssapi_krb5.so.2.2      
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/d861ebb9591e1df1a976daed3647b3da/libkrb5support.so.0.1      
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/fe8eadb6d18a039846578f3c06ff4de7/libk5crypto.so.3.1         
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/66c3bc8b77614fd5412317f9b504eca0/libcom_err.so.2.1          
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/b39a79b8f3c07df3c91e50a2fb8ed970/libkrb5.so.3.3             
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/37c74ba908b7557fdc1301b97e4599e2/libkeyutils.so.1.9         
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/c321937f4b7676d21947a671f6512a9f/libresolv-2.31.so          
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/b55f0a03af7958f26e6f90344d8344bd/libmpdec.so.2.5.1          
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/0f7c29fad209f3c1e245c0410016f541/libcrypt.so.1.1.0          
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/f0547fdc13079257d974515d68115421/libpanelw.so.6.2           
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/2e93e13b373621a7d3aaddacd6701fa8/libssl.so.1.1              
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/7e4a2af8d6beb462ca4f10954fd94f1a/libuuid.so.1.3.0           
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/cb5e1aed69e5825344104409380618b7/libffi.so.7.1.0            
Created symbol database for                                                                                   
/vms/test_image/autotest/libs/28598832a44cc1a2556cba6069c8f153/libreadline.so.8.1         
                                                                                                              
Your config file '/vms/test_image/autotest/module.cfg' for modules was updated            

Configuration file natch.cfg was created.
You can edit it before using Natch.

Settings completed! Now you can launch emulator and enjoy! :)

	Natch in record mode: 'run_record.sh'
	Natch in replay mode: 'run_replay.sh'
	Qemu without Natch: 'run_qemu.sh'
```

По завершении работы natch_run.py для виртуальной машины создается diff файл:
```
Formatting '/vms/test_image/autotest/sample1/test_image_debian.diff', fmt=qcow2 cluster_size=65536 extended_l2=off compression_type=zlib size=21474836480 backing_file=/vms/test_image/test_image_debian.qcow2 backing_fmt=qcow2 lazy_refcounts=off refcount_bits=16
```

Следом появляется сообщение ```Recording a sample1 scenario...```. На этом этапе запускается скрипт run_record_sample1.exp:
```bash
#!/usr/bin/expect -f

set timeout -1

# Params obtained from the parent script (automation.sh)
set vmPath [lindex $argv 0]
set projPath [lindex $argv 1]
set sample [lindex $argv 2]
set imageName [lindex $argv 3]

# Uncomment the line below to disable the VM output
log_user 0

log_file -noappend /tmp/$sample-record.log

# Boot the VM
# To use the approach with your VM ensure to grab the initrd.img and vmlinuz from root dir on your VM
spawn /usr/bin/natch/bin/natch-qemu-x86_64 \
-monitor tcp:localhost:45654,server,nowait \
-nographic \
-m 4G \
-initrd $vmPath/initrd.img \
-kernel $vmPath/vmlinuz \
-append "root=/dev/sda1 console=ttyS0" \
-os-version Linux \
-icount shift=1,rr=record,rrfile=$projPath/$sample/record.bin,rrsnapshot=record \
-drive file=$projPath/$sample/$imageName.diff,if=none,id=disk \
-drive driver=blkreplay,if=none,image=disk,id=disk-rr \
-device ide-hd,drive=disk-rr \
-netdev user,id=net0, \
-device e1000,netdev=net0 \
-object filter-replay,id=replay,netdev=net0 \
-plugin natch,config=$projPath/natch.cfg,replay=$sample

set vmID $spawn_id

# OS login
expect -i vmID "login: "	{ send -i vmID "user\n" }
expect -i vmID "Password: "	{ send -i vmID "user\n" }

# Switch to the sample directory
expect -i vmID "$ "         { send -i vmID "cd Sample1\n" }
expect -i vmID "$ "

# Connect from host to the VM by telnet to save a snapshot
spawn telnet localhost 45654
set tnID "$spawn_id"
expect "(natch) "
send -i tnID "savevm autosave\n"
expect -i tnID "(natch) "

# When snapshot is saved, everything is ready to record a scenario

# Execute a test app
send -i vmID "./test_sample\n"

# When the application execution is completed, the OS prompt is expected
expect -i vmID "$ "
```

Этот скрипт загружает виртуальную машину и автоматически записывается тестовый сценарий для первого примера. 

По завершении работы expect-скрипта активность возвращается к automation.sh и возникает сообщение ```Replaying the sample1 scenario...```, а затем 
```
Natch monitor - type 'help' for more information
(natch) 
Natch_v.2.4_work-8103-g2ae3f27bbb
(c) 2020-2023 ISP RAS

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


Затем запускается Snatch, сгенерированные архивы добавляются в него и проходят проверку:
```
Snatch started.
Creating a project sample1
The project sample1 has been created.
Checking content...
   ∟ callgraph size: 194862 bytes
   ∟ interp_callgraph size: 0 bytes
   ∟ resources size: 0 bytes
   ∟ process_tree size: 2729 bytes
   ∟ files size: 0 bytes
   ∟ process_info size: 6902 bytes
   ∟ process_timeline size: 8942 bytes
The content check for the project sample1 has been finished.
Creating a project sample2
The project sample2 has been created.
Checking content...
   ∟ callgraph size: 194434 bytes
   ∟ interp_callgraph size: 0 bytes
   ∟ resources size: 0 bytes
   ∟ process_tree size: 1298 bytes
   ∟ files size: 0 bytes
   ∟ process_info size: 3099 bytes
   ∟ process_timeline size: 4071 bytes
The content check for the project sample2 has been finished.
```

После чего запускается snatch.py:
```python
import datetime as dt                                        				# to get time in a delta format
import glob													 				# to search the web driver
import os  																	# to manipulate the dirs and files
import time 																# to hardcode the delays
from pathlib import Path                                        			# to obtain a home directory
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains    		# to move cursor to an element
from selenium.webdriver.common.by import By									# to locate an element
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait						# to wait for an element
from selenium.webdriver.support import expected_conditions
from webdriver_manager.firefox import GeckoDriverManager


class SnatchTesting():

	# Initialize browser
	def initBrowser():

		global driver

		# These options are to configure the saving PDFs
		options = FirefoxOptions()
		options.set_preference("browser.download.folderList", '2')
		options.set_preference("browser.download.manager.showWhenStarting", False)
		options.set_preference("browser.download.dir", "~/Downloads")
		options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
		options.set_preference("browser.helperApps.alwaysAsk.force", False)

		options.set_preference("pdfjs.disabled", True)

		options.set_preference("plugin.scan.Acrobat", "99.0")
		options.set_preference("plugin.scan.plid.all", False)

		# Try to install the webdriver
		try:
			driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

		# Sometimes we may get issues with the driver installation, so we can try to bypass the installation 
		# and use the previously downloaded driver
		except Exception as error:
			driverDir = str(Path.home()) + "/.wdm/drivers/geckodriver/linux64/"
			lastUsedDriverPath = max(glob.glob(os.path.join(driverDir, '*/')), key=os.path.getmtime) + "geckodriver"
			driver = webdriver.Firefox(service=FirefoxService(lastUsedDriverPath), options=options)

		isDone = False
		attempt = 1
		# Sometimes a page cannot be opened in a browser from the first attempt
		while (not isDone) and (attempt < 10):
			try:
				# Open Snatch in the browser
				driver.get("http://127.0.0.1:8000")
				isDone = True
				print(f"Snatch opened in browser.")

			except Exception as error:
				print(f"Snatch cannot be opened: {error}, attempt #{attempt}.")
				time.sleep(5)
				attempt += 1

	def waitFor(what):

		loaded = WebDriverWait(driver, 10).until(
			expected_conditions.visibility_of_element_located((By.XPATH, what))
		)

	def switchAndClick(what):

		# Very often the usual function click() does not work, below is the best solution:
		driver.execute_script('arguments[0].scrollIntoView(true);', what)
		actions.move_to_element(what).click().perform()

		# Scroll up to the top
		topElement = driver.find_element(By.XPATH, "//div[@class='inner_menu_bar']")
		driver.execute_script("return arguments[0].scrollIntoView(true);", topElement)



SnatchTesting.initBrowser()

locale = os.getenv('LANG')

actions = ActionChains(driver)

# Get the date in a required format
date = dt.date.today()

# Downloads folder depends on a locale
if "ru_RU" in locale:
	downloadsFolder = '/Загрузки/'
else:
	downloadsFolder = '/Downloads/'

# Wait for the page load
SnatchTesting.waitFor("//span[@data-bs-toggle='dropdown']")

# Open Projects menu
projectMenu = driver.find_element(By.XPATH, "//span[@data-bs-toggle='dropdown']")
SnatchTesting.switchAndClick(projectMenu)
SnatchTesting.waitFor("//button[@data-bs-target='#newProjModal']")

# Obtain the list of added projects
projects = driver.find_elements(By.XPATH, "//*[@id='projectsList']/li[@class='li_elem']")

# For every project
for project in projects:

	# Open the project
	SnatchTesting.switchAndClick(project)
	SnatchTesting.waitFor("//button[@id='moduleGraph']")

	# Grab the app name from the page title
	appName = driver.find_element(By.XPATH, "//title").get_attribute('innerHTML').strip()

	# Full path to the expected PDF report
	pdfRepFile = str(Path.home()) + downloadsFolder + "report-" + appName + "-" + str(date.day) + "-" + str(date.month) + "-" + str(date.year) + ".pdf"

	# If the file already exists, we will remove it
	if os.path.isfile(pdfRepFile) == True:
		os.remove(pdfRepFile)
	
	# Open the Module graph just to have the report to include it
	mGraph = driver.find_element(By.XPATH, "//button[@id='moduleGraph']")
	SnatchTesting.switchAndClick(mGraph)
	SnatchTesting.waitFor("//button[@data-tab-id='moduleGraph']")

	# Open Project menu
	SnatchTesting.switchAndClick(projectMenu)
	SnatchTesting.waitFor("//button[@data-bs-target='#reportModal']")

	# Open "Export to PDF" dialog
	exportBtn = driver.find_element(By.XPATH, "//button[@href='#reportModal']")
	SnatchTesting.switchAndClick(exportBtn)
	SnatchTesting.waitFor("//div[@id='reportModal']/div/div/div/h5[@class='modal-title']")

	# Generate the report
	genReport = driver.find_element(By.XPATH, "//button[@id='generateReport']")
	SnatchTesting.switchAndClick(genReport)

	noSpinner = 0
	# While the report is generating we see a spinner, so we have to wait
	while os.path.isfile(pdfRepFile) == False and noSpinner == 0:
		try:
			generationSpinner = driver.find_element(By.XPATH, "//div[@id='globalSpinner' and contains(@class,'block')]/div/h1[@id='globalSpinnerText']")
			# Still generating...
			time.sleep(0.1)

		except Exception as error:
			# The generating spinner disappeared
			noSpinner = 1

	attempt = 0
	# The file appears in the directory not immediately, so we still have to wait
	while ( os.path.isfile(pdfRepFile) == False ) and ( attempt < 50 ):
		time.sleep(0.1)
		attempt += 1

	# If the file appeared in the dir
	if os.path.isfile(pdfRepFile):

		# Sometimes we may see an error, this is just to handle it
		try:
			alertBox = driver.find_element(By.XPATH, f"//div[contains(@class,'alert-danger')]/div")
			alertText = alertBox.get_attribute('innerHTML').strip()

			print(f"Report generation caused the error: {alertText}.")

			# Close the alert box
			alertClose = driver.find_element(By.XPATH, f"//*[@id='alertPlaceholder']/div[*]/div/button")
			alertClose.click()

		# Otherwise everything is fine
		except:
			print(f"Report {pdfRepFile} ({round(os.path.getsize(pdfRepFile)/1024, 2)} KB) has been generated.")


	# If the generation spinner disappeared but the archive was not created
	elif noSpinner == 1:
		print("The report was not created (please check the downloaded files in the browser) or the generating was suddenly stopped.")

	# Again open the Project menu
	SnatchTesting.switchAndClick(projectMenu)

# Close the browser
driver.close()

```
Он открывает Firefox. Открывается проект, выполняется переход на Module Graph для его активации, а затем генерируется и сохраняется PDF отчет.
Действия повторяются для второго проекта.
```
[WDM] - Downloading: 19.9kB [00:00, 11.2MB/s]
[WDM] - Downloading: 100%|███████████████████████████████████████████████| 3.10M/3.10M [00:00<00:00, 7.11MB/s]
Snatch opened in browser.
Report /home/gteys/Downloads/report-sample1-24-1-2024.pdf (342.62 KB) has been generated.
Report /home/gteys/Downloads/report-sample2-24-1-2024.pdf (414.53 KB) has been generated.
```

В результате в каталоге Downloads мы получили PDF отчеты для двух тестовых приложений.
Следует обратить особое внимание, что автоматизация намеренно не очищает базу данных уже загруженных ранее проектов в Snatch, так что, если вы ранее уже загружали свои проекты в него, они не пропадут; более того, - для них также будут сгенерированы отчеты.

