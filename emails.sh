#python mbox_converter.py
rm emails.db
sqlite-utils insert emails.db emails emails_since_2020.csv --csv
sqlite-utils enable-fts emails.db emails body
datasette publish heroku --name political-emails emails.db --extra-options="--config default_page_size:50 --config sql_time_limit_ms:30000 --config facet_time_limit_ms:10000"
