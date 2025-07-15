#!/bin/bash
# Script para probar conectividad con los servidores

echo "=== Probando conectividad con Ansible ==="
echo

echo "1. Verificando conectividad básica..."
ansible all -i inventario/hosts.yml -m ping

echo
echo "2. Verificando información del sistema..."
ansible all -i inventario/hosts.yml -m setup -a "filter=ansible_distribution*"

echo
echo "3. Verificando espacio en disco..."
ansible all -i inventario/hosts.yml -m shell -a "df -h /"

echo
echo "4. Verificando memoria..."
ansible all -i inventario/hosts.yml -m shell -a "free -h"

echo
echo "=== Pruebas completadas ==="
