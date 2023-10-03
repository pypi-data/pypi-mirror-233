import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to DEBUG, you can change this if you want
    format='%(levelname)s:%(message)s'  
)

STATE_ABBREVIATIONS = STATE_ABBREVIATIONS = {
    'AL': 'Ala.',
    'AK': 'Alaska',
    'AZ': 'Ariz.',
    'AR': 'Ark.',
    'CA': 'Calif.',
    'CO': 'Colo.',
    'CT': 'Conn.',
    'DE': 'Del.',
    'FL': 'Fla.',
    'GA': 'Ga.',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Ill.',
    'IN': 'Ind.',
    'IA': 'Iowa',
    'KS': 'Kan.',
    'KY': 'Ky.',
    'LA': 'La.',
    'ME': 'Maine',
    'MD': 'Md.',
    'MA': 'Mass.',
    'MI': 'Mich.',
    'MN': 'Minn.',
    'MS': 'Miss.',
    'MO': 'Mo.',
    'MT': 'Mont.',
    'NE': 'Neb.',
    'NV': 'Nev.',
    'NH': 'N.H.',
    'NJ': 'N.J.',
    'NM': 'N.M.',
    'NY': 'N.Y.',
    'NC': 'N.C.',
    'ND': 'N.D.',
    'OH': 'Ohio',
    'OK': 'Okla.',
    'OR': 'Ore.',
    'PA': 'Pa.',
    'RI': 'R.I.',
    'SC': 'S.C.',
    'SD': 'S.D.',
    'TN': 'Tenn.',
    'TX': 'Tex.',
    'UT': 'Utah',
    'VT': 'Vt.',
    'VA': 'Va.',
    'WA': 'Wash.',
    'WV': 'W.Va.',
    'WI': 'Wis.',
    'WY': 'Wyo.',
    'Alabama': 'Ala.',
    'Alaska': 'Alaska',
    'Arizona': 'Ariz.',
    'Arkansas': 'Ark.',
    'California': 'Calif.',
    'Colorado': 'Colo.',
    'Connecticut': 'Conn.',
    'Delaware': 'Del.',
    'Florida': 'Fla.',
    'Georgia': 'Ga.',
    'Hawaii': 'Hawaii',
    'Idaho': 'Idaho',
    'Illinois': 'Ill.',
    'Indiana': 'Ind.',
    'Iowa': 'Iowa',
    'Kansas': 'Kan.',
    'Kentucky': 'Ky.',
    'Louisiana': 'La.',
    'Maine': 'Maine',
    'Maryland': 'Md.',
    'Massachusetts': 'Mass.',
    'Michigan': 'Mich.',
    'Minnesota': 'Minn.',
    'Mississippi': 'Miss.',
    'Missouri': 'Mo.',
    'Montana': 'Mont.',
    'Nebraska': 'Neb.',
    'Nevada': 'Nev.',
    'New Hampshire': 'N.H.',
    'New Jersey': 'N.J.',
    'New Mexico': 'N.M.',
    'New York': 'N.Y.',
    'North Carolina': 'N.C.',
    'North Dakota': 'N.D.',
    'Ohio': 'Ohio',
    'Oklahoma': 'Okla.',
    'Oregon': 'Ore.',
    'Pennsylvania': 'Pa.',
    'Rhode Island': 'R.I.',
    'South Carolina': 'S.C.',
    'South Dakota': 'S.D.',
    'Tennessee': 'Tenn.',
    'Texas': 'Tex.',
    'Utah': 'Utah',
    'Vermont': 'Vt.',
    'Virginia': 'Va.',
    'Washington': 'Wash.',
    'West Virginia': 'W.Va.',
    'Wisconsin': 'Wis.',
    'Wyoming': 'Wyo.'
}


def state_abbr(df, columns=None):
    """
    Replace state abbreviations or full state names in specified columns of a pandas DataFrame with AP style abbreviations.

    Args:
        df (pandas.DataFrame): The DataFrame containing state abbreviations or full state names to be replaced.
        columns (list or None): A list of column names to parse. If None, all string columns are processed.

    Returns:
        pandas.DataFrame: A new DataFrame with state abbreviations replaced by AP style abbreviations.
    """
    
    # Create a copy of the input DataFrame to avoid modifying the original
    cleaned_df = df.copy()
    
    if columns is None:
        columns_to_process = cleaned_df.select_dtypes(include='object').columns
    else:
        columns_to_process = columns
    
    # iterate through the selected columns
    for column in columns_to_process:
        logging.info(f"Processing column: {column}")
        
        for state_key, ap_style_abbr in STATE_ABBREVIATIONS.items():
            
            cleaned_df[column] = cleaned_df[column].str.replace(
                r'\b' + state_key + r'\b|\b' + ap_style_abbr.lower() + r'\b',
                ap_style_abbr,
                case=False,  # case-insensitive replacement
                regex=True  
            )
        
        cleaned_df[column] = cleaned_df[column].str.strip()
    
    return cleaned_df
