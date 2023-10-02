import sys
import os

directory = os.getcwd()
sys.path.append(f'{directory}/../src/')
from teqoa-water-use-equations.water-use-equations import CalculateTrans
from teqoa-water-use-equations.water-use-equations import CalculateEvapoTrans
from teqoa-water-use-equations.water-use-equations import CalculateKCMethod
from teqoa-water-use-equations.water-use-equations import CalculateKCBMethod
from teqoa-water-use-equations.water-use-equations import CalculateEtoMethod
from teqoa-water-use-equations.water-use-equations import CalculateRs
from teqoa-water-use-equations.water-use-equations import EvapoTrans
from teqoa-water-use-equations.water-use-equations import Trans
from teqoa-water-use-equations.water-use-equations import Kc
from teqoa-water-use-equations.water-use-equations import Ke
from teqoa-water-use-equations.water-use-equations import Ke_wet
from teqoa-water-use-equations.water-use-equations import Kc_ini__wet
from teqoa-water-use-equations.water-use-equations import t1_days
from teqoa-water-use-equations.water-use-equations import REW
from teqoa-water-use-equations.water-use-equations import TEW
from teqoa-water-use-equations.water-use-equations import Eso
from teqoa-water-use-equations.water-use-equations import Kcmax
from teqoa-water-use-equations.water-use-equations import Kcb
from teqoa-water-use-equations.water-use-equations import Kd
from teqoa-water-use-equations.water-use-equations import Fceff
from teqoa-water-use-equations.water-use-equations import Kcbfull
from teqoa-water-use-equations.water-use-equations import Fr
from teqoa-water-use-equations.water-use-equations import Beta
from teqoa-water-use-equations.water-use-equations import ETo
from teqoa-water-use-equations.water-use-equations import Rn
from teqoa-water-use-equations.water-use-equations import Rnl
from teqoa-water-use-equations.water-use-equations import KsRs_over_Rso_minus_Kso
from teqoa-water-use-equations.water-use-equations import Rs_over_Rso
from teqoa-water-use-equations.water-use-equations import constant_Sqrt_Exp_a
from teqoa-water-use-equations.water-use-equations import sigmaTK4
from teqoa-water-use-equations.water-use-equations import sigmaTmin_K4
from teqoa-water-use-equations.water-use-equations import ws
from teqoa-water-use-equations.water-use-equations import sigmaTmax_K4
from teqoa-water-use-equations.water-use-equations import Rns
from teqoa-water-use-equations.water-use-equations import R_so
from teqoa-water-use-equations.water-use-equations import R_a
from teqoa-water-use-equations.water-use-equations import Delta
from teqoa-water-use-equations.water-use-equations import dr
from teqoa-water-use-equations.water-use-equations import Phi
from teqoa-water-use-equations.water-use-equations import J
from teqoa-water-use-equations.water-use-equations import es_e_a_kPa
from teqoa-water-use-equations.water-use-equations import Rs
from teqoa-water-use-equations.water-use-equations import e_o_Tmin_kPa
from teqoa-water-use-equations.water-use-equations import e_o_Tmax_kPa
from teqoa-water-use-equations.water-use-equations import yKPaPerDegCelcius
from teqoa-water-use-equations.water-use-equations import Tmean
from teqoa-water-use-equations.water-use-equations import pKPa
from teqoa-water-use-equations.water-use-equations import changeKPaPerDegCelcius
from teqoa-water-use-equations.water-use-equations import e_a_kPa
from teqoa-water-use-equations.water-use-equations import es_kPa


# TESTS

# In[64]:

def test_Rs():
    assert Rs(18.5, 9, 33.58) == 17.077584333125102, "Should be 17.07584333125102"


# In[65]:


def test_Tmean():
    assert Tmean(18.5, 9) == 13.75, "Should be 13.75"


# In[66]:


def test_ChangeKPaPerDegCelcius():
    assert changeKPaPerDegCelcius(13.75) == 0.10226801573987343, "Should be 0.10226801573987343"


# In[67]:


def test_pKPa():
    assert pKPa(68) == 100.49877513067669, "Should be 100.49877513067669"


# In[68]:


def test_yKPaPerDegCelcius():
    assert yKPaPerDegCelcius(68) == 0.0668316854619, "Should be 0.0668316854619"


# In[69]:


def test_e_o_Tmax_kPa():
    assert e_o_Tmax_kPa(18.5) == 2.1297773032821605, "Should be 2.1297773032821605"


# In[70]:


def test_e_o_Tmin_kPa():
    assert e_o_Tmin_kPa(9) == 1.1480604779781116, "Should be 1.1480604779781116"


# In[71]:


def test_es_kPa():
    assert es_kPa(2.1297773032821605,  1.1480604779781116) == 1.6389188906301362, "Should be 1.6389188906301362"


# In[72]:


