# Laboratorio de Ansible - Aplicación TODO de 3 Capas

## Descripción
Este laboratorio enseña los conceptos básicos de Ansible mediante el despliegue de una aplicación TODO completa con:
- **Frontend**: Nginx sirviendo interfaz web
- **Backend**: Flask API (Python)
- **Base de Datos**: PostgreSQL

## Arquitectura
```
[Cliente] → [Nginx:80] → [Flask:5000] → [PostgreSQL:5432]
```

## Estructura del Proyecto
```
ansible-laboratorio/
├── inventario/
│   ├── hosts.yml              # Inventario de servidores
│   └── group_vars/            # Variables por grupos
├── playbooks/
│   ├── site.yml              # Playbook principal
│   ├── webserver.yml         # Configuración Nginx
│   ├── appserver.yml         # Configuración Flask
│   └── database.yml          # Configuración PostgreSQL
├── files/                   # Archivos de configuración
└── app/                     # Código de la aplicación
```

## Requisitos
- Ansible 2.9+
- 3 servidores Ubuntu/CentOS (pueden ser VMs o contenedores)
- Acceso SSH con sudo

## Uso
```bash
# Verificar conectividad
ansible all -i inventario/hosts.yml -m ping

# Desplegar aplicación completa
ansible-playbook -i inventario/hosts.yml playbooks/site.yml

# Desplegar componentes individuales
ansible-playbook -i inventario/hosts.yml playbooks/webserver.yml
ansible-playbook -i inventario/hosts.yml playbooks/appserver.yml
ansible-playbook -i inventario/hosts.yml playbooks/database.yml
```

## Objetivos de Aprendizaje
1. Configuración de inventarios y grupos
2. Uso de variables básicas
3. Instalación y configuración de servicios
4. Manejo de archivos y permisos
5. Orquestación de aplicaciones multi-tier
