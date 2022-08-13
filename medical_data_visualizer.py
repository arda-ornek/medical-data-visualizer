from click import style
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')
df = df.sort_values(by='cardio')
#print(df.info())
# Add 'overweight' column
df['overweight'] = 10
#print(df['overweight'].head())
for x in df.index:
    if ( (df.iloc[x,4]) / ((df.iloc[x,3]/100)*(df.iloc[x,3]/100)) ) > 25:
        df.iloc[x,13]=1
    else:
        df.iloc[x,13]=0

#print(df['overweight'].head())
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = df['cholesterol'].replace([1],0)
df['cholesterol'] = df['cholesterol'].replace([2,3],1)
df['gluc'] = df['gluc'].replace([1],0)
df['gluc'] = df['gluc'].replace([2,3],1)
# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    melted=pd.melt(df,id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight','smoke'])
    #print(melted)
    
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    grouped = melted.groupby(melted.cardio)
    melt1 = grouped.get_group(0)
    #print(melt1)
    melt2 = grouped.get_group(1)
    #print(melt2)
    # Draw the catplot with 'sns.catplot()'
    fig, axs = plt.subplots(1,2, figsize=(18,10))
    sns.countplot(x="variable",hue="value",data=melt1,ax=axs[0])
    sns.countplot(x="variable",hue="value",data=melt2,ax=axs[1])
    


    
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    cleaned=df.copy()
    #print(len(cleaned))
    for y in df.index:
        if ((df.iloc[y,6]) > (df.iloc[y,5])) or ((df.iloc[y,3]) < (df['height'].quantile(0.025))) or ((df.iloc[y,3]) > (df['height'].quantile(0.975))) or ((df.iloc[y,4]) < (df['weight'].quantile(0.025))) or ((df.iloc[y,4]) > (df['weight'].quantile(0.975))):
            cleaned.drop(df.index[y],inplace=True)

    #print(len(cleaned))
    df_heat = None

    # Calculate the correlation matrix
    cleaned = cleaned.astype({"id": float,"age": float,"sex": float,"height": float,"ap_hi": float,"ap_lo": float,"cholesterol": float,"gluc": float,"smoke": float,"alco": float,"active": float,"cardio": float,"overweight": float})
    #print(cleaned.info())
    corr = cleaned.corr()
    
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(18,10))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, mask=mask,vmin=-0.08,vmax=0.24,annot=True, linecolor="w", linewidths=1,fmt='.1f')


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
