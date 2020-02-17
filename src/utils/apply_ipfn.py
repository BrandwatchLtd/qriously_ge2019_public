"""All code is released under the MIT License.

Copyright 2020 Brandwatch

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without 
limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, RISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
 OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import pandas as pd
from ipfn import ipfn


def apply_ipfn(data_df, proportions, check_marginals=False):

    data_df = data_df.copy()  # the ipfn code overwrites the df it runs on, so we make a copy
        
    
    if len(proportions) == 1:
        
        # Weighting by a single column isn't supported by the ipfn module, it seems; so we implement that calculation
        # here ourselves.

        weighting_col = list(proportions.keys())[0]
        
        weight_dict = proportions[weighting_col].to_dict()
        
        assert weighting_col in data_df
        assert data_df[weighting_col].notnull().all()
        
        for x in weight_dict.values():
            assert x >= 0
            assert x <= 1

            
        raw_props = (data_df[weighting_col].value_counts() / data_df.shape[0]).to_dict()  # Get the raw proportions

        
        # Check that the set of categories appearing in weight_dict is exactly equal to the set appearing in
        # the data.
        # (There might be an argument for allowing extra categories in weight_dict provided the desired weight is zero,
        # but it's an odd edge case.)

        assert set(weight_dict.keys()) == set(raw_props.keys())
        
        weight_mapping = { k: v / raw_props[k] for k, v in weight_dict.items() }

        data_df['Weight'] = data_df[weighting_col].map(weight_mapping)
        
        res_df = data_df

        if check_marginals:
            
            # Checking the marginals is pretty unnecessary in the single-column case, but we implement it anyway
            # so that this function has a uniform interface.

            desired_props = pd.Series(weight_dict).to_frame('Desired')
            delivered_props = (res_df.groupby(weighting_col).agg(Delivered = ('Weight', 'sum')) / res_df.shape[0])
            
            marginal_check_df = pd.merge(desired_props, delivered_props, left_index=True, right_index=True, validate='one_to_one')
            marginal_check_df['AbsDiff'] = (marginal_check_df['Desired'] - marginal_check_df['Delivered']).abs()

            return res_df, {weighting_col: marginal_check_df}

        else:
            return res_df
        
        
    else:
    
        data_df = data_df.copy()  # the ipfn code overwrites the df it runs on, so we make a copy
        assert 'total' not in list(data_df)
        data_df['total'] = 1
        
        aggregates = []
        dimensions = []
        
        for col, props in proportions.items():
            
            props_series = pd.Series(props) if type(props) == dict else props
            props_series = props_series / props_series.sum() # Normalise, for our sins
            props_series = props_series.rename('total')
    
            dimensions.append([col])
            aggregates.append(props_series)
        
        
        IPF = ipfn.ipfn(data_df, aggregates, dimensions, max_iteration=20000)
        res_df = IPF.iteration()
    
        res_df = res_df.rename({'total': 'Weight'}, axis='columns')
        
        res_df['Weight'] = res_df['Weight'] * res_df.shape[0]
        
    
        # Now for our peace of mind, we see how close the ipfn code has managed to get to the marginals that we asked for.

        if check_marginals:

            marginal_dfs = dict()

            for col, prop_series in zip(map(lambda x: x[0], dimensions), aggregates):

                desired_props = prop_series.rename('Desired')
                delivered_props = (res_df.groupby(col).agg(Delivered = ('Weight', 'sum')) / res_df.shape[0])

                merged_df = pd.merge(desired_props.to_frame(), delivered_props, left_index=True, right_index=True, validate='one_to_one')

                merged_df['AbsDiff'] = (merged_df['Desired'] - merged_df['Delivered']).abs()

                marginal_dfs[col] = merged_df

            return res_df, marginal_dfs

        else:
            return res_df