#!/bin/bash

#Buscar entradas fallidas de inicio de sesion
failed_attempts=$(grep -c 'Failed password' /var/log/auth.log*)

echo $failed_attempts
