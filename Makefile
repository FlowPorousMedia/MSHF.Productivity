SRC_DIR := src
LOCALE_DIR := $(SRC_DIR)/translations
BABEL_CFG := $(SRC_DIR)/babel.cfg
POT_FILE := $(SRC_DIR)/messages.pot
LANGS := en ru

.PHONY: extract update compile init translate

extract:
	pybabel extract -F $(BABEL_CFG) -o $(POT_FILE) $(SRC_DIR)

update:
	pybabel update -i $(POT_FILE) -d $(LOCALE_DIR)

compile:
	pybabel compile -d $(LOCALE_DIR)

init:
	for lang in $(LANGS); do \
		pybabel init -i $(POT_FILE) -d $(LOCALE_DIR) -l $$lang; \
	done

translate: extract update compile

run:
	python3 main.py
