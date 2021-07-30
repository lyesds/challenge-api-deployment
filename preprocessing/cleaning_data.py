import pandas as pd
import numpy as np


def preprocess(input_dict):
    """
    Read the input data (JSON format), merge it with administrative information (city, region, province),
    and preprocess it (missing value, categorical data).
    :return: a dataframe with one row that can be passed to the .predict method of the ML model to predict the price.
    """
    # ds = pd.read_json("data/"+input_filename+".json", orient='index')
    ds = pd.DataFrame.from_dict(input_dict, orient='index')

    dummy = pd.read_csv('data/dummy.csv', encoding='latin1')
    ds = pd.concat([ds, dummy], axis=0)

    postalcode = pd.read_csv('data/postalcode.csv', encoding='latin1')
    postalcode.sort_values(by=['postalCode', 'Sous_Commune'], inplace=True)
    # Keeping only first row (corresponding to the principal municipality when postalCode ends with 0)
    # for rows having same postalCode
    postalcode.drop_duplicates(['postalCode'], keep='first', inplace=True, ignore_index=True)
    # postalcode.info()

    postalcode.rename(columns={"postalCode": "location"}, inplace=True)
    ds = pd.merge(ds, postalcode, how='left', on="location")

    # Convert missing values with median score for terrace and garden area, and facade count
    # Creating new columns for median scores (except the land_surface column)
    ds['median_terrace_area'] = np.nan
    ds['median_garden_area'] = np.nan
    ds['median_facade'] = np.nan

    # Check median of these 3 variable
    # print(ds['terrace_area'].median(), ds['garden_area'].median(), ds['facade_count'].median())

    # TERRACE
    # Creating a median_terrace_area column: if 'terrace_area' information is available, take that, else put 16.0 as a median score.

    ds['median_terrace_area'] = np.where(ds['terrace'] == 1, ds['terrace_area'],
                                         (np.where(ds['terrace'] == 0, 16.0, ds['median_terrace_area'])))

    # If there is a terrace but the area is unknown, put 16.0 as the median score
    ds['median_terrace_area'] = np.where((ds['terrace'] == 1 & ds['terrace_area'].isnull()), 16.0,
                                         ds['median_terrace_area'])

    # GARDEN
    # Fill the column with given conditions for median garden area column
    ds['median_garden_area'] = np.where(ds['garden'] == 1, ds['garden_area'],
                                        (np.where(ds['garden'] == 0, 200.0, ds['median_garden_area'])))

    # If there is a garden but the area is unknown, put 16.0 as the median score
    ds['median_garden_area'] = np.where((ds['garden'] == 1 & ds['garden_area'].isnull()), 200.0,
                                        ds['median_terrace_area'])

    # FACADE
    # If facade count data is available, use that, else put 2 as median score
    ds['median_facade'] = np.where(ds['facade_count'].notnull(), ds['facade_count'],
                                   (np.where(ds['facade_count'].isnull(), 2, ds['median_facade'])))

    ds['type_num'] = pd.get_dummies(ds.type, drop_first=True)
    building_condition_num = pd.get_dummies(ds['building_condition'], drop_first=False)
    region_num = pd.get_dummies(ds['Region'], drop_first=False, prefix='reg')
    province_num = pd.get_dummies(ds['Province'], drop_first=False)

    ds = pd.concat([ds, building_condition_num, region_num, province_num], axis=1)

    # Fill with zero land_surface for apartments
    ds['land_surface'] = np.where(ds['type_num'] == 0, 0, ds['land_surface'])

    ds = ds.head(1) # keep only the real input JSON data = 1st row
    ds = ds.select_dtypes(exclude=['object']) # not used in model
    ds = ds.drop(['garden_area', 'terrace_area', 'land_surface', 'facade_count'], axis=1) # not used in model

    print('Data after preprocessing')
    print(ds.shape)

    return ds


'''
ds = preprocess('input')
print(ds)
'''