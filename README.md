# Laboratorio de Ansible - Proyectos Educativos

Este repositorio contiene tres proyectos progresivos para aprender Ansible desde lo básico hasta conceptos intermedios, incluyendo el uso de roles.

## Estructura del Laboratorio

```
ansible-laboratorio/
├── proyecto1/          # Proyecto básico: Nginx + Node.js (Playbooks)
└── proyecto2/          # Proyecto básico: Nginx + Node.js (Roles)
```

## Proyecto 1: Hello World API (Básico)

**Ideal para:** Estudiantes que nunca han usado Ansible

### Arquitectura
```
[Cliente] → [Nginx:80] → [localhost:3000 Node.js]
```

### Características
- **1 servidor** (todo en uno)
- **Aplicación simple** Hello World API desde GitHub
- **Sin base de datos** - enfoque en conceptos básicos
- **Configuración mínima** - solo 1 archivo para cambiar IP
- **Clonado automático** - repositorio desde GitHub
- **Conceptos básicos**: inventarios, playbooks, módulos fundamentales

### Objetivos de Aprendizaje
1. Configuración de inventarios
2. Clonado de repositorios con `git`
3. Instalación de paquetes con `apt`
4. Manejo de servicios con `systemd`
5. Copia de archivos con `copy`
6. Proxy reverso básico con Nginx

---

## Proyecto 2: Hello World API con Roles (Básico-Intermedio)

**Ideal para:** Estudiantes que completaron el Proyecto 1 y quieren aprender sobre roles

### Arquitectura
```
[Cliente] → [Nginx:80] → [localhost:3000 Node.js]
```

### Características
- **1 servidor** (todo en uno)
- **Misma aplicación** que Proyecto 1 pero con roles
- **Organización por roles** - separación de servicios
- **Reutilización** - roles pueden usarse en otros proyectos
- **Conceptos de roles**: estructura, variables, handlers

### Objetivos de Aprendizaje
1. Estructura y organización de roles
2. Variables por defecto en roles
3. Handlers en roles
4. Separación de responsabilidades
5. Reutilización de código
6. Mejores prácticas de organización

## Cómo Usar Este Laboratorio

### Para Instructores
1. **Empezar con Proyecto 1** - conceptos básicos
2. **Avanzar a Proyecto 2** - misma aplicación con roles
3. Cada proyecto tiene ejercicios progresivos
4. Documentación completa incluida

### Para Estudiantes
1. **Requisitos**: Conocimientos básicos de Linux y SSH
2. **Tiempo estimado**: 
   - Proyecto 1: 1 hora
   - Proyecto 2: 2 horas
3. **Progresión recomendada**: Completar en orden 1 → 2 → 3

## Requisitos Generales

### Software
- Ansible 2.9+
- Servidores Ubuntu 20.04+ (VMs, contenedores, o cloud)
- Acceso SSH con sudo

### Conocimientos Previos
- Comandos básicos de Linux
- Conceptos de SSH
- Nociones básicas de redes (IP, puertos)

## Configuración Rápida

### Proyecto 1 (Básico)
```bash
cd proyecto1
# 1. Editar inventario/inventory.ini con tu IP
# 2. Ejecutar
ansible-playbook -i inventario/inventory.ini playbooks/site.yml
```

### Proyecto 2 (Básico-Intermedio)
```bash
cd proyecto2
# 1. Editar inventario/inventory.ini con tu IP
# 2. Ejecutar
ansible-playbook -i inventario/inventory.ini playbooks/site.yml
```

## Documentación

Cada proyecto incluye:
- `README.md` - Descripción general
- `CONFIGURACION.md` - Guía para cambiar IPs
- `INSTRUCCIONES.md` - Pasos detallados
- Scripts de prueba y verificación

## Conceptos Cubiertos

### Proyecto 1
- [x] Inventarios básicos
- [x] Playbooks simples
- [x] Módulos: `apt`, `copy`, `file`, `systemd`, `git`
- [x] Clonado de repositorios
- [x] Verificaciones con `uri`

### Proyecto 2
- [x] Estructura y organización de roles
- [x] Variables por defecto en roles
- [x] Handlers en roles
- [x] Separación de responsabilidades
- [x] Reutilización de código
- [x] Mejores prácticas de organización

## Contribuciones

Este laboratorio está diseñado para ser educativo y práctico. Si encuentras mejoras o tienes sugerencias, son bienvenidas.

## Licencia

Material educativo de libre uso para instituciones y estudiantes.