def test_e_a_kPa(e_o_Tmin_kPa, RH_max, e_o_Tmax_kPa, RH_min):
    assert e_a_kPa(1.1480604779781116, 94, 2.1297773032821605, 56) == 1.1359260695687174, "Should be 1.1359260695687174"


# In[73]:


def test_es_e_a_kPa():
    assert es_e_a_kPa(1.6389188906301362, 1.1359260695687174) == 0.5029928210614187, "Should be 0.5029928210614187"


# In[74]:


def test_J():
    assert J('2015-10-01') == 274,  "Should be 274"


# In[75]:


def test_Phi():
    assert Phi() == -0.5944591432292687, "Should be -0.5944591432292687"


# In[76]:


def test_dr():
    assert dr(274) == 1.000142016763776, "Should be 1.000142016763776"


# In[77]:


def test_Delta():
    assert Delta(274) == -0.07527428503456446, "Should be -0.07527428503456446"


# In[78]:


def test_ws():
    assert ws(-0.5944591432292687, -0.07527428503456446) == 1.6218026908516492, "Should be 1.6218026908516492"


# In[79]:


def test_R_a():
    assert R_a(1.000142016763776, 1.6218026908516492, -0.5944591432292687, -0.07527428503456446) == 33.58183056040035, "Should be 33.58183056040035"


# In[80]:


def test_R_so():
    assert R_so(33.58183056040035,68) == 25.23204420986241, "Should be 25.23204420986241"


# In[81]:


def test_Rns():
    assert Rns(12.97503) == 9.9907731,  "Should be 9.9907731"


# In[82]:


def test_sigmaTmax_K4():
    assert sigmaTmax_K4(18.5) == 35.47883731897841,  "Should be 35.47883731897841"


# In[83]:


def test_sigmaTmin_K4():
    assert sigmaTmin_K4(8.96) == 31.059709819021048, "Should be 31.059709819021048"


# In[84]:


def test_sigmaTK4():
    assert sigmaTK4(35.47883731897841, 31.059709819021048) == 33.26927356899973, "Should be 33.26927356899973"


# In[85]:


def test_constant_Sqrt_Exp_a():
    assert constant_Sqrt_Exp_a(1.1359260695687174) == 0.19078823450026852, "Should be 0.19078823450026852"


# In[86]:


def test_Rs_over_Rso():
    assert Rs_over_Rso(12.97503, 25.23204420986241) == 0.5142282524587711, "Should be 0.5142282524587711"


# In[87]:


def test_KsRs_over_Rso_minus_Kso():
    assert KsRs_over_Rso_minus_Kso(0.5142282524587711) == 0.34420814081934115, "Should be 0.34420814081934115"


# In[88]:


def test_Rnl():
    assert Rnl(33.26927356899973, 0.19078823450026852, 0.34420814081934115) == 2.1848219228794674,  "Should be 2.1848219228794674"


# In[89]:


def test_Rn():
    assert Rn(9.9907731, 2.1848219228794674) == 7.805951177120533, "Should be 7.805951177120533"


# In[90]:


def test_ETo():
    assert ETo(0.10226801573987343, 7.805951177120533, 0.0668316854619, 13.7, 0.958, 1.6389188906301362, 1.1359260695687174) == 2.2360981722638624, "Should be 2.2360981722638624"


# In[91]:


def test_Beta():
    assert Beta(274) == 1.0516114686001923, "Should be 1.0516114686001923"


# In[92]:


def test_Fr():
    assert Fr(0.10226801573987343, 0.0668316854619, 0.958) == 0.6628665868111075, "Should be 0.6628665868111075"


# In[93]:


def test_Kcbfull():
    assert Kcbfull(0.10226801573987343, 0.0668316854619, 0.958, 55.77) == 0.7319880300802437, "Should be 0.7319880300802437"


# In[94]:


def test_Fceff():
    assert Fceff(274) == 0.1842842571849718, "Should be 0.1842842571849718"


# In[95]:


def test_Kd():
    assert Kd(0.1842842571849718) == 0.3685685143699436, "Should be 0.3685685143699436"


# In[96]:


def test_Kcb():
    assert Kcb(0.3685685143699436, 0.7319880300802437) == 0.3013593150647598,  "Should be 0.3013593150647598"


# In[ ]:





# In[97]:


# C. CALCULATION OF CROP FACTOR (KC)


# In[98]:


def test_Kcmax():
     assert Kcmax(0.958, 55.77, 0.3013593150647598) == 1.104276553750677, "Should be 1.104276553750677"


# In[99]:


def test_Eso():
    assert Eso(1.104276553750677, 0.3013593150647598, 2.2360981722638624) == 1.7954017699047267, "Should be 1.7954017699047267"


# In[100]:


def test_TEW():
    assert TEW() == 24.224999999999998, "Should be 24.224999999999998"


# In[101]:


def test_REW():
    assert REW() == 8, "Should be 8"


# In[102]:


def test_t1_days():
    assert t1_days(1.7954017699047267) == 4.4558271770137114, "Should be 4.4558271770137114"


# In[103]:


def test_Kc_ini__wet():
    assert Kc_ini__wet(1.7954017699047267, 2.2360981722638624) == 0.36480212956228353, "Should be 0.36480212956228353"


# In[104]:


def test_Ke_wet():
    assert Ke_wet(0.36480212956228353) == 0.36480212956228353, "Should be 0.36480212956228353"


# In[105]:


def test_Ke():
    assert Ke(0.36480212956228353) == 0.4248021295622835, "Should be 0.4248021295622835"


# In[106]:


def test_Kc():
    assert Kc(0.4248021295622835, 0.3013593150647598) == 0.7261614446270434, "Should be 0.7261614446270434"


# In[ ]:





# In[107]:


# D. WATER USE ESTIMATES


# In[108]:


def test_Trans():
    assert Trans(0.3013593150647598, 2.2360981722638624) == 0.6738690136109989, "Should be 0.6738690136109989"


# In[ ]:





# In[124]:


def test_EvapoTrans():
    assert EvapoTrans(0.7261614446270434, 2.2360981722638624) == 1.6237682790990176, "Should be 1.6237682790990176"


# In[ ]:





# In[125]:


def test_CalculateRs():
    assert CalculateRs(18.46, 8.96, '2015-10-01') == 17.07851529052873, "Should be 17.07851529052873"


# In[ ]:





# In[123]:


def test_CalculateEtoMethod():
    assert CalculateEtoMethod(18.46, 8.96, 33.58, 94, 55.77, 0.958, 12.97503, 68) == 2.235361346363096,  "Should be 2.235361346363096"


# In[ ]:





# In[121]:


def test_CalculateKCBMethod():
    assert CalculateKCBMethod(13.75, 274, 0.958, 55.77, 68) == 0.3013593150647598, "Should be 0.3013593150647598"


# In[ ]:





# In[114]:


def test_CalculateKCMethod():
    assert CalculateKCMethod(0.958,  0.958, 0.30, 2.24) == 0.8836219066408875, "Should be 0.8836219066408875"


# In[ ]:





# In[ ]:





# In[115]:


def test_CalculateEvapoTrans():
    assert CalculateEvapoTrans(18.5, 8.96, 94, 55.77, 0.958, '2015-10-01', 12.97503, 68) == (0.72623248886082, 0.3013037075559142, 2.237302630970609, 1.6248018580246464), "Should be (0.72623248886082, 0.3013037075559142, 2.237302630970609, 1.6248018580246464)"


# In[ ]:





# In[116]:


def test_CalculateTrans():
    assert CalculateTrans(18.5, 8.96, 94, 55.77, 0.958, '2015-10-01', 12.97503, 68) == 0.6741075776360458, "Should be 0.6741075776360458"


# In[117]:




# In[ ]:





# In[126]:


if __name__ == "__main__":
    # A CALCULATION OF ETo
    test_Rs()
    test_Tmean()
    test_ChangeKPaPerDegCelcius()
    test_pKPa()
    test_yKPaPerDegCelcius()
    test_e_o_Tmax_kPa()
    test_e_o_Tmin_kPa()
    test_es_kPa()
    test_es_e_a_kPa()
    test_J()
    test_Phi()
    test_dr()
    test_Delta()
    test_ws()
    test_R_a()
    test_R_so()
    test_Rns()
    test_sigmaTmax_K4()
    test_sigmaTmin_K4()
    test_sigmaTK4()
    test_constant_Sqrt_Exp_a()
    test_Rs_over_Rso()
    test_KsRs_over_Rso_minus_Kso()
    test_Rnl()
    test_Rn()
    test_ETo() # IMPORTANT VALUE
    
    # B. CALCULATION OF BASAL CROP FACTOR (KCB)
    test_Beta()
    test_Fr()
    test_Kcbfull()
    test_Fceff()
    test_Kd()
    test_Kcb()
    
    # C. CALCULATION OF CROP FACTOR (KC)
    test_Kcmax()
    test_Eso()
    test_TEW()
    test_REW()
    test_t1_days()
    test_Kc_ini__wet()
    test_Ke_wet()
    test_Ke()
    test_Kc()
    test_CalculateEvapoTrans()
    
    # D. WATER USE ESTIMATES
    test_Trans()
    test_EvapoTrans()
    
    #CalculateRs
    test_CalculateRs()
    
    #CalculateEtoMethod
    test_CalculateEtoMethod()
    
    #CalculateKCBMethod
    test_CalculateKCBMethod()
    
    #CalculateKCMethod
    test_CalculateKCMethod()
    
    #CalculateTrans
    test_CalculateTrans()
    
    #CalculateEvapoTrans
    test_CalculateEvapoTrans()
    print("Everything passed")


# In[ ]: