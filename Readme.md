# 📊 Análisis de Fútbol Internacional (1872-2024)

## 📝 Descripción
Este proyecto analiza la ventaja de jugar como local en el fútbol internacional, utilizando un conjunto de datos históricos que abarca desde 1872 hasta 2024. La aplicación web interactiva, construida con Streamlit, permite a los usuarios explorar diferentes aspectos del fútbol internacional, incluyendo estadísticas de partidos, análisis de torneos y patrones históricos.

## 🎯 Características Principales
- Análisis de ventaja local en diferentes contextos
- Visualización interactiva de datos históricos
- Filtros por período temporal y torneos
- Análisis detallado de goles y resultados
- Comparativa entre sedes neutrales y no neutrales

## 🛠 Tecnologías Utilizadas
- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Plotly
- Seaborn
- Matplotlib

## 📋 Requisitos Previos
```bash
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
```

## 🚀 Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/analisis-futbol-internacional.git
cd analisis-futbol-internacional
```

2. Crear y activar un entorno virtual (opcional pero recomendado)
```bash
python -m venv env
# En Windows
env\Scripts\activate
# En macOS/Linux
source env/bin/activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 💻 Uso

1. Ejecutar la aplicación Streamlit
```bash
streamlit run app.py
```

2. Abrir el navegador web y acceder a la dirección local proporcionada (generalmente http://localhost:8501)

## 📁 Estructura del Proyecto
```
analisis-futbol-internacional/
├── app.py                  # Aplicación principal de Streamlit
├── requirements.txt        # Dependencias del proyecto
├── data/
│   ├── results.csv        # Dataset principal
│   ├── shootouts.csv      # Datos de penales
│   └── goalscorers.csv    # Datos de goleadores
├── README.md              # Documentación del proyecto
└── .gitignore            # Archivos ignorados por git
```

## 📊 Datasets
El proyecto utiliza tres conjuntos de datos principales:
- `results.csv`: Resultados de partidos internacionales
- `shootouts.csv`: Información sobre definiciones por penales
- `goalscorers.csv`: Registro de goleadores

### Estructura de los Datasets

#### results.csv
- `date`: Fecha del partido
- `home_team`: Equipo local
- `away_team`: Equipo visitante
- `home_score`: Goles del equipo local
- `away_score`: Goles del equipo visitante
- `tournament`: Nombre del torneo
- `city`: Ciudad donde se jugó
- `country`: País donde se jugó
- `neutral`: Indica si fue en sede neutral

#### shootouts.csv
- `date`: Fecha del partido
- `home_team`: Equipo local
- `away_team`: Equipo visitante
- `winner`: Ganador de la tanda
- `first_shooter`: Equipo que pateó primero

#### goalscorers.csv
- `date`: Fecha del partido
- `home_team`: Equipo local
- `away_team`: Equipo visitante
- `team`: Equipo que anotó
- `scorer`: Nombre del goleador
- `own_goal`: Indica si fue autogol
- `penalty`: Indica si fue penal

## 📈 Características de la Aplicación
1. **Filtros Interactivos**
   - Selector de rango temporal
   - Selección múltiple de torneos
   - Filtros por equipos

2. **Visualizaciones**
   - Distribución de resultados
   - Evolución temporal
   - Análisis por torneo
   - Estadísticas de goles
   - Patrones de ventaja local

3. **Estadísticas**
   - Métricas generales
   - Análisis de rendimiento
   - Comparativas históricas

## 🤝 Contribuir
Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## 👥 Autores
- Tu Nombre - [Tu GitHub](https://github.com/tu-usuario)

## 🙏 Agradecimientos
- Kaggle por proporcionar el dataset
- La comunidad de Streamlit por sus excelentes herramientas
- Todos los contribuidores al proyecto

## 📬 Contacto
- Tu Nombre - [@tu_twitter](https://twitter.com/tu_usuario)
- Email - tu.email@ejemplo.com
- Link del Proyecto: [https://github.com/tu-usuario/analisis-futbol-internacional](https://github.com/tu-usuario/analisis-futbol-internacional)