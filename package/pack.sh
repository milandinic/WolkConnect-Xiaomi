#!/bin/bash
rm -rf wolk-xiaomi*
tar -zcvf wolk-xiaomi_0.0.orig.tar.gz ../../WolkConnect-Python-Xi/ --exclude=package --exclude=.git

tar -zxvf wolk-xiaomi_0.0.orig.tar.gz

cd WolkConnect-Python-Xi/ && debuild -us -uc -b -d
