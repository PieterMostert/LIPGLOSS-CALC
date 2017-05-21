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

# Initialize ingredients:
ingredient_names = ['Silica', 'Kaolin', 'Ball Clay','Potash Feldspar', 'Soda Feldspar', 'Neph Sy', 'Wollastonite', 'Whiting', 'Talc',
                    'Magnesite', 'Zinc Oxide', 'Frit 3110', 'Frit 3124', 'Frit 3134', 'Frit 3195', 'Tricalcium Phosphate',
                    'Lithium Carbonate', 'Red Iron Oxide', 'Gillespie Borate', 'Cornwall Stone']
# Note that '0'='LOI', '1'='cost', and '2'='clay'
ingredient_comp={}
ingredient_comp['Silica']={'SiO2':100}
ingredient_comp['Kaolin']={'Al2O3':40.21,'SiO2':47.29}
ingredient_comp['Ball Clay']={'Al2O3':25.02,'SiO2':59.06,'MgO':0.3,'CaO':0.3,'K2O':0.9,'Na2O':0.2,'Fe2O3':1.02,
                                                 'TiO2':1}
ingredient_comp['Neph Sy']={'Al2O3':23.3,'SiO2':60.7,'CaO':0.7,'MgO':0.1,'K2O':4.6,'Na2O':9.8,'Fe2O3':0.1}
ingredient_comp['Potash Feldspar']={'Al2O3':18.32,'SiO2':64.72,'K2O':16.92}
ingredient_comp['Soda Feldspar']={'Al2O3':19.44,'SiO2':68.74,'Na2O':11.82}
ingredient_comp['Wollastonite']={'SiO2':51.72,'CaO':48.28}
ingredient_comp['Whiting']={'CaO':56.1}
ingredient_comp['Talc']={'SiO2':63.38,'MgO':31.87}
ingredient_comp['Magnesite']={'MgO':47.8}
ingredient_comp['Zinc Oxide']={'ZnO':100}
ingredient_comp['Frit 3110']={'SiO2':66.88,'Al2O3':6.02,'CaO':5.64,'K2O':3.45,'Na2O':15.12,'B2O3':2.89}
ingredient_comp['Frit 3124']={'SiO2':55.30,'Al2O3':9.90,'CaO':14.07,'K2O':0.68,'Na2O':6.28,'B2O3':13.77}
ingredient_comp['Frit 3134']={'SiO2':46.51,'CaO':20.13,'Na2O':10.28,'B2O3':23.09}
ingredient_comp['Frit 3195']={'SiO2':48.35,'Al2O3':11.98,'CaO':11.36,'Na2O':5.69,'B2O3':22.62}
ingredient_comp['Tricalcium Phosphate']={'CaO':54.22,'P2O5':45.78}
ingredient_comp['Lithium Carbonate']={'Li2O':40.74,'0':59.26}
ingredient_comp['Red Iron Oxide']={'Fe2O3':95}
ingredient_comp['Gillespie Borate']={'SiO2':11.8,'Al2O3':1.7, 'B2O3':24.49,'CaO':22.99,'MgO':3.9,'Na2O':3.77}
ingredient_comp['Cornwall Stone']={'SiO2':73.78,'Al2O3':16.33,'CaO':1.81,'K2O':4.3,'Na2O':3.3,'MgO':0.14,'Fe2O3':0.19,
                                           'TiO2':0.15}

