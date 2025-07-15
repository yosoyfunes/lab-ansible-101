# Instrucciones del Laboratorio de Ansible

## Preparación del Entorno

### 1. Requisitos Previos
- 3 servidores Ubuntu 20.04+ (pueden ser VMs, contenedores Docker, o instancias cloud)
- Ansible 2.9+ instalado en la máquina de control
- Acceso SSH con sudo a todos los servidores
- Python 3 instalado en todos los servidores

### 2. Configuración de Servidores
**⚠️ PASO CRÍTICO:** Antes de continuar, lee el archivo `CONFIGURACION.md` y actualiza todas las direcciones IP en los archivos de configuración.

Los archivos que debes modificar son:
- `inventario/hosts.yml`
- `files/nginx.conf`
- `files/todo-app.service`
- `files/pg_hba.conf`

### 3. Configuración SSH
Asegúrate de tener acceso SSH sin contraseña:
```bash
# Generar clave SSH si no tienes una
ssh-keygen -t rsa -b 4096

# Copiar clave a cada servidor
ssh-copy-id ubuntu@IP_SERVIDOR_1
ssh-copy-id ubuntu@IP_SERVIDOR_2
ssh-copy-id ubuntu@IP_SERVIDOR_3
```

## Ejecución del Laboratorio

### Paso 1: Verificar Conectividad
```bash
# Probar conectividad básica
ansible all -i inventario/hosts.yml -m ping

# O usar el script incluido
./scripts/test-connectivity.sh
```

### Paso 2: Despliegue por Componentes (Recomendado para aprendizaje)
```bash
# 1. Configurar base de datos
ansible-playbook -i inventario/hosts.yml playbooks/database.yml

# 2. Configurar servidor de aplicación
ansible-playbook -i inventario/hosts.yml playbooks/appserver.yml

# 3. Configurar servidor web
ansible-playbook -i inventario/hosts.yml playbooks/webserver.yml
```

### Paso 3: Despliegue Completo
```bash
# Desplegar toda la aplicación de una vez
ansible-playbook -i inventario/hosts.yml playbooks/site.yml
```

## Verificación

### 1. Verificar Servicios
```bash
# Estado de PostgreSQL
ansible databases -i inventario/hosts.yml -m shell -a "systemctl status postgresql"

# Estado de la aplicación Flask
ansible appservers -i inventario/hosts.yml -m shell -a "systemctl status todo-app"

# Estado de Nginx
ansible webservers -i inventario/hosts.yml -m shell -a "systemctl status nginx"
```

### 2. Probar la Aplicación
- Accede a `http://IP_DEL_SERVIDOR_WEB` en tu navegador
- Deberías ver la interfaz de la aplicación TODO
- Prueba crear, completar y eliminar tareas

### 3. Endpoints de la API
- `GET /api/tasks` - Listar todas las tareas
- `POST /api/tasks` - Crear nueva tarea
- `PUT /api/tasks/{id}` - Actualizar tarea
- `DELETE /api/tasks/{id}` - Eliminar tarea
- `GET /health` - Estado del backend

## Ejercicios para Estudiantes

### Ejercicio 1: Modificar Variables
1. Cambia el puerto de la aplicación Flask de 5000 a 8080
2. Actualiza las variables necesarias
3. Re-ejecuta los playbooks afectados

### Ejercicio 2: Agregar Nuevo Servidor Web
1. Agrega un segundo servidor web al inventario
2. Ejecuta el playbook de webserver
3. Verifica que ambos servidores funcionen

### Ejercicio 3: Personalizar Configuración
1. Modifica el archivo `files/nginx.conf` para cambiar el puerto de escucha
2. Actualiza el archivo `files/todo-app.service` para cambiar variables de entorno
3. Aplica los cambios ejecutando los playbooks correspondientes

### Ejercicio 4: Monitoreo
1. Agrega un playbook para instalar y configurar un monitor básico
2. Crea checks de salud para todos los servicios
3. Implementa alertas básicas

## Troubleshooting

### Problemas Comunes

1. **Error de conexión SSH**
   - Verifica que las IPs sean correctas
   - Confirma que el usuario tenga acceso sudo
   - Revisa la configuración de SSH

2. **Error de permisos**
   - Asegúrate de usar `become: yes` donde sea necesario
   - Verifica que el usuario tenga permisos sudo

3. **Servicios no inician**
   - Revisa los logs: `journalctl -u nombre-servicio`
   - Verifica la configuración de templates
   - Confirma que las dependencias estén instaladas

4. **Base de datos no conecta**
   - Verifica que PostgreSQL esté ejecutándose
   - Revisa la configuración de pg_hba.conf
   - Confirma que el firewall permita conexiones

### Comandos Útiles
```bash
# Ver logs de Ansible
tail -f ansible.log

# Ejecutar en modo verbose
ansible-playbook -vvv -i inventario/hosts.yml playbooks/site.yml

# Ejecutar solo en un servidor específico
ansible-playbook -i inventario/hosts.yml playbooks/webserver.yml --limit web01

# Verificar sintaxis sin ejecutar
ansible-playbook -i inventario/hosts.yml playbooks/site.yml --syntax-check

# Modo dry-run
ansible-playbook -i inventario/hosts.yml playbooks/site.yml --check
```
