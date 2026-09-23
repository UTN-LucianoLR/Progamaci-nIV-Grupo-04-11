productos = [
{"nombre": "Laptop", "precio": 1200, "stock": 15},
{"nombre": "Mouse", "precio": 25, "stock": 5},
{"nombre": "Teclado", "precio": 75, "stock": 25},
{"nombre": "Monitor", "precio": 300, "stock": 8},
]

# # esta linea crea una lista vacía para almacenar los productos con bajo stock   
# productos_bajo_stock = []
# # se recorre la lista de productos y se imprime el nombre y precio de cada producto
# for producto in productos:
#     # se imprime el nombre y precio del producto
# print(f"Producto: {producto['nombre']}, Precio: ${producto['precio']}")
#  # se verifica si el stock del producto es menor a 10, si es así se agrega a la lista de productos con bajo stock
# if producto['stock'] < 10:
#     # se agrega el producto a la lista de productos con bajo stock
# productos_bajo_stock.append(producto)

# # se imprime la lista de productos con bajo stock
# print("\nProductos con bajo stock:")
# # se imprime cada producto en la lista de productos con bajo stock
# print(productos_bajo_stock)

# esta funcion calcula el precio promedio de los precios en la lista
# def calcular_promedio_precio(lista):
#     # este if verifica que la lista no este vacia, si es asi retorna 0
#     if not lista:
#         return 0
#     # se saca el promedio de los precios 
#     total_precio = sum(p['precio'] for p in lista)
#     # se devuelve la suma dividida entre la cantidad de indices en la lista
#     return total_precio / len(lista)

# # se llama a la funcion calcular_promedio_precio y se le pasa la lista de productos como argumento
# precio_promedio = calcular_promedio_precio(productos)
# # se imprime el precio promedio de los productos con dos decimales
# print(f"\nEl precio promedio de los productos es: ${precio_promedio:.2f}")

import csv

productos_desde_csv = []

with open('datos.csv', mode='r', encoding='utf-8') as archivo_csv:
    lector_csv = csv.DictReader(archivo_csv)

    for fila in lector_csv:
        fila['id'] = int(fila['id'])
        fila['precio'] = int(fila['precio'])
        fila['stock'] = int(fila['stock'])

        productos_desde_csv.append(fila)

print("\nLista de productos desde CSV:")

for producto in productos_desde_csv:
    print(
        f"Producto: {producto['nombre']}, "
        f"Precio: ${producto['precio']}, "
        f"Stock: {producto['stock']}"
    )