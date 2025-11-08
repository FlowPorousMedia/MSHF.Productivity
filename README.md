# MSHF.Productivity

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-3.2%2B-010101?logo=plotly)](https://dash.plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/User_Guide-Wiki-blue?logo=github)](https://github.com/FlowPorousMedia/MSHF.Productivity/wiki)
[![Open Issues](https://img.shields.io/github/issues-raw/FlowPorousMedia/MSHF.Productivity?color=0088ff)](https://github.com/FlowPorousMedia/MSHF.Productivity/issues)
[![Status](https://img.shields.io/badge/Status-Beta-brightgreen)]()

**Программа для оценки продуктивности горизонтальных скважин с многозонным гидроразрывом пласта (МГРП)**

Программа предоставляет инженерам-нефтяникам удобный инструмент для быстрой оценки дебита скважин 
с МГРП при стационарной фильтрации с помощью аналитических моделей

**Productivity Evaluation Tool for Multistage Fractured Horizontal Wells (MSHF)**

This software tool enables petroleum engineers to rapidly forecast production rates for multistage 
fractured horizontal wells. It utilizes analytical modeling to perform steady-state flow analysis, 
providing a quick and efficient solution for well performance evaluation.

[Онлайн версия программы (Online Tool)](https://mshf-productivity.onrender.com)

> ⚠️ **Примечание (Note):**
> При первом запуске онлайн-версии может быть небольшая задержка загрузки — это нормально.
> The first load of the online version may take a bit longer — this is normal.


[Руководство пользователя (User Guide)](https://github.com/FlowPorousMedia/MSHF.Productivity/wiki)

---

## Содержание

* [О проекте](#о-проекте)
* [Ключевые возможности](#ключевые-возможности)
* [Установка и запуск](#установка-и-запуск)
* [Документация](#документация)
* [Релизы](#релизы)
* [Поддержка](#поддержка)
* [Авторы](#авторы)
* [Лицензия](#лицензия)

## О проекте

**MSHF.Productivity** — это программа для оценки продуктивности (дебита) горизонтальных скважин (ГС) с многозонным гидроразрывом пласта (МГРП).

Проектирование и анализ эксплуатации таких скважин требуют сложных расчетов. Данное приложение предоставляет пользователям гибкий инструмент для:
-   **Сравнительного анализа** различных конфигураций трещин ГРП.
-   **Оптимизации параметров** гидроразрыва (длина, проводимость, количество трещин, расстояние между ними).
-   **Быстрой оценки** потенциальной продуктивности скважины на этапе проектирования.

В программе используются проверенные аналитические формулы для обеспечения достоверных результатов:
1. Li H., Jia Zh., Wei Zh. (1996). A New Method to Predict Performance of Fractured Horizontal Wells. International Conference on Horizontal Well Technology, Calgary, Alberta, Canada. https://doi.org/10.2118/37051-MS
2. Guo B. Schechter D. (1997). A Simple and Rigorous Mathematical Model for Estimating Inflow Performance of Wells Intersecting Long Fractures. Paper SPE 38104 presented at the SPE Asia Pacific Oil and Gas Conference and Exhibition, Kuala Lumpur. https://doi.org/10.2118/38104-MS
3. Guo B., Yu X., Khoshgahdam M. (2009). Simple Analytical Model for Predicting Productivity of Multifractured Horizontal Wells. SPE Reservoir Evaluation & Engineering 12 (06), pp. 879–885. https://doi.org/10.2118/114452-PA
4. Елкин С.В., Алероев А.А., Веремко Н.А., Чертенков М.В. (2016). Учет влияния безразмерной проводимости на экспресс-расчет дебита жидкости после многозонного гидроразрыва пласта. Нефтяное хозяйство, 12, с. 110–113.
5. Potashev K., Mazo A., Mukhina M., Uraimov A., Maklakov D., Khamidullin M. (2024). High-speed algorithm for computing the inflow to multiple-fractured horizontal wells using stream tubes. Comput Geosci, 28, pp. 1389–1411. https://doi.org/10.1007/s10596-024-10322-w



## Установка и запуск

Следуйте этим инструкциям, чтобы получить копию проекта и запустить его на вашей локальной машине.

#### Предварительные требования

*   Python 3.11 или новее

#### Клонирование репозитория

```bash
# Клонируйте репозиторий
git clone https://github.com/FlowPorousMedia/MSHF.Productivity.git

# Перейдите в директорию проекта
cd MSHF.Productivity
```

#### Создание виртуального окружения (рекомендуется)

```bash
# Для Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Для Windows
python -m venv venv
.\venv\Scripts\activate
```

#### Установка зависимостей

```bash
pip install -r requirements.txt
```

#### Запуск приложения

После успешной установки зависимостей запустите приложение.

```bash
python main.py
```

или

```bash
python -m dash run
```

Сервер разработки запустится локально. Откройте ваш веб-браузер и перейдите по адресу `http://127.0.0.1:8050/`.

## Документация 
Полное руководство пользователя, включающее теоретическое обоснование методов расчета, подробное описание интерфейса, 
инструкцию по работе с программой и примеры типовых расчетов, доступно в **Wiki** данного репозитория.

➡️ **[Руководство пользователя](https://github.com/FlowPorousMedia/MSHF.Productivity/wiki)**

## Релизы

Актуальные версии программы можно найти на странице [Releases](https://github.com/FlowPorousMedia/MSHF.Productivity/releases).

## Поддержка

Мы активно используем Issues для отслеживания багов, идей и планирования новых функций.

#### Прежде чем создать новую задачу:

1.  Поищите по [существующим задачам](https://github.com/FlowPorousMedia/MSHF.Productivity/issues) — возможно, ваша проблема или идея уже обсуждается.
2.  Для багов: используйте [шаблон для багов](https://github.com/FlowPorousMedia/MSHF.Productivity/issues/new?template=bug_report.yml) и укажите:
    *   Версию проекта/ОС/браузера.
    *   Четкие шаги для воспроизведения.
    *   Ожидаемое и фактическое поведение.
3.  Для новых идей: используйте [шаблон для фич](https://github.com/FlowPorousMedia/MSHF.Productivity/issues/new?template=feature_request.yml), опишите проблему, которую она решает, и предложите реализацию.


## Авторы
*   [Марсель Хамидуллин](https://www.researchgate.net/profile/Marsel-Khamidullin)
*   [Константин Поташев](https://www.researchgate.net/profile/Konstantin-Potashev)

## Лицензия

© FlowPorousMedia, 2025. Все права защищены

Этот проект распространяется под лицензией [MIT](LICENSE)
