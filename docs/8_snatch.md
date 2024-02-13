<div style="page-break-before:always;">
</div>

# <a name="snatch"></a>8. Анализ поверхности атаки с помощью SNatch

*SNatch* – это инструмент с графическим интерфейсом, предназначенный для постобработки и отображения данных, полученных от инструмента *Natch*. Работать с этим интерфейсом можно через браузер.

## 8.1. Системные требования

Тестирование инструмента проводилось на ОС Ubuntu 20.04, Ubuntu 22.04, Debian 11 и Alt 10. В качестве браузеров использовались Google Chrome версии 105.0.5148.2 и выше и Mozilla Firefox версии 101.0 и выше.

## 8.2. Настройка и запуск

Установка *SNatch* описана в подразделе [Установка графической подсистемы SNatch](2_setup.md#setup_snatch).

В комплект поставки входят скрипты *snatch_start.sh* и *snatch_stop.sh* для запуска и остановки *SNatch* соответственно. Скрипт *snatch_start.sh* запускает необходимые для работы службы, а также открывает браузер с интерфейсом. В терминал, из которого был запущен скрипт, будут приходить сообщения от сервера, однако, он свободен для использования, поэтому по окончании работы из него же можно запустить скрипт *snatch_stop.sh* для остановки служб. Запускать *snatch_stop.sh* следует всегда, в противном случае процессы останутся висеть в памяти вашего компьютера до перезагрузки.

Все скрипты для *SNatch* можно запускать из любого расположения. Если по какой-то причине при запуске
*snatch_start.sh* страница в браузере не загрузилась, но при этом службы запустились, следует обновить страницу.

После выполнения скрипта *snatch_start.sh* в этом же терминале начнут выводиться информационные сообщения о работе *SNatch* и сообщения о возникающих ошибках. Полученные сообщения можно использовать для отслеживания внутреннего процесса работы *SNatch* и в качестве данных при формировании обращений об обнаруженных багах. Помимо этого ведется логирование работы в файл *snatch.log*, который расположен в папке *Snatch*.

## 8.3. Работа со *SNatch*

<img src=images/snatch/snatch_main_ui.png><figcaption>_Окно SNatch_</figcaption>

На данном рисунке показано окно *SNatch*, где цифрами обозначены основные элементы интерфейса:

1. Кнопка для вызова главного меню, из которого можно создать новый проект, запустить ряд функций, относящихся к открытому проекту, и открыть существующий проект.
2. Меню открытого проекта. Содержит список доступных данных для проекта (таких как: граф процессов, граф модулей, дерево процессов, граф вызовов и т.д.)
3. Кнопка для сворачивания меню проекта.
4. Кнопка для генерации дополнительных графов для проекта (граф вызовов, граф вызовов интерпретаторов и флейм граф).
5. Название открытого проекта. По нажатию на элемент активируется режим редактирования, и имя проекта можно изменить.
6. Панель открытых вкладок с содержимым. Каждая вкладка содержит имя и кнопку закрытия. Также на панели представлена кнопка для быстрого закрытия всех вкладок.
7. Кнопки для выбора языка интерфейса (русский/английский).
8. Окно отображения содержимого.

### 8.3.1. Главное меню
Главное меню предоставляет доступ к созданию нового проекта, настройкам, экспорту открытого проекта в .pdf и информации о проекте. Также здесь отображается список существующих проектов, открытие которых осуществляется по нажатию на имя, а удаление – по нажатию на кнопку с изображением корзины рядом с именем (для удаления всех проектов можно нажать на изображение корзины рядом с заголовком "проекты").

<img src=images/snatch/snatch_menu.png><figcaption>_Главное меню_</figcaption>


#### 8.3.1.1. Создание проекта

Для создания нового проекта необходимо выбрать в главном меню пункт *Новый проект...*.

При создании нового проекта открывается модальное окно:

<img src=images/snatch/snatch_new_proj_modal.png><figcaption>_Создание проекта_</figcaption>

В данном окне пользователь должен ввести имя нового проекта в соответствующее поле *Имя проекта*,
а также выбрать архив от *Natch* в поле *Выберите архив*. Эти поля являются обязательными при создании проекта, поэтому только при их заполнении становится активна кнопка *Создать*. Если в момент выбора файла архива поле имени не заполнено, то в него автоматически подставится имя файла. По нажатию на *Создать* создаётся проект, запускается обработка архива, и окно закрывается. При нажатии на кнопку *Закрыть* окно закрывается без создания проекта.

Помимо обязательных полей в данном окне присутствует опциональное поле *Описание*, в котором можно оставить пользовательские заметки. При работе с проектом эту информацию можно будет увидеть в разделе *О проекте*.

Название проекта не может содержать ряд специальных символов, и *Snatch* не даст их использовать как при первичном создании проекта, так и при переименовании.

При обработке архива можно параллельно запускать создание новых проектов, однако это может привести к общему замедлению работы.

Во время обработки архива поверхности атаки в верхней части экрана появляется шкала прогресса следующего вида:

<img src=images/snatch/snatch_progressbar.png><figcaption>_Шкала прогресса_</figcaption>

В процессе обработки текст, сопровождающий шкалу прогресса, будет изменяться таким образом, чтобы оповещать об актуальном статусе выполняемой задачи. Нажатие на кнопку *Стоп* прерывает процесс обработки.

При создании проекта (и открытии проекта без сохраненных вкладок) в нём по умолчанию открывается окно графа процессов.

#### 8.3.1.2. Настройки

Для открытия окна настроек необходимо вызвать из главного меню пункт *Настройки*. Содержимое открытого окна будет иметь следующий вид:

<img src=images/snatch/snatch_settings.png><figcaption>_Настройки_</figcaption>

В настоящий момент в настройках представлены только поля для конфигурации соединения со *[Svacer](https://www.ispras.ru/technologies/svace/)*, а именно: сетевой адрес, логин и пароль. Это же окно будет открыто при первой попытке взаимодействия со *Svacer* из графа процессов, если параметры соединения не были ранее заданы.

#### 8.3.1.3. Экспортирование проекта

Для экспортирования основной информации о текущем проекте необходимо вызвать из главного меню пункт *Экспортировать в pdf*. Содержимое открытого окна будет иметь следующий вид:

<img src=images/snatch/snatch_export_modal.png><figcaption>_Окно экспорта_</figcaption>

В данном окне можно выбрать какие именно данные попадут в сгенерированный файл. Выбирать можно из: [графа процессов](#process_graph), [графа модулей](#module_graph), [дерева процессов](#process_tree) и [ресурсов](#resources). Для графа процессов и графа модулей включение в экспорт доступно только после первого открытия, так как требуется первоначальная конфигурация этих графов (в противном случае в окне будет отображаться информационное сообщение). Для дерева процессов и ресурсов можно с помощью переключателей настроить будет ли в сгенерированных данных отображаться информация о процессах, запущенных с root-привилегиями, процессах ядра, а так же полный объем информации, или только о взаимодействии с помеченными данными. После нажатия кнопки *Создать* будет запущен процесс генерации файла, по завершении которого пользователю будет предложено сохранить полученный файл.

Помимо выбранных пунктов в сгенерированный файл всегда попадает содержимое вкладки "О проекте" и таблица соответствия внутренних идентификаторов процессов к имеющимся о них данным.

#### 8.3.1.4. О проекте

Для открытия информации о проекте необходимо вызвать из главного меню пункт *О проекте*. Содержимое открытой вкладки будет иметь следующий вид:

<img src=images/snatch/snatch_about_project.png><figcaption>_Данные о проекте_</figcaption>

Окно содержит следующие элементы:

1. Данные о загруженном архиве: дата создания, рабочая директория, гостевая ОС, диапазон шагов (процессорных инструкций) сценария, порог пометок, данные о рассматриваемых источниках пометок.
2. Статистика помеченных данных в рассматриваемом сценарии.
3. Версия *Natch*, на которой происходила запись архива.
4. Заметки для проекта. По умолчанию здесь размещается содержимое поля *Описание*, если оно было использовано при создании проекта. Заметки можно редактировать, сохранение происходит автоматически.

### <a name="info_block"></a>8.3.2. Информационный блок

Информационный блок – это единообразный элемент, поддерживаемый большей частью информационных окон, служащий для отображения расширенной информации о выбранном элементе. Для каждой вкладки с содержимым информационный блок индивидуальный, он сохраняет свое состояние при переключении между вкладками. Конкретное содержимое информационного блока и функционал для различных типов вкладок могут различаться, однако общие элементы также присутствуют:

<img src=images/snatch/snatch_info_block.png><figcaption>_Информационный блок_</figcaption>
<img src=images/snatch/snatch_info_block_hidden.png><figcaption>_Скрытый элемент_</figcaption>

К общим интерфейсным элементам информационного блока относятся:

1. Стрелки перемещения по истории выбранных элементов. Становятся активны, если было выбрано более одного элемента. При перемещении по истории новый выбранный элемент будет добавлен после текущей позиции, а не в конец списка.
2. Кнопка закрытия информационного блока. На ряде вкладок поддерживается закрытие по нажатию в свободную область окна.
3. Элемент управления шириной блока. Перетягивается по горизонтальной оси.
4. Отметка о том, что текущий элемент "скрыт". Появляется, если выбранный элемент (либо элемент в истории) был скрыт опциями отображения содержимого во вкладке (например: "Скрыть бессимвольные графы" в графе вызовов).

### <a name="process_graph"></a>8.3.3. Граф процессов

Граф процессов открывается автоматически после создания проекта, при наличии в проекте помеченных данных (в противном случае будет выведено информационное сообщение). Его также можно открыть через меню проекта.

Для каждого нового проекта, построенного на основании одного и того же архива, первоначальное построение графа процессов и расположение узлов на нем будет одинаковым. При дальнейшем взаимодействии с графом, положение его узлов сохраняется. Таким образом при повторном открытии графа процессов узлы будут расположены так же, как и в прошлый раз, при этом не будет происходить перестроение графа с учетом физической модели.

Отдельно отметим, что на текущем этапе разработки граф процессов может содержать некоторые неточности. При несоответствии данных между графом и другими аналитиками, стоит ориентироваться на последние.

*Граф процессов* выглядит следующим образом:

<img src=images/snatch/snatch_process_graph.png><figcaption>_Граф процессов_</figcaption>

В окне графа процессов представлены следующие элементы:

1. Шкала выбора активного шага выполнения. Перемещение по данной шкале соответствующим образом изменяет отображаемый граф.
2. Кнопки сохранения (экспорта в pdf) текущего состояния графа. По нажатию кнопки "Сохранить" происходит создание цветного изображения графа, по нажатию на "ЧБ" – черно-белого, "JSON" – сохраняет текстовое представление графа в json-формате.
3. Выбор режима отображения графа. Граф процессов поддерживает 4 режима отображения:
   * *Активные* – отображаются элементы (узлы и стрелки), которые задействованы на текущем шаге;
   * *Прошлые* – отображаются элементы, которые задействованы на текущем шаге, а также те, которые произошли в прошлом (узлы и стрелки серого цвета);
   * *Значимые* – отображаются элементы, которые задействованы на текущем шаге, а также те узлы, которые были задействованы в прошлом и при этом еще будут задействованы в будущем, и прошедшие стрелки между ними (узлы и стрелки бледных цветов);
   * *Все* – отображаются элементы, которые задействованы на текущем шаге, а также те узлы (но не стрелки), которые вообще существуют на схеме (узлы бледных цветов).
4. Легенда графа. Описывает набор отображаемых на графе узлов и их внешний вид. По нажатию на элемент легенда скрывается и может быть повторно вызвана нажатием на оставшийся "язычок". Элемент "источник пометок" описывает не форму, а вид рамки элемента (на данный момент если источником помеченных данных являлась "Сеть", то её вид рамки не изменится, требуется доработка).
4. Граф процессов. Интерактивный граф, отображающий взаимодействие процессов, работавших с помеченными данными. Расположение узлов на графе можно изменять удобным для пользователя образом. При наличии информации о контейнерах, они будут отображены на графе в виде зеленых блоков, содержащих соответствующие им процессы. При нажатии на узел происходит отображение бокового информационного блока:

<img src=images/snatch/snatch_process_infoblock.png><figcaption>_Информационный блок_</figcaption>

В информационном блоке содержатся: название выбранного элемента, его свойства, кнопка открытия соответствующего отфильтрованного графа модулей.

При нажатии правой кнопкой мыши на узел в графе процессов появляется контекстное меню, из которого можно осуществить взаимодействие со *Svacer*. При первой попытке взаимодействия пользователю будет предложено установить адрес сервера, имя и пароль пользователя (если ранее это не было установлено через раздел *Settings*). Затем пользователь увидит окно следующего вида:

<img src=images/snatch/snatch_svacer.png><figcaption>_Параметры открытия Svacer_</figcaption>

В данном окне можно выбрать проект *Svace*, ветку и снэпшот. После нажатия на кнопку *Open* будет открыто новое окно браузера со *Svacer*, сконфигурированным в соответствии с установленными параметрами.

### <a name="module_graph"></a>8.3.4. Граф модулей

Открытие графа модулей происходит по нажатию на соответствующий пункт меню в разделе *Основные графы*. При нажатии открывается новая вкладка следующего вида:

<img src=images/snatch/snatch_module_graph.png><figcaption>_Граф модулей_</figcaption>

Функционал этого окна почти полностью повторяет функционал графа процессов (см 6.3.2):

1. Шкала выбора активного шага выполнения. Перемещение по данной шкале соответствующим образом изменяет отображаемый граф.
2. Кнопки экспорта графа в цветном, черно-белом варианте и в json-формате.
3. Сворачиваемая легенда графа. Описывает набор отображаемых на графе узлов и их внешний вид.
4. Граф модулей. Интерактивный граф, отображающий взаимодействие модулей, работавших с помеченными данными. Расположение узлов на графе можно изменять удобным для пользователя образом. Стрелки, описывающие взаимодействие, сопровождаются номером, соответствующим очередности взаимодействия. Номер с символом "*" означает, что между узлами было более одного взаимодействия (очередность номера описывает только первый случай этого взаимодействия).

Так же, как и в графе процессов, нажатие на узел в графе модулей вызывает информационный блок, содержащее данные о выбранном элементе.
Первоначальное построение для одного и того же архива будет всегда одинаковым, а при взаимодействии с графом его положение сохраняется и воспроизводится при последующем открытии.

### 8.3.5. Графы вызовов
#### 8.3.5.1. Классический граф вызовов

В процессе первоначальной обработки архива поверхности атаки граф вызовов не создаётся. Чтобы граф вызовов появился в проекте, необходимо нажать на кнопку *Создать* рядом с соответствующим пунктом в боковом меню. Повторное нажатие кнопки до завершения генерации приведет к отмене процесса. По завершении генерации в боковом меню проекта под пунктом *Дополнительные графы* станет активным пункт *Граф вызовов* и появится пункт *Граф вызовов интерпретаторов* (при наличии в архиве соответствующего лог файла, описано в [граф вызовов интерпретаторов](#interp_call_graph)). Для открытия графа вызовов достаточно нажать на данный пункт в меню. После открытия появится новая вкладка с соответствующим названием, а в окне отображения содержимого откроется граф, представленный в виде древовидной структуры:

<img src=images/snatch/snatch_call_graph.png><figcaption>_Граф вызовов_</figcaption>

В данном окне представлены следующие элементы:

1. Чекбоксы опций. *Скрыть бессимвольные графы* прячет из отображаемого графа деревья, не содержащие распознанных символов (если данная опция неактивна, то в текущем проекте все деревья содержат символьную информацию). *Полные пути модулей* задаёт формат отображения имен модулей на графе: сокращенный или полный путь.
2. Поле для фильтрации графа. Вводимая строка расценивается как regex. При вводе строки и нажатии на кнопку "лупа" либо клавиши *Enter* происходит фильтрация графа, где заданная строка ищется в полном пути функции, имени модуля и других текстовых параметрах записи. Если запись удалось обнаружить, то на отфильтрованном графе она будет выделена зеленой рамкой. Если записей, удовлетворяющих условиям фильтра, найдено не было, вместо графа будет выведено сообщение "Элементов, соответствующих фильтру, не найдено". Нажатие на символ "крестик" сбрасывает фильтрацию и возвращает граф к исходному состоянию.
3. Кнопка включения демонстрации дочерних узлов на отфильтрованном графе. Если этот режим активирован, то для каждого элемента, удовлетворяющего фильтру, будут показаны все дочерние узлы. В противном случае граф будет обрубаться на найденном элементе.
4. Элементы управления графом. Первая кнопка (три горизонтальные черты с буквой "А") раскрывает все ветви графа; кнопка с буквой "S" раскрывает только символизированные ветви. Повторное нажатие кнопки сворачивает граф. Нажатие на кнопки +/- рядом с веткой раскрывает/сворачивает данную ветку в дереве.
5. Содержимое графа. В корне дерева отображается имя процесса, к которому относится данный граф вызовов. Каждый узел дерева содержит имя вызванной функции (адрес смещения в модуле, при отсутствии символьной информации), путь к файлу исходного кода и строка в файле, относящаяся к началу функции, имя модуля. Синим цветом выделяются функции непосредственно взаимодействовавшие с помеченными данными. При наведении курсора на "синие" функции возникает всплывающая подсказка, содержащая номера строк в исходниках, где происходило взаимодействие с помеченными данным. Бежевым цветом выделяются функции интерпретатора, вызванные на этом шаге.

При нажатии на функцию правой кнопкой мыши появляется контекстное меню, из которого можно запустить генерацию вспомогательных данных для [Futag](https://github.com/ispras/Futag), скопировать имя функции, а так же перейти к соответствующей записи в графе вызовов интерпретатора для "бежевых" функций. Сгенерированные данные для [Futag](https://github.com/ispras/Futag) будут помещены в файл в папке *snatch_directory/fuzzing_targets*.

При нажатии на функцию левой кнопкой мыши происходит отображение информационного блока:

<img src=images/snatch/snatch_callgraph_infoblock.png><figcaption>_Информация о функции_</figcaption>

В данном окне содержатся: имя функции, её опции, стек вызовов вплоть до выбранной функции. Синим на стеке вызовов отображаются функции, взаимодействовавшие с помеченными данными.
Кнопка "Создать лог пометок" доступна только для работавших с пометками функций (выделены синим цветом). При её нажатии будет сгенерирован файл с текстовым описанием всех операций пометок, вызванных данной функцией. Полученный файл отобразится в меню проекта в разделе "Логи пометок", откуда его можно скачать.

#### <a name="interp_call_graph"></a>8.3.5.2. Граф вызовов интерпретаторов

При построении графа вызовов строится и граф вызовов интерпретаторов (в настоящее время поддерживаются Python и Java), если в архиве содержалась соответствующая информация. Визуально и функционально данный граф повторяет классический граф вызовов:

<img src=images/snatch/snatch_interp_call_graph.png><figcaption>_Граф вызовов интерпретаторов_</figcaption>

Из контекстного меню функции, вызываемого правой кнопкой мыши, можно перейти в классический граф вызовов, где будет выбран соответствующий элемент.

### 8.3.6. Флейм граф

Как и *Граф вызовов* при создании проекта флейм граф не генерируется. Для генерации необходимо нажать на кнопку *Создать* и по завершении вызвать флейм граф нажатием на пункт в меню проекта. Обращаем внимание, генерация флейм графа – ощутимо медленный процесс, поэтому если вам кажется, что генерация зависла, то с большой вероятностью это не так: просто требуется еще подождать. Во флейм графе отображаются функции в соответствии с порядком их вызова (снизу-вверх), размер же зависит от продолжительности выполнения функции. Выглядит окно флейм графа следующим образом:

<img src=images/snatch/snatch_flame_graph.png><figcaption>_Флейм граф_</figcaption>

В данном окне представлены следующие элементы:

1. Выпадающий список построенных флейм графов, сгруппированный по процессам. Графы, относящиеся к пользовательским потокам, помечены словом *user*, выполнявшиеся ядром – *kernel*. При нажатии на пункт списка произойдет открытие соответствующего флейм графа.
2. Список цветовых схем графа. По умолчанию выбирается схема "warm" с оттенками теплого цвета для обычных функций. Во всех цветовых схемах яркий синий цвет обозначает функции, взаимодействовавшие с помеченными данными.
3. Поле поиска по выбранному флейм графу. Вводимая строка расценивается как regex. Поиск производится по строке и сопоставляется с именем функции, если элементы были найдены, то в поле поиска появляется счетчик вида "0/N" (где N – количество найденных совпадений), при этом первый найденный элемент становится активным на графе. Если совпадений не найдено, счетчик будет иметь вид "0/0". Перемещение по найденным элементам можно осуществлять интерфейсными стрелками либо нажатием клавиши *Enter*. Сброс к исходному состоянию происходит по нажатию кнопки "крестик".
4. Кнопки дополнительных условий поиска. "Aa" – активирует учёт регистра при поиске, "W" – ищет совпадения слова полностью.
5. Кнопки навигации по флейм графу. Используются для перемещения между функциями, работавшими с помеченными данными. Нажатие на кнопку *вниз* делает активным следующую такую функцию, *вверх* – предыдущую, а *Сброс* сбрасывает граф к исходному состоянию (активным становится корневой блок).
6. Список функций, работавших с помеченными данными. В данном списке показано имя функции (либо смещение относительно адреса загрузки модуля, в отсутствии символьной информации) и продолжительность работы функции (синим цветом) в выполненных процессорных инструкциях. При нажатии на пункт в этом списке, соответствующая функция на флейм графе становится активной и для нее вызывается информационный блок.
7. Флейм граф. В верхней части показано имя открытого флейм графа. Синим цветом на флейм графе отображаются функции, взаимодействовавшие с помеченными данными. При нажатии на любой блок флейм графа он становится активным, т.е. занимает 100% ширины графа, с соответствующим расширением дочерних блоков. Также для выделенной функции будет отображен информационный блок со свойствами этой функции (по аналогии с информационными блоками, описанными выше, для графа вызовов, графа процессов и т.д.)

Информационный блок для элементов флейм графа выглядит следующим образом:

<img src=images/snatch/snatch_flame_infoblock.png><figcaption>_Информационный блок флейм графа_</figcaption>

Здесь отдельно необходимо объяснить содержимое раздела "потомки": данный список содержит потомков первого уровня для данного элемента, синим цветом выделены функции, работавшие с помеченными данными, в овале в правой части показана продолжительность работы функции в инструкциях. Если функции соответствует вызов функции интерпретатора, то информация об интерпретаторе будет указана в бежевом блоке. Каждый пункт списка активный, при нажатии происходит выбор соответствующего элемента на графе.

### 8.3.7. Временной граф процессов

Для открытия временного графа процессов необходимо вызвать из меню проекта пункт *Временной граф процессов*. Содержимое открытой вкладки будет иметь следующий вид:

<img src=images/snatch/snatch_process_timeline.png><figcaption>_Временной граф процессов_</figcaption>

Временной граф процессов представляет собой граф, где горизонтальная ось отображает время выполнения процесса, от его начала и до завершения. Синим цветом на графе показаны процессы, в которых происходило взаимодействие с помеченными данными, бледно-розовым - процессы с root-привилегиями, ярко-розовым - процессы с root-привилегиями, взаимодействовавшие с помеченными данными. Зеленым фоном отмечены границы контейнеров.

В данном окне представлены следующие элементы:

1. Набор фильтров отображаемой информации. При установленной галочке *Процессы ядра* на графе будут отображаться процессы уровня ядра; при галочке *Системные процессы* будут отображаться процессы ОС; при галочке *Процессы контейнеризации* будут отображаться служебные процессы функционирования контейнеров (на данный момент docker).
2. Боковая панель. При нажатии на процесс появляется боковая панель со следующей информацией о процессе (не для всех процессов доступен полный набор информации): имя процесса, название контейнера, pid, uid, имя пользователя при наличии, путь к исполняемому файлу, исполняемая команда, родительские процессы.
3. Кнопка открытия вкладки с графом процессов на моменте, когда выбранный процесс появился на графе первый раз.
4. Всплывающее меню с краткой информацией о процессе (появляется при наведении). Включает в себя путь к бинарному файлу и строку запуска при наличии.

По умолчанию граф полностью вмещается по ширине в отображаемое окно, однако можно увеличить масштаб графа с помощью комбинации *Ctrl+Scroll*. В таком случае движение по горизонтальной оси для просмотра графа осуществляется с помощью перетаскивания графа с зажатой левой кнопкой мыши. Движение по вертикальной оси при этом осуществляется с помощью *Scroll* мышью.

### <a name="process_tree"></a>8.3.8. Дерево процессов

Для открытия дерева процессов необходимо вызвать из меню проекта пункт *Дерево процессов*. Содержимое открытой вкладки будет иметь следующий вид:

<img src=images/snatch/snatch_process_tree.png><figcaption>_Дерево процессов_</figcaption>

На дереве процессов показано отношение между процессами в формате "родитель-потомок", при этом процессы непосредственно взаимодействовавшие с помеченными данными, выделены синим цветом. Ярко-розовым цветом выделены процессы, запущенные с root-привилегиями и работавшие с помеченными данными, а бледно-розовым - просто запущенные с root-привилегиями. Помимо имени процесса на графе также отображаются его идентификаторы pid и uid, имя пользователя, и команда, которой он был запущен (если удалось её определить).

Для дерева доступен фильтр *Только помеченные*, который оставляет в дереве только те процессы, которые работали с помеченными данными, или являлись родителями процессов, работавших с помеченными данными.

Механизм фильтрации по строке аналогичен используемому в графе вызовов и полностью функционально его повторяет.

### <a name="modules"></a>8.3.9. Список модулей

Для открытия списка модулей необходимо вызвать из меню проекта пункт *Модули*. Содержимое открытой вкладки будет иметь следующий вид:

<img src=images/snatch/snatch_modules.png><figcaption>_Список модулей_</figcaption>

В данном окне представлены следующие элементы:

1. Чекбокс для отображения пустых модулей, т.е. без символьной информации. По умолчанию отключен.
2. Список символизированных модулей. В правой части указывается количество символизированных имен функций и строк в исходниках.
3. Список пустых модулей.
4. Контекстное меню для копирования полного пути модуля.

### <a name="resources"></a>8.3.10. Список ресурсов

Для открытия списка ресурсов проекта необходимо вызвать из меню проекта пункт *Ресурсы*. Содержимое открытой вкладки будет иметь следующий вид:

<img src=images/snatch/snatch_resources.png><figcaption>_Список ресурсов_</figcaption>

Ресурсы описываются древовидной структурой, где в корне располагается название процесса. Цветовая индикация процессов означают следующее: бледно-розовые - процессы с root-привилегиями; ярко-розовые - процессы с root-привилегиями, взаимодействовавшие с помеченными данными; синие - пользовательские процессы, взаимодействовавшие с помеченными данными.

Окно содержит следующие элементы:

1. Фильтр *Только помеченные*, который оставляет в списке только те процессы, которые работали с помеченными данными.
2. Пользовательский фильтр по строке, в стандартном режиме аналогичен по функционалу фильтрации в графе вызовов.
3. Переключатель режима фильтрации "по содержимому транзакций". При активном переключателе поиск будет осуществляться в содержимом транзакций, в результате в дереве останутся только те ресурсы, где данная строка была обнаружена.
4. Список ресурсов процесса. При наличии будут отображены: используемые им модули (синим обозначены работавшие с помеченными данными) с полным именем и базовым адресом загрузки; использованные сокеты; использованные файлы; использованные скрипты. Файлы и сокеты будут помечены синим, если через них проходили помеченные данные.
5. Описание конкретного элемента. Для сокета или файла при наличии будет указан объем данных операций записи или чтения. Список операций доступен для просмотра в панели операций при нажатии на элемент. При наличии для сокета указывается тип и адрес, после знака "<->" указывается адрес соединенного сокета, после знака ":" указывается имя процесса, с которым создано соединение посредством данного сокета.
6. Выбор вида представления данных.
7. В режиме фильтрации "по содержимому" появляется чекбокс, с помощью которого можно переключаться между режимом отображения всех транзакций для выбранного ресурса, и транзакциями с найденной поисковой строкой.
8. Описание транзакции. Тип операции (чтение/запись), порядковый номер, смещение данных в файле для файловых операций, выделенная зеленой рамкой найденная строка (при наличии).

### 8.3.11. Список файлов

Для открытия списка файлов проекта необходимо вызвать из меню проекта пункт *Файлы*. Содержимое открытой вкладки будет иметь следующий вид:

<img src=images/snatch/snatch_files.png><figcaption>_Список файлов_</figcaption>

В списке представлены файлы, с которыми была работа в сценарии. Голубым цветом отмечены файлы, в которые попали помеченные данные. Для каждого файла можно развернуть список процессов, которые взаимодействовали с файлом (открывали/читали/писали/запускали его). Если файл открывал процесс ядра, то в список этот файл не попадет. В список процессов процессы ядра также не попадают. Цветовая индикация процессов аналогична используемой в списке ресурсов. В боковом меню отображается информация о выбранном процессе и кнопка *Открыть в Ресурсах* для перехода во вкладку *Ресурсы* с отображением информации об искомом файле.

Для списка доступны фильтры по имени директории, в которой расположен файл. Если фильтр недоступен, значит нет ни одного файла, подпадающего под него.

Механизм фильтрации по строке аналогичен используемому в графе вызовов и полностью функционально его повторяет.

### 8.3.12. Сетевой трафик

Доступ к информации о сетевом трафике будет предоставлен только при сборе соответствующих данных во время работы *Natch* (это делается по умолчанию, а в архив помещается \*.pcap файл). Для интерактивной работы с предоставленными данными необходимо иметь установленный в системе [Wireshark](https://www.wireshark.org/).
Для открытия данных о сетевом трафике проекта необходимо вызвать из меню проекта пункт *Сетевой трафик*. Содержимое открытой вкладки будет иметь следующий вид:

<img src=images/snatch/snatch_traffic.png><figcaption>_Сетевой трафик_</figcaption>

Окно содержит следующие элементы:

1. Кнопка открытия в *Wireshark* pcap файла с сетевыми пакетами (только входящими), которые были помечены в анализируемом сценарии. Открытие *Wireshark* с нужным файлом произойдет автоматически.
2. Кнопка открытия в *Wireshark* pcap файла с сетевыми пакетами (входящими и исходящими), которые появлялись в анализируемом сценарии.
3. Кнопка открытия в *Wireshark* pcap файла с сетевыми пакетами (входящими и исходящими), которые появлялись в системе, начиная со старта.
4. Список MAC-адресов, участвовавших в работе анализируемого сценария. По нажатию на элемент списка произойдет открытие *Wireshark* с примененным фильтром для выбранного устройства.
5. Список сетевых сессий (взаимодействий между двумя сетевыми адресами), участвовавших в работе анализируемого сценария. Нажатие на элемент списка запустит *Wireshark* с фильтром на взаимодействие между указанными адресами. Зеленый блок в заголовке описывает количество элементов в списке.

## 8.4. Список горячих клавиш

### 8.4.1. Общие комбинации

- *Ctrl+Alt+N* – вызывает модальное окно создания нового проекта
- *Ctrl+Alt+G* – запускает одновременную генерацию флейм графа и графа вызовов
- *Ctrl+Alt+C* – открывает граф вызовов (при наличии)
- *Ctrl+Alt+F* – открывает флейм граф (при наличии)
- *Ctrl+Alt+P* – открывает граф процессов
- *Ctrl+Alt+M* – открывает граф модулей
- *Ctrl+Alt+L* – открывает временной граф процессов
- *Ctrl+Alt+R* – открывает дерево процессов
- *Ctrl+Alt+O* – открывает список модулей
- *Ctrl+Alt+E* – открывает список ресурсов
- *Ctrl+Alt+A* – открывает список файлов
- *Ctrl+Alt+I* – открывает сетевой трафик
- *Ctrl+X* – закрывает текущую вкладку в окне *SNatch*. Также вкладку можно закрыть по нажатию колесиком мыши.
- *Ctrl+Shift+X* – закрывает все открытые вкладки в окне *SNatch*
- *Shift+Tab* – выбирает следующую открытую вкладку в окне *SNatch*

### 8.4.2. Управление интерактивными элементами вкладок

Флейм граф:

- *↓* – переход к следующей помеченной функции
- *↑* – переход к предыдущей помеченной функции
- *Ctrl+↓* – сброс состояния флейм графа

Граф процессов:

- *→* – переход к следующему шагу
- *←* – переход к предыдущему шагу
- *Ctrl+→* – переход к последнему шагу
- *Ctrl+←* – переход к первому шагу
- *Ctrl+↓* – выбор предыдущего режима отображения
- *Ctrl+↑* – выбор следующего режима отображения

Граф модулей:

- *→* – переход к следующему шагу
- *←* – переход к предыдущему шагу
- *Ctrl+→* – переход к последнему шагу
- *Ctrl+←* – переход к первому шагу

## 8.5. Отладочная информация

При возникновении ошибок следует обратиться к отладочной информации и передать её разработчикам с описанием сценария возникновения ошибки. Отладочная информация выводится в файл *snatch.log* в корне *Snatch*.

