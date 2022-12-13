#!/bin/bash

# get IPs
IP_ADDRESS=$(hostname -i)
IP_HOST_ONE=$(dig +short featurebase1)
IP_HOST_FOUR=$(dig +short featurebase4)
IP_HOST_THREE=$(dig +short featurebase3)

# munge the IP for this box
if [ "$IP_ADDRESS" = "$IP_HOST_ONE" ]; then
    HOSTNAME=featurebase1
fi
if [ "$IP_ADDRESS" = "$IP_HOST_THREE" ]; then
    HOSTNAME=featurebase3
fi
if [ "$IP_ADDRESS" = "$IP_HOST_FOUR" ]; then
    HOSTNAME=featurebase4
fi

# start featurebase
/featurebase/fb/featurebase server --config featurebase.conf --name $NAME --sql.endpoint-enabled --bind $IP_ADDRESS:$BIND_PORT --etcd.listen-client-address http://$IP_ADDRESS:$CLIENT_PORT --etcd.listen-peer-address http://$IP_ADDRESS:$PEER_PORT --etcd.initial-cluster="featurebase1=http://$IP_HOST_ONE:10301,featurebase4=http://$IP_HOST_FOUR:40301,featurebase3=http://$IP_HOST_THREE:30301"