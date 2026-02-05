# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**Система бенчмарков для измерения реальной производительности ИИ-агентов программирования**

## Результаты

**[Посмотреть результаты бенчмарков](https://careti.ai/ru/benchmark)**

## Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/caretive-ai/careti-benchmark.git
cd careti-benchmark

# Проверить целостность данных
python3 scripts/verify-data.py

# Пример использования
python3 scripts/example-usage.py
```

## Почему этот бенчмарк?

### Ограничения существующих бенчмарков

| Бенчмарк | Ограничение |
|----------|-------------|
| **HumanEval** | Измеряет только генерацию одной функции, оторван от реальной разработки |
| **SWE-bench** | Измеряет решение задач GitHub, но не отражает использование инструментов агентом |
| **MBPP** | Простые задачи Python, нет поддержки сложных многофайловых задач |

**Ключевая проблема**: Существующие бенчмарки измеряют только "способность генерации кода". Но реальные ИИ-агенты программирования (Cline, Cursor, Careti и др.) **используют инструменты, видят ошибки и исправляют их, делают несколько попыток**.

### Что измеряет этот бенчмарк

```
Традиционный: Задача → Модель → Код → Оценка (1 раз)
Careti:       Задача → Агент → Код → Тест → [Обратная связь об ошибке] → Повтор → ... → Финальный результат
```

## Последние результаты (Hard Suite 100)

| Ранг | Модель | 1-я попытка | Итоговый | Ср. попытки | Стоимость |
|------|--------|-------------|----------|-------------|-----------|
| #1 | Gemini 2.5 Flash | 70-92% | **98%** | 1.11-1.44 | $0.05-0.13 |
| #2 | GLM-4.7 | 89-92% | **97-98%** | 1.11-1.15 | $0.18 |
| #3 | Gemini 3 Pro (Preview) | 66-67% | **92-93%** | 1.53-1.57 | $0.60 |
| #4 | Solar Pro2 | 61-64% | **81-86%** | 1.82-1.87 | $0.75-0.87 |
| #5 | Solar Pro3 | 70% | **75%** | 1.71 | $1.35 |
| #6 | HyperCLOVA X | 1-2% | **1-2%** | 3.03-3.06 | $0.22-0.31 |

## Ключевые метрики

| Метрика | Значение | Почему важно? |
|---------|----------|---------------|
| **Успех 1-й попытки** | Доля успеха с первой попытки | "Интуиция" агента - определяет время ожидания пользователя |
| **Итоговый успех** | Доля успеха включая повторы | "Способность решать проблемы" агента |
| **Среднее попыток** | Среднее количество попыток на задачу | Показатель эффективности |
| **Стоимость** | Общая стоимость API | Экономическая целесообразность |

## Условия завершения

| Условие | Описание |
|---------|----------|
| `success` | Тест пройден |
| `max_attempts` | Достигнуто макс. попыток (5) |
| `timeout` | Превышен лимит времени (300с) |
| `oscillation` | Обнаружен паттерн A↔B осцилляции |
| `same_error` | Та же ошибка повторена 3 раза |

## Сырые данные

Директория `results/` содержит полные данные бенчмарков в формате JSON.

### Структура данных

```json
{
  "problem_id": "h01-longest-substring",
  "model": "Gemini 2.5 Flash",
  "success": true,
  "attempts": 2,
  "first_attempt_success": false,
  "total_time_ms": 9599,
  "cost_usd": 0.00094,
  "input_tokens": 4330,
  "output_tokens": 484,
  "prompt_mode": "careti",
  "termination_reason": "success",
  "attempt_history": [
    {
      "attempt": 1,
      "success": false,
      "latency_ms": 6229,
      "error": "SyntaxError: invalid syntax"
    },
    {
      "attempt": 2,
      "success": true,
      "latency_ms": 3370
    }
  ]
}
```

### Поиск оригинальных задач

Задачи Hard Suite включены в `problems/hard-suite.json`:

```python
import json
import urllib.request

# Скачать задачи
url = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main/problems/hard-suite.json"
problems = json.loads(urllib.request.urlopen(url).read())

# Найти задачу по ID
problem = next(p for p in problems if p["id"] == "h01-longest-substring")
print(problem["prompt"])
print(problem["test_code"])
```

## Структура файлов

```
problems/
  hard-suite.json       # 100 задач с промптами и тестовым кодом

results/2026-02-hard-suite/
  results.json          # 2100 индивидуальных результатов тестов
  summary.json          # Агрегированная статистика по моделям

scripts/
  verify-data.py        # Проверка целостности данных
  example-usage.py      # Примеры скриптов анализа
```

## Лицензия

MIT

---

**Made by [Caretive](https://caretive.ai)** - Разработчики ИИ-агента программирования Careti
