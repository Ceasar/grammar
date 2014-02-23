

test:
	py.test test_grammar.py

coverage:
	py.test --verbose --cov-report term-missing --cov=grammar test_regular.py
