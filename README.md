# GitLab-WH
This is a web service for **GitLab Free** owners that will help you **expand functionality to the Premium/Ultimate version**, as well as further automate some development processes.

# Запуск для отладки
## Linux
```bash
granian --interface asgi --log --log-level debug --loop uvloop src/main:gitlab_wh
```

## Windows
```bash
granian --interface asgi --log --log-level debug --loop auto src/main:gitlab_wh
```

# Запуск тестов
## С помощью [Coverage](https://coverage.readthedocs.io/en/7.3.2/index.html)
```bash
coverage run -m pytest tests/
```

## Просмотр отчета
```bash
coverage report -m --skip-covered
```
