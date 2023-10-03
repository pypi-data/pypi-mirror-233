import pandas as pd
import hei
import nutrition as nutri


def convert_to_100g(row):
    # TODO: support more units than lb and oz
    if row['units'] == 'oz':
        return row['amount'] * 28.3495 * 0.01
    elif row['units'] == 'lb':
        return row['amount'] * 453.592 * 0.01
    else:
        return None


class FoodFrame:
    """
    A FoodFrame object allows you to calculate information about a nutritional dataset.
    To instantiate a FoodFrame object, you need a datafile. The requirements for this datafile are in the README.
    Once you have created a FoodFrame, you can perform the following operations and analyses:
    - HEI score for a given set of foodbanks and a give set of years
    - nutritional analysis (future)
    - sustainability analysis (future)
    """

    def __init__(self, data_file):
        """Instantiates a FoodFrame object.

    PARAMETERS
    ----------
    data_file -- .csv file with the food and foodbank data

    OBJECT VARIABLES
    ----------------
    The following are object level variables which are instantiated in this constructor.

    self.df -- the main dataframe used for all operations
    self.multibank -- boolean is True if dataset contains multiple foodbanks, False otherwise
    self.code_type -- string is 'usda' or 'wweia'
    self.unspecified_quantities -- boolean is True if unspecified quantities are retained
    """
        self.df = pd.read_csv(data_file)

        # check if dataset contains multiple food banks
        if 'food_bank' in self.df.columns:
            self.multibank = True
        else:
            # self.df['food_bank'] = ['Food Bank']
            self.multibank = False

        # check whether dataset uses USDA or WWEIA food codes
        if len(self.df.iloc[1]['food_code']) == 8:
            self.code_type = 'usda'
        # TODO: WWEIA coding not integrated into nutrition.py and hei.py
        elif len(self.df.iloc[1]['food_code']) == 4:
            self.code_type = 'wweia'
        else:
            print('Error occurred: Food code type must be USDA or WWEIA')

        # check for date column and convert to year, month, day columns
        if 'date' in self.df.columns:
            self.df['date'] = self.df['date'].str.replace(r'[^\w\s]+', '')
            self.df['date'] = pd.to_datetime(self.df['date'], format='%Y%m%d')
            self.df['year'] = self.df['date'].dt.year
            self.df['month'] = self.df['date'].dt.month
            self.df['day'] = self.df['date'].dt.day

        # check and convert units to 100-gram equivalents
        if 'units' in self.df.columns:
            if len(self.df[self.df['units'] == 'quantity_not_specified']) < 0.1 * len(self.df):
                print("Dropping rows with unspecified quantities since they are less than 10% of the dataset.")
                self.df = self.df[self.df]  # fix, print rows
            self.df['100g'] = self.df.apply(convert_to_100g, axis=1)
            self.unspecified_quantities = False
        else:
            self.unspecified_quantities = True
            print("Rows with unspecified qualities represent more than 10/% of the dataset. Analytics not calculated. \
                Some operations restricted.")

        # check conditions for nutrition
        if not self.unspecified_quantities:
            self.clean_df = self.df[['food_code', '100g', 'food_bank', 'date']]
            self.nutri_df = nutri.get_nutrition_df(self.clean_df, '')  # blank extended file path for now
            # TODO: add a list of yearly HEI scores, food bank HEI scores

    def get_hei(self, food_banks=all, years=all):
        if food_banks == all:
            food_banks = self.nutri_df['food_bank'].unique()
        if years == all:
            years = self.nutri_df['year'].unique()
        selected_df = self.nutri_df.loc[
            (self.nutri_df['year'].isin(years)) & (self.nutri_df['food_bank'].isin(food_banks))]
        return hei.get_hei_df(selected_df)


# TODO: Future features
"""
  def desc_stats(self, food_banks=all):
    #TODO: Annie
    '''
    Print and return dataset statistics.

    This function calculates basic, descriptive statistics
    for a user-defined set of food_banks. The default is to
    calculate statistics for the set of all food_banks, for
    which the user may use the keywords shortcut 'all'.

    Reported statistics include:
    - Number of food banks in set,
    - Number of different foods in set,
    - Number of total rows in set,
    - Averages, minimums, and maximums for other numerical variables

    Parameters
    ----------
      food_banks -- the food bank to calculate stats for (default=all)

    Returns
    -------
    string
      formatted string of descriptive statistics
    '''
    if food_banks==all:
      # code here to set food_banks to column as list

    try:
      if isinstance(food_banks, list):
        ## code here
      else:
        raise ValueError('Keyword argument must be a list.')

    except ValueError as error:
      print('Error occured: ' + repr(error))

  def annual_hei_report():
    '''Prints HEI scores for all food banks by year.'''
  def nutrition_report(food_banks=all, years=all):
    '''Prints descriptive nutritional information.'''
  def banks_hei_report():
  def get_time_range(food_banks=all):
    #RETURN a tuple with a time range
  def report_time_range(food_banks=all):
    #PRINT formatted time range
  def print_nutrition_columns:
    #PRINTS the nutrition columns user has access to
  def get_nutrition_average(column_name, food_banks=all, years=all)
"""
