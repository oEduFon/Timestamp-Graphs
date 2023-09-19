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
diretorio = 'D:\\Downloads\\imagens do evscope\\imagens\\1.00s\\Occultation'
entries = listdir(diretorio)
i=0
soma_ciclos=0
soma_midf=0
soma_exp=0
n = len(entries)
cycle_array = [0]*(n-1)
midframe_array = [0]*(n-1)
exp_array = [0]*(n-1)
x_axis = [0]*(n-1)

"""
Loop que pega informações do header de cada imagem e salva nos arrays correspondentes.
"""

while (i<n-1):

    """Verifica se existem arquivos não fits no diretório"""
    if(entries[i].find('.fits')==-1):
        continue

    """Armazena em current_frame_D_OBS o tempo de início da exposição e em current_frame_D_END o tempo de fim da exposição, ambos do frame atual"""
    hdulist = fits.open(diretorio+"\\"+entries[i])
    if(int((hdulist[0].header['DATE-OBS'])[11:13])!=0):
        hours_obs = int((hdulist[0].header['DATE-OBS'])[11:13])
    else:
        hours_obs = 24
    current_frame_D_OBS = float((hdulist[0].header['DATE-OBS'])[17:])+int((hdulist[0].header['DATE-OBS'])[14:16])*60+hours_obs*3600


    if(int((hdulist[0].header['DATE-END'])[11:13])!=0):
        hours_end = int((hdulist[0].header['DATE-END'])[11:13])
    else:
        hours_end = 24
    current_frame_D_END = float((hdulist[0].header['DATE-END'])[17:])+int((hdulist[0].header['DATE-END'])[14:16])*60+hours_end*3600


    """Armazena em next_frame o tempo de início da exposição do próximo frame"""
    hdulist = fits.open(diretorio+"\\"+entries[(i+1)])
    if(int((hdulist[0].header['DATE-OBS'])[11:13])!=0):
        hours = int((hdulist[0].header['DATE-OBS'])[11:13])
    else:
        hours = 24
    next_frame = float((hdulist[0].header['DATE-OBS'])[17:])+int((hdulist[0].header['DATE-OBS'])[14:16])*60+hours*3600

    """
    Realiza os cálculos: 
    Subtraindo os inícios de exposição para encontrar a duração do ciclo 
    Subtrai o fim do frame atual do inicio do frame seguinte para resultar no tempo midframe
    Subtrai o tempo entre frames da duração do ciclo para achar a duração da exposição
    """

    ciclo = next_frame - current_frame_D_OBS
    midframe = next_frame - current_frame_D_END
    exp = (ciclo - midframe)*1000
    soma_ciclos = soma_ciclos + ciclo
    soma_midf = soma_midf + midframe
    soma_exp = soma_exp + exp
    cycle_array[i] = ciclo
    midframe_array[i] = midframe
    exp_array[i] = exp
    x_axis[i] = i+1
    i=i+1
"""
Realiza os cálculos de média e desvio padrão amostral
"""

media_ciclos = soma_ciclos/(n-1)
media_midf = soma_midf/(n-1)
media_exp = soma_exp/(n-1)
i=0
somatorio_ciclos = 0
somatorio_midf = 0
somatorio_exp = 0

while (i<n-1):
    somatorio_ciclos = somatorio_ciclos+(cycle_array[i]-media_ciclos)**2
    somatorio_midf = somatorio_midf+(midframe_array[i]-media_midf)**2
    somatorio_exp = somatorio_exp+(exp_array[i]-media_exp)**2
    i=i+1
dp_ciclos = sqrt(somatorio_ciclos/(n-2))
dp_midf = sqrt(somatorio_midf/(n-2))
dp_exp = sqrt(somatorio_exp/(n-2))

"""
Apresenta os dados
"""
print('A média dos ciclos é {:.3} s'.format(media_ciclos))
print('O desvio padrão dos ciclos é {:.3} s'.format(dp_ciclos))
print('A média midframe é {:.3} s'.format(media_midf))
print('O desvio padrão midframe é {:.3} s'.format(dp_midf))
print('A média da exposição é {:.3} ms'.format(media_exp))
print('O desvio padrão da exposição é {:15e} ms'.format(dp_exp))
print('O número de frames é', n)
"""
Construção de gráficos
"""
figure, axis = plt.subplots(nrows=3, ncols=1)
figure.suptitle('Gráficos EVscope (1s de exposição)')
axis[0].plot(x_axis, cycle_array)
axis[0].set_title("Duração dos Ciclos")
axis[0].set_ylabel("Ciclo (s)")
axis[1].plot(x_axis, midframe_array)
axis[1].set_title("Tempo entre Frames")
axis[1].set_ylabel("Midframe (s)")
axis[2].plot(x_axis, exp_array)
axis[2].set_title("Tempo de Exposição")
axis[2].set_ylabel("Exposição (ms)")

axis[2].set_ylim(0.999, 0.101)
axis[2].yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.3f'))

plt.subplots_adjust(hspace=0.8, left=0.16)
plt.show()
