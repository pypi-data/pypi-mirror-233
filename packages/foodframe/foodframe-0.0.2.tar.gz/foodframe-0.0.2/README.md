#######
WELCOME
#######

FoodFrame is a Python package that provides analyses of food datasets. Currently, FoodFrame provides nutritional information for a given set of food using USDA or WWEIA codes. This information includes a Healthy Eating Index (HEI) score. FoodFrame is the first Python package available (to our knowledge) that allows you to easily calculate an HEI score for a food dataset with different amounts and units of foods. You can calculate HEI scores for any subset of food banks and years in your dataset, if you have such information.

We are currently working on expanding FoodFrame to allow for more general nutrition analysis, sustainability analysis through collaboration with ReFed, and trend analysis based on yearly or seasonal cycles. If you have a comment, suggestion, or question, please email Annie Lamar at kalamar [at] stanford [dot] edu.



######################
DATA FILE REQUIREMENTS
######################

Your data file should be a .csv file. Place the file in the 'data' directory.

Required columns:

- food_code: may be either a USDA code or What We Eat in America (WWEIA) code

- amount: the amount of each item (integer or float only)

Optional columns:

- date: in YEAR-MONTH-DAY format
- food_bank: which food bank a line of data belongs to
- units: the unit type for the amount column. Values supported are 'oz' and 'lb'. If not included, the calculations default to pounds.*

*Note: if you don't know the units for a particular row, list the units as "quantity_not_specified". If less than 10% of lines have units listed as "quantity_not_specified", those lines are dropped from the dataset. If more than 10% of lines have units listed as "quantity_not_specified", most analyses will be not be performed.*