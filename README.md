## Телеграм-бот Python Quiz
### Описание бота
- Основная функция данного бота - прохождение Квиза по вопросом о языке программирования Python.


- При получении команды "/start" происходит сохранение в БД ID пользователя.


- Бот предлагает начать игру с помощью кнопки "Начать игру" (аналог команды "/quiz").


- После того как пользователь отправляет боту сообщение с названием города бот обрабатывает полученную от API инфорацию, сохраняет её в базу данных (с привязкой к конкретному пользователю) и присылает пользователю ответ с вариантами конкретных метерологических показателей посредством встроенных кнопок.



### Зависимости
- Бот написан на языке программирования Python v3


- Для полноценного функционирования бота используются следующие библиотеки:
    ```
  aiogram
  aiosqlite
  asyncio

    ```
  
### Инструкция для запуска бота

- Запуск бота может осуществляться с ПК администратора, либо нужно использовать для этих целей виртуальную машину.