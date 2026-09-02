<img src="docs/images/logo/logo.png" width=10%>

**Natch v.3.4**

:man_mechanic: [Телеграм-канал поддержки Natch](https://t.me/ispras_natch)
____
_В связи с переходом на новую версию аппаратных ключей инструмента лицензирования Sentinel до окончания действия всех выданных лицензий будут поддерживаться два варианта дистрибутива.
Если у вас старые ключи Sentinel, то следует брать дистрибутив из папки Sentinel_YM, если вы новый пользователь *Natch* -- дистрибутив для вас в папке Sentinel_XE._

_В постфиксах указаны первые символы кодов вендора системы лицензирования Sentinel -- YMYCK и XEKDC. Этот код можно увидеть на обратной стороне вашего аппаратного ключа с лицензией
(либо определить по числовому коду в соответствующем поле графы ключа в Sentinel Admin Control Center после установки драйверов Sentinel Runtime: 101213 для YMYCK и 36343 для XEKDC)._

_Также рекомендуется переустановить окружение (aksusbd\_*current_version*\_amd64.deb для Ubuntu/Debian/Astra), пакет находится в папке с дистрибутивом.
Для Alt необходимо выполнить epm play aksusbd._
____

Natch (Network Application Tainting Can Help) -- это инструмент для определения поверхности атаки, основанный на полносистемном эмуляторе QEMU.

Основная функция Natch -- получение списка модулей (исполняемых файлов и динамических библиотек) и функций, используемых системой во время выполнения задачи.

Результат работы инструмента представлен множеством интерактивных аналитик, которые собраны в веб-интерфейсе *SNatch*.





### :rocket: Начало работы

[1. Что такое Natch](docs/1_natch.md)

[2. Настройка окружения для работы с Natch](docs/2_setup_env.md)

[3. Установка и настройка Natch](docs/3_setup.md)

[4. Запуск тестовых примеров Natch](docs/4_launch_test_samples.md)


### :crystal_ball: Работа с Natch

[5. Командный интерфейс Natch](docs/5_natch_cmd.md)

[6. Подготовка образа с объектом оценки](docs/6_prepare_image)

[7. Создание проекта](docs/7_create_project.md)

[8. Определение источников пометки](docs/8_taint_source.md)

[9. Запись и воспроизведение сценариев](docs/9_scenario_work.md)

[10. Анализ поверхности атаки с помощью SNatch](docs/10_snatch.md)

[11. Дополнительные возможности Natch](docs/11_additional.md)

[12. Автоматизация процессов](docs/12_automation.md)

[13. Примеры использования Natch](docs/13_applications.md)

### :interrobang: Справочная информация

[14. Системные требования и ограничения Natch](docs/14_requirements)

[15. FAQ](docs/15_faq.md)


### :paperclip: Приложения

[А. Настройка окружения для использования лицензированного Natch](docs/app1_license.md)

[Б. Конфигурационные файлы Natch](docs/app2_configs.md)

[В. Формат списка исполняемых модулей](docs/app3_module_cfg.md)

[Г. Графы взаимодействия помеченных процессов и модулей](docs/app4_graphs.md)

[Д. Формат файла с покрытием кода](docs/app5_coverage.md)

[Е. Изменение командной строки эмулятора](docs/app6_cmd_line.md)

[Ж. Рекомендации по подготовке и анализу объекта оценки](docs/app8_oo_preparation.md)

[З. История релизов Natch](docs/app9_releases.md)

-----

:video_camera: [Видеозаписи вебинаров](https://nextcloud.ispras.ru/index.php/s/3LEqid57bn8PYGx)

:loudspeaker: [Выступления на конференциях](docs/conferences.md)

:ballot_box_with_check: [Практическое применение Natch](docs/trophies.md)

:mortar_board: [Научные публикации](docs/publications.md)
