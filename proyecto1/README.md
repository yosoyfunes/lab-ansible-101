# Laboratorio de Ansible - Proyecto 1: Nginx + Node.js

## Descripción
Este es un laboratorio básico de Ansible que despliega una aplicación simple en un solo servidor:
- **Frontend**: Nginx como proxy reverso (puerto 80)
- **Backend**: Node.js API (puerto 3000) en el mismo servidor

## Arquitectura
```
[Cliente] → [Nginx:80] → [localhost:3000 Node.js]
```

## Estructura del Proyecto
```
proyecto1/
├── inventario/
│   └── inventory.ini        # Inventario de servidores
├── playbooks/
│   └── site.yml             # Playbook principal
└── files/                   # Archivos de configuración
```

## Requisitos
- Docker para crear un servidor y nodo
- Conexión a internet (para clonar repositorio)

## Objetivos de Aprendizaje
1. Configuración básica de inventarios
2. Clonado de repositorios con `git`
3. Instalación de paquetes con `apt`
4. Configuración de servicios con `supervisorctl`
5. Copia de archivos con `copy`
6. Proxy reverso básico con Nginx

## Preparar el Laboratorio con Docker

```bash
# 1. Crear una red Docker para conectar los contenedores
docker network create ansible_network

# 2. Crear la carpeta para almacenar las claves SSH que usará Ansible
mkdir -p inventario/.ssh

# 3. Generar un par de claves SSH (sin passphrase) para la autenticación entre nodos
ssh-keygen -t rsa -b 2048 -f inventario/.ssh/id_rsa -N ''

# 4. Crear el contenedor del nodo gestionado (nodo1)
docker run --name nodo1 --network ansible_network -d yosoyfunes/ansible-nodos:v1

# 5. Copiar la clave pública generada al nodo1 para permitir el acceso SSH sin contraseña
docker exec -i nodo1 bash -c "mkdir -p /root/.ssh && cat >> /root/.ssh/authorized_keys" < inventario/.ssh/id_rsa.pub

# 6. Crear el contenedor del servidor Ansible, montando el directorio de trabajo actual
docker run -ti --name ansible-server \
  --network ansible_network -d -v $(pwd):/ansible_work -w /ansible_work yosoyfunes/ansible-server:v1
```

## Uso
```bash
# Ingresar al contenedor de Ansible Server
docker exec -ti ansible-server bash

# Verificar conectividad
ansible all -i inventario/inventory.ini -m ping

# Desplegar aplicación completa
ansible-playbook -i inventario/inventory.ini playbooks/site.yml
```

---
**Este laboratorio toma como base:**
- Repositorio NodeJS: [https://github.com/yosoyfunes/nodejs-helloworld-api.git](https://github.com/yosoyfunes/nodejs-helloworld-api.git)
- Contenedores Docker con Ansible: [https://github.com/yosoyfunes/ansible-server.git](https://github.com/yosoyfunes/ansible-server.git)