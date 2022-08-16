import pandas as pd
import numpy as np

mappings1 = {
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


def getCount(dict_, x, mappings_= mappings1):
    pairs = { 'gender': ('checkMale', 'checkFemale'), 
    'class': ('checkClass1', 'checkClass2', 'checkClass3'), 
    'title' : ('checkMaster', 'checkMiss', 'checkMrs', 'checkMr', 'checkRare'), 
    'familysize': ('checkMedium', 'checkLarge', 'checkAlone'), 
    'embarkation': ('checkSouthampton', 'checkQueenstown', 'checkCherbourg'), 
    'fare': ('checkLowFare', 'checkMediumFare', 'checkHighFare')}
    vec_ = np.array([True]*x.shape[0])
    for p in pairs.keys():
        l_main = [False]*x.shape[0]
        # print(pairs[p])
        for k in pairs[p]: #k_tuple:
            if dict_['vals'][k]:
                col_name = (mappings_[k])
                l_ =  x[col_name] == dict_['vals'][k]
                l_main = l_main | l_
        vec_ = vec_ & l_main
    json_keys = [i for i in dict_['vals'].keys() if ('check' in i) and ('_'  in i)]
    vec_age = np.array([False]*x.shape[0])
    for k in json_keys:
        if dict_['vals'][k]:
            # for the Age column
            splits = k.split('_')
            # print(splits)
            start_ = int(splits[1])
            end_ = int(splits[2])
            l_ = (x['Age'] > start_) & (x['Age'] <= end_)
            vec_age = vec_age | l_
    print('total records:', 'Age:',sum(vec_age), "Checks:",sum(vec_))
    final_ = vec_age&vec_
    number_died = sum(x.loc[final_, "Survived_0"])
    number_survived = sum(x.loc[final_, "Survived_1"])
    # Survival by Age Group
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ages = [(0, 18), (18, 35), (35, 55), (55, 100)]
    df = x.loc[final_ , :]
    vec_survAge = []
    vec_diedAge= []
    for age in ages:
        st_= age[0]
        en_= age[1]
        ind = (df['Age']>st_) & (df['Age']<=en_)
        vec_survAge.append(sum(df.loc[ind, 'Survived_1']))
        vec_diedAge.append(sum(df.loc[ind, 'Survived_0']))

    return sum(final_), number_died, number_survived, vec_survAge, vec_diedAge

# getCount(dict_, mappings_)

def performMapping(inference_set):
    mappings_ = {
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

    x_columns = ['Age', 'Survived_0', 'Survived_1', 'Pclass_1', 'Pclass_2', 'Pclass_3',
        'Honorific_Master.', 'Honorific_Mr.', 'Sex_female', 'Sex_male',
        'FamilySize_Alone', 'FamilySize_Large', 'FamilySize_Medium',
        'FareGroup_HighFare', 'FareGroup_LowFare', 'FareGroup_MediumFare',
        'Embarked_C', 'Embarked_Q', 'Embarked_S', 'YoungWomen', 'MarriedWomen',
        'RareHonorific']
    inference_set_dic = {}
    for key_ in inference_set.keys():
        if not ((key_ == "model") or (key_ == "exact_age") or 
                (key_ == "inference") or (key_ == "marital")):
            if key_ == "age":
                # print(key_, "|-->", inference_set[key_], inference_set["exact_age"])
                inference_set_dic["Age"] = [inference_set["exact_age"]]
            else:
                sub_dic = mappings_[key_]
                key_col_set_to_1 = sub_dic[inference_set[key_]]
                # print(key_, "-->", inference_set[key_], "-->" , key_col_set_to_1)
                inference_set_dic[key_col_set_to_1] = [1] 
                # get all cols
                all_cols = list(sub_dic.values())
                all_cols = [i for i in all_cols if i != key_col_set_to_1]
                for i in all_cols:
                    inference_set_dic[i] = [0]

    cols = [i for i in x_columns if "Survi" not in i]
    df_inference = pd.DataFrame(inference_set_dic)[cols]
    return df_inference

