import pandas as pd
import glob
from tqdm import tqdm

def main(transfer_list, vin_list):
    transfer_df = pd.read_csv(transfer_list)
    vin_df = pd.read_csv(vin_list)
    
    # create mew fields in transfer file
    transfer_df['Suggested_VIN'] = ''
    transfer_df['Location'] = ''
    transfer_df['Suggested_SKU'] = ''

    tqdm.pandas()
    pbar = tqdm(transfer_df.iterrows(), total=len(transfer_df))
    
    # search the vin list for locations
    for i, j in pbar:
        vin = transfer_df.loc[i, ['VIN']][0]
        results = vin_df.index[vin_df[' Number'] == vin].to_list()
        pbar.set_description(vin)
        try:
            # print(vin_df.loc[results[-1], 'Location'])
            transfer_df.loc[i, 'Location'] = vin_df.loc[results[-1], 'Location']
            transfer_df.loc[i, 'Suggested_SKU'] = vin_df.loc[results[-1], 'Item']
            transfer_df.loc[i, 'Suggested_VIN'] = vin_df.loc[results[-1], ' Number']
            
            
        except Exception as e:
            new_vin = vin.replace('O', '0')
            results1 = vin_df.index[vin_df[' Number'] == new_vin].to_list()
            try:
                transfer_df.loc[i, 'Location'] = vin_df.loc[results1[-1], 'Location']
                transfer_df.loc[i, 'Suggested_SKU'] = vin_df.loc[results1[-1], 'Item']
                transfer_df.loc[i, 'Suggested_VIN'] = vin_df.loc[results1[-1], ' Number']
            
            except:
                new_vin1 = vin.replace('0', 'O')
                results2 = vin_df.index[vin_df[' Number'] == new_vin1].to_list()
                try:
                    transfer_df.loc[i, 'Location'] = vin_df.loc[results2[-1], 'Location']
                    transfer_df.loc[i, 'Suggested_SKU'] = vin_df.loc[results2[-1], 'Item']
                    transfer_df.loc[i, 'Suggested_VIN'] = vin_df.loc[results2[-1], ' Number']

                except:
                    pass
            
        # write results to file
        transfer_df.to_csv("SearchResults.csv", index=False)
    
if __name__ == '__main__':

    vin_list = ''
    transfer_list = ''

    # find the proper files
    for file in glob.glob('AvailableDenagoVINNumbersResults*.csv'):
        vin_list = file
        
    for file in glob.glob('transfervins*.csv'):
        transfer_list = file
        
    main(transfer_list, vin_list)
