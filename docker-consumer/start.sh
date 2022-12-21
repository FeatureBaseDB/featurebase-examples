#!/bin/bash

/featurebase/idk/molecula-consumer-csv --pilosa-hosts="featurebase:10101" --batch-size=10000 --auto-generate --index=consumer --files=/featurebase/sample.csv

# used for debugging only
# while true
# do
#   sleep 1
# done
