from telethon import TelegramClient, events, Button
import json
import os
import asyncio
from config import api_id, api_hash, bot_token

client = TelegramClient('task_bot', api_id, api_hash).start(bot_token=bot_token)

tasks = {}
awaiting_task = {}
awaiting_reminder_confirmation = {}
awaiting_reminder_time = {}
awaiting_deletion = {}
awaiting_completion = {}

def save_tasks():
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

def load_tasks():
    global tasks
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    else:
        tasks = {}

load_tasks()

async def send_reminder(user_id, task):
    await client.send_message(user_id, f'Напоминание: {task}')

async def schedule_reminder(user_id, task, minutes):
    await asyncio.sleep(minutes * 60)
    await send_reminder(user_id, task)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.text('➕ Добавить задачу', resize=True), Button.text('📋 Список задач', resize=True)],
        [Button.text('❌ Удалить задачу', resize=True), Button.text('✔️ Завершить задачу', resize=True)]
    ]
    await event.respond("Привет! Я бот для управления задачами. Выберите действие:", buttons=buttons)

@client.on(events.NewMessage(pattern='➕ Добавить задачу'))
async def prompt_new_task(event):
    awaiting_task[event.sender_id] = True
    await event.respond('Напишите вашу задачу.')

@client.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id
    if event.out:
        return
    if user_id in awaiting_task and not event.message.text.startswith('➕ Добавить задачу'):
        task = event.message.text
        if task:
            if str(user_id) not in tasks:
                tasks[str(user_id)] = []
            tasks[str(user_id)].append({'task': task, 'completed': False})
            save_tasks()
            del awaiting_task[user_id]
            awaiting_reminder_confirmation[user_id] = task
            await event.respond('Задача принята! Нужно ли вам напомнить о выполнении этой задачи? (Да/Нет)')
    elif user_id in awaiting_reminder_confirmation:
        answer = event.message.text.lower()
        if answer == 'да':
            awaiting_reminder_time[user_id] = awaiting_reminder_confirmation[user_id]
            del awaiting_reminder_confirmation[user_id]
            await event.respond('Через сколько минут напомнить?')
        elif answer == 'нет':
            del awaiting_reminder_confirmation[user_id]
            await event.respond('Хорошо, задача сохранена без напоминания.')
        else:
            await event.respond('Пожалуйста, ответьте "Да" или "Нет".')
    elif user_id in awaiting_reminder_time:
        try:
            minutes = int(event.message.text)
            task = awaiting_reminder_time[user_id]
            del awaiting_reminder_time[user_id]
            await event.respond(f'Напоминание установлено через {minutes} минут.')
            await schedule_reminder(user_id, task, minutes)
        except ValueError:
            await event.respond('Пожалуйста, укажите время в минутах числом.')
    elif user_id in awaiting_deletion:
        if event.message.text.lower() == 'все':
            if str(user_id) in tasks:
                tasks[str(user_id)] = []
                save_tasks()
                del awaiting_deletion[user_id]
                await event.respond('Все задачи удалены.')
            else:
                await event.respond('У вас нет задач для удаления.')
        else:
            try:
                task_number = int(event.message.text) - 1
                if str(user_id) in tasks and 0 <= task_number < len(tasks[str(user_id)]):
                    deleted_task = tasks[str(user_id)].pop(task_number)
                    save_tasks()
                    del awaiting_deletion[user_id]
                    await event.respond(f'Задача "{deleted_task["task"]}" удалена.')
                else:
                    await event.respond('Неверный номер задачи. Попробуйте снова.')
            except ValueError:
                await event.respond('Пожалуйста, укажите номер задачи числом или введите "все" для удаления всех задач.')
    elif user_id in awaiting_completion:
        try:
            task_number = int(event.message.text) - 1
            if str(user_id) in tasks and 0 <= task_number < len(tasks[str(user_id)]):
                tasks[str(user_id)][task_number]['completed'] = True
                save_tasks()
                del awaiting_completion[user_id]
                await event.respond(f'Задача "{tasks[str(user_id)][task_number]["task"]}" завершена!')
            else:
                await event.respond('Неверный номер задачи. Попробуйте снова.')
        except ValueError:
            await event.respond('Пожалуйста, укажите номер задачи числом.')

@client.on(events.NewMessage(pattern='📋 Список задач'))
async def list_tasks(event):
    user_id = str(event.sender_id)
    if user_id in tasks and tasks[user_id]):
        message = "Ваши задачи:\n"
        for idx, task in enumerate(tasks[user_id], start=1):
            status = "✔️" if task['completed'] else "❌"
            message += f"{idx}. {task['task']} {status}\n"
        await event.respond(message)
    else:
        await event.respond("У вас нет задач.")

@client.on(events.NewMessage(pattern='❌ Удалить задачу'))
async def prompt_delete_task(event):
    awaiting_deletion[event.sender_id] = True
    await event.respond('Пожалуйста, укажите номер задачи, которую нужно удалить, или напишите "все" для удаления всех задач.')

@client.on(events.NewMessage(pattern='✔️ Завершить задачу'))
async def prompt_complete_task(event):
    awaiting_completion[event.sender_id] = True
    await event.respond('Пожалуйста, укажите номер задачи, которую нужно завершить.')

client.start()
client.run_until_disconnected()
