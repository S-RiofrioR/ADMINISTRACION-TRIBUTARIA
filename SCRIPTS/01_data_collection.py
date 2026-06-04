"""
Script 01: Recolección de Datos
================================
Descarga datos del Banco Mundial (WDI y WGI) para el análisis de crowding-out.
"""

import pandas as pd
import wbgapi as wb
import os
import time

def descargar_datos_banco_mundial():
    """
    Descarga datos del Banco Mundial para Ecuador, Panamá y Costa Rica.
    """
    
    # Definir países y período
    paises = ['ECU', 'PAN', 'CRI']  # Códigos ISO del Banco Mundial
    años = list(range(2010, 2025))  # 2010-2024
    
    print("=" * 60)
    print("RECOLECCIÓN DE DATOS - BANCO MUNDIAL")
    print("=" * 60)
    
    # Diccionario de indicadores
    indicadores = {
        'NE.GDI.TOTL.ZS': 'FBKF_PIB',           # Formación bruta de capital fijo (% PIB)
        'GC.TAX.TOTL.GD.ZS': 'Presion_Fiscal',  # Ingresos fiscales (% PIB)
        'GE.EST': 'Eficiencia_Gobierno'         # Efectividad del gobierno
    }
    
    # Crear carpeta de salida si no existe
    os.makedirs('DATOS/raw', exist_ok=True)
    
    # Descargar cada indicador
    for codigo, nombre in indicadores.items():
        print(f"\nDescargando: {nombre} ({codigo})...")
        time.sleep(1)  # Pausa para no saturar la API
        
        try:
            # Obtener datos de forma correcta
            datos_lista = []
            
            for pais in paises:
                for año in años:
                    try:
                        valor = wb.data.Series(codigo, econ=pais, time=año)
                        if len(valor) > 0 and pais in valor.index:
                            valor_pais = valor[pais]
                        else:
                            valor_pais = None
                    except:
                        valor_pais = None
                    
                    datos_lista.append({
                        'economia': pais,
                        'año': año,
                        nombre: valor_pais
                    })
            
            # Crear DataFrame
            df = pd.DataFrame(datos_lista)
            
            # Eliminar filas con valores nulos
            df = df.dropna(subset=[nombre])
            
            # Guardar
            archivo_salida = f"DATOS/raw/wb_{nombre.lower()}.csv"
            df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
            print(f"✅ Guardado en: {archivo_salida}")
            print(f"   Observaciones válidas: {len(df)}")
            
        except Exception as e:
            print(f"❌ Error al descargar {nombre}: {str(e)}")
            print(f"   Intentando método alternativo...")
            
            # Método alternativo: descargar todos los datos y filtrar
            try:
                df = wb.data.DataFrame(codigo, paises, mrv=20)  # Últimos 20 valores
                df = df.reset_index()
                
                # Filtrar años 2010-2024
                df = df[df['time'].between(2010, 2024)]
                df.columns = ['economia', 'año', nombre]
                
                archivo_salida = f"DATOS/raw/wb_{nombre.lower()}.csv"
                df.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
                print(f"✅ Guardado (método alternativo) en: {archivo_salida}")
                print(f"   Observaciones: {len(df)}")
                
            except Exception as e2:
                print(f"❌ Error también en método alternativo: {str(e2)}")
    
    print("\n" + "=" * 60)
    print("Proceso de descarga completado")
    print("=" * 60)

if __name__ == "__main__":
    descargar_datos_banco_mundial()