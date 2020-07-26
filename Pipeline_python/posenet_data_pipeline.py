import pandas as pd
import matplotlib.pyplot as plt

calm_csv = "../Pose_class_data/pose_class_0_calm_cleaned.csv"
happy_csv = "../Pose_class_data/pose_class_1_happy_cleaned.csv"
threat_csv = "../Pose_class_data/pose_class_2_threatening_cleaned.csv"

def label_from_pid_coord(point_id, coord):
    return "{}{}".format(point_id, coord)

def df_from_cleaned_csv(ccsv_path):
    csv_df = pd.read_csv(ccsv_path)

    # Pandas seems to be row-major by default, so functions like
    # DataFrame.describe() seems to expect that sort of format
    # Swap the rows and columns, cut off the first three rows, and
    # drop the last column (NaN)
    new_df = csv_df.transpose()[3:]
    del new_df[35]

    # 'Squish' together the point id with the coordinate to have 
    # a single column label for each set of data
    col_names = [label_from_pid_coord(point_id, coord) for point_id in range(17) for coord in ['X','Y']]
    col_names.append('Time Elapsed')
    rename_dict = {}
    for i in range(len(col_names)):
        rename_dict[i] = col_names[i]

    # Rename the column indicies of the modified csv Dataframe to
    # their corresponding 'squished' column labels
    new_df = new_df.rename(columns=rename_dict)

    # Convert datatype to float64 before returning
    return new_df.astype(float)

calm_df = df_from_cleaned_csv(calm_csv)    
happy_df = df_from_cleaned_csv(happy_csv)    
threat_df = df_from_cleaned_csv(threat_csv)    

print("========== CALM DATA ==========")
print(calm_df.describe())

print("\n========== HAPPY ==========")
print(happy_df.describe())

print("\n========== THREATENING ==========")
print(threat_df.describe())
