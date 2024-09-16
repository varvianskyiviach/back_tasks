# ==============
# local
# ==============

.PHONY: run
run:
	uvicorn main:app --reload

# ==============
# docker db
# ==============

.PHONY: db_up, db_down
db:
	docker compose up -d postgres
stop:
	docker compose stop postgres
rm:
	docker compose rm -f postgres