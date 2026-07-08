from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Configuración de la conexión a tu PostgresApp de Mac
# (Por defecto, PostgresApp usa tu nombre de usuario de Mac como BD y usuario)
DB_PARAMS = {
    "host": "localhost",
    "database": "postgres",  # Si te da error, luego lo cambiamos por tu usuario de Mac
    "user": "postgres",
    "port": 5432
}

def inicializar_base_de_datos():
    """Función para crear las tablas reales en Postgres si no existen"""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    
    # Creamos la tabla de Pedidos real en tu PostgreSQL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id_pedido INT PRIMARY KEY,
            cliente_nombre VARCHAR(100),
            total DECIMAL(10, 2)
        );
    """)
    
    # Creamos la tabla intermedia de Lineas de Pedido con su Foreign Key
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lineas_pedido (
            id_linea SERIAL PRIMARY KEY,
            pedido_id INT REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
            producto_id INT
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

# Ejecutamos la creación de tablas al arrancar la API
inicializar_base_de_datos()


@app.post("/nuevo-pedido/")
def recibir_pedido(pedido: dict):
    # 1. Validación básica
    if pedido["total"] <= 0:
        return {"estado": "ERROR", "mensaje": "El total debe ser mayor que cero."}
        
    nombre_limpio = pedido["cliente"]["nombre"].upper()
    
    try:
        # 2. Conectar a PostgreSQL Real
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # 3. INSERTAR EN TABLA PEDIDOS
        cursor.execute(
            "INSERT INTO pedidos (id_pedido, cliente_nombre, total) VALUES (%s, %s, %s) ON CONFLICT (id_pedido) DO NOTHING;",
            (pedido["id_pedido"], nombre_limpio, pedido["total"])
        )
        
        # 4. INSERTAR EN TABLA INTERMEDIA (Lineas_Pedido)
        productos = [101, 102]
        for prod_id in productos:
            cursor.execute(
                "INSERT INTO lineas_pedido (pedido_id, producto_id) VALUES (%s, %s);",
                (pedido["id_pedido"], prod_id)
            )
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "estado": "GUARDADO_EN_POSTGRES_REAL",
            "mensaje": f"El pedido {pedido['id_pedido']} se ha guardado físicamente en tu Mac."
        }
        
    except Exception as e:
        return {"estado": "ERROR_BD", "detalles": str(e)}