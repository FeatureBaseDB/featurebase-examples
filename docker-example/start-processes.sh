#!/bin/bash

# start featurebase
/featurebase/fb/featurebase server --config featurebase.conf &

# create topic
sleep 15
/featurebase/kafka/bin/kafka-topics.sh --create --topic allyourbase --bootstrap-server kafka:29094
sleep 15

# start kafka consumer over and over
for (( ; ; ))
do
/featurebase/idk/molecula-consumer-kafka-static --topics allyourbase --index allyourbase  --header schema.json --kafka-hosts kafka:29094 --featurebase-hosts "featurebase:10101" --future.rename --allow-missing-fields --auto-generate --external-generate --track-progress --concurrency 1 --batch-size 100000 --verbose
done

