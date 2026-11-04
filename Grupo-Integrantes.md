Persona 1

 Nombre: Mendoza Juan Ignacio 

 Rol: Product owner/Dev

 Valor que más valora: Compromiso y respecto

 Superpoder: Comunicacion

Persona 2

 Nombre: Lotero Rolón, Luciano Nicolás 

 Rol: Scrum master/Dev

 Valor que más valora: Adaptabilidad

 Superpoder: Persistencia

Persona 3

 Nombre: Diaz Lucia 

 Rol: Dev

 Valor que más valora: comunicación y organización

 Superpoder: investigando

Persona 4

 Nombre: Walter Nahuel Filippi Farmar 

 Rol: Dev

 Valor que más valora: Responsabilidad y confianza 

 Superpoder: Resolución de problemas 

Reglas del grupo: honestidad, disponibilidad, puntualidad.

# **TABLERO TRELLO: TaskFlow (Clases 10 a 13)**
## **CÓMO ARMARLO EN TRELLO**
1. Creá un tablero nuevo: "TaskFlow - Programación IV".

2. Creá estas listas, en este orden: 

   1. Backlog

   2. Por hacer

   3. En desarrollo

   4. En revisión

   5. Hecho

3. Creá estas etiquetas de color: 

   6. PRIORIDAD ALTA (rojo)

   7. PRIORIDAD MEDIA (amarillo)

   8. PRIORIDAD BAJA (verde)

   9. ÉPICA (azul), para identificar la épica de cada tarjeta.

4. Por cada tarjeta: copiá el título en el nombre de la tarjeta, pegá la descripción, agregá la etiqueta de prioridad y creá un checklist llamado "Criterios de aceptación" con los ítems indicados.

5. Ubicá la tarjeta en la lista que figura en "Columna".

## **ÉPICA 1: Tiempo real con Redis (Clase 10)**
### **[E1-01] Instalar Redis y dejarlo como servicio**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 1 Descripción: Instalar Redis (apt, Homebrew, WSL2 o Docker) y agregar channels-redis a requirements.txt. Checklist "Criterios de aceptación":

- [ ] redis-cli ping responde PONG

- [ ] channels-redis figura en requirements.txt
### **[E1-02] Configurar Redis como channel layer**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 1 Descripción: Reemplazar InMemoryChannelLayer por RedisChannelLayer, con la URL tomada de REDIS_URL (por defecto redis://127.0.0.1:6379). Checklist "Criterios de aceptación":

- [ ] El servidor arranca sin errores

- [ ] El grupo de conexiones vive en Redis y no en memoria del proceso
### **[E1-03] Emitir evento task_created desde la API REST**
Columna: Backlog | Etiquetas: PRIORIDAD ALTA, ÉPICA 1 Descripción: Crear NotificationService (notify_task_created y _send) y llamarlo desde perform_create después de guardar. Checklist "Criterios de aceptación":

- [ ] Un POST exitoso (201) entrega el evento a los miembros conectados al proyecto

- [ ] Si Redis está caído, la tarea se guarda, se registra el error en el log y no hay 500
### **[E1-04] Autenticar el WebSocket con JWT en la URL**
Columna: Backlog | Etiquetas: PRIORIDAD ALTA, ÉPICA 1 Descripción: Implementar JWTAuthMiddleware y get_user_from_token, y envolver el URLRouter en asgi.py. Checklist "Criterios de aceptación":

- [ ] Un access token válido permite conectarse

- [ ] Sin token, con token inválido o vencido, la conexión se rechaza

- [ ] Se usa el access token, nunca el refresh
### **[E1-05] Restringir el consumer a miembros del proyecto**
Columna: Backlog | Etiquetas: PRIORIDAD ALTA, ÉPICA 1 Descripción: En connect, cerrar la conexión si el usuario no está autenticado o no es miembro (MembershipService.is_member). Checklist "Criterios de aceptación":

- [ ] Un no miembro no puede suscribirse ni recibir eventos

- [ ] La regla es la misma que en la API REST
### **[E1-06] Presencia online/offline por proyecto**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 1 Descripción: Avisar al grupo cuando un usuario se conecta o desconecta (presence_update y marca joined). Checklist "Criterios de aceptación":

- [ ] Los avisos de conexión y desconexión llegan a todo el grupo

- [ ] Una conexión rechazada no genera aviso "offline"
### **[E1-07] Eventos task_updated y task_completed (tarea para la casa)**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 1 Descripción: Emitir eventos desde perform_update y desde la acción complete, reutilizando _send. Checklist "Criterios de aceptación":

