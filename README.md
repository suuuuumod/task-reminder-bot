# Telegram Task Bot

Telegram Task Bot - это бот для управления задачами в Telegram. Он позволяет добавлять, просматривать, удалять и завершать задачи, а также устанавливать напоминания о задачах.

## Возможности

- **Добавить задачу:** Бот запросит описание задачи.
- **Просмотр списка задач:** Бот отобразит все текущие задачи.
- **Удалить задачу:** Бот запросит номер задачи для удаления. Введите "все", чтобы удалить все задачи.
- **Завершить задачу:** Бот запросит номер задачи для завершения.
- **Установить напоминание:** Бот запросит время в минутах, через которое нужно напомнить о задаче.

## Запуск

1. Клонируйте репозиторий или скачайте архив с проектом.
2. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```
3. В файле `config.py` укажите ваши `api_id`, `api_hash` и `bot_token`.
4. Запустите бота:
    ```sh
    python bot.py
    ```

## Использование

1. Отправьте команду `/start`, чтобы начать взаимодействие с ботом.
2. Используйте кнопки для добавления, просмотра, удаления и завершения задач.
3. Следуйте инструкциям бота для выполнения операций.

## Пример

- Добавить задачу:
  1. Нажмите кнопку "➕ Добавить задачу".
  2. Введите описание задачи.
  3. Следуйте инструкциям для установки напоминания (по желанию).

- Удалить все задачи:
  1. Нажмите кнопку "❌ Удалить задачу".
  2. Введите "все".

## Требования

- Python 3.6+
- Telethon

## Лицензия

Этот проект лицензирован под лицензией MIT.
