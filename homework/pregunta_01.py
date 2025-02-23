import os
import pandas as pd
import matplotlib.pyplot as plt

def pregunta_01():
    generar_dashboard()

def generar_dashboard():
    # Crear directorio de salida si no existe
    os.makedirs('docs', exist_ok=True)
    
    # Cargar los datos
    df = cargar_datos()
    
    # Generar visualizaciones
    grafico_almacen(df)
    grafico_envio(df)
    grafico_calificacion(df)
    grafico_peso(df)
    
    # Generar el archivo HTML
    generar_html()

def cargar_datos():
    """Carga los datos del archivo CSV y verifica que no esté vacío."""
    """Carga los datos del archivo CSV."""
    df = pd.read_csv('files/input/shipping-data.csv')
    if df.empty:
        raise ValueError('El archivo CSV está vacío o no se pudo cargar correctamente.')
    return df

def grafico_almacen(df):
    """Genera y guarda el gráfico de envíos por almacén."""
    plt.figure()
    df.Warehouse_block.value_counts().plot.bar(
        title='Envíos por almacén',
        xlabel='Bloque de almacén',
        ylabel='Cantidad de registros',
        color='tab:blue',
        fontsize=8,
    )
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.savefig('docs/shipping_per_warehouse.png')

def grafico_envio(df):
    """Genera y guarda el gráfico del modo de envío."""
    plt.figure()
    df.Mode_of_Shipment.value_counts().plot.pie(
        title='Modo de envío',
        wedgeprops={'width': 0.35},
        ylabel='',
        colors=['tab:blue', 'tab:orange', 'tab:green']
    )
    plt.savefig('docs/mode_of_shipment.png')

def grafico_calificacion(df):
    """Genera y guarda el gráfico de calificación de clientes."""
    plt.figure()
    stats = df.groupby('Mode_of_Shipment').Customer_rating.agg(['mean', 'min', 'max'])
    plt.barh(
        y=stats.index,
        width=stats['max'] - 1,
        left=stats['min'],
        height=0.9,
        color='lightgray',
        alpha=0.8,
    )
    colores = ['tab:green' if x >= 3 else 'tab:orange' for x in stats['mean']]
    plt.barh(
        y=stats.index,
        width=stats['mean'] - 1,
        left=stats['min'],
        height=0.5,
        color=colores,
        alpha=1,
    )
    plt.title('Calificación promedio de clientes')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.savefig('docs/average_customer_rating.png')

def grafico_peso(df):
    """Genera y guarda el gráfico de distribución de peso."""
    plt.figure()
    df.Weight_in_gms.plot.hist(
        title='Distribución del peso enviado',
        color='tab:orange',
        edgecolor='white',
    )
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.savefig('docs/weight_distribution.png')

def generar_html():
    """Genera un archivo HTML para visualizar los gráficos."""
    contenido_html = """<!DOCTYPE html>
    <html>
        <body>
            <h1>Dashboard de Envíos</h1>
            <div style='width: 45%; float: left;'>
                <img src='docs/envios_por_almacen.png' alt='Envíos por almacén'>
                <img src='docs/modo_envio.png' alt='Modo de envío'>
            </div>
            <div style='width: 45%; float: right;'>
                <img src='docs/calificacion_clientes.png' alt='Calificación de clientes'>
                <img src='docs/distribucion_peso.png' alt='Distribución de peso'>
            </div>
        </body>
    </html>"""
    with open('docs/index.html', 'w') as archivo:
        archivo.write(contenido_html)

pregunta_01()
