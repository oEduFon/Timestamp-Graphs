import astropy.io
from astropy.io import fits
from math import sqrt
import matplotlib.pyplot as plt
i=1
soma=0
n=999
midframe_array = [0]*n
x_axis = [0]*n
while (i<n+1):
    filenumber = str(i)
    filename_end = filenumber.zfill(5)+'.fits'
    
    hdulist = fits.open(r"C:\Users\10999\Desktop\SharpCap Captures\2022-10-24\0.03s-1000f\21_50_01Z\24_10_2022_21_50_01Z_"+filename_end)
    endexp = float((hdulist[0].header['DATE-OB2'])[17:])+int((hdulist[0].header['DATE-OB2'])[14:16])*60
    filenumber = str(i+1)
    filename_end = filenumber.zfill(5)+'.fits'
    hdulist = fits.open(r"C:\Users\10999\Desktop\SharpCap Captures\2022-10-24\0.03s-1000f\21_50_01Z\24_10_2022_21_50_01Z_"+filename_end)
    startexp = float((hdulist[0].header['DATE-OBS'])[17:])+int((hdulist[0].header['DATE-OBS'])[14:16])*60
    midframe_time = startexp - endexp
    soma=soma+midframe_time
    #print(i+1, '-', i, '=', midframe_time)
    midframe_array[i-1] = midframe_time
    x_axis[i-1] = i
    i=i+1
media = soma/n
i=0
somatorio=0
while (i<n):
    somatorio=somatorio+(midframe_array[i]-media)**2
    i=i+1

dp = sqrt(somatorio/n)
print('A média é', media)
print('O desvio padrão é', dp)
plt.plot(x_axis, midframe_array)
plt.xlabel('Frame')
plt.ylabel('Tempo entre frames')
plt.title('Tempo ocioso por frame')
plt.show()