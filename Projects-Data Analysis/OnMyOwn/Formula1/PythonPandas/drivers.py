import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Lee el archivo CSV
df = pd.read_csv('../RawCSVArchives/drivers.csv')

# Calcula el conteo de cada nacionalidad y selecciona las 10 principales
top_countries = df['nationality'].value_counts().head(10)
mostCommon = top_countries.index[0]


# Crea el gráfico de torta
plt.figure(figsize=(8, 8))
plt.pie(top_countries, 
        labels=top_countries.index, 
        autopct='%1.1f%%', 
        startangle=45, 
        explode=[0.1 if x == mostCommon else 0 for x in top_countries.index],
        colors=['#FFD700', '#228B22', '#FF0000', '#4B0082', '#9932CC', '#FF1493', '#FF4500', '#40E0D0', '#D2691E', '#000080'])
plt.legend(loc='upper left', 
           bbox_to_anchor=(-0.1, 1.),
           fontsize=8)
plt.title('Top 10 Nationalities of F1 Drivers', fontsize=16)
plt.show()

# autopct='%1.1f%%' significa que muestra el porcentaje con un decimal




# pandas plotting kind options
# 'line' : line plot (default)
# 'bar' : vertical bar plot
# 'barh' : horizontal bar plot
# 'hist' : histogram
# 'box' : boxplot
# 'kde' : Kernel Density Estimation plot
# 'density' : same as 'kde'
# 'area' : area plot
# 'pie' : pie plot
# 'scatter' : scatter plot
# 'hexbin' : hexbin plot

