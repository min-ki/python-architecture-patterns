# python-architecture-patterns

파이썬으로 살펴보는 아키텍처 패턴을 읽고 실습한 레포지토리

실습 내용은 [cosmicpython](https://www.cosmicpython.com/)에서 확인하실 수 있습니다.

## 가상환경 구성

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install pytest`
3. `pip install requirements.txt`
4. `pip install -e src/`

## Makefile 구성

- pytest --tb=short 에서 tb는 traceback을 의미한다. 여기서 사용한 short은 짧은 traceback 포맷을 사용하겠다는 의미이다.
- entr: https://github.com/eradman/entr

## docker-compose 구성

- `docker-compose up -d`
- mailhog: 이메일 전송 테스트 도구
- postgres: 데이터베이스
- redis: 메시지 브로커

## 목차

### Part 1: Building an Architecture to Support Domain Modeling

- [x] 1. Domain Modeling
- [x] 2. Repository Pattern
- [x] 3. A Brief Interlude: On Coupling and Abstractions
- [x] 4. Our First Use Case: Flask API and Service Layer
- [x] 5. TDD in High Gear and Low Gear
- [x] 6. Unit of Work Pattern
- [x] 7. Aggregates and Consistency Boundaries

### Part 2: Event-Driven Architecture

- [x] 8. Events and the Message Bus
- [x] 9. Going to Town on the Message Bus
- [x] 10. Commands and Command Handler
- [x] 11. Event-Driven Architecture: Using Events to Integrate Microservices
- [x] 12. Command-Query Responsibility Segregation (CQRS)
- [x] 13. Dependency Injection (and Bootstrapping)
