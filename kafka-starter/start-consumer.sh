#!/bin/bash
chmod 755 ../../idk/*

for (( ; ; ))
do
../../idk/molecula-consumer-kafka-static --topics allyourbase --index allyourbase  --header schema.json --kafka-hosts localhost:9092 --featurebase-hosts "localhost:10101" --future.rename --allow-missing-fields --auto-generate --external-generate --track-progress --concurrency 1 --batch-size 100000 --verbose
done