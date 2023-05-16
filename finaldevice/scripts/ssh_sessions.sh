#!/bin/bash
num_sessions=$(ps aux | grep -c 'ssh ')
echo $num_sessions
