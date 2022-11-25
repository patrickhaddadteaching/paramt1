from ipywidgets import interact, interact_manual, widgets, Label
import numpy as np
import functools
from time import time, sleep
import matplotlib.pyplot as plt
from scipy.special import comb

test_size_max=1024
nb_p=100
v_p=0.5*np.arange(1,nb_p+1,dtype=np.float64)/(nb_p+1)
m_p_binomial=np.zeros((nb_p,test_size_max+1,test_size_max+1),dtype=np.float64)
a=np.broadcast_to(np.arange(test_size_max+1),(test_size_max+1,test_size_max+1))
b=comb(a,a.T)


for i_p in range(nb_p):
  p=v_p[i_p]
  for n in range(test_size_max+1):
    m_p_binomial[i_p,n,:n+1]=b[:n+1,n]*(p**np.arange(n+1))*((1-p)**(n-np.arange(n+1)))

    
v_h=-1*(np.log2(v_p)*(v_p)+np.log2(1-v_p)*(1-v_p))
myfont_dict = {'family': 'serif','color':  'darkblue','weight': 'normal','size': 16}
def paramt1(entropy_in,test_size,v_Th):
  Th_low=int(v_Th[0])
  Th_high=int(v_Th[1])
  closest_index=abs(v_h-entropy_in).argmin()
  v_proba_error=m_p_binomial[:,test_size,:Th_low].sum(1)+m_p_binomial[:,test_size,Th_high:].sum(1)
  if Th_low>=Th_high:
    v_proba_error[:]=1.0
  v_percent_error=v_proba_error*100
  plt.figure(1,figsize=[10,5])
  plt.plot(v_h[closest_index],v_percent_error[closest_index],'rx')
  plt.plot([v_h[closest_index],v_h[closest_index]],[0,v_percent_error[closest_index]],'r')
  plt.plot([0,v_h[closest_index]],[v_percent_error[closest_index],v_percent_error[closest_index]],'r')
  plt.plot(v_h,v_percent_error)
  plt.text(0.05,50,'%s%.2f'%("Alarm {:.0f}% of the time if entropy =".format(v_percent_error[closest_index]),v_h[closest_index]), fontdict=myfont_dict)
  plt.xlabel('Entropy')
  plt.ylabel('Percentage of alarm')
  plt.ylim([0,105])
  plt.xlim([0,1])
  plt.show()
im=interact(paramt1,entropy_in=widgets.FloatSlider(value=0.5,min=0,max=1),test_size=widgets.IntSlider(value=512,min=0,max=1024),v_Th = widgets.IntRangeSlider(value = [int(512/2-50),int(512/2+50)], min = 0, max = 1024, step = 1 ))
im.widget.close()
im.widget.children[0].description='Entr. Target'
im.widget.children[1].description='Latency'
im.widget.children[2].description='Thresh.'

im.widget.children[0].layout=widgets.Layout(width='650px')
im.widget.children[1].layout=widgets.Layout(width='415px')
im.widget.children[2].layout=widgets.Layout(width='650px')
v_box_top=widgets.VBox([im.widget.children[0],im.widget.children[1],im.widget.children[2],im.widget.children[3]])    
