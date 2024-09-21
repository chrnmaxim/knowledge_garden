---
title: Монтирование бакета на ВМ Compute Cloud
draft: false
tags:
  - YandexCloud
---
### Начало работы

#### 1. Установить rclone на Linux:
```bash
sudo -v ; curl https://rclone.org/install.sh | sudo bash
```
#### 2. [Создать профиль подключения](https://yandex.cloud/ru/docs/storage/tutorials/s3-disk-connect?utm_referrer=about%3Ablank#:~:text=%D0%BA%20Object%20Storage-,%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%82%D0%B5%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20Object%20Storage,-%D0%92%20%D1%80%D0%B0%D0%B1%D0%BE%D1%87%D0%B5%D0%B9%20%D0%BF%D0%B0%D0%BF%D0%BA%D0%B5) к Object Storage.
### Монтировать вручную
#### 1. Смонтировать бакет

```bash
rclone mount s3-connect:<имя_бакета>  <директория> --vfs-cache-mode off --allow-non-empty --daemon
```
`--vfs-cache-mode off`

In this mode (the default) the cache will read directly from the remote and write directly to the remote without caching anything on disk.

This will mean some operations are not possible

	- Files can't be opened for both read AND write
	- Files opened for write can't be seeked
	- Existing files opened for write must have O_TRUNC set
	- Files open for read with O_TRUNC will be opened write only
	- Files open for write only will behave as if O_TRUNC was supplied
	- Open modes O_APPEND, O_TRUNC are ignored
	- If an upload fails it can't be retried
`--allow-non-empty`

Allow mounting over a non-empty directory

`--daemon`

Run mount in background and exit parent process

#### 2. Удалить маунт
```bash
fusermount -u <директория>
```
### Автоматический запуск через демон
#### 1. Создать демон
```bash
nano .config/systemd/user/rclone@.service
```

```bash
[Unit]
Description=rclone: Remote FUSE filesystem for cloud storage config %i
Documentation=man:rclone(1)
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
PermissionsStartOnly=true
ExecStartPre=/usr/bin/mkdir -p /home/worker/media/%i
ExecStart= \
  /usr/bin/rclone mount s3-connect:<bucket>-%i /home/<user>/<ditecroty>/%i \
    --config=/home/<user>/.config/rclone/rclone.conf \
    --vfs-cache-mode writes \
    --vfs-cache-max-size 100M \
    --allow-other \
    --allow-root
ExecStop=/bin/fusermount -u /home/<user>/<ditecroty>/&i

[Install]
WantedBy=default.target
```

* `--allow-other `

	Allow access to other users

* `--allow-root`

	Allow access to root user
	Необходимо для обхода [[#^384334|ошибки запуска]] Docker контейнера с монтированным бакетом в качестве volume.

* `%i`

	Постфикс бакета и директории.
	Например, для бакета backend-dev == backend-%i.
	Позволяет создавать несколько запущенных демонов для разных бакетов и директорий.
	Можно использовать вместо имени бакета.

* `WantedBy=default.target`

	Необходимо для запуска демона после перезагрузки ВМ.

Чтобы разрешить доступ к маунту всем пользователям, если активирован флаг `--allow-other` , раскомментировать опцию `user_allow_other` в
```bash
sudo nano /etc/fuse.conf
```


#### 2. Перезагрузить демон
```bash
systemctl --user daemon-reload
```

#### 3. Просмотр статуса демона
```bash
systemctl --user status rclone@dev
```

#### 4. Запуск демона
```bash
systemctl --user enable --now rclone@dev
```

* После `@` указывается постфикс  бакета.
 
### Документация
* [Документация rclone](https://rclone.org/commands/rclone_mount/)
* [Документация Yandex Cloud. Подключение бакета как диска в Windows](https://yandex.cloud/ru/docs/storage/tutorials/s3-disk-connect?utm_referrer=about%3Ablank)
* [Rclone systemd service. GitHub Gist](https://gist.github.com/kabili207/2cd2d637e5c7617411a666d8d7e97101)
* [Can't expose a fuse based volume to a Docker container](https://stackoverflow.com/questions/28865407/cant-expose-a-fuse-based-volume-to-a-docker-container) ^384334

----
📂 [[Yandex Cloud]]

Последнее изменение: 21.09.2024 20:08