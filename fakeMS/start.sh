#!/bin/bash

# osmo-trx-uhd 실행 (백그라운드)
osmo-trx-uhd -C /root/osmo-trx-uhd.cfg &

# trxcon 실행 (백그라운드)
./trxcon &

# mobile 실행 (포그라운드)
mobile -c /root/mobile.cfg