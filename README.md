# Категоризация сайтов

Это программа которая поможет избежать посещение поддельных, фишинговых и вредоносных сайтов. Также она блоокирует  сайты с шок-контентом. Больше можете не беспокоиться за вашу безопасность использования Интернета и ваших детей


## Table Of Content

- [Загрузка](#Загрузка)
- [О проекте](#О-проекте)
- [Сайт](#сайт)
- [Ссылки](#ссылки)

## Загрузка

1. Скачивание утилиты для прокси-сервера

```bash
sudo apt-get install squid -y
```

2. Запуск сервера

```bash
systemctl start squid
```

3. Добавление службы Squid в автозагрузку:

```bash
sudo systemctl enable squid
```

4. Создание файлика с заблокированными сайтами

```bash
sudo touch /etc/squid/bad-sites.acl
```

5. Создание скрипта на Python для обновленя списка на устройстве

```bash
sudo touch /etc/squid/update-blocked-sites.py
```
И сразу напишем программу:
```bash
sudo nano /etc/squid/update-blocked-sites.py
```
```python
import requests

url = 'https://dolomite-bubbly-icecream.glitch.me/uploads/bad_sites.txt'
response = requests.get(url)
with open('/etc/squid/bad-sites.acl', 'wt') as f:
    for el in str(response.content, "UTF-8").split("\n"):
        f.write(el + "\n")
```

6. Настроим кофигурационный файл
```bash
sudo nano /etc/squid/squid.conf
```
Запишем туда
```bash
acl blocked_sites dstdomain "/etc/squid/bad-sites.acl"
deny_info https://dolomite-bubbly-icecream.glitch.me/block  blocked_sites
http_access deny blocked_sites
```
7. Настроем таблицу cron для ежедневного обновления в 03:00

```bash
sudo crontab -e -u root
```
Запишем в таблицу
```bash
0 03 * * * /usr/bin/python /etc/squid/update-blocked-sites.py
0 03 * * * systemctl restart squid
```

## О проекте

Данная программа представляет собой инструмент для контроля доступа к определенным сайтам в сети Интернет. Она отслеживает, на какие сайты заходит пользователь. Если сайт находится в списке заблокированных, программа блокирует его и перенаправляет на https://dolomite-bubbly-icecream.glitch.me/block.

Список заблокированных сайтов хранится на [сервере](https://dolomite-bubbly-icecream.glitch.me/), который может обновлять любой пользователь. Также пользователи могут обжаловать попадание сайта в этот список.

Данная программа может быть полезна для родительского контроля и защиты от нежелательного контента в Интернете. Она также может использоваться в организациях для контроля доступа к сайтам.

## Сайт
На [сайте](https://dolomite-bubbly-icecream.glitch.me/list) можно ознакомиться со всеми заблокированными доменами
Можно [самому](https://dolomite-bubbly-icecream.glitch.me/) отправить известные вредоносные сайты, чтобы помочь поддерживать актуальность 


## Ссылки

* [Сайт](https://dolomite-bubbly-icecream.glitch.me/list)
