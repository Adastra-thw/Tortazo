#!/bin/sh

# Script to launch DbVisualizer by manually invoking Java

# Please note that it's *not* recommended to launch DbVisualizer
# with this script. Instead use the "dbvis" launcher on UNIX/Linux
# or the command "open DbVisualizer.app" on Mac OS X.

if [ -z "$DBVIS_HOME" ] ; then 
  DBVIS_HOME=`dirname $0`
fi

JAVA_EXEC=java

CP="$DBVIS_HOME/resources"
CP="$CP:$DBVIS_HOME/lib/*"

# Get the Java version
JAVA_VER=$(java -version 2>&1 | sed 's/java version "\(.*\)\.\(.*\)\..*"/\1\2/; 1q')

MAX_PERM_SIZE="-XX:MaxPermSize=192m"
if [ $JAVA_VER -gt 17 ] ; then
  MAX_PERM_SIZE=""
fi

$JAVA_EXEC -Xmx512M $MAX_PERM_SIZE -Dsun.locale.formatasdefault=true -splash:"$DBVIS_HOME/resources/splash-animated.gif" -Ddbvis.home="$DBVIS_HOME" -cp $CP com.onseven.dbvis.DbVisualizerGUI "$@"
