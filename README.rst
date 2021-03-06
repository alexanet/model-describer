.. -*- mode: rst -*-
.. image:: https://travis-ci.com/DataScienceSquad/model-describer.svg?token=1GNkopDprh4icqumn6Mz&branch=master
    :target: https://travis-ci.com/DataScienceSquad/model-describer

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    
.. image:: https://img.shields.io/pypi/pyversions/ansicolortags.svg
    :target: https://pypi.python.org/pypi/model-describer

model-describer: Simple code to make 'black box' machine learning models interpretable to humans
===================================================================================================

model-describer makes it possible for everyday humans to understand 'black-box' machine learning models in two key ways:

1. model-describer helps us understand how the model 'believes' different groups behave within the model 

2. model-describer helps makes it clear where the model is making particularly accurate or inaccurate predictions

To make communicating these findings to your team easy, model-describer outputs: 

- Are created with simple Python code at the end of your existing machine learning workflow and require no model re-training
- Are compelling interactive HTML files that are small enough to be emailed. 
- Attachment only require your teammate/client to have a web browser to open your attachment. No server or messy installation required.
- Do not expose your potentially sensitive raw data. Only summaries of the data are included in the final HTML file. This also makes it possible to summarize models built on extremely large datasets into file sizes that are small enough for email. 

Sample Outputs
================

Impact
------------

Currently, many people substitute `variable importance <https://en.wikipedia.org/wiki/Random_forest#Variable_importance>`_  charts for an understanding of how the model works. While genuinely helpful, these plots do not contribute to understanding how different subgroups behave differently under the hood of the model. In the example below (`full notebook here <https://github.com/DataScienceSquad/model-describer/blob/master/docs/notebooks/WineQuality_Example.ipynb>`_ and `parameter list here <https://github.com/DataScienceSquad/model-describer/tree/master/docs>`_ ) all you have to do to produce the interactive chart is this simple segment of code:

.. code-block:: python

    SV = SensitivityViz(clf,
                       model_df=finaldf,
                       ydepend=ydepend,
                       cat_df=df,
                       featuredict=None,
                       groupbyvars=['AlcoholContent'],
                       aggregate_func=np.mean,
                       verbose=None,
                        std_num=2
                       )
    SV.run(output_type='html', output_path='path/to/save.html')

Please note all descriptive text is automatically generated by model-describer and use quartiles as cutoff points for the narrative text:

.. image:: https://github.com/DataScienceSquad/model-describer/blob/master/images/Impact_Gif.gif
    :target: https://github.com/DataScienceSquad/model-describer/blob/master/images/Impact_Gif.gif

In the above example, each variable's chart is generated by going through the dataset and generating two predictions for each row. First, model-describer uses the modelObject to generate a prediction on all of the original data. Then each variable in question is increased by one standard deviation and the model is run again on the synthetic data. The average gap in predictions between the real data and the simulated data is the 'impact' that variable has on the dependent variable. This is repeated for all variables you are interested in. For categorical variables, the synthetic data is created by setting data not at the mode to the mode and measuring the change in the predicted values.   

Error
------------

There are a hundred ways to skin an error chart. Almost all of them are reasonable. However, few can be proceeded by the comment

.. code-block:: python

   #Send To Boss As Attachment With No Additional Editing
    EV.save('/filepathtoboss')

model-describer helps fill that gap for you. These error charts group the level of error by type and show where the error vary for different parts of different variables. Again, only one line of code is required to run it.

.. code-block:: python

    EV = ErrorViz(modelobj = modelObjc,
                       model_df = xTrainData,
                       ydepend= yDepend,
                       cat_df = wine_sub,
                       groupbyvars = groupbyVars,
                       featuredict = featuredict,
                       verbose=None)
    EV.run(output_type='html', output_path='path/to/save.html')


.. image:: https://github.com/DataScienceSquad/model-describer/blob/master/images/Error_Gif.gif
    :target: https://github.com/DataScienceSquad/model-describer/blob/master/images/Error_Gif.gif

For a more detailed example, see our `example notebook <https://github.com/DataScienceSquad/model-describer/blob/master/docs/notebooks/WineQuality_Example.ipynb>`_ and `parameter list here <https://github.com/DataScienceSquad/model-describer/tree/master/docs>`_.

Installation
==============

Installation is easy.

.. code-block:: python

   pip install model-describer

Requirements
----------------

model-describer requires:

- numpy >= 1.14.0 
- pandas >= 0.22.0 
- scikit-learn >= 0.19.1 
- scipy >= 1.0.0

Helpful Tips
===============

Handling Categorical Variables
---------------------------------

In many models, categorical variables are present as independent variables. To provide meaningful charts, model-describer require categorical dummies to have the naming convention varname_category (for example Gender_Male and Gender_Female). One way to generate these is:

