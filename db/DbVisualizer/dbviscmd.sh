#!/bin/sh -v

# Script to launch the command line interface for DbVisualizer

if [ -z "$DBVIS_HOME" ] ; then 
  DBVIS_HOME=`dirname $0`
fi

JAVA_EXEC=java

CP="$DBVIS_HOME/resources"
CP="$CP:$DBVIS_HOME/lib/*"

$JAVA_EXEC -Xmx512M -Dsun.locale.formatasdefault=true -Djava.awt.headless=true -Ddbvis.home="$DBVIS_HOME" -cp $CP com.onseven.dbvis.DbVisualizerCmd "$@"
