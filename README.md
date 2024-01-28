# GitLab-WH
This is a web service for **GitLab Free** owners that will help you **expand functionality to the Premium/Ultimate version**, as well as further automate some development processes.

Docs - https://inf-inf.github.io/gitlab-wh/

# Local Debug
## Linux
```bash
granian --interface asgi --log --log-level debug --loop uvloop src/main:gitlab_wh.app
```

## Windows
```bash
granian --interface asgi --log --log-level debug --loop auto src/main:gitlab_wh.app
```

# Tests
## With [Coverage](https://coverage.readthedocs.io/en/7.3.2/index.html)
```bash
coverage run -m pytest tests/
```

## View the report
```bash
coverage report -m --skip-covered
```

## Integration
```bash
./tests/integration_tests.sh
```
