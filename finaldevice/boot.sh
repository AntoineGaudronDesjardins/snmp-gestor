#!/bin/sh

# Start rsyslog deamon
rsyslogd

# Start ssh deamon
/usr/sbin/sshd

# Start snmp deamon
/usr/sbin/snmpd -Dall -f

