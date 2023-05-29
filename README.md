# python-architecture-patterns


## 가상환경 구성

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install pytest`
3. `pip install requirements.txt`
4. `pip install -e src/`

## Makefile 구성

- pytest --tb=short 에서 tb는 traceback을 의미한다. 여기서 사용한 short은 짧은 traceback 포맷을 사용하겠다는 의미이다.
- entr: https://github.com/eradman/entr


## 진행상황
### Part 1: Building an Architecture to Support Domain Modeling
- [X] 1. Domain Modeling
- [X] 2. Repository Pattern
- [ ] 3. A Brief Interlude: On Coupling and Abstractions
- [ ] 4. Our First Use Case: Flask API and Service Layer
- [ ] 5. TDD in High Gear and Low Gear
- [ ] 6. Unit of Work Pattern
- [ ] 7. Aggregates and Consistency Boundaries

### Part 2: Event-Driven Architecture
- [ ] 8. Events and the Message Bus
- [ ] 9. Going to Town on the Message Bus
- [ ] 10. Commands and Command Handler
- [ ] 11. Event-Driven Architecture: Using Events to Integrate Microservices
- [ ] 12. Command-Query Responsibility Segregation (CQRS)
- [ ] 13. Dependency Injection (and Bootstrapping)
