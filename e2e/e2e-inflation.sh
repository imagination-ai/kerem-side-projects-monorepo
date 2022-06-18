# Docker setup

docker-compose down --volumes --remove-orphans
docker-compose up -d inflation
sleep 10
echo Docker setup done.

# Crawling
echo CRAWLING starting for a small dataset.
crawl_output=$(http :8000/Crawl\?excel_path\=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1Xv5UOTpzDPELdtk8JW1oDWbjpsEexAKKLzgzZBB-2vw%2Fedit%23gid%3D0 | jq .data.filename | tr -d '"') || exit -1
echo CRAWL output will be: ${crawl_output}. Giving 5 seconds waiting.

# Parsing
echo PARSING starting for the crawl output: ${crawl_output}
parse_output=$(http :8000/Parse?source_filename=${crawl_output} | jq .data.filename | tr -d '"') || exit -1
echo PARSING should be done soon and output will be: ${parse_output}

docker-compose down
echo "Success!"
