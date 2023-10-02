#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import requests as req
import xml.etree.ElementTree as et

import math
import numpy as np


# In[4]:



# In[5]:


_alt = 68
_phi = 34.06
_alpha = 0.23

_rl = 202
_h = 4.5
_Kcbcover = 0.05

_SWC_FC = 0.189
_SWC_WP = 0.055
_Ze = 0.15
_Sa = 80
_tw = 243/107
_fw = 0.52

_Ke_dry = 0.06 

_fc = 0.16 

_soilTexture = 'Sandy'

def Update_h(treeHeight):
     global _h
     _h = treeHeight

def Update_fc(fc):
     global _fc
     _fc = fc

def Update_soilTexture(soilTexture):
     global _soilTexture
     _soilTexture = soilTexture

# In[6]:
def Update_fw(irrigationSystem):
     global _fw
     _fw = irrigationSystem

# In[7]:

def Update_Kcbcover(coverCrop):
     global _Kcbcover
     _Kcbcover = coverCrop


# In[8]:


def Rs(Tmax, Tmin, Ra):
    return 0.165 * math.sqrt(Tmax - Tmin) * Ra


# In[9]:


def Tmean(Tmax, Tmin):
    return (Tmax + Tmin) / 2


# In[10]:


def changeKPaPerDegCelcius(tmean):
    return (4098 * (0.6108 * np.exp((17.27*tmean)/(tmean+237.3)))) / math.pow((tmean + 237.3), 2)


# In[11]:


def pKPa(altitude):
    # global _alt
    print(altitude)
    return 101.3*(((293-0.0065 * altitude)/293)**5.26)


# In[12]:


def yKPaPerDegCelcius(altitude):
    return pKPa(altitude) * 0.000665


# In[13]:


def e_o_Tmax_kPa(Tmax):
    return 0.6108*np.exp((17.27*Tmax)/(Tmax+237.3))


# In[14]:


def e_o_Tmin_kPa(Tmin):
    return 0.6108*np.exp((17.27*Tmin)/(Tmin+237.3))


# In[15]:


def es_kPa(e_o_Tmax_kPa, e_o_Tmin_kPa):
    return (e_o_Tmax_kPa+e_o_Tmin_kPa)/2


# In[16]:


def e_a_kPa(e_o_Tmin_kPa, RH_max, e_o_Tmax_kPa, RH_min):
    return ((e_o_Tmin_kPa*(RH_max/100))+(e_o_Tmax_kPa*(RH_min/100)))/2


# In[17]:


def es_e_a_kPa(es_kPa, e_a_kPa):
    return es_kPa - e_a_kPa


# In[18]:


def J(date):
    d = np.datetime64(date)
    x = pd.to_datetime(d)
    firstDate = str(x.date().year) + "-01" + "-01"
    days = d - np.datetime64(firstDate) + 1
    return days.astype(int)


# In[19]:


def Phi():
    global _phi
    return (np.pi/180) * -_phi


# In[20]:


def dr(j):
    return 1 + 0.033 * np.cos(((2*np.pi) / 365) * j)


# In[21]:


def Delta(j):
    return 0.409 * np.sin(((2 * np.pi) / 365) * j - 1.39)


# In[22]:


def ws(phi, delta):
    return math.acos(-np.tan(phi) * np.tan(delta))


# In[23]:


def R_a(dr, ws, phi, delta):
    return ( (24 * 60) / np.pi) * 0.082 * dr * ((ws) * np.sin(phi) * np.sin(delta) + np.cos(phi) * np.cos(delta) * np.sin(ws))


# In[24]:


def R_so(ra, altitude):
    # global _alt
    return (0.75 + 2 * 10**-5 * altitude) * ra


# In[25]:


def Rns(Rs_Solar_Rad):
    global _alpha
    return (1 - _alpha) * Rs_Solar_Rad


# In[26]:


def sigmaTmax_K4(Tmax):
    return (4.903 * 10** - 9) * ((Tmax + 273.16) ** 4)


# In[27]:


def sigmaTmin_K4(Tmin):
    return (4.903 * 10** -9) * ((Tmin + 273.16) ** 4)


# In[28]:


def sigmaTK4(sigmaTmax_K4, sigmaTmin_K4):
    return (sigmaTmax_K4 + sigmaTmin_K4) / 2


# In[29]:


def constant_Sqrt_Exp_a(e_a_kPa):
    return 0.34 - 0.14 * np.sqrt(e_a_kPa)


# In[30]:


def Rs_over_Rso(Rs, Rso):
    return Rs /  Rso


# In[31]:


def KsRs_over_Rso_minus_Kso(Rs_over_Rso):
    return (1.35 * Rs_over_Rso) - 0.35


# In[32]:


def Rnl(sigmaTK4, constant_Sqrt_Exp_a, KsRs_over_Rso_minus_Kso):
    return sigmaTK4 * constant_Sqrt_Exp_a * KsRs_over_Rso_minus_Kso