.. code-block:: python

   # depndent variable
   ydepend = 'target'
   # construct dataframe for modelling
   model_df = df.loc[:, df.columns != ydepend]
   model_df = pd.get_dummies(model_df)

Handling NaNs
-----------------

Missing data needs to be specially handled within model-describer. For any data the user wishes to treat as missing, numeric columns must maintain the original missing value NaN. Users should map NaN values in string variables to a more descriptive value like 'Missing'. In order to make missing data more visually appealing the html output, you can use the following construct:

.. code-block:: python

    # fill object dtype columns with null to map to html output as a category
    df = df.apply(lambda x: x.fillna('Missing') if x.dtype.kind == 'O' else x)
    # and get dummies as usual
    ydepend = 'target'
    model_df = pd.get_dummies(df.loc[:, df.columns != ydepend])
    # build and train model, etc.
    ...
    # pass to model-describer
    WB = ErrorViz(...cat_df = df, model_df = model_df)

model-describer uses the prediction methods native to the machine learning method used for training. As such, if the trained model fed to model-describer cannot process NaNs, model-describer will also be unable to process those NaNs.

Managing Output Length
------------------------

Many times, models will have hundreds (or more) of independent variables. To select a more managable subset of variables, use the keepfeaturelist parameter (present in both functions). By feeding in this list the user will make the HTML output only print output relating to the specified variables.

.. code-block:: python

    keepfeaturelist = ['col1', 'col2', 'col3']

    SV = SensitivityViz(...
                            keepfeaturelist=keepfeaturelist)


Formatting Column Names for Output HTML
----------------------------------------

If columns have unintuitive or especially long names, simply rename the columns up front in your anlaysis script and the new names will propagate throughout the pipeline into the html output.

.. code-block:: python

    col_rename = {'col1': 'demographic_age', 'col2': 'demographic_sex', 'col3': 'demographic_race'}
    df.rename(columns=col_rename, inplace=True)
    # create modelling dataframe, create dummies, build model, and specify model-describer

Formatting numeric variable outputs
--------------------------------------

If some variables contain especially long or small numbers, it is advisable to format these for better looking output.

.. code-block:: python

    df = pd.DataFrame({'col1': np.random.uniform(10000000, 20000000, 1000)})
    # format numbers
    df['col1'] = list(map(lambda p: round(p, 2), df['col1']/10000000))
    # rename column
    df.rename(columns={'col1': 'col1(10000000s)'}, inplace=True)

FAQs
--------------

Answers to additional questions about assumptions model-describer makes in its calculations can be found `here <https://github.com/DataScienceSquad/model-describer/wiki/FAQ>`_. 


Supported Machine Learning Libraries
=======================================

model-describer currently supports all traditional sklearn regression methods and all sklearn binary classification methods. model-describer does not support multi-class classification at this time. PLS Regression, PLS Cannonical, Isotonic Regression, Mutlitask Lasso & Multi-task ElasticNet are not supported as they do not produce a single prediction for each row like other classifiers do. model-describer will look to add support for other machine learning libraries the future. In all implementations, model-describer is committed to keeping our 'one line of code' promise. 

model-describer currently only supports traditional tabular data. model-describer is hoping to include text, audio, video, and images in the future but they are not part of the current implementation. 

Other Python Machine Learning Interpretability Projects
----------------------------------------------------------

For those looking for intepretation of individual points, please see the `Lime <https://github.com/marcotcr/lime>`_ project and its good work. `PyCEbox <https://github.com/AustinRochford/PyCEbox>`_ also has a different take on `classic partial dependence plots <http://scikit-learn.org/stable/auto_examples/ensemble/plot_partial_dependence.html>`_. `SHAP <https://github.com/slundberg/shap>`_ is another model-agnostic method for machine learning interpretation. 


Authors:
==========

Authors include: `Daniel Byler <https://www.linkedin.com/in/danielbyler/>`_, `Venkatesh Gangavarapu <https://www.linkedin.com/in/venkatesh-gangavarapu-9845b36b/>`_, `Jason Lewris <https://www.linkedin.com/in/jasonlewris/>`_, `Shruti Panda <https://www.linkedin.com/in/shruti-panda-1466216a/>`_

Acknowledgements
-------------------

Thanks to `Kenton Andersen <https://www.linkedin.com/in/kentonandersen/>`_ for his tireless help in running and operating our development environment. Additional acknowledgements include:

- `Shanti Jha <https://www.linkedin.com/in/shantijha/>`_
- `Brian Ray <https://www.linkedin.com/in/brianray/>`_
- `Jim Guszcza <https://www.linkedin.com/in/jim-guszcza-5330375/>`_
 
Please drop us a line in the issues section as bugs or feature requests arise. 
