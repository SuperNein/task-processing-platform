# Лабораторная работа 4

**Асинхронный исполнитель задач**

---

## Цель работы

- Научиться реализовывать приложения с асинхронной моделью управления.

---

## Структура проекта 

```
task-processing-platform
│   pyproject.toml
│   README.md
│   requirements.txt
│
├───tests
├───examples
│           
└───src
    │   demo_execution.py               # Демонстрация обработки задач
    │   main.py
    │   
    ├───common
    │       constants.py
    │       logging_config.py
    │                
    ├───core
    │   │   async_task_queue.py         # Асинхронная очередь задач
    │   │   descriptors.py              # Дескрипторы полей Task
    │   │   enums.py                    # Перечисления типов Priority, Status
    │   │   executor.py                 # Асинхронный исполнитель
    │   │   task_model.py               # Класс Task
    │   │   task_queue.py               # Коллекция TaskQueue
    │   │
    │   └───exceptions                  # Исключения для core
    │           executor_errors.py
    │           task_errors.py
    │           task_queue_errors.py
    │
    ├───handlers                        # Асинхронные обработчики задач
    │       failing_handler.py
    │       print_handler.py
    │
    ├───protocols
    │       handler.py                  # Контракт обработчиков задач
    │       sources.py                  # Контракт источников задач
    │
    ├───services
    │       loader.py                   # Загрузчик задач из источника
    │       validation.py               # Валидатор источников задач по контракту
    │      
    └───sources
            API_stub_source.py
            file_source.py
            generator_source.py
```

---

## Установка

### Установка и тесты

```
# Установка зависимостей
pip install -r requirements.txt

# Запуск examples
python -m src.main

# Покрытие тестами
pytest tests/ --cov=src/ --cov-report=term-missing
```

### Библиотеки

- pytest

---

## Реализация

### Модель Task

Пользовательский класс с атрибутами:
- id — уникальный идентификатор задачи
- description — текстовое описание задачи
- priority - приоритет
- status - статус задачи
- created_at - время создания
- is_closed - статус закрытия задачи

Задачи поддерживают операцию сложения. В результате возвращается новая задача с объединенным описанием и приоритетом, равным максимальному из двух исходных.

### Источники

- Задачи, загружаемые из JSON файла
- Задачи, генерируемые программно (генератор)
- Задачи, получаемые из API-заглушки (под API-заглушкой понимается упрощённый программный компонент, имитирующий внешний источник задач)

Все источники реализуют единый метод:

```
get_tasks() -> Iterable[Task]
```

### Очереди задач

#### Синхронная

TaskQueue - итерируемая коллекция задач, совместимая со стандартными конструкциями Python (for, list, sum).

Поддерживает ленивую фильтрацию:

```
TaskQueue.filter.status()      # По статусу задач
TaskQueue.filter.priority()    # По диапазону приоритетов
TaskQueue.filter()             # По произвольному предикату
```

#### Асинхронная

AsyncTaskQueue - асинхронно итерируемая обертка над asyncio.Queue со строгой типизацией элементов 


---

## Выводы

В ходе работы я освоил:
- Асинхронную обработку задач
- Использование контекстных менеджеров
- Тестирование асинхронных функций