# In[33]:


def Rn(Rns, Rnl):
    return Rns - Rnl


# In[34]:


def ETo(changeKPaPerDegCelcius, Rn, yKPaPerDegCelcius, Tmean, windspd, es_kPa, e_a_kPa):
    K15 = changeKPaPerDegCelcius
    AJ15 = Rn
    AK15 = 0
    M15 = yKPaPerDegCelcius
    I15 = Tmean
    F15 = windspd
    P15 = es_kPa
    Q15 = e_a_kPa
    return ((0.408 * K15) * (AJ15 - AK15) + (M15 * (900 / (I15 + 273)) * F15 * (P15 - Q15))) / (K15 + (M15 * (1 + 0.34 * F15)))


# In[ ]:





# In[35]:


# B. CALCULATION OF BASAL CROP FACTOR (KCB)


# In[36]:


def Beta(j):
    phi = Phi()
    delta = Delta(j)
    return math.asin(np.sin(phi) * np.sin(delta) + np.cos(phi) * np.cos(delta))


# In[37]:


def Fr(changeKPaPerDegCelcius, yKPaPerDegCelcius, Windspd):
    global _rl
    K15 = changeKPaPerDegCelcius
    M15 = yKPaPerDegCelcius
    F15 = Windspd
    return (K15 * 1000 + M15 * 1000 * (1 + 0.34 * F15)) / (K15 * 1000 + M15 * 1000 *(1 + 0.34 * F15 * _rl / 37))


# In[38]:


def Kcbfull(changeKPaPerDegCelcius, yKPaPerDegCelcius, Windspd, RH_min):
    global _h
    fr = Fr(changeKPaPerDegCelcius, yKPaPerDegCelcius, Windspd)
    F15 = Windspd
    E15 = RH_min
    return fr * (min(1 + 0.1 * _h, 1.2)+((0.04 * (F15 - 2) - 0.004 * (E15 - 45)) * (_h / 3) ** (0.3)))


# In[39]:


def Fceff(j):
    beta = Beta(j)
    return  1 if(_fc / np.sin(beta) > 1) else _fc / np.sin(beta)


# In[40]:


def Kd(fceff):
    global _h
    return min(1, 2 * fceff, fceff ** (1 / (1 + _h)))


# In[41]:


def Kcb(Kd, Kcbfull):
    global _Kcbcover
    return _Kcbcover + Kd * (max(Kcbfull - _Kcbcover, (Kcbfull - _Kcbcover) / 2))


# In[ ]:





# In[42]:


# C. CALCULATION OF CROP FACTOR (KC)


# In[43]:


def Kcmax(Windspd, RH_min, Kcb):
    global _h
    return max((1.2 + ((0.04 * (Windspd - 2) - 0.004 * (RH_min - 45)) * (_h / 3) ** (0.3))),(Kcb + 0.05))


# In[44]:


def Eso(Kcmax, Kcb, ETo):
    return (Kcmax - Kcb) * ETo


# In[45]:


def TEW():
    global _SWC_FC
    global _SWC_WP
    global _Ze
    return 1000 * (_SWC_FC - 0.5 * _SWC_WP) * _Ze


# In[46]:

_C = 1
def REW():
     global _Sa
     global _C
     rew = 20 - 0.15 * _Sa
     if (_soilTexture == 'Loam'):
          rew =  11 - 0.06 * _C
     if (_soilTexture == 'Clay'):
          rew = 8 + 0.006
     return rew


# In[47]:


def t1_days(Eso):
    return REW() / Eso


# In[48]:


def Kc_ini__wet(Eso, ETo):
    global _tw
    global _fw
    return (TEW() - (TEW() - REW()) * np.exp((-(_tw * Eso - REW())) / (TEW() - REW()))) / (_tw * ETo) * _fw


# In[49]:


def Ke_wet(Kc_ini__wet):
    return 0 if(Kc_ini__wet < 0) else Kc_ini__wet


# In[50]:


def Ke(Ke_wet):
    global _Ke_dry
    return Ke_wet + _Ke_dry


# In[51]:


def Kc(Ke, Kcb):
    return Ke + Kcb


# In[ ]:





# In[52]:


# D. WATER USE ESTIMATES


# In[53]:


def Trans(Kcb, ETo):
    return Kcb * ETo


# In[54]:


def EvapoTrans(Kc, ETo):
    return Kc * ETo


# In[ ]:





# In[55]:


# CALCULATE FINAL VALUES


# In[56]:


# CalculateKCBMethod
def CalculateKCBMethod(tmean, j, windspd, rH_min, altitude):

    fceff = Fceff(j)
    kd = Kd(fceff)

    _changeKPaPerDegCelcius = changeKPaPerDegCelcius(tmean)
    _yKPaPerDegCelcius = yKPaPerDegCelcius(altitude)
    kcbfull = Kcbfull(_changeKPaPerDegCelcius, _yKPaPerDegCelcius, windspd, rH_min)
    
    return Kcb(kd, kcbfull)


# In[ ]:





# In[57]:


# CalculateEtoMethod
def CalculateEtoMethod(Tmax, Tmin, Ra, RH_max, RH_min, Windspd, rs_Solar_Rad, altitude):
    
    # rs = Rs(Tmax, Tmin, Ra)
    rso = R_so(Ra, altitude)
    rs_over_Rso = Rs_over_Rso(rs_Solar_Rad, rso) # incorrect
    _ksRs_over_Rso_minus_Kso = KsRs_over_Rso_minus_Kso(rs_over_Rso) # incorrect
    
    tmean = Tmean(Tmax, Tmin)
    _changeKPaPerDegCelcius = changeKPaPerDegCelcius(tmean)
    _yKPaPerDegCelcius = yKPaPerDegCelcius(altitude)
    
    _e_o_Tmax_kPa = e_o_Tmax_kPa(Tmax)
    _e_o_Tmin_kPa  = e_o_Tmin_kPa(Tmin)
    _es_kPa = es_kPa(_e_o_Tmax_kPa, _e_o_Tmin_kPa)
 
    _e_a_kPa = e_a_kPa(_e_o_Tmin_kPa, RH_max, _e_o_Tmax_kPa, RH_min)
    _constant_Sqrt_Exp_a = constant_Sqrt_Exp_a(_e_a_kPa) # correct
    
    _sigmaTmax_K4 = sigmaTmax_K4(Tmax)
    _sigmaTmin_K4 = sigmaTmin_K4(Tmin)  
    _sigmaTK4 = sigmaTK4(_sigmaTmax_K4, _sigmaTmin_K4) # correct

    
    rnl = Rnl(_sigmaTK4, _constant_Sqrt_Exp_a, _ksRs_over_Rso_minus_Kso)
    rns = Rns(rs_Solar_Rad)
    rn = Rn(rns, rnl)  
    
    return ETo(_changeKPaPerDegCelcius, rn, _yKPaPerDegCelcius, tmean, Windspd, _es_kPa, _e_a_kPa)


# In[ ]:





# In[58]:


# CalculateRs
def CalculateRs(Tmax, Tmin, date):
    j = J(date)
    _dr = dr(j)
    
    delta = Delta(j)
    phi = Phi() 
    _ws = ws(phi, delta)

    Ra = R_a(_dr,_ws, phi, delta)
    return Rs(Tmax, Tmin, Ra)


# In[ ]:





# In[59]:


# CalculateKCMethod
def CalculateKCMethod(windspd, rH_min, kcb, eTo):
    
    kcmax = Kcmax(windspd, rH_min, kcb)

    eso = Eso(kcmax, kcb, eTo)
    kc_ini__wet = Kc_ini__wet(eso, eTo)
    ke_wet = Ke_wet(kc_ini__wet)
    ke = Ke(ke_wet)
    
    return Kc(ke, kcb)


# In[ ]:


# In[60]:


# In[ ]:


# In[61]:


# CalculateEvapoTrans
def CalculateEvapoTrans(Tmax, Tmin, RH_max, RH_min, windspd, date, rs_Solar_Rad, altitude):
    j = J(date)
    _dr = dr(j)
    
    delta = Delta(j)
    phi = Phi()
    _ws = ws(phi, delta)

    Ra = R_a(_dr,_ws, phi, delta)
    tmean = Tmean(Tmax, Tmin)
    
    Kcb = CalculateKCBMethod(tmean, j, windspd, RH_min, altitude)
    
    Eto = CalculateEtoMethod(Tmax, Tmin, Ra, RH_max, RH_min, windspd, rs_Solar_Rad, altitude)
    
    Kc =  CalculateKCMethod(windspd, RH_min, Kcb, Eto)
    return Kc, Kcb, Eto, EvapoTrans(Kc, Eto)


# In[ ]:





# In[62]:


def CalculateTrans(Tmax, Tmin, RH_max, RH_min, windspd, date, rs_Solar_Rad, altitude):
    j = J(date)
    _dr = dr(j)
    
    delta = Delta(j)
    phi = Phi()
    _ws = ws(phi, delta)

    Ra = R_a(_dr,_ws, phi, delta)
    tmean = Tmean(Tmax, Tmin)
    
    Kcb = CalculateKCBMethod(tmean, j, windspd, RH_min, altitude)
    Eto = CalculateEtoMethod(Tmax, Tmin, Ra, RH_max, RH_min, windspd, rs_Solar_Rad, altitude)

    return Trans(Kcb, Eto)


# In[ ]:



def AltWindSpeed(windspeed):
    return windspeed * (4.87 / (np.log2(67.8 * 10 - 5.42)))

# In[ ]:





# In[63]:
