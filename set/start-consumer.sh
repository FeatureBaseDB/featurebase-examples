#!/bin/bash
chmod 755 ../../idk/*

for (( ; ; ))
do
../../idk/molecula-consumer-kafka-static --topics allyourbase --index allyourbase  --header schema.json --kafka-hosts localhost:9092 --featurebase-hosts "localhost:10101" --future.rename --allow-missing-fields --primary-key-fields draw_id --concurrency 4 --batch-size 500000
done