"""
This file contains long lists of categories used by other Python classes.
There are also functions available to print these lists.
"""

'''
FNDDS  is a database that provides the nutrient values for foods and beverages reported in What We Eat in America, the 
dietary intake component of the National Health and Nutrition Examination Survey.
'''
fndds_columns_to_convert = ['Food code',
                            'WWEIA Category number',
                            'Energy (kcal)',
                            'Protein (g)',
                            'Carbohydrate (g)',
                            'Sugars, total (g)',
                            'Fiber, total dietary (g)',
                            'Total Fat (g)',
                            'Fatty acids, total saturated (g)',
                            'Fatty acids, total monounsaturated (g)',
                            'Fatty acids, total polyunsaturated (g)',
                            'Cholesterol (mg)',
                            'Retinol (mcg)',
                            'Vitamin A, RAE (mcg_RAE)',
                            'Carotene, alpha (mcg)',
                            'Carotene, beta (mcg)',
                            'Cryptoxanthin, beta (mcg)',
                            'Lycopene (mcg)',
                            'Lutein + zeaxanthin (mcg)',
                            'Thiamin (mg)',
                            'Riboflavin (mg)',
                            'Niacin (mg)',
                            'Vitamin B-6 (mg)',
                            'Folic acid (mcg)',
                            'Folate, food (mcg)',
                            'Folate, DFE (mcg_DFE)',
                            'Folate, total (mcg)',
                            'Choline, total (mg)',
                            'Vitamin B-12 (mcg)',
                            'Vitamin B-12, added (mcg)',
                            'Vitamin C (mg)'
                            'Vitamin D (D2 + D3) (mcg)',
                            'Vitamin E (alpha-tocopherol) (mg)',
                            'Vitamin E, added (mg)',
                            'Vitamin K (phylloquinone) (mcg)',
                            'Calcium (mg)',
                            'Phosphorus (mg)',
                            'Magnesium (mg)',
                            'Iron (mg)',
                            'Zinc (mg)',
                            'Copper (mg)',
                            'Selenium (mcg)',
                            'Potassium (mg)',
                            'Sodium (mg)',
                            'Caffeine (mg)',
                            'Theobromine (mg)',
                            'Alcohol (g)',
                            '4:0 (g)',  # butyric acid
                            '6:0 (g)',  # caproic acid
                            '8:0 (g)',  # caprylic acid
                            '10:0 (g)',  # capric acid
                            '12:0 (g)',  # lauric acid
                            '14:0 (g)',  # myristic acid
                            '16:0 (g)',  # palmitic acid
                            '18:0 (g)',  # stearic acid
                            '16:1 (g)',  # palmitoleic acid
                            '18:1 (g)',  # oleic acid
                            '20:1 (g)',  # gadoleic acid
                            '22:1 (g)',  # erucic acid
                            '18:2 (g)',  # linoleic acid
                            '18:3 (g)',  # alpha linolenic acid
                            '18:4 (g)',  # CHEBI:132503
                            '20:4 (g)',  # arachidonic acid
                            '20:5 n-3 (g)',  # eicosapentaenoic acid
                            '22:5 n-3 (g)',  # docosapentaenoic acid
                            '22:6 n-3 (g)',  # docosahexaenoic acid
                            'Water (g)']

