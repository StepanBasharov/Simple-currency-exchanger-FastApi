# Микросервис для конвертации валют 

<h2>Стек технологий</h2>
<ul>
<li>Python 3.10</li>
<li>FastAPI</li>
<li>SQLAlchemy</li>
<li>Alembic</li>
<li>Postgresql</li>
<li>Docker-compose</li>
</ul>

<h2>Деплой</h2>
<li>Создайте файл .env и скопируйте в него содержимое example.env</li>
<code>
HOST="0.0.0.0"
PORT=8000
DB_URL="postgresql+asyncpg://postgres:postgres@db/exchange_db"
DB_URL_ALEMBIC="postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/exchange_db"
</code>
<li>Запустите команду <code>docker-compose up --build -d</code></li>
<li>Запустите команду <code>alembic upgrade head</code></li>

<h4>Сервис полностью готов к работе :)</h4>