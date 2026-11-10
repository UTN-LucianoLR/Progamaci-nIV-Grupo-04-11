import sys
import websocket

if len(sys.argv) < 3:
    print("Uso: python escuchar.py <proyecto_id> <access_token>")
    sys.exit(1)

proyecto, token = sys.argv[1], sys.argv[2]
url = f"ws://127.0.0.1:8000/ws/projects/{proyecto}/?token={token}"
print(f"Conectando a {url} ...")

try:
    ws = websocket.create_connection(url)
    print("Conectado. Esperando mensajes (Ctrl+C para salir)...")
    while True:
        print(ws.recv())
except KeyboardInterrupt:
    print("\nDesconectado.")
except Exception as e:
    print(f"Error de conexión: {e}")
