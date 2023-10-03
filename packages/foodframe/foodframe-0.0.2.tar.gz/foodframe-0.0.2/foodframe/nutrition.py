import categories as cats
import pandas as pd


def get_nutrition_df(food_df, folder_path):
    """
    Returns a dataframe with added nutritional information for each row of food data.
    Amounts are converted to 100g equivalents in the instantiation of a FoodFrame.
    """
    # obtain and merge FNDDS and FPED
    fndds_df = pd.read_csv(folder_path + 'data/fndds_17_18.csv')
    fndds_df[cats.fndds_columns_to_convert] = fndds_df[cats.fndds_columns_to_convert].apply(pd.to_numeric)
    fndds_df.rename({'Food code': 'food_code'}, axis=1, inplace=True)
    fped_df = pd.read_csv(folder_path + 'data/fped_17_18.csv')
    fped_df.rename({'FOODCODE': 'food_code'}, axis=1, inplace=True)
    merged_nutrition_df = pd.merge(fndds_df, fped_df, on='food_code')

    # merge food bank data and nutrition data
    nutrition_available = merged_nutrition_df['food_code']
    food_df = food_df[food_df['food_code'].isin(nutrition_available)]
    nutrition_df = pd.merge(food_df, merged_nutrition_df, on='food_code')

    # multiply nutrition amounts in 100-gram equivalents by number of equivalents
    for nutrition_category in cats.nutrition_categories:
        nutrition_df[nutrition_category] = nutrition_df[nutrition_category] * nutrition_df['100g']

    # renaming columns
    nutrition_df = nutrition_df.rename(columns={'F_TOTAL (cup eq.)': 'total_fruits_cup',
                                                'G_WHOLE (oz. eq.)': 'whole_grains_oz',
                                                'G_REFINED (oz. eq.)': 'refined_grains_oz',
                                                'D_TOTAL (cup eq.)': 'dairy_cup',
                                                'ADD_SUGARS (tsp. eq.)': 'added_sugars_tsp',
                                                'Fatty acids, total saturated (g)': 'saturated_fats_g',
                                                'Fatty acids, total monounsaturated (g)': 'monounsaturated_fats_g',
                                                'Fatty acids, total polyunsaturated (g)': 'polyunsaturated_fats_g',
                                                'Energy (kcal)': 'energy_kcal'})

    # calculate HEI component columns
    nutrition_df['whole_fruits_cup'] = nutrition_df['total_fruits_cup'] - nutrition_df['F_JUICE (cup eq.)']
    nutrition_df['total_vegetables_cup'] = nutrition_df['V_TOTAL (cup eq.)'] + nutrition_df['V_LEGUMES (cup eq.)']
    nutrition_df['greens_and_beans_cup'] = nutrition_df['V_DRKGR (cup eq.)'] + nutrition_df['V_LEGUMES (cup eq.)']
    nutrition_df['total_protein_foods_oz'] = nutrition_df['PF_TOTAL (oz. eq.)'] + nutrition_df['PF_LEGUMES (oz. eq.)']
    nutrition_df['seafood_and_plant_proteins_oz'] = (nutrition_df['PF_SEAFD_HI (oz. eq.)'] +
                                                     nutrition_df['PF_SEAFD_LOW (oz. eq.)'] +
                                                     nutrition_df['PF_SOY (oz. eq.)'] +
                                                     nutrition_df['PF_NUTSDS (oz. eq.)'] +
                                                     nutrition_df['PF_LEGUMES (oz. eq.)'])
    nutrition_df['sodium_g'] = nutrition_df['Sodium (mg)'] / 1000

    return nutrition_df
