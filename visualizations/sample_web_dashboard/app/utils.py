import pandas as pd
import numpy as np

"""
Both the functions in this file help convert the data from the frontend (received in the 
form of a json request) to the data names and format of the dataframe.

These are mapping functions and depend on the naming convention used in the frontend vs backend.

"""

MAPPINGS = {
    'check_0_18': (0, 18),
    'check_18_35': (18, 35),
    'check_35_55': (35, 55),
    'check_55_100': (55, 100),
    "checkMale": "Sex_male",
    "checkFemale": "Sex_female",
    'checkClass1': 'Pclass_1',
    'checkClass2': 'Pclass_2',
    'checkClass3': 'Pclass_3',
    'checkAlone': 'FamilySize_Alone',
    'checkMedium': 'FamilySize_Medium',
    'checkLarge': 'FamilySize_Large',
    'checkSouthampton': 'Embarked_S',
    'checkQueenstown': 'Embarked_Q',
    'checkCherbourg': 'Embarked_C',
    'checkLowFare': 'FareGroup_LowFare',
    'checkMediumFare': 'FareGroup_MediumFare',
    'checkHighFare': 'FareGroup_HighFare',
    'checkMaster': 'Honorific_Master.',
    'checkMr': 'Honorific_Mr.',
    'checkMiss': 'YoungWomen',
    'checkMrs': 'MarriedWomen',
    'checkRare': 'RareHonorific'
    }


def get_count(req_dict, df, column_to_checkbox_map= MAPPINGS):
    """
    - When request Data is received from the frontend, it needs to be mapped to data columns 
        in the df. This is not a simple mapping becasue the frontend displays information 
        that is meant to be user friendly, but the df does not curate information in that format.

    - This function will perform this mapping and then also calculate the number of rows
        for the selected checked values. 
    """
    checkbox_categories = { 
        'gender': ('checkMale', 'checkFemale'), 
        'class': ('checkClass1', 'checkClass2', 'checkClass3'), 
        'title' : ('checkMaster', 'checkMiss', 'checkMrs', 'checkMr', 'checkRare'), 
        'familysize': ('checkMedium', 'checkLarge', 'checkAlone'), 
        'embarkation': ('checkSouthampton', 'checkQueenstown', 'checkCherbourg'), 
        'fare': ('checkLowFare', 'checkMediumFare', 'checkHighFare')}
    ind_selected_vals = np.array([True]*df.shape[0])
    # Find which checkBoxess in the above dictionary have been received in the 
    # req_dict from the frontend
    for checkbox_category in checkbox_categories.keys():
        # For this checkbox_category go to every possible checkBox value and check if it is True
        ind_vec = [False]*df.shape[0]
        for checkbox in checkbox_categories[checkbox_category]:
            # For this checkBox check if it has been received as True in the req_dict
            # If it has been set to True, select the corresponding rows from the data frame
            if req_dict['vals'][checkbox]:
                col_name = (column_to_checkbox_map[checkbox])
                tmp_vec =  df[col_name] == req_dict['vals'][checkbox]
                # An | operation between the different values of the same checkbox_category
                ind_vec = ind_vec | tmp_vec
        # An & operation between variables
        ind_selected_vals = ind_selected_vals & ind_vec
    # Age is a more complicated variable as it is a range as in 0-18 while 
    # the data in the df does not have ranges it has integer values. So, we need to select
    # values from these ranges.
    json_age_keys = [i for i in req_dict['vals'].keys() if ('check' in i) and ('_'  in i)]
    vec_age = np.array([False]*df.shape[0])
    for age_check in json_age_keys:
        if req_dict['vals'][age_check]:
            # for the Age column
            splits = age_check.split('_')
            start_ = int(splits[1])
            end_ = int(splits[2])
            tmp_vec = (df['Age'] > start_) & (df['Age'] <= end_)
            vec_age = vec_age | tmp_vec
    # Perform and & operation as AGE is just another variable
    final_indexes_selected_vals = vec_age & ind_selected_vals
    number_died = sum(df.loc[final_indexes_selected_vals, "Survived_0"])
    number_survived = sum(df.loc[final_indexes_selected_vals, "Survived_1"])
    # Survival by Age Group
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AGES = ((0, 18), (18, 35), (35, 55), (55, 100))
    df = df.loc[final_indexes_selected_vals , :]
    vec_survAge = []
    vec_diedAge = []
    for age in AGES:
        start_age= age[0]
        end_age= age[1]
        ind = (df['Age'] > start_age) & (df['Age'] <= end_age)
        vec_survAge.append(sum(df.loc[ind, 'Survived_1']))
        vec_diedAge.append(sum(df.loc[ind, 'Survived_0']))
    return sum(final_indexes_selected_vals), number_died, number_survived, vec_survAge, vec_diedAge


def perform_mapping(inference_set):
    """
    - This function receives the inference request from the frontend
    - Transforms this inference request data into a format that corresponds to the 
        training data frame's features that were used to train the model.
    - A data frame will be returned by this function.
    - This data frame can then be passed to the model for inference
    """
    MAPPINGS_ = {
            "class": {"first": "Pclass_1", "second": "Pclass_2", "third": "Pclass_3"},
            "gender": {"male": "Sex_male", "female": "Sex_female"},
            "age": {"age" :"Age"},
            "title" : {
                "Mr.": "Honorific_Mr.", 
                "Mrs.": "MarriedWomen", 
                "Master": "Honorific_Master.",
                "Miss": "YoungWomen", 
                "Others": "RareHonorific"} , 
            "familySize": {
                "Alone": "FamilySize_Alone",
                "Medium": "FamilySize_Medium", 
                "Large": "FamilySize_Large" 
            },
            "embarkation": {
                "Queenstown": "Embarked_Q",
                "Cherbourg": "Embarked_C",
                "Southampton": "Embarked_S" 
            },
            "fare": {
                "low": "FareGroup_LowFare" , 
                "medium": "FareGroup_MediumFare" , 
                "high" : "FareGroup_HighFare"
            }
        }

    df_columns = (
        'Age', 'Survived_0', 'Survived_1', 'Pclass_1', 'Pclass_2', 'Pclass_3',
        'Honorific_Master.', 'Honorific_Mr.', 'Sex_female', 'Sex_male',
        'FamilySize_Alone', 'FamilySize_Large', 'FamilySize_Medium',
        'FareGroup_HighFare', 'FareGroup_LowFare', 'FareGroup_MediumFare',
        'Embarked_C', 'Embarked_Q', 'Embarked_S', 'YoungWomen', 'MarriedWomen',
        'RareHonorific')
    inference_set_dic = {}
    for checkbox_category in inference_set.keys():
        if not checkbox_category in ("model", "exact_age", "inference", "marital"):
            if checkbox_category == "age":
                inference_set_dic["Age"] = [inference_set["exact_age"]]
            else:
                sub_dic = MAPPINGS_[checkbox_category]
                df_column_True = sub_dic[inference_set[checkbox_category]]
                inference_set_dic[df_column_True] = [1] 
                # get all cols
                all_cols_False = [column_ for column_ in list(sub_dic.values()) if column_ != df_column_True]
                for df_column_False in all_cols_False:
                    inference_set_dic[df_column_False] = [0]

    cols = [column_ for column_ in df_columns if "Survi" not in column_]
    df_inference = pd.DataFrame(inference_set_dic)[cols]
    return df_inference