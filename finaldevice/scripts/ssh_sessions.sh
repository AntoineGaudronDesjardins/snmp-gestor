#!/bin/bash
num_sessions=$(netstat | grep -c 'ssh')
echo $num_sessions
