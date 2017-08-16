#!/usr/bin/env bash
TARGET_C2=$1
TARGET_LOG=$2
FILTER=$3
IS_LOG=`ls | grep *.log`

if [ "$IS_LOG" == 0 ] ; then
    cat $TARGET_LOG.* | $FILTER | grep $TARGET_C2
else
    zcat $TARGET_LOG.* | $FILTER | grep $TARGET_C2
fi