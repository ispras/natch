# Руководство пользователя Natch

**Natch** (**N**etwork **A**pplication **T**ainting **C**an **H**elp) — инструмент для определения поверхности атаки, основанный на полносистемном эмуляторе QEMU.

**Natch** предназначен для поиска поверхности атаки: приложений, программных модулей и функций, участвующих в обработке заданных входных данных.
Инструмент оснащен графической подсистемой **SNatch** для интерактивного анализа результатов и построения отчетов.




::::{grid} 3
:gutter: 2

:::{grid-item-card} <H2>{octicon}`rocket` Начало работы</H2>

* [Что такое Natch](1_natch)
* [Настройка окружения для работы с Natch](2_setup_env)
* [Установка и настройка Natch](3_setup)
* [Запуск тестовых примеров](4_launch_test_samples)
:::
:::{grid-item-card} <H2>{octicon}`terminal` Работа с Natch</H2>

- [Командный интерфейс Natch](5_natch_cmd)
- [Подготовка образа с объектом оценки](6_prepare_image)
- [Создание проекта](7_create_project)
- [Определение источников пометки](8_taint_source)
- [Запись и воспроизведение сценариев](9_scenario_work)
- [Анализ поверхности атаки с помощью SNatch](10_snatch)
- [Дополнительные возможности Natch](11_additional)
- [Автоматизация процессов](12_automation)
- [Примеры использования Natch](13_applications)
:::
:::{grid-item-card} <H2>{octicon}`question` Справочная информация</H2>

* [Системные требования и ограничения Natch](14_requirements)
* [Часто задаваемые вопросы (FAQ)](15_faq)
* [Телеграм-канал поддержки Natch](https://t.me/ispras_natch)
:::

::::


### {octicon}`paperclip` Приложения

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

### {octicon}`briefcase` Дополнительные материалы
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
2_setup_env
3_setup
4_launch_test_samples
```

```{toctree}
:numbered:
:maxdepth: 1
:caption: Работа с Natch
:hidden:

5_natch_cmd
6_prepare_image
7_create_project
8_taint_source
9_scenario_work
10_snatch
11_additional
12_automation
13_applications
```

```{toctree}
:numbered:
:maxdepth: 1
:caption: Справочная информация
:hidden:

14_requirements
15_faq
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

