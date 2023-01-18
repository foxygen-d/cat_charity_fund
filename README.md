# Финальный проект спринта: приложение QRKot


![alt text](https://pictures.s3.yandex.net/resources/sprint2_picture1_1672399951.png)


## Оглавление

* [Задача проекта](#задача)
    * [Проекты](#проекты)
    * [Пожертвования](#пожертвования)
    * [Пользователи](#пользователи)
* [Технические подробности и требования](#технические-подробности-и-требования)
    * [Пользователи](#d0bfd0bed0bbd18cd0b7d0bed0b2d0b0d182d0b5d0bbd0b8-1)
    * [Проекты](#d0bfd180d0bed0b5d0bad182d18b-1)
    * [Права пользователей](#права-пользователей)
    * [Пожертвования](#d0bfd0bed0b6d0b5d180d182d0b2d0bed0b2d0b0d0bdd0b8d18f-1)
* [Процесс «инвестирования»](#процесс-«инвестирования»)


## Задача
Создать приложение для Благотворительного фонда поддержки котиков **QRKot**

Фонд собирает пожертвования на различные целевые проекты:
* на медицинское обслуживание нуждающихся хвостатых
* на обустройство кошачьей колонии в подвале
* на корм оставшимся без попечения кошкам
* на любые цели, связанные с поддержкой кошачьей популяции


### Проекты

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу *First In, First Out*: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.


### Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.


### Пользователи

Целевые проекты создаются администраторами сайта.

Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.

Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.


## Технические подробности и требования

Скачайте спецификацию проекта openapi.json:

Для просмотра документации загрузите файл на сайт https://redocly.github.io/redoc/. Вверху страницы есть кнопка **Upload a file**, нажмите её и загрузите скачанный файл. Спецификация проекта отобразится в формате ReDoc. Ваш API должен соответствовать всем требованиям документации.

В приложении должно быть три модели: 
* Пользователи
* Проекты
* Пожертвования


### Пользователи

Все настройки пользователей возьмите из проекта по бронированию переговорок.
* Используйте библиотеку FastAPI Users.
* В настройках укажите транспорт Bearer и стратегию JWT.
* Подключите роутеры Auth Router, Register Router, Users Router.
* Не изменяйте базовую модель пользователя.
* Установите запрет на удаление пользователей: эндпоинт удаления пользователя переопределите на deprecated.


### Проекты

Создайте модель CharityProject, свяжите её с таблицей `charityproject` в базе данных

Столбцы таблицы `charityproject`:
* `id` — первичный ключ
* `name` — уникальное название проекта, обязательное строковое поле; допустимая длина строки — от 1 до 100 символов включительно
* `description` — описание, обязательное поле, текст; не менее одного символа
* `full_amount` — требуемая сумма, целочисленное поле; больше 0
* `invested_amount` — внесённая сумма, целочисленное поле; значение по умолчанию — 0
* `fully_invested` — булево значение, указывающее на то, собрана ли нужная сумма для проекта (закрыт ли проект); значение по умолчанию — False
* `create_date` — дата создания проекта, тип DateTime, должно добавляться автоматически в момент создания проекта
* `close_date` — дата закрытия проекта, DateTime, проставляется автоматически в момент набора нужной суммы


### Права пользователей

Любой посетитель сайта (в том числе неавторизованный) может посмотреть список всех проектов

Суперпользователь может: 
* создавать проекты
* удалять проекты, в которые не было внесено средств
* изменять название и описание существующего проекта, устанавливать для него новую требуемую сумму (но не меньше уже внесённой)

Никто не может менять через API размер внесённых средств, удалять или модифицировать закрытые проекты, изменять даты создания и закрытия проектов

Любой зарегистрированный пользователь может сделать пожертвование

Зарегистрированный пользователь может просматривать только свои пожертвования, при этом ему выводится только четыре поля:
* `id`
* `comment`
* `full_amount`
* `create_date`

Информация о том, инвестировано пожертвование в какой-то проект или нет, обычному пользователю недоступна

Суперпользователь может просматривать список всех пожертвований, при этом ему выводятся все поля модели

Редактировать или удалять пожертвования не может никто


### Пожертвования

Создайте модель Donation, свяжите её с таблицей `donation` в базе данных

Столбцы таблицы `donation`:
* `id` — первичный ключ
* `user_id` — id пользователя, сделавшего пожертвование. Foreign Key на поле user.id из таблицы пользователей
* `comment` — необязательное текстовое поле
* `full_amount` — сумма пожертвования, целочисленное поле; больше 0
* `invested_amount` — сумма из пожертвования, которая распределена по проектам; значение по умолчанию равно 0
* `fully_invested` — булево значение, указывающее на то, все ли деньги из пожертвования были переведены в тот или иной проект; по умолчанию равно False
* `create_date` — дата пожертвования; тип DateTime; добавляется автоматически в момент поступления пожертвования
* `close_date` — дата, когда вся сумма пожертвования была распределена по проектам; тип DateTime; добавляется автоматически в момент выполнения условия


## Процесс «инвестирования»

Сразу после создания нового проекта или пожертвования должен запускаться процесс «инвестирования» (увеличение `invested_amount` как в пожертвованиях, так и в проектах, установка значений `fully_invested` и `close_date`, при необходимости).

Если создан новый проект, а в базе были «свободные» (не распределённые по проектам) суммы пожертвований — они автоматически должны инвестироваться в новый проект, и в ответе API эти суммы должны быть учтены. То же касается и создания пожертвований: если в момент пожертвования есть открытые проекты, эти пожертвования должны автоматически зачислиться на их счета.

Функции, отвечающие за инвестирование, должны вызываться непосредственно из API-функций, отвечающих за создание пожертвований и проектов. Сами функции инвестирования (или одну универсальную функцию) можно расположить в директории app/services/ в отдельном файле с подходящим именем.

**Важно!** В процессе инвестиций вызывайте метод `commit()` только в самом конце функции, когда все расчёты уже произведены. Это гарантирует, что все операции будут произведены за единую транзакцию, и никто из других пользователей не изменит состояние проектов или пожертвований, пока осуществляются подсчёты для инвестиции.

После коммита выполните `refresh()` того объекта, который вы будете возвращать из эндпоинта, иначе при выполнении кода будет выброшена ошибка `sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here`


[:arrow_up:Оглавление](#Оглавление)
