# LIPGLOSS-CALC
The computational core of LIPGLOSS. This is an older version. I've rearranged things in the LIPGLOSS repo, but it needs more work.

Run calculations.py to define the calc_restrictions function. This defines the demo inputs demo_res_bounds, demo_ingredients and 
demo_other. Running calc_restrictions(demo_res_bounds, demo_ingredients, demo_other) in the shell should print the following output (after an irrelevant warning):

{'umf_SiO2': [3.0, 4.0], 'umf_Al2O3': [0.3, 0.5], 'umf_CaO': [1.0, 1.0], 'mass_perc_SiO2': [64.37, 72.7413], 'mass_perc_Al2O3': [10.0961, 16.0642], 'mass_perc_CaO': [16.142, 21.0089], 'mole_perc_SiO2': [67.7419, 75.0], 'mole_perc_Al2O3': [6.12245, 10.0], 'mole_perc_CaO': [18.1818, 23.2558], 'ingredient_0': [38.1822, 52.0639], 'ingredient_1': [21.3466, 33.6225], 'ingredient_7': [24.5522, 31.2068], 'other_0': [7.0, 12.0]}
