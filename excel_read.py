#import libraries for normal distribution use.
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
from matplotlib.ticker import FormatStrFormatter

#import libraries for excel read
import pandas as pd

#declaring the position/name of the excel file
file_name =  'ola_ta_layers_metrhseis.xlsx'
#input the position/name of the sheet.
print("which sheet?")
sheet = input()

#------------------Variables--------------------

#need for do/while simulation
i=0;
#initialize the val add
add = 0

#---------------------------------------------Functions--------------------------------------------
def norm_dist_calc(meas_thick, layer_name, info): #norm_dist_calc(array[], name of layer, subtitle)
	global add
	global i
	
	add = 0
	i =0

	#find the length of the array
	meas_length = len(meas_thick)

	print("length is:", end=" ")
	print(meas_length)	

	#starting to find the average
	for i in range(meas_length):
		add = add+meas_thick[i]
	average = add/meas_length

	print("average is:", end=" ")
	print(average)

	#initialize the vars again
	add =0
	i =0
	extract = 0

	#create: Σ(xi-x)^2
	for i in range(meas_length):
		extract = (meas_thick[i] - average)**2
		add = add + extract

	#Create σ^2 = [Σ(xi-x)^2]/(N-1) =variance
	s_2 = add/(meas_length -1)


	#Create σ =sqrt[[Σ(xi-x)^2]/(N-1)] =standard deviation
	s = (s_2)**(0.5)

	print("s^2 is:", end=" ")
	print(s_2)


	print("s is:", end=" ")
	print(s)

	#show average +- n*σ
	average_minus_s = average - s
	print("68.27% minus is", end=" ")
	print(average_minus_s)

	average_plus_s = average + s
	print("68.27% plus is", end=" ")
	print(average_plus_s)

	average_minus_2s = average - 2*s
	print("95.45% minus is", end=" ")
	print(average_minus_2s)

	average_plus_2s = average + 2*s
	print("95.45% plus is", end=" ")
	print(average_plus_2s)

	average_minus_3s = average - 3*s
	print("99.73% minus is", end=" ")
	print(average_minus_3s)

	average_plus_3s = average + 3*s
	print("99.73% plus is", end=" ")
	print(average_plus_3s)


	#--------scatter vertical lines to show +-n*σ---------------

	#the horizontal points for average + n*σ are already known.
	#the vertical points are needed, which, are the same values.

	moufa =[] #(vertical lines) will be filled with values up to 0.25 
	average_minus_68 = [] #(one value horizontal) will be filled with one single value.
	average_plus_68 = []	#(one value horizontal) will be filled with one single value.
	average_minus_95 = []
	average_plus_95 = []
	average_minus_99 = []
	average_plus_99 = []

	for i in range(0,260,2):
		j = i/1000
		if(j<=0.006):	
			average_minus_68.append(average_minus_s) #[xyz, xyz, xyz.... ,xyz]
			average_plus_68.append(average_plus_s)  #[xyz, xyz, xyz.... ,xyz]
			average_minus_95.append(average_minus_2s) #[xyz, xyz, xyz.... ,xyz]
			average_plus_95.append(average_plus_2s) #[xyz, xyz, xyz.... ,xyz]
			average_minus_99.append(average_minus_3s) #[xyz, xyz, xyz.... ,xyz]
			average_plus_99.append(average_plus_3s) #[xyz, xyz, xyz.... ,xyz]	
			moufa.append(j) #[0.00, 0.02, 0.04.... ,0.25]

	#title and subtitle
	fig = plt.figure()
	fig.suptitle(layer_name, fontsize=14, fontweight='bold') #bold title
	ax = fig.add_subplot(111) #create the ax figure
	fig.subplots_adjust(top=0.85) #top distance
	
	#Use the info
	ax.set_title(info) #title

	#horizontal and vertical labels
	ax.set_xlabel('Thickness [nm]')
	ax.set_ylabel('Φμ,(σ)^2(Χ)')

	# positioned on % of the window
	#68.27
	ax.text(0.33, 0.9, '68.27%',color='blue',transform=ax.transAxes, fontsize=8)
	ax.text(0.64, 0.9, '68.27%',color='blue',transform=ax.transAxes, fontsize=8)

	#95.45
	ax.text(0.18, 0.9, '95.45%',color='green',transform=ax.transAxes, fontsize=8)
	ax.text(0.78, 0.9, '95.45%',color='green',transform=ax.transAxes, fontsize=8)

	#99.73
	ax.text(0.94, 0.9, '99.73%',color='green',transform=ax.transAxes, fontsize=8)
	ax.text(0.03, 0.9, '99.73%',color='green',transform=ax.transAxes, fontsize=8)

	#positioned on numerical of the window
	s_round = "%.2f" % s
	ax.annotate("x-" +str(s_round), (average_minus_s, 0))
	ax.annotate("x-2*" +str(s_round), (average_minus_2s, 0))
	ax.annotate("x-3*" +str(s_round), (average_minus_3s, 0))

	ax.annotate("x+" +str(s_round), (average_plus_s, 0))
	ax.annotate("x+2*" +str(s_round), (average_plus_2s, 0))
	ax.annotate("x+3*" +str(s_round), (average_plus_3s, 0))

	#Vertical lines for each average +- σ*n
	#scatter average - 68
	ax.scatter(average_minus_68, moufa, s=0.1)

	#scatter average + 68
	ax.scatter(average_plus_68, moufa, s=0.1)

	#scatter average - 95
	ax.scatter(average_minus_95, moufa, s=0.1)

	#scatter average + 95
	ax.scatter(average_plus_95, moufa, s=0.1)

	#scatter average - 99
	ax.scatter(average_minus_99, moufa, s=0.1)

	#scatter average + 99
	ax.scatter(average_plus_99, moufa, s=0.1)



	#------------building the normal distibution graph----------
	#average (the mean or expectation of the distribution (and also its median and mode))
	# σ^2 =variance
	#σ standard deviation

	#Returns evenly spaced numbers over a specified interval.
	hor_axes = np.linspace(average - 3*s, average + 3*s, 1000)  #horizontal axes

	#attempt to see vertical axes
	vertical_axes = stats.norm.pdf(hor_axes, average, s)

	#pdf for probability density function
	ax.plot(hor_axes, vertical_axes)

	#set axes accuracy
	#ax.yaxis.set_major_formatter(FormatStrFormatter('%g')) #type of accuracy
	#ax.yaxis.set_ticks(np.arange(0, 0.3, 0.02)) #from 0 to 3 with steo of 0.02

	#plt.text( 1 , 1 , 'test', fontsize = 100, color='green')
	plt.show()





