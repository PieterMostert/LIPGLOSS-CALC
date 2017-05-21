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

from pulp import *

from restrictions import *
#from pulp2dim import *

# SECTION 1
# Set up variables and universal restrictions for LP problem

prob = pulp.LpProblem('Glaze recipe', pulp.LpMaximize)
solver = GLPK()
lp_var = {}     # dictionary for the variables in the linear programming problem prob.

for total in ['ingredient_total', 'fluxes_total', 'ox_mass_total', 'ox_mole_total']:
    lp_var[total] = pulp.LpVariable(total, 0, None, pulp.LpContinuous)           # used to normalize

for index in ingredient_dict:
    ing = 'ingredient_'+index
    lp_var[ing] = pulp.LpVariable(ing, 0, None, pulp.LpContinuous)
    
for ox in oxide_dict:
    lp_var['mole_'+ox] = pulp.LpVariable('mole_'+ox, 0, None, pulp.LpContinuous)
    lp_var['mass_'+ox] = pulp.LpVariable('mass_'+ox, 0, None, pulp.LpContinuous)
    prob += lp_var['mole_'+ox]*oxide_dict[ox].molar_mass == lp_var['mass_'+ox]   # relate mole percent and unity
    prob += sum(ingredient_compositions[index][ox]*lp_var['ingredient_'+index]/100 \
                for index in ingredient_dict if ox in ingredient_compositions[index]) \
            == lp_var['mass_'+ox], ox     # relate ingredients and oxides

for index in other_dict:
    ot = 'other_'+index
    coefs = other_dict[index].numerator_coefs
    linear_combo = [(lp_var[key], coefs[key]) for key in coefs]
    lp_var[ot] = pulp.LpVariable(ot, 0, None, pulp.LpContinuous)
    prob += lp_var[ot] == LpAffineExpression(linear_combo)         # relate this variable to the other variables.

prob += lp_var['ingredient_total'] == sum(lp_var['ingredient_'+index] for index in ingredient_dict), 'ing_total'
prob += lp_var['fluxes_total'] == sum(oxide_dict[ox].flux*lp_var['mole_'+ox] for ox in oxide_dict)
prob += lp_var['ox_mass_total'] == sum(lp_var['mass_'+ox] for ox in oxide_dict)
prob += lp_var['ox_mole_total'] == sum(lp_var['mole_'+ox] for ox in oxide_dict)

# SECTION 2

def print_res_type(normalization):   # Used to display error message
    if normalization == "lp_var['fluxes_total']":
        prt = 'UMF '
    elif normalization == "0.01*lp_var['ox_mass_total']":
        prt = '% weight '
    elif normalization == "0.01*lp_var['ox_mole_total']":
        prt = '% molar '
    else:
        prt = ''
    return prt

# Define calc function

def calc_restrictions(restriction_bounds, recipe_ingredients, recipe_other):
    ''' restriction bounds must be a dictionary with keys of the form
        'umf_'+ox, 'mass_perc_'+ox, 'mole_perc_'+ox, where ox is in recipe_oxides (defined below),
        'ingredient_'+index, where index is in recipe_ingredients
        or 'other_'+index, where index is in recipe_other.
        The values of restriction_bounds are of the form [low,upp], where low and upp are,
        respectively, the user-defined lower and upper bounds for that restriction.
        recipe_ingredients and recipe_other are lists of indices representing the ingredients
        and other restrictions used in the recipe'''

    global prob

    recipe_oxides = set()
    for index in recipe_ingredients:
        recipe_oxides = recipe_oxides.union(set(ingredient_compositions[index]))  # Is there a more efficient way to do this?
     
