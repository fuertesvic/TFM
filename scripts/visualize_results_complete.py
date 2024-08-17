### Plots the results for the feature importances, i.e the metric Evaluation
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

def normalize_row(row):
    """Normalizes the values of row between 1 and 0"""
    norm_row = []
    maxval = max(row)
    for el in row:
        norm_row.append(el/maxval)
    return norm_row

def norm_df(df):
    """Normalizes the whole dataframe, and also reduces its numerical precision"""
    df = round(df,2)
    for index, row in df.iterrows():
        row = normalize_row(row)
        df.loc[index] = row
    return df

def preprocess_files(df):
    
    RLs = ["btc","clc","compression","cs","eh","llm","lorawan",
           "mems","oppnet","privacy","qtmmech","relgraph","smartcit",
           "smartcontract","smartind","socpsych","stgn"]
    
    df = df.drop(['nodeID','Year'],axis=1)
    df = norm_df(df)
    df.insert(0,'RL',RLs)
    return df

def plot_df(df,imp_type):
    """Bar plot with the different metric importances for all RL's"""
    # Extracting data
    RLs = df['RL']
    variables = gain_df.columns[1:]  # exclude the 'Research Line' column
    n_categories = len(RLs)
    n_vars = len(variables)

    # Bar width and positions
    bar_width = 0.1
    x = np.arange(n_categories)
    offsets = np.arange(n_vars) * bar_width

    # Plotting
    fig, ax = plt.subplots(figsize=(12,4))

    for i, var in enumerate(variables):
        ax.bar(x + offsets[i], df[var], bar_width, label=var)

    # Customizing the plot
    ax.set_xticks(x + bar_width * (n_vars - 1) / 2)
    plt.xticks(rotation=45, ha="right")
    ax.set_xticklabels(RLs)

    ax.set_xlabel('RLs')
    ax.set_ylabel(f'Normalized {imp_type}')
    ax.set_title('Feature Importance on Predicting the Evolution of the Dynamic Graph')
    ax.legend()
    plt.show()

def boxplot_df(df,imp_type):
    """Does a boxplot of the metrics importance for all RL's"""
    metric_data = []
    for metric in df.columns[1:]:
        metric_data.append(df[metric].values)

    #sns.set(style="ticks")

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    fig, ax = plt.subplots(figsize=(8,6))

    meanprops    = dict(marker='o', markerfacecolor='red', markeredgecolor='black', markersize=8)
    boxprops     = dict(linestyle='-', linewidth=2, color='black')
    whiskerprops = dict(linestyle='-', linewidth=2, color='black')
    capprops     = dict(linestyle='-', linewidth=2, color='black')
    medianprops  = dict(linestyle='-', linewidth=2.5, color='yellow')

    ax.boxplot(metric_data, showmeans=True, meanprops=meanprops, boxprops=boxprops,
           whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops)


    ax.set_xticklabels(['SDcen','SClCoef','DBC','DG','DI','DClC','DClCen','DKatz'])
    ax.set_title(f"Feature Importance ({imp_type})  on describing the Evolution of the Network")
    ax.set_xlabel("Network Metrics")
    ax.set_ylabel(f"Normalized {imp_type}")
    plt.xticks(fontsize=10,rotation=45, ha="center")
    plt.grid()
    plt.ylim([0,1.05])
    #plt.show()
    plt.savefig(f"{imp_type}_complete.svg")

def calculate_significance(df):
    print(df.head())
    SDcen = df['SDcen'].values
    SClCoef = df['SClCoef'].values
    DBcen = df['DBcen'].values
    DG  = df['DG'].values
    DI  = df['DI'].values
    DClcoef = df['DClCoef'].values
    DClcen = df['DClcen'].values
    DKatz = df['DKatz'].values
    
    static_metrics = np.concatenate((SDcen,SClCoef))
    dynamic_metrics = np.concatenate((DBcen,DG,DI,DClcoef,DClcen,DKatz))
    t_stat,p_value = stats.ttest_ind(static_metrics,dynamic_metrics)
    #print(f"T stat: {t_stat}    P_value: {p_value}:")

    u_stat,p_value = stats.mannwhitneyu(static_metrics,dynamic_metrics)
    print(f"\nU stat: {u_stat}    P_value: {p_value}")
    # h_stat,p_value = stats.kruskal(SDC,SCC,DBC,DG,DI)
    # print(f"\nH stat: {h_stat}    P_value: {p_value}")

    # print(h_stat)
    # print(p_value)

if __name__ == '__main__':
    
    gain_df = preprocess_files(pd.read_csv('complete/FI_g'))
    weight_df = preprocess_files(pd.read_csv('complete/FI_w'))
    # plot_df(gain_df,'Gain')
    # plot_df(weight_df,'Weight')
    boxplot_df(gain_df,'Gain')
    boxplot_df(weight_df,'Weight')
    print("Significance Test (U test) for Gain:")
    calculate_significance(gain_df)
    print("Significance Test (U test) for Weight:")
    calculate_significance(weight_df)
    