#-------------------------------------User's input starts---------------------------------------------
#needs fixing
if(sheet[0] == 'R' or sheet[0] == 'r'): #if sheet name starts with R (Regionxxx) then its a string (name of sheet).
	pass
else: #else, it must be a number (number of sheet)
	sheet = int(sheet)

print("how many layers?")
layers = input()
layers = int(layers)

#load the excel sheet
excel_sheet_load = pd.read_excel(io=file_name, sheet_name=sheet)
#-------------------------------------User's input ends---------------------------------------------


#--------------------------------Layer Count-----------------------------------
#load the Measured thickness column, untill the string 'end'
#simulate do
if(layers == 1):
	#find out the name of the layer
	layer1 = excel_sheet_load.at[0,'Layer']
	#find the info col	
	info = excel_sheet_load.at[0,'Info']

	#create array of measured thickness values
	meas_thick_1 = []
	while True: #do:
		value = excel_sheet_load.at[i,'Meas.Thick. [nm]']
		i = i+1;
		if (value == 'end'): #use end under the last value
			break
		else:
			meas_thick_1.append(float(value))

	#create the graph
	norm_dist_calc(meas_thick_1, layer1, info)

elif(layers == 2):
#find out the names of the two layers.
	layer1 = excel_sheet_load.at[0,'Layer']
	layer2 = excel_sheet_load.at[1,'Layer']

	#find the info col	
	info = excel_sheet_load.at[0,'Info']

	print("Layer 1 is:", end=" ")
	print(layer1)

	print("Layer 2 is:", end=" ")
	print(layer2)
#Two arrays, one for each layer
	layer1_meas_thick = []
	layer2_meas_thick = []
	
#fill the arrays
	i=0
	while(excel_sheet_load.at[i,'Meas.Thick. [nm]'] != 'end'):
		if(excel_sheet_load.at[i,'Layer'] == layer1):
			layer1_meas_thick.append(float(excel_sheet_load.at[i,'Meas.Thick. [nm]']))
		elif(excel_sheet_load.at[i,'Layer'] == layer2):
			layer2_meas_thick.append(float(excel_sheet_load.at[i,'Meas.Thick. [nm]']))
		i=i+1

	print("Layer 1 array:", end=" ") #'end' helps prints on the same line
	print(layer1_meas_thick)

	print("Layer 2 array:", end=" ")
	print(layer2_meas_thick)

	#create the graph
	norm_dist_calc(layer1_meas_thick, layer1, info)
	norm_dist_calc(layer2_meas_thick, layer2, info)


		
elif(layers ==3):
#find out the names of the three layers.
	layer1 = excel_sheet_load.at[0,'Layer']
	layer2 = excel_sheet_load.at[1,'Layer']
	layer3 = excel_sheet_load.at[2,'Layer']	

	#find the info col	
	info = excel_sheet_load.at[0,'Info']

	print("Layer 1 is:", end=" ")
	print(layer1)

	print("Layer 2 is:", end=" ")
	print(layer2)

	print("Layer 3 is:", end=" ")
	print(layer3)

#Three arrays, one for each layer
	layer1_meas_thick = []
	layer2_meas_thick = []
	layer3_meas_thick = []
	
	
#fill the arrays
	i=0
	while(excel_sheet_load.at[i,'Meas.Thick. [nm]'] != 'end'):
		if(excel_sheet_load.at[i,'Layer'] == layer1):
			layer1_meas_thick.append(float(excel_sheet_load.at[i,'Meas.Thick. [nm]']))
		elif(excel_sheet_load.at[i,'Layer'] == layer2):
			layer2_meas_thick.append(float(excel_sheet_load.at[i,'Meas.Thick. [nm]']))
		elif(excel_sheet_load.at[i,'Layer'] == layer3):
			layer3_meas_thick.append(float(excel_sheet_load.at[i,'Meas.Thick. [nm]']))
		i=i+1

	print("Layer 1 array:", end=" ") #'end' helps prints on the same line
	print(layer1_meas_thick)

	print("Layer 2 array:", end=" ")
	print(layer2_meas_thick)

	print("Layer 3 array:", end=" ")
	print(layer3_meas_thick)

	#create the graph
	norm_dist_calc(layer1_meas_thick, layer1, info)
	norm_dist_calc(layer2_meas_thick, layer2, info)
	norm_dist_calc(layer3_meas_thick, layer3, info)

#----------------------------------------------Layer Graph------------------------------------------










