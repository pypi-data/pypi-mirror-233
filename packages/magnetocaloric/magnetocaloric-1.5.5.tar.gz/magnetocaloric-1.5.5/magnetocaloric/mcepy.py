import numpy as np
import xlsxwriter
import tableprint
from random import randint
import xlrd
import matplotlib.pyplot as plt
from num2words import num2words
import sys
import itertools


from .interpol import interpol
from .Msqr_HbyM import Msqr_HbyM
from .data_reading import data_reading
from .color_marker import color_marker
from .data_plotting import data_plotting
from .delSm_T import delSm_T
from .delSm_Pivoting import delSm_Pivoting
from .MH_Pivoting import MH_Pivoting
from .arrott_plotting import arrott_plotting
from .RCP_plotting import RCP_plotting
from .data_writing import data_writing
from .T_FWHM_RCP import T_FWHM_RCP
from .data_3d_plotting import mce_3d
from .mag_sus import mag_sus


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

plt.rcParams.update({'font.size':7})

import tableprint
from num2words import num2words



import bcrypt
from datetime import datetime, timedelta
today = datetime.today()
now = datetime.now()
dd = today.day
mm = today.month
yy = today.year
mu = now.minute


def mce(samp_name, file_dir, sheet_index, T_row, H_col, g_name, M_unit, H_unit, T_unit, plot_legend, loc, field, linear_threshold, save_data):
    """
    Perform Magnetocaloric Effect (MCE) analysis.

    Args:
        n (int): Number of temperature values.
        one_n (int): Number of data points at each temperature.

    Returns:
        None: The function performs the MCE analysis and generates plots, without returning any value.
    """
    # Data Collection

    H, M, T, n, one_n, two_n = data_reading(file_dir, sheet_index, T_row, H_col)
    
    # Entropy Change Calculation
    three_entropy_change_con, temperatures, Label_one = delSm_T(n, one_n, two_n, H, M, T)
    five_entropy_change_con, six_entropy_change_con = delSm_Pivoting(n, three_entropy_change_con, Label_one, temperatures)

    # Color and Marker Definitions
    colour, marker = color_marker()

    # Magnetization and Field Reshaping
    one_M_plot_final, two_M_plot_final = MH_Pivoting(one_n, n, M, H)

    # Arrott Plot
    H_plot_final, M_sqr, one_H_by_M_con = Msqr_HbyM(one_n, n, M, H, T, one_M_plot_final)

    # Data Visualization
    data_plotting(g_name, one_n, n, T, H, M_unit, H_unit, T_unit, colour, marker, Label_one, plot_legend, loc, one_M_plot_final, two_M_plot_final, H_plot_final, temperatures, five_entropy_change_con, M_sqr, one_H_by_M_con)

    # Modified Arrott Plot
    M_pow_MFT, H_by_M_pow_MFT, M_pow_TMFT, H_by_M_pow_TMFT, M_pow_3DH, H_by_M_pow_3DH, M_pow_3DI, H_by_M_pow_3DI = arrott_plotting(g_name, n, one_M_plot_final, one_H_by_M_con)

    susceptibility_final = []
    if (g_name== 'sus_plot' or g_name== 'all_plots'):
    # Susceptibility
        susceptibility_final = mag_sus(g_name, n, one_n, T, H, M, M_unit, H_unit, T_unit, field, linear_threshold)
    else:
        pass
    if (g_name== 'RCP_plot' or g_name== 'all_plots'):
        # Calculate T_FWHM and RCP
        T_FWHM_con,T_FWHM_con_final, RCP_con, RCP_final, H_for_RCP = T_FWHM_RCP(n, Label_one, six_entropy_change_con)

        # Plot RCP and T_FWHM
        RCP_plotting(g_name, M_unit, H_unit, T_unit, T_FWHM_con,T_FWHM_con_final, Label_one, RCP_con, RCP_final, H_for_RCP, samp_name)
    else:
        pass
    # Store Data to Excel Files
    if (save_data == 'allow'):
        data_writing(g_name, file_dir, n, T, Label_one, six_entropy_change_con, M_sqr, one_H_by_M_con, M_pow_MFT, H_by_M_pow_MFT, M_pow_TMFT, H_by_M_pow_TMFT, M_pow_3DH, H_by_M_pow_3DH, M_pow_3DI, H_by_M_pow_3DI, susceptibility_final, T_FWHM_con_final, RCP_final, H_for_RCP)
    else:
        pass
    return ("")

         