- [ ] Ambos eventos llegan a clientes conectados con el mismo formato que task_created
### **[E1-08] Prueba end-to-end con dos clientes**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 1 Descripción: Ejecutar escuchar.py con dos usuarios miembros del proyecto y crear una tarea por REST. Checklist "Criterios de aceptación":

- [ ] Ambos clientes reciben task_created sin refrescar

- [ ] Al cerrar uno, el otro recibe el aviso "offline"

- [ ] Un token inválido produce error de handshake
### **[E1-09] Reconexión automática en el cliente**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 1 Descripción: Implementar conectarProyecto con backoff exponencial (1s, 2s, 4s, tope 30s), jitter, renovación del token y resincronización por REST. Checklist "Criterios de aceptación":

- [ ] Tras un corte, reintenta con esperas crecientes

- [ ] Al reconectar vuelve a pedir las tareas por REST

- [ ] cerrar() no dispara reintentos
### **[E1-10] Respuesta escrita: Redis vs. Kafka (tarea para la casa)**
Columna: Backlog | Etiquetas: PRIORIDAD BAJA, ÉPICA 1 Descripción: Responder con conclusiones propias la pregunta 3 del cuestionario. Checklist "Criterios de aceptación":

- [ ] Compara modelo, persistencia y casos de uso de Redis pub/sub, Redis Streams, RabbitMQ y Kafka

- [ ] Justifica la elección para TaskFlow

## **ÉPICA 2: GraphQL sobre el dominio existente (Clase 11)**
### **[E2-01] Instalar Graphene-Django y configurar el esquema**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 2 Descripción: Instalar graphene-django, agregarlo a INSTALLED_APPS, definir GRAPHENE["SCHEMA"] y crear config/schema.py. Checklist "Criterios de aceptación":

- [ ] El servidor arranca

- [ ] /graphql/ responde
### **[E2-02] Definir los tipos ProjectType, TaskType y TagType**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 2 Descripción: DjangoObjectType con fields explícitos y convert_choices_to_enum = False. Checklist "Criterios de aceptación":

- [ ] El campo owner no se expone

- [ ] status y priority devuelven texto en minúsculas, igual que REST
### **[E2-03] Queries con las mismas reglas de permisos**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 2 Descripción: Implementar allProjects, task(id) y tasksByStatus usando tasks_visible_for y MembershipService.projects_for. Checklist "Criterios de aceptación":

- [ ] Sin token, allProjects devuelve []

- [ ] Pedir una tarea ajena devuelve null

- [ ] No se pueden leer datos de proyectos ajenos
### **[E2-04] Mutation createTask con validaciones y permisos de REST**
Columna: Backlog | Etiquetas: PRIORIDAD ALTA, ÉPICA 2 Descripción: Validar con TaskSerializer, verificar admin con MembershipService.is_admin y llamar a NotificationService. Checklist "Criterios de aceptación":

- [ ] priority: "urgente" devuelve error en errors

- [ ] Un miembro sin rol admin recibe error de permiso

- [ ] La tarea creada dispara task_created
### **[E2-05] Autenticación JWT en /graphql/**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 2 Descripción: Crear JWTGraphQLView que valida el header Authorization en dispatch, y registrar la ruta con csrf_exempt. Checklist "Criterios de aceptación":

- [ ] Con token válido, info.context.user está autenticado

- [ ] Con token inválido, la petición sigue como anónima sin romper la respuesta
### **[E2-06] Evitar el problema N+1**
Columna: Por hacer | Etiquetas: PRIORIDAD MEDIA, ÉPICA 2 Descripción: Agregar prefetch_related("tasks") en la query de proyectos. Checklist "Criterios de aceptación":

- [ ] La cantidad de consultas SQL no crece con el número de proyectos (2 consultas con 6 proyectos)
### **[E2-07] Prueba integral en GraphiQL**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 2 Descripción: Ejecutar los casos de la guía: anónimo, con token, consulta anidada, mutation válida y los tres errores esperados. Checklist "Criterios de aceptación":

- [ ] Cada caso devuelve el resultado documentado

- [ ] La mutation dispara la notificación en un cliente WebSocket abierto
### **[E2-08] Mutation updateTaskStatus (tarea para la casa)**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 2 Descripción: Seguir el patrón de CreateTask, buscar la tarea con tasks_visible_for y validar con TaskSerializer(partial=True). Checklist "Criterios de aceptación":

- [ ] Solo el admin del proyecto puede cambiar el estado

- [ ] Se aplican las reglas de la Clase 4 igual que en un PATCH
### **[E2-09] Protección contra consultas costosas y límites de uso**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 2 Descripción: Limitar profundidad, calcular costo por query, deshabilitar introspección en producción y agregar rate limiting a JWTGraphQLView. Checklist "Criterios de aceptación":

- [ ] Una consulta demasiado profunda se rechaza

- [ ] La introspección está desactivada con DEBUG=False
### **[E2-10] Comparación REST vs. GraphQL con caso propio (tarea para la casa)**
Columna: Backlog | Etiquetas: PRIORIDAD BAJA, ÉPICA 2 Descripción: Redactar un caso real donde usarían cada uno y justificarlo. Checklist "Criterios de aceptación":

- [ ] Cubre over-fetching, under-fetching, caché, errores y versionado

## **ÉPICA 3: Testing, CI/CD y despliegue (Clase 12)**
### **[E3-01] Configurar pytest, pytest-django y pytest-cov**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Crear pytest.ini, eliminar core/tests.py y crear la carpeta core/tests/ con **init**.py. Checklist "Criterios de aceptación":

- [ ] pytest corre sin errores de import
### **[E3-02] Crear conftest.py con fixtures y entorno aislado**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Fixtures ana, beto, proyecto y cliente; autouse para InMemoryChannelLayer, mock de HolidayService y sin throttling. Checklist "Criterios de aceptación":

- [ ] Los tests corren sin Redis ni internet

- [ ] Cada test se ejecuta de forma independiente
### **[E3-03] Tests unitarios de servicios**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Probar TaskService.mark_completed (con y sin fecha límite) y HolidayService.is_holiday. Checklist "Criterios de aceptación":

- [ ] Los tres tests pasan

- [ ] Completar sin fecha lanza ValidationError
### **[E3-04] Tests de integración de endpoints y permisos**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Probar 401 sin autenticar, aislamiento entre proyectos, creación por admin (201) y rechazo a miembro (403). Checklist "Criterios de aceptación":

- [ ] Los cuatro tests pasan

- [ ] El test de tarea ajena verifica que no aparece en el listado
### **[E3-05] Medir cobertura y verificar una regla de permisos**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 3 Descripción: Ejecutar pytest --cov=core --cov-report=term-missing. Comentar temporalmente check_project_admin para confirmar que un test falla. Checklist "Criterios de aceptación":

- [ ] Se genera el reporte de cobertura

- [ ] El test de permisos falla al quitar la regla y vuelve a pasar al restaurarla
### **[E3-06] Pipeline de CI en GitHub Actions**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Crear .github/workflows/ci.yml con disparo en push y PR a main, variables env y pasos de instalación y tests. Checklist "Criterios de aceptación":

- [ ] El pipeline corre en cada push

- [ ] Aparece en verde en la pestaña Actions

- [ ] No se usan secretos reales en el archivo
### **[E3-07] Configurar settings para producción**
Columna: Por hacer | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Seleccionar motor con DB_ENGINE, instalar psycopg y whitenoise, agregar WhiteNoise a MIDDLEWARE, definir STATIC_ROOT y CSRF_TRUSTED_ORIGINS. Checklist "Criterios de aceptación":

- [ ] Sin DB_ENGINE, todo sigue funcionando con SQLite

- [ ] pytest sigue dando 7 passed

- [ ] staticfiles/, .env y .env.* están en .gitignore
### **[E3-08] Dockerfile y .dockerignore**
Columna: Backlog | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Imagen basada en python:3.12-slim, con collectstatic en el build y migrate + Daphne como comando de arranque. Checklist "Criterios de aceptación":

- [ ] docker build termina sin errores

- [ ] .env, venv/ y db.sqlite3 no quedan dentro de la imagen
### **[E3-09] Orquestar con docker-compose (web, PostgreSQL y Redis)**
Columna: Backlog | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Definir web, db (con healthcheck y volumen pgdata) y redis, y crear .env.docker. Checklist "Criterios de aceptación":

- [ ] docker compose up -d --build levanta los tres servicios

- [ ] /admin/ carga con estilos

- [ ] Los datos persisten tras docker compose down

- [ ] manage.py check --deploy ejecutado y revisado
### **[E3-10] Desplegar en PaaS (Render o Railway)**
Columna: Backlog | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Conectar el repo, cargar variables en el panel, usar Neon o Supabase y Upstash o Redis Cloud, y crear el superusuario desde la consola. Checklist "Criterios de aceptación":

- [ ] La URL pública responde

- [ ] No hay error 400 (ALLOWED_HOSTS) ni 403 CSRF en el login

- [ ] Ninguna clave ni .env está en el repositorio

- [ ] Cada push a main con CI verde dispara un despliegue
### **[E3-11] Versionado SemVer y plan de rollback**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 3 Descripción: Crear el tag v1.0.0, subirlo con git push --tags y documentar cómo volver a un despliegue anterior. Checklist "Criterios de aceptación":

- [ ] El tag existe en GitHub

- [ ] El procedimiento de rollback está escrito e incluye la advertencia sobre migraciones
### **[E3-12] Observabilidad básica**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 3 Descripción: Verificar /api/health/, enviar logs importantes a la salida estándar y revisarlos con docker compose logs. Checklist "Criterios de aceptación":

- [ ] /api/health/ responde 200

- [ ] Los errores relevantes aparecen en los logs del contenedor
### **[E3-13] Entrega final del proyecto**
Columna: Backlog | Etiquetas: PRIORIDAD ALTA, ÉPICA 3 Descripción: Repo con historial desde la Clase 1, CI en verde, URL de despliegue, reporte de cobertura y documento de 1 a 2 carillas con decisiones de arquitectura. Checklist "Criterios de aceptación":

- [ ] Repositorio con historial completo

- [ ] CI en verde

- [ ] URL de despliegue funcionando

- [ ] Reporte de cobertura incluido

- [ ] Documento de arquitectura terminado

## **ÉPICA 4: Frontend mínimo (Clase 13, OPCIONAL)**
### **[E4-01] Agregar el origen del frontend a CORS**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 4 Descripción: Incluir [http://127.0.0.1:5500](http://127.0.0.1:5500) en CORS_ALLOWED_ORIGINS. Checklist "Criterios de aceptación":

- [ ] Las peticiones desde la página no muestran errores de CORS
### **[E4-02] Crear index.html con login y panel de tareas**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 4 Descripción: Dos secciones (login-box y app-box), un select de proyectos y un campo para nueva tarea. Checklist "Criterios de aceptación":

- [ ] La sección de app está oculta hasta el login

- [ ] El HTML carga sin errores en consola
### **[E4-03] Login y manejo del access token**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 4 Descripción: Implementar login() contra /api/token/, con mensajes para credenciales incorrectas y para el 429. Checklist "Criterios de aceptación":

- [ ] Un login válido muestra el panel

- [ ] Un login inválido muestra el mensaje de error

- [ ] El token se guarda en memoria
### **[E4-04] Listar proyectos y tareas paginadas**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 4 Descripción: Implementar loadProjects() y loadTasks() con data.results y textContent. Checklist "Criterios de aceptación":

- [ ] El desplegable muestra solo los proyectos del usuario

- [ ] La lista muestra título y estado de cada tarea
### **[E4-05] Crear tareas desde la página**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 4 Descripción: Implementar createTask() con el proyecto elegido y mostrar los errores de la API. Checklist "Criterios de aceptación":

- [ ] Un admin crea la tarea y la ve arriba de la lista

- [ ] Un miembro ve el error 403 en rojo
### **[E4-06] Servir la página localmente y probar el flujo completo**
Columna: Backlog | Etiquetas: PRIORIDAD MEDIA, ÉPICA 4 Descripción: Usar python3 -m http.server 5500 --bind 127.0.0.1 o Live Server. Checklist "Criterios de aceptación":

- [ ] El flujo login → listado → creación funciona de punta a punta
### **[E4-07] Subir el frontend a su propio repositorio**
Columna: Backlog | Etiquetas: PRIORIDAD BAJA, ÉPICA 4 Descripción: git init, commit y push a un repositorio nuevo taskflow-frontend. Checklist "Criterios de aceptación":

- [ ] El repositorio existe en GitHub con el código actual
### **[E4-08] Mejoras opcionales (Parte 5 de la clase)**
Columna: Backlog | Etiquetas: PRIORIDAD BAJA, ÉPICA 4 Descripción: Token en sessionStorage con botón "Salir"; paginación con Anterior/Siguiente; conexión al WebSocket de la Clase 10 para refrescar al llegar task_created. Checklist "Criterios de aceptación":

- [ ] Cada mejora funciona por separado sin romper el flujo base