# First, test for obvious errors

    recipe_fluxes = [ox for ox in recipe_oxides if oxide_dict[ox].flux == 1]

    if sum(oxide_dict[ox].flux for ox in recipe_oxides) == 0:
        print('No flux! You have to give a flux.')
        return

    for res_key, bounds in restriction_bounds.items():
        if bounds[0] > bounds[1]:
            res = restr_dict[res_key]
            print('Incompatible ' + print_res_type(res.normalization) + 'bounds on ' + res.name)
            return

    delta = 0.1**9

    if sum(restriction_bounds['umf_'+ox][0] for ox in recipe_fluxes) > 1 + delta:
        print('Sum of UMF flux lower bounds > 1')
        return
        
    if sum(restriction_bounds['umf_'+ox][1] for ox in recipe_fluxes) < 1 - delta:
        print('Sum of UMF flux upper bounds < 1')
        return

    for t in ['mass_perc_', 'mole_perc_']:
        if sum(restriction_bounds[t+ox][0] for ox in recipe_oxides) > 100 + delta:
            print('Sum of ' + t + 'lower bounds > 100')
            return

        if sum(restriction_bounds[t+ox][1] for ox in recipe_oxides) < 100 - delta:
            print('Sum of ' + t + 'upper bounds < 100')
            return
        
    sum_ing_low = sum(restriction_bounds['ingredient_'+index][0] for index in recipe_ingredients)
    if sum_ing_low > 100 + delta:
        print('The sum of the ingredient lower bounds is '+str(sum_ing_upp)
              +'. Decrease one of the lower bounds by at least '+str(sum_ing_upp-100))     #will be a problem if they're all < sum_ing_upp-100
        return

    sum_ing_upp = sum(restriction_bounds['ingredient_'+index][1] for index in recipe_ingredients)
    if sum_ing_upp < 100 - delta:
        print('The sum of the ingredient upper bounds is only '+str(sum_ing_upp)
              +'. Increase one of the upper bounds by at least '+str(100-sum_ing_upp))
        return

# Set user-imposed bounds

    for index in ingredient_dict:
        ing = 'ingredient_'+index
        if index in recipe_ingredients:
            ing_low = 0.01*restriction_bounds[ing][0]
            ing_upp = 0.01*restriction_bounds[ing][1]
        else:
            ing_low = 0
            ing_upp = 0
        prob.constraints[ing+'_lower'] = lp_var[ing] >= ing_low*lp_var['ingredient_total']      # ingredient lower bounds    
        prob.constraints[ing+'_upper'] = lp_var[ing] <= ing_upp*lp_var['ingredient_total']      # ingredient upper bounds
     
    for ox in oxide_dict:          
        if ox in recipe_oxides:     
            prob.constraints[ox+'_umf_lower'] = lp_var['mole_'+ox] >= restriction_bounds['umf_'+ox][0]*lp_var['fluxes_total']   # oxide UMF lower bounds
            prob.constraints[ox+'_umf_upper'] = lp_var['mole_'+ox] <= restriction_bounds['umf_'+ox][1]*lp_var['fluxes_total']   # oxide UMF upper bounds
            prob.constraints[ox+'_wt_%_lower'] = lp_var['mass_'+ox] >= 0.01*restriction_bounds['mass_perc_'+ox][0]*lp_var['ox_mass_total']    # oxide weight % lower bounds
            prob.constraints[ox+'_wt_%_upper'] = lp_var['mass_'+ox] <= 0.01*restriction_bounds['mass_perc_'+ox][1]*lp_var['ox_mass_total']    # oxide weight % upper bounds
            prob.constraints[ox+'_mol_%_lower'] = lp_var['mole_'+ox] >= 0.01*restriction_bounds['mole_perc_'+ox][0]*lp_var['ox_mole_total']   # oxide mol % lower bounds
            prob.constraints[ox+'_mol_%_upper'] = lp_var['mole_'+ox] <= 0.01*restriction_bounds['mole_perc_'+ox][1]*lp_var['ox_mole_total']   # oxide mol % upper bounds

        else:
            try:
                del prob.constraints[ox+'_umf_lower']
                del prob.constraints[ox+'_umf_upper']
                del prob.constraints[ox+'_wt_%_lower']
                del prob.constraints[ox+'_wt_%_upper']
                del prob.constraints[ox+'_mol_%_lower']
                del prob.constraints[ox+'_mol_%_upper']
            except:
                pass

    for index in other_dict:
        if index in recipe_other:  
            other_norm = eval(other_dict[index].normalization)               
            prob.constraints['other_'+index+'_lower'] = lp_var['other_'+index] >= restriction_bounds['other_'+index][0]*other_norm   # lower bound
            prob.constraints['other_'+index+'_upper'] = lp_var['other_'+index] <= restriction_bounds['other_'+index][1]*other_norm   # upper bound
        else:
            try:
                del prob.constraints['other_'+index+'_lower']
                del prob.constraints['other_'+index+'_upper']
            except:
                pass

# To do. Figure out a way of running a pre-solver at this point

# Calculate the upper and lower bounds imposed on all the variables:

    calc_bounds = {}  # Will be of the same form as restriction_bounds     
    for key in restriction_bounds:
        calc_bounds[key] = list([0,0])       # set up the list that will contain the calculated lower and upper bounds
        res = restr_dict[key]
        prob.constraints['normalization'] = eval(res.normalization) == 1  # Apply the normalization of the restriction in question
                                                                          # Apparently this doesn't slow things down a whole lot
        for sign in [1,-1]:               # calculate lower and upper bounds.
            i = int((sign+1)/2)           # 1 -> 1 (upper), -1 -> 0 (lower)
            prob += sign*lp_var[res.objective_func], res.name
            prob.writeLP('constraints.lp')
            prob.solve(solver)
            if prob.status == 1:
                calc_bounds[key][i] = abs(sign*pulp.value(prob.objective))  # we use abs above to avoid showing -0.0, but this could cause
                                                                            # problems if we introduce other attributes that can be negative
                                                    
            else:
                try:
                    print(LpStatus[prob.status])
                except:
                    print('No solution. Problem status '+prob.status)
                prob.writeLP('constraints.lp')
                return

    return calc_bounds

##    def calc_2d_projection(self, prob, lp_var, proj_frame):  # This is designed to be run when only the x and y variables have changed; it does not take
##                                               # into account changes to upper and lower bounds. It should be possible to detect when the
##                                               # user has clicked in one of the entry boxes since the last time calc_restrictions was run,
##                                               # and give a warning in this case. Something like, if you have changed any bounds, click
##                                               # 'Calculate restrictions' to apply them.
##         
##        #Need this for 2d projection
##        tdp = 1
##
##        if len(self.variables) == 2:
##            x_var = restr_dict[self.variables['x']]
##            y_var = restr_dict[self.variables['y']]
##            if x_var.normalization == y_var.normalization:
##                prob.constraints['normalization'] =  eval(x_var.normalization) == 1
##                var_x = lp_var[x_var.objective_func]
##                var_y = lp_var[y_var.objective_func]
##
##            else:
##                messagebox.showwarning(" ", '2-dim projection of restrictions with different normalizations not implemented yet')
##                tdp = 0
##        else:
##            tdp = 0
##             
##        if tdp == 1:
##            vertices = prob.two_dim_projection(var_x, var_y)            # defined in pulp2dim file
##
##     # Display 2-d projection of feasible region onto 'x'-'y' axes
##        if tdp == 1:
##            canvas = Canvas(proj_frame, width=450, height=450, bg = 'white', borderwidth = 1, relief = 'solid')
##            canvas.create_polygon_plot(vertices)
##            canvas.pack(expand='yes', fill='both')

demo_res_bounds = {'umf_SiO2':[3,4],'umf_Al2O3':[0.3,0.5],'umf_CaO':[0,1],
                   'mass_perc_SiO2':[0,100],'mass_perc_Al2O3':[0,100],'mass_perc_CaO':[0,100],
                   'mole_perc_SiO2':[0,100],'mole_perc_Al2O3':[0,100],'mole_perc_CaO':[0,100],
                   'ingredient_0':[0,100],'ingredient_1':[0,100],'ingredient_7':[0,100],
                   'other_0':[7,12]}
demo_ingredients = ['0', '1', '7']
demo_other = ['0']
