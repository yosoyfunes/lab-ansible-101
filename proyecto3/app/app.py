#!/usr/bin/env python3
"""
Aplicación TODO - Backend Flask
Laboratorio de Ansible
"""

from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'todoapp'),
    'user': os.getenv('DB_USER', 'todouser'),
    'password': os.getenv('DB_PASSWORD', 'todopass123'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def init_db():
    """Inicializa la base de datos con la tabla de tareas"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cur.close()
            conn.close()
            print("Base de datos inicializada correctamente")
        except Exception as e:
            print(f"Error inicializando la base de datos: {e}")

@app.route('/')
def index():
    """Página principal con interfaz simple"""
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>TODO App - Laboratorio Ansible</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .task { padding: 10px; border: 1px solid #ddd; margin: 5px 0; }
            .completed { background-color: #f0f8f0; }
            input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
            button { padding: 10px 20px; background: #007cba; color: white; border: none; cursor: pointer; }
            button:hover { background: #005a87; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📝 TODO App - Laboratorio Ansible</h1>
            <p><strong>Backend:</strong> Flask en {{ request.host }}</p>
            
            <h2>Agregar Nueva Tarea</h2>
            <form id="taskForm">
                <input type="text" id="title" placeholder="Título de la tarea" required>
                <textarea id="description" placeholder="Descripción (opcional)"></textarea>
                <button type="submit">Agregar Tarea</button>
            </form>
            
            <h2>Lista de Tareas</h2>
            <div id="tasks"></div>
            
            <script>
                // Cargar tareas al iniciar
                loadTasks();
                
                // Manejar envío del formulario
                document.getElementById('taskForm').addEventListener('submit', function(e) {
                    e.preventDefault();
                    addTask();
                });
                
                function loadTasks() {
                    fetch('/api/tasks')
                        .then(response => response.json())
                        .then(tasks => {
                            const tasksDiv = document.getElementById('tasks');
                            tasksDiv.innerHTML = '';
                            tasks.forEach(task => {
                                const taskDiv = document.createElement('div');
                                taskDiv.className = 'task' + (task.completed ? ' completed' : '');
                                taskDiv.innerHTML = `
                                    <h3>${task.title}</h3>
                                    <p>${task.description || 'Sin descripción'}</p>
                                    <p><small>Creada: ${new Date(task.created_at).toLocaleString()}</small></p>
                                    <button onclick="toggleTask(${task.id}, ${!task.completed})">
                                        ${task.completed ? 'Marcar Pendiente' : 'Marcar Completada'}
                                    </button>
                                    <button onclick="deleteTask(${task.id})" style="background: #dc3545;">Eliminar</button>
                                `;
                                tasksDiv.appendChild(taskDiv);
                            });
                        });
                }
                
                function addTask() {
                    const title = document.getElementById('title').value;
                    const description = document.getElementById('description').value;
                    
                    fetch('/api/tasks', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({title, description})
                    })
                    .then(response => response.json())
                    .then(() => {
                        document.getElementById('title').value = '';
                        document.getElementById('description').value = '';
                        loadTasks();
                    });
                }
                
                function toggleTask(id, completed) {
                    fetch(`/api/tasks/${id}`, {
                        method: 'PUT',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({completed})
                    })
                    .then(() => loadTasks());
                }
                
                function deleteTask(id) {
                    if (confirm('¿Estás seguro de eliminar esta tarea?')) {
                        fetch(`/api/tasks/${id}`, {method: 'DELETE'})
                            .then(() => loadTasks());
                    }
                }
            </script>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Obtiene todas las tareas"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, title, description, completed, created_at FROM tasks ORDER BY created_at DESC')
        tasks = []
        for row in cur.fetchall():
            tasks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'completed': row[3],
                'created_at': row[4].isoformat() if row[4] else None
            })
        cur.close()
        conn.close()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Crea una nueva tarea"""
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Título requerido'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id',
            (data['title'], data.get('description', ''))
        )
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': task_id, 'message': 'Tarea creada exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Actualiza una tarea"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos requeridos'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor()
        if 'completed' in data:
            cur.execute('UPDATE tasks SET completed = %s WHERE id = %s', (data['completed'], task_id))
        if 'title' in data:
            cur.execute('UPDATE tasks SET title = %s WHERE id = %s', (data['title'], task_id))
        if 'description' in data:
            cur.execute('UPDATE tasks SET description = %s WHERE id = %s', (data['description'], task_id))
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Tarea actualizada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Elimina una tarea"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Tarea eliminada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Endpoint de salud"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
