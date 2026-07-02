import pandas as pd
import numpy as np

#Function used to calculate the frequency of each claim type for a particular factor
def frequency_calc(df, by_group, key = None):
    
    results = []

    #For each Claim Type, calculate the exposure and append it to a list
    for claim_type in ["ad", "bi", "pd", "th", "ws"]:
    
        temp = (
            df.groupby(by_group)
              .agg(
                  total_exposure=("exposure", "sum"),
                  claims=(f"{claim_type}_count", "sum")
              )
              .reset_index()
        )
    
        temp["frequency"] = temp["claims"] / temp["total_exposure"]
    
        temp["claim_type"] = claim_type
    
        results.append(temp)
    
    #Extract the complete list as a new dataframe
    df_out = pd.concat(results, ignore_index=True).fillna(0)
    
    #Replacing values
    df_out["claim_type"] = df_out["claim_type"].str.replace(
        {
            "ad":"Accidental",
            "pd":"Third Party Property",
            "ws":"Windscreen",
            "bi":"Bodily Injuries",
            "th": "Fire/Theft"
        }
    )
    #If provided, replace the by_group values using an input dictionary
    if key:
        
        df_out[by_group] = df_out[by_group].replace(key)
    

    #Pivot the data frame 
    pivot = df_out.pivot(
        index=by_group,
        columns="claim_type",
        values="frequency"
    )

    return df_out, pivot
    



#Function used to calculate the severity of each claim type for a particular factor
def severity_calc(df, by_group, key = None):
    
    results = []

    #For each Claim Type, calculate the exposure and append it to a list
    for claim_type in ["ad", "bi", "pd", "th", "ws"]:
    
        temp = (
            df.groupby(by_group)
              .agg(
                  total_incurred=(f"{claim_type}_incurred", "sum"),
                  claims=(f"{claim_type}_count", "sum")
              )
              .reset_index()
        )
    
        temp["severity"] = temp["total_incurred"] / temp["claims"]
    
        temp["claim_type"] = claim_type
    
        results.append(temp)
    
    #Extract the complete list as a new dataframe
    df_out = pd.concat(results, ignore_index=True).fillna(0)
    
    #Replacing values
    df_out["claim_type"] = df_out["claim_type"].str.replace(
        {
            "ad":"Accidental",
            "pd":"Third Party Property",
            "ws":"Windscreen",
            "bi":"Bodily Injuries",
            "th": "Fire/Theft"
        }
    )
    #If provided, replace the by_group values using an input dictionary
    if key:
        
        df_out[by_group] = df_out[by_group].replace(key)
    

    #Pivot the data frame 
    pivot = df_out.pivot(
        index=by_group,
        columns="claim_type",
        values="severity"
    )

    return df_out, pivot