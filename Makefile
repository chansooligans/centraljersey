.PHONY: tests_all test-file 

tests_all:
	poetry run pytest -v -rP tests/*

test-file:
	poetry run pytest -v -rP $(file)
