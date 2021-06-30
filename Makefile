run:
	uvicorn --host 0.0.0.0 main:app --reload
install:
	pip install -r requirements.txt