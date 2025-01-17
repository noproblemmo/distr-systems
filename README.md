# Задачи

## 0. Система контроля версий (Done)

Если Вы используете распределенную систему управления версиями (например git), то одна задача считается решенной.

## 1. Базовая библиотека (Done)

Выделить библиотеку для построения прототипов распределенных систем. Примеры сущностей: компьютер, сетевой интерфейс, комьютерная сеть. "Сеть" должна обеспечивать адресацию "компьютеров" и передачу данных.

## 2. Прототип DNS (Done)

* Реализовать нерекурсивный запрос (см. пример на Википедии). (Done)
* Реализорвать рекурсивный запрос. (Done)
* Написать небольшой текст о проблеме рекурсивных запросов. Можно продемонстрировать тестами или демо-кодом. (Done)

Рекурсивные DNS запросы считаются небезопасными, так как после отправки пакета на указанный в настройках сетевой карты сервер мы не знаем куда он пойдет дальше и сколько прыжков ему придется совершить, чтобы сделать resolve доменного имени. Это число может быть большим, что говорит о большом количестве участников в этой цепочке. Вероятность подмены искомого IP в таком случае увеличивается.

Однако это не единственная проблема рекурсиных DNS запросов. Злоумышленник может отправить большое количество несуществующих имен на DNS сервер для resolve, что заставит сервер их закэшировать до resolve'а корневыми серверами, что заставит потратить дополнительные ресурсы DNS сервера.

Примеры: 
* https://www.securitylab.ru/news/508472.php
* https://www.tadviser.ru/index.php/%D0%A1%D1%82%D0%B0%D1%82%D1%8C%D1%8F:%D0%90%D1%82%D0%B0%D0%BA%D0%B8_%D0%BD%D0%B0_DNS-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0#.D0.90.D1.82.D0.B0.D0.BA.D0.B0_.D1.81_.D0.BF.D0.BE.D0.BC.D0.BE.D1.89.D1.8C.D1.8E_.D1.80.D0.B5.D0.BA.D1.83.D1.80.D1.81.D0.B8.D0.B2.D0.BD.D1.8B.D1.85_DNS-.D0.B7.D0.B0.D0.BF.D1.80.D0.BE.D1.81.D0.BE.D0.B2

## 3. Репликация (Done)

Разработать прототип системы с репликацией. Использовать базовую библиотеку (несколько компьютеров в сети). Показать в тестах штатный режим работы системы (запись и использование данных), поломки (например, вышел из строя основной компьютер).

Ссылки:

* [Шардирование vs репликация: масштабируем БД](https://zen.yandex.ru/media/id/5af88d8c482677990692cd7c/shardirovanie-vs-replikaciia-masshtabiruem-bd-5cfb901e83e84200af3e1dfa)
* [Путеводитель по репликации баз данных](https://habr.com/ru/post/514500/)

## 4. Шардирование (Done)

Разработать прототип системы с шардированием. Показать в тестах штатный режим работы (запись и использование данных), и поломки.

Ссылки:

* [Шардирование vs репликация: масштабируем БД](https://zen.yandex.ru/media/id/5af88d8c482677990692cd7c/shardirovanie-vs-replikaciia-masshtabiruem-bd-5cfb901e83e84200af3e1dfa)
* [Теория шардирования](https://habr.com/ru/company/oleg-bunin/blog/433370/)
* [Шардирование баз данных](https://ru.bmstu.wiki/%D0%A8%D0%B0%D1%80%D0%B4%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D0%B1%D0%B0%D0%B7_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85)

## 5. BitTorrent (Done)

Разработать прототип пиринговой системы для обмена файлами в соотвествии с основными принципами работы протокола BitTorrent. Реализовать работу с трекером. Использовать базовую библиотеку.

Ссылки:

* [Как работают торренты и насколько это законно](https://club.dns-shop.ru/blog/t-326-internet/44272-kak-rabotaut-torrentyi-i-naskolko-eto-zakonno/)
* [BitTorrent](https://ru.bmstu.wiki/BitTorrent)

## 5.5. Распределенная хеш-таблица

Разработать код, объясняющий, что такое распределенная хеш-таблица. Показать добавление, поиск и перераспределение данных.

* [Распределённая хеш-таблица](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F_%D1%85%D0%B5%D1%88-%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0)
* [Distributed Hash Tables, Part I](https://www.linuxjournal.com/article/6797)
* [Простое базовое объяснение распределенной таблицы Hash (DHT)](https://coderoad.ru/144360/%D0%9F%D1%80%D0%BE%D1%81%D1%82%D0%BE%D0%B5-%D0%B1%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5-%D0%BE%D0%B1%D1%8A%D1%8F%D1%81%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D0%B9-%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D1%8B-Hash-DHT)
* [Протокол DHT](http://translatedby.com/you/protocol-dht/)

## 6. Блокчейн

Разработать прототип блокчейн-системы. Материалы [How to Build a Blockchain in Python](https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/) и [Блокчейн на Python](https://habr.com/ru/company/ruvds/blog/589371/) дают хорошее представление о принципах работы блокчейна.

При разворачивании системы на "компьютерах" базовой библиотеки (задача 1) полезно разобрать материал [Создаем Blockchain с нуля на Python](https://python-scripts.com/blockchain). Если такое разворачивание покажется трудным или бессмысленным, то можно повторить
реализацию с Flask. Это будет очень полезно с точки зрения освоения технологий.
