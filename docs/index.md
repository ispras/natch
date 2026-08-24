# Руководство пользователя Natch

**Natch** (**N**etwork **A**pplication **T**ainting **C**an **H**elp) — инструмент для определения поверхности атаки, основанный на полносистемном эмуляторе QEMU.

**Natch** предназначен для поиска поверхности атаки: приложений, программных модулей и функций, участвующих в обработке заданных входных данных.
Инструмент оснащен графической подсистемой **SNatch** для интерактивного анализа результатов и построения отчетов.




::::{grid} 3
:gutter: 2

:::{grid-item-card} {octicon}`rocket` Начало работы

* [Что такое Natch](1_natch)
* [Установка и настройка Natch](2_setup)
* [Запуск тестовых примеров](3_launch_test_samples)
* [Настройка окружения для работы с Natch](4_setup_env)
:::
:::{grid-item-card} {octicon}`terminal` Работа с Natch

- [Командный интерфейс Natch](5_natch_cmd)
- [Создание проекта](6_create_project)
- [Определение источников пометки](7_taint_source)
- [Запись и воспроизведение сценариев](8_scenario_work)
- [Анализ поверхности атаки с помощью SNatch](9_snatch)
- [Дополнительные возможности Natch](10_additional)
- [Автоматизация процессов](11_automation)
- [Примеры использования Natch](12_applications)
:::
:::{grid-item-card} {octicon}`question` Справочная информация

* [Часто задаваемые вопросы (FAQ)](13_faq)
* [Системные требования и ограничения Natch](14_requirements)
:::

::::


## {octicon}`book` Приложения

::::{grid}

:::{grid-item}
* [Настройка окружения для использования лицензированного Natch](app1_license)
* [Конфигурационные файлы Natch](app2_configs)
* [Формат списка исполняемых модулей](app3_module_cfg)
* [Графы взаимодействия помеченных процессов и модулей](app4_graphs)
:::

:::{grid-item}
* [Формат файла с покрытием кода](app5_coverage)
* [Изменение командной строки эмулятора](app6_cmd_line)
* [Рекомендации по подготовке и анализу объекта оценки](app7_oo_preparation)
* [История релизов Natch](app8_releases)
:::

::::

## {octicon}`briefcase` Дополнительные материалы
::::{grid}

:::{grid-item}

* [{octicon}`device-camera-video` Видеозаписи вебинаров](https://nextcloud.ispras.ru/index.php/s/3LEqid57bn8PYGx)
* [{octicon}`megaphone` Выступления на конференциях](conferences)
* [{octicon}`star` Практическое применение Natch](trophies)
* [{octicon}`mortar-board` Научные публикации](publications)
:::

::::





```{toctree}
:numbered:
:maxdepth: 1
:caption: Начало работы
:hidden:

1_natch
2_setup
3_launch_test_samples
4_setup_env
```

```{toctree}
:numbered:
:maxdepth: 1
:caption: Работа с Natch
:hidden:

5_natch_cmd
6_create_project
7_taint_source
8_scenario_work
9_snatch
10_additional
11_automation
12_applications
```

```{toctree}
:numbered:
:maxdepth: 1
:caption: Справочная информация
:hidden:

13_faq
14_requirements
```

```{toctree}
:maxdepth: 1
:caption: Приложения
:hidden:

app1_license
app2_configs
app3_module_cfg
app4_graphs
app5_coverage
app6_cmd_line
app7_oo_preparation
app8_releases
```

```{toctree}
:maxdepth: 1
:caption: Дополнительные материалы
:hidden:

conferences
trophies
publications
```