'''
The list nutrition_categories contains all the columns with nutritional information from both the FNDDS and the FPED.
'''
nutrition_categories = ['Energy (kcal)',
                        'Protein (g)',
                        'Carbohydrate (g)',
                        'Sugars, total(g)',
                        'Fiber, total dietary (g)',
                        'Total Fat (g)',
                        'Fatty acids, total saturated (g)',
                        'Fatty acids, total monounsaturated (g)',
                        'Fatty acids, total polyunsaturated (g)',
                        'Cholesterol (mg)',
                        'Retinol (mcg)',
                        'Vitamin A, RAE (mcg_RAE)',
                        'Carotene, alpha (mcg)',
                        'Carotene, beta (mcg)',
                        'Cryptoxanthin, beta (mcg)',
                        'Lycopene (mcg)',
                        'Lutein + zeaxanthin (mcg)',
                        'Thiamin (mg)',
                        'Riboflavin (mg)',
                        'Niacin (mg)',
                        'Vitamin B-6 (mg)',
                        'Folic acid (mcg)',
                        'Folate, food (mcg)',
                        'Folate, DFE (mcg_DFE)',
                        'Folate, total (mcg)',
                        'Choline, total (mg)',
                        'Vitamin B-12 (mcg)',
                        'Vitamin B-12, added (mcg)',
                        'Vitamin C (mg)',
                        'Vitamin D (D2 + D3) (mcg)',
                        'Vitamin E (alpha-tocopherol) (mg)',
                        'Vitamin E, added (mg)',
                        'Vitamin K (phylloquinone) (mcg)',
                        'Calcium (mg)',
                        'Phosphorus (mg)',
                        'Magnesium (mg)',
                        'Iron (mg)',
                        'Zinc (mg)',
                        'Copper (mg)',
                        'Selenium (mcg)',
                        'Potassium (mg)',
                        'Sodium (mg)',
                        'Caffeine (mg)',
                        'Theobromine (mg)',
                        'Alcohol (g)',
                        '4:0 (g)',  # butyric acid
                        '6:0 (g)',  # caproic acid
                        '8:0 (g)',  # caprylic acid
                        '10:0 (g)',  # capric acid
                        '12:0 (g)',  # lauric acid
                        '14:0 (g)',  # myristic acid
                        '16:0 (g)',  # palmitic acid
                        '18:0 (g)',  # stearic acid
                        '16:1 (g)',  # palmitoleic acid
                        '18:1 (g)',  # oleic acid
                        '20:1 (g)',  # gadoleic acid
                        '22:1 (g)',  # erucic acid
                        '18:2 (g)',  # linoleic acid
                        '18:3 (g)',  # alpha linolenic acid
                        '18:4 (g)',  # CHEBI:132503
                        '20:4 (g)',  # arachidonic acid
                        '20:5 n-3 (g)',  # eicosapentaenoic acid
                        '22:5 n-3 (g)',  # docosapentaenoic acid
                        '22:6 n-3 (g)',  # docosahexaenoic acid
                        'Water (g)',
                        'F_TOTAL (cup eq.)',
                        'F_CITMLB (cup eq.)',
                        'F_OTHER (cup eq.)',
                        'F_JUICE (cup eq.)',
                        'V_TOTAL (cup eq.)',
                        'V_DRKGR (cup eq.)',
                        'V_REDOR_TOTAL (cup eq.)',
                        'V_REDOR_TOMATO (cup eq.)',
                        'V_REDOR_OTHER (cup eq.)',
                        'V_STARCHY_TOTAL (cup eq.)',
                        'V_STARCHY_POTATO (cup eq.)',
                        'V_STARCHY_OTHER (cup eq.)',
                        'V_OTHER (cup eq.)',
                        'V_LEGUMES (cup eq.)',
                        'G_TOTAL (oz. eq.)',
                        'G_WHOLE (oz. eq.)',
                        'G_REFINED (oz. eq.)',
                        'PF_TOTAL (oz. eq.)',
                        'PF_MPS_TOTAL (oz. eq.)',
                        'PF_MEAT (oz. eq.)',
                        'PF_CUREDMEAT (oz. eq.)',
                        'PF_ORGAN (oz. eq.)',
                        'PF_POULT (oz. eq.)',
                        'PF_SEAFD_HI (oz. eq.)',
                        'PF_SEAFD_LOW (oz. eq.)',
                        'PF_EGGS (oz. eq.)',
                        'PF_SOY (oz. eq.)',
                        'PF_NUTSDS (oz. eq.)',
                        'PF_LEGUMES (oz. eq.)',
                        'D_TOTAL (cup eq.)',
                        'D_MILK (cup eq.)',
                        'D_YOGURT (cup eq.)',
                        'D_CHEESE (cup eq.)',
                        'OILS (grams)',
                        'SOLID_FATS (grams)',
                        'ADD_SUGARS (tsp. eq.)',
                        'A_DRINKS (no. of drinks)']

'''
The list hei_categories contains the 13 categories that compose the Healthy Eating Index.
'''
hei_categories = ['total_fruits',
                  'whole_fruits',
                  'total_vegetables',
                  'greens_and_beans',
                  'whole_grains',
                  'dairy',
                  'total_protein_foods',
                  'seafood_and_plant_proteins',
                  'fatty_acids',
                  'refined_grains',
                  'added_sugars',
                  'sodium',
                  'saturated_fats']

'''
The dictionary fatty_acid_key maps the carbon representation of a fatty acid to the acid name.
'''
fatty_acid_key = {
    '4:0 (g)': 'butyric acid',
    '6:0 (g)': 'caproic acid',
    '8:0 (g)': 'caprylic acid',
    '10:0 (g)': 'capric acid',
    '12:0 (g)': 'lauric acid',
    '14:0 (g)': 'myristic acid',
    '16:0 (g)': 'palmitic acid',
    '18:0 (g)': 'stearic acid',
    '16:1 (g)': 'palmitoleic acid',
    '18:1 (g)': 'oleic acid',
    '20:1 (g)': 'gadoleic acid',
    '22:1 (g)': 'erucic acid',
    '18:2 (g)': 'linoleic acid',
    '18:3 (g)': 'alpha linolenic acid',
    '18:4 (g)': 'CHEBI:132503',
    '20:4 (g)': 'arachidonic acid',
    '20:5 n-3 (g)': 'eicosapentaenoic acid',
    '22:5 n-3 (g)': 'docosapentaenoic acid',
    '22:6 n-3 (g)': 'docosahexaenoic acid',
}


def print_nutritional_categories():
    """Prints a list of the columns with nutritional information."""
    print("Printing nutritional categories...")
    for cat in fndds_columns_to_convert:
        print(cat)


def print_hei_categories():
    """Prints the thirteen HEI categories."""
    print("Printing HEI categories...")
    for cat in hei_categories:
        print(cat)


def print_fatty_acid_info():
    """Prints fatty acid names and corresponding carbon numbering."""
    print("Printing fatty acid names and carbon numbering... ")
    for key in fatty_acid_key.keys():
        print(key, "(", fatty_acid_key[key], ")")
