# LIPGLOSS - Graphical user interface for constructing glaze recipes
# Copyright (C) 2017 Pieter Mostert

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# version 3 along with this program (see LICENCE.txt).  If not, see
# <http://www.gnu.org/licenses/>.

# Contact: pi.mostert@gmail.com

# We define the Restriction, Oxide, Ingredient,and Other classes

# SECTION 1
# Define Restriction class

class Restriction:
    'Oxide UMF, oxide % molar, oxide % weight, ingredient, SiO2:Al2O3 molar, KNaO UMF, etc'
    
    def __init__(self, index, name, objective_func, normalization, default_low, default_upp, dec_pt = 1):

        self.index = index     # We will always have restr_dict[index] = Restriction(index, ...)
        self.name = name
        self.objective_func = objective_func
        self.normalization = normalization
        self.default_low = default_low
        self.default_upp = default_upp
        self.dec_pt = dec_pt
        
        self.calc_bounds = {}

# SECTION 2
# Define Oxide class and initialize oxides

class Oxide:
    
     def __init__(self, molar_mass, flux):
         'SiO2, Al2O3, B2O3, MgO, CaO, etc'

         self.molar_mass = molar_mass
         self.flux = flux  # either 0 or 1

import oxidefile
oxide_dict = {}
for ox in oxidefile.oxides:
    if ox in oxidefile.fluxes:
        flux = 1
    else:
        flux = 0
    oxide_dict[ox] = Oxide(oxidefile.molar_mass_dict[ox], flux)

# SECTION 3
# Define Ingredient class and initialize ingredients

class Ingredient:    # Ingredients will be referenced by their index, a string consisting of a unique natural number
    
    def __init__(self, name, oxide_comp):

        self.name = name
        self.oxide_comp = oxide_comp  # dictionary giving weight percent of each oxide in the ingredient

import ingredientfile
ingredient_dict = {}
ingredient_compositions = {}
for r, name in enumerate(ingredientfile.ingredient_names):
    ingredient_dict[str(r)] = Ingredient(name, ingredientfile.ingredient_comp[name])
    ingredient_compositions[str(r)] = ingredientfile.ingredient_comp[name]

# SECTION 4
# Define and initialize instances of Other class

class Other:
    
    def __init__(self, name, numerator_coefs, normalization, def_low, def_upp, dec_pt):
        'SiO2:Al2O3, LOI, cost, total clay, etc'

        self.name = name
        self.numerator_coefs = numerator_coefs   # a dictionary with keys of the form mass_ox, mole_ox, ingredient_i,
                                                 # and values real numbers that are the coefficients in the linear
                                                 # combination of basic variables that define the numerator.
        self.normalization = normalization     # For now, just a text string of the form 'lp_var[...]'
        self.def_low = def_low
        self.def_upp = def_upp
        self.dec_pt = dec_pt

other_dict = {}
other_dict['0'] = Other('SiO2_Al2O3', {'mole_SiO2':1}, "lp_var['mole_Al2O3']", 3, 18, 2)   # Using 'SiO2:Al2O3' gives an error
other_dict['1'] = Other('KNaO UMF', {'mole_K2O':1, 'mole_Na2O':1}, "lp_var['fluxes_total']", 0, 1, 3)
other_dict['2'] = Other('KNaO % mol', {'mole_K2O':1, 'mole_Na2O':1}, "0.01*lp_var['ox_mole_total']", 0, 100, 1)
other_dict['3'] = Other('RO UMF', {'mole_MgO':1, 'mole_CaO':1, 'mole_BaO':1, 'mole_SrO':1}, "lp_var['fluxes_total']", 0, 1, 3)


# SECTION 5
# Initialize the restr_dict dictionary
# Define default recipe bounds (optional)

restr_dict = {}  # a dictionary with keys of the form 'umf_'+ox, 'mass_perc_'+ox, 'mole_perc_'+ox, 'ingredient_'+index or 'other_'+index

for ox in oxide_dict:   # create oxide restrictions
    def_upp = 1   # default upper bound for oxide UMF
    dp = 3
    if ox == 'SiO2':
        def_upp = 100
        dp = 2
    elif ox == 'Al2O3':
        def_upp = 10
    restr_dict['umf_'+ox] = Restriction('umf_'+ox, ox, 'mole_'+ox, "lp_var['fluxes_total']", 0, def_upp, dec_pt = dp)
    restr_dict['mass_perc_'+ox] = Restriction('mass_perc_'+ox, ox, 'mass_'+ox, "0.01*lp_var['ox_mass_total']", 0, 100, dec_pt = 2) 
    restr_dict['mole_perc_'+ox] = Restriction('mole_perc_'+ox, ox, 'mole_'+ox, "0.01*lp_var['ox_mole_total']", 0, 100, dec_pt = 2)
    
for index in ingredient_dict:
    restr_dict['ingredient_'+index] = Restriction('ingredient_'+index, ingredient_dict[index].name, 'ingredient_'+index,
                                                  "0.01*lp_var['ingredient_total']", 0, 100)

for index in other_dict:
    ot = other_dict[index]  
    restr_dict['other_'+index] = Restriction('other_'+index, ot.name, 'other_'+index, ot.normalization, ot.def_low, ot.def_upp,
                                             dec_pt=ot.dec_pt)

