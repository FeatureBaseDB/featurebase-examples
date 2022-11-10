#!/bin/bash

# start featurebase
/featurebase/fb/featurebase server --config featurebase.conf &

# start kafka
/featurebase/kafka/bin/zookeeper-server-start.sh /featurebase/kafka/config/zookeeper.properties &
/featurebase/kafka/bin/kafka-server-start.sh /featurebase/kafka/config/server.properties &

# create topic
sleep 5
/featurebase/kafka/bin/kafka-topics.sh --create --topic allyourbase --bootstrap-server 0.0.0.0:9092

# start kafka consumer
# for (( ; ; ))
# do
# /featurebase/idk/molecula-consumer-kafka-static --topics allyourbase --index allyourbase  --header schema.json --kafka-hosts 0.0.0.0:9092 --featurebase-hosts "0.0.0.0:10101" --future.rename --allow-missing-fields --auto-generate --external-generate --track-progress --concurrency 1 --batch-size 100000 --verbose
# done

/bin/bash