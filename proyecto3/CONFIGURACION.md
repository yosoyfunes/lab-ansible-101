# Configuración del Laboratorio

## ⚠️ IMPORTANTE: Configurar IPs antes de ejecutar

Antes de ejecutar los playbooks, debes actualizar las direcciones IP en varios archivos para que coincidan con tus servidores reales.

### 1. Actualizar Inventario
Edita el archivo `inventario/hosts.yml` y cambia las IPs:

```yaml
webservers:
  hosts:
    web01:
      ansible_host: TU_IP_SERVIDOR_WEB    # Cambiar por IP real
appservers:
  hosts:
    app01:
      ansible_host: TU_IP_SERVIDOR_APP    # Cambiar por IP real
databases:
  hosts:
    db01:
      ansible_host: TU_IP_SERVIDOR_DB     # Cambiar por IP real
```

### 2. Actualizar Archivos de Configuración

#### Archivo: `files/nginx.conf`
Busca esta línea y cambia la IP del servidor de aplicación:
```nginx
proxy_pass http://192.168.1.11:5000;
```
Cambiar `192.168.1.11` por la IP real de tu servidor de aplicación.

#### Archivo: `files/todo-app.service`
Busca esta línea y cambia la IP del servidor de base de datos:
```
Environment="DB_HOST=192.168.1.12"
```
Cambiar `192.168.1.12` por la IP real de tu servidor de base de datos.

#### Archivo: `files/pg_hba.conf`
Busca esta línea y cambia la IP del servidor de aplicación:
```
host    todoapp         todouser        192.168.1.11/32         md5
```
Cambiar `192.168.1.11` por la IP real de tu servidor de aplicación.

### 3. Ejemplo de Configuración Completa

Si tus servidores tienen las IPs:
- Servidor Web: `10.0.1.100`
- Servidor App: `10.0.1.101`  
- Servidor DB: `10.0.1.102`

Entonces debes cambiar:

**En `inventario/hosts.yml`:**
```yaml
webservers:
  hosts:
    web01:
      ansible_host: 10.0.1.100
appservers:
  hosts:
    app01:
      ansible_host: 10.0.1.101
databases:
  hosts:
    db01:
      ansible_host: 10.0.1.102
```

**En `files/nginx.conf`:**
```nginx
proxy_pass http://10.0.1.101:5000;
```

**En `files/todo-app.service`:**
```
Environment="DB_HOST=10.0.1.102"
```

**En `files/pg_hba.conf`:**
```
host    todoapp         todouser        10.0.1.101/32         md5
```

### 4. Verificar Configuración

Después de hacer los cambios, verifica que todo esté correcto:

```bash
# Probar conectividad
ansible all -i inventario/hosts.yml -m ping

# Verificar que las IPs sean correctas
grep -r "192.168.1" files/
```

Si el comando `grep` devuelve resultados, significa que aún tienes IPs de ejemplo sin cambiar.

## Notas Importantes

- **Consistencia**: Asegúrate de que las IPs sean consistentes en todos los archivos
- **Conectividad**: Todos los servidores deben poder comunicarse entre sí
- **SSH**: Configura acceso SSH sin contraseña a todos los servidores
- **Sudo**: El usuario debe tener permisos sudo en todos los servidores
