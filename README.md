# python-architecture-patterns


## 가상환경 구성

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install pytest`
3. `pip install requirements.txt`
4. `pip install -e src/`

## Makefile 구성

- pytest --tb=short 에서 tb는 traceback을 의미한다. 여기서 사용한 short은 짧은 traceback 포맷을 사용하겠다는 의미이다.
- entr: https://github.com/eradman/entr
