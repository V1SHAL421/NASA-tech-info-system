.PHONY: run test install lint freeze

run:
	streamlit run /Users/vishal/Documents/NASA-tech-info-system/src/main.py

test:
	pytest tests/

lint:
	ruff check .
	ruff format .

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt