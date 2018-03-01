# sensitivity plot creation and testing

from sklearn.ensemble import RandomForestRegressor
from whitebox.eval import WhiteBoxSensitivity
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

from whitebox.eval import WhiteBoxError
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

from whitebox.utils.utils import create_wine_data

df = create_wine_data(None)

# set up y var
# set up some params
ydepend = 'free sulfur dioxide'


model_df = pd.get_dummies(df.loc[:, df.columns != ydepend])

# build model
clf = RandomForestRegressor()
clf.fit(model_df,
        df.loc[:, ydepend])

df.columns

WB = WhiteBoxSensitivity(clf,
                   model_df=model_df,
                   ydepend=ydepend,
                   cat_df=df,
                   keepfeaturelist=None,
                   groupbyvars=['alcohol', 'Type'],
                   verbose=None,
                    std_num=2,
                    autoformat_types=True,
                   )

WB.run(output_type='html',
       output_path='SENSITIVITYTEST.html')

def pandas_switch_modal_dummy(cur_col,
                              cat_df,
                              copydf):
    """
    switch modal value for categorical variable converted
    for modelling with pd.get_dummies. If col n-modal,
    select first modal value sorted alphabetically

    :param cur_col: str current column
    :param cat_df: dataframe original format
    :param copydf: dataframe copy of data used for modelling
    :return: modal value, dataframe with non-modal values switched
    :rtype: str, pd.DataFrame
    """

    # map categories with main column name to properly subset
    all_type_cols = ['{}_{}'.format(cur_col, cat) for cat in cat_df.loc[:, cur_col].unique()]
    # find the mode from the original cat_df for this column
    # if column is bimodal, selecting the first modal
    # value which is sorted alphabetically
    modal_val = str(cat_df[cur_col].mode().values[0])
    # find the columns within all_type_cols related to the mode_val
    mode_col = list(filter(lambda x: modal_val in x, all_type_cols))
    # convert mode cols to all 1's
    copydf.loc[:, mode_col] = 1
    # convert all other non mode cols to zeros
    non_mode_col = list(filter(lambda x: modal_val not in x, all_type_cols))
    # filter to columns present in the model dataframe
    non_mode_col = list(set(non_mode_col) & set(copydf.columns))
    # switch non modal columns to 0
    copydf.loc[:, non_mode_col] = 0
    # return df with switch modal column
    return modal_val, copydf


model_df.head()
copydf = model_df.copy(deep=True)

copydf.loc[:, 'alcohol_low'] = 0
copydf.loc[:, 'alcohol_medium'] = 0
copydf.loc[:, 'alcohol_high'] = 1

modal, switched = pandas_switch_modal_dummy('alcohol', df, copydf)
modal
df['alcohol'].mode()
switched.filter(regex='alcohol').describe()

switched.columns.tolist() == model_df.columns.tolist()

preds = clf.predict(switched)
preds2 = clf.predict(model_df)

final = preds-preds2
np.mean(final)
model_df.filter(regex='alcohol').describe()

np.mean(preds)
np.mean(preds2)