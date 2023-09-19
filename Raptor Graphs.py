from astropy.io import fits
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from os import listdir


"""
Parâmetros:
entries: armazena o nome dos arquivos
i: contador
soma_ciclos: soma da duração de todos os ciclos
soma_midf: soma dos tempos entre frames
soma_exp: soma dos tempos de exposição
n: quantidade de frames
Listas:
cycle_array: guarda a duração do ciclo
midframe_array: guarda a duração entre frames
exp_array: guarda a duração do ciclo sem o tempo midframe (exposição)
x_axis: guarda o número de cada frame para ser o eixo X do gráfico gerado
"""
diretorio = 'C:\\Users\\user\\Desktop\\it\\SExTA\\2s'
entries = listdir(diretorio)
i=0
soma_ciclos=0
n = len(entries)
cycle_array = [0]*(n-1)
x_axis = [0]*(n-1)

"""
Loop que pega informações do header de cada imagem e salva nos arrays correspondentes.
"""

while (i<n-1):

    """Verifica se existem arquivos não fits no diretório"""
    if(entries[i].find('.fits')==-1):
        continue

    """Armazena em current_frame a timestamp do frame atual"""
    hdulist = fits.open(diretorio+"\\"+entries[i])
    if(int((hdulist[0].header['TIMESTMP'])[11:13])!=0):
        hours_obs = int((hdulist[0].header['TIMESTMP'])[11:13])
    else:
        hours_obs = 24
    current_frame = float((hdulist[0].header['TIMESTMP'])[17:])+int((hdulist[0].header['TIMESTMP'])[14:16])*60+hours_obs*3600



    """Armazena em next_frame a timestamp do próximo frame"""
    hdulist = fits.open(diretorio+"\\"+entries[(i+1)])
    if(int((hdulist[0].header['TIMESTMP'])[11:13])!=0):
        hours = int((hdulist[0].header['TIMESTMP'])[11:13])
    else:
        hours = 24
    next_frame = float((hdulist[0].header['TIMESTMP'])[17:])+int((hdulist[0].header['TIMESTMP'])[14:16])*60+hours*3600
    


    """ 
    Subtraindo as timestamps para encontrar a duração do ciclo 
    """

    ciclo = next_frame - current_frame
    soma_ciclos = soma_ciclos + ciclo
    cycle_array[i] = ciclo
    x_axis[i] = i+1
    i=i+1
"""
Realiza os cálculos de média e desvio padrão amostral
"""

media_ciclos = soma_ciclos/(n-1)
i=0
somatorio_ciclos = 0

while (i<n-1):
    somatorio_ciclos = somatorio_ciclos+(cycle_array[i]-media_ciclos)**2
    i=i+1
dp_ciclos = sqrt(somatorio_ciclos/(n-2))

"""
Apresenta os dados
"""
print(diretorio[31:37])
print('A média dos ciclos é {:.3} s'.format(media_ciclos))
print('O desvio padrão dos ciclos é {:.3} s'.format(dp_ciclos))

"""
Construção de gráficos
"""
figure, axis = plt.subplots(nrows=1, ncols=1)
plt.plot(x_axis, cycle_array)
plt.xlabel('Frame')
plt.ylabel('Tempo (s)')
plt.title('Tempo entre Timestamps ('+diretorio[31:37]+')')
#plt.subplots_adjust(hspace=0.8, left=0.16)
plt.show()
