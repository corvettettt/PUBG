import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random as r

kills = pd.read_csv('deaths/kill_match_stats_final_0.csv')
kills = kills.dropna(axis = 0, how = "any")
kills["kill_distance"] = ((kills["killer_position_x"] - kills["victim_position_x"]) ** 2 + (kills["killer_position_y"] - kills["victim_position_y"]) ** 2) ** (1/2)
kills["place_diff"] = kills["victim_placement"] - kills["killer_placement"]
winners = dict(kills[kills["killer_placement"] == 1][["killer_name", "match_id"]].groupby("match_id").size())
kills["winner_kills"] = kills["match_id"].map(winners, kills["match_id"])

def remove_outliers(kills, var):
    lower_bound = np.quantile(kills[var], 0.25) - (1.5 * (np.quantile(kills[var], 0.75) - np.quantile(kills[var], 0.25)))
    upper_bound = np.quantile(kills[var], 0.75) + (1.5 * (np.quantile(kills[var], 0.75) - np.quantile(kills[var], 0.25)))
    kills = kills[(kills[var] >= lower_bound) & (kills[var] <= upper_bound)]
    return kills



def distribution_cont(kills, var):
    if var == "kill_distance":
        kills = remove_outliers(kills, var)
    plt.hist(kills[var])
    plt.axvline(x = np.mean(kills[var]), c = "r")
    plt.text(0.7, 0.9, f"Mean: {round(np.mean(kills[var]), 2)}", transform = plt.gca().transAxes)
    plt.xlabel(f"{var}")
    plt.ylabel("Count")
    plt.title(f"Distribution of {var}")
    plt.show()
    
def basic_plot(kills, var):
    if var == "killed_by":
        grouped = kills.groupby(var).size().sort_values(ascending = False).head(10)
        plt.xticks(rotation = 90)
    else:
        grouped = kills.groupby(var).size().sort_values(ascending = False)
    plt.bar(grouped.index.values, grouped.values)
    plt.title(f"{var} Distribution")
    plt.show()

def prop_list(lst):
    weapons = list(lst)
    weapon_props = []
    distinct_weapons = list(set(weapons))
    for i in distinct_weapons:
        counter = 0
        for j in weapons:
            if i == j:
                counter += 1
        weapon_props.append(counter / len(weapons))
    return dict(zip(distinct_weapons, weapon_props))
distances["weapon_prop"] = distances["killed_by"].map(prop_list(distances["killed_by"]), distances["killed_by"])
def get_weapons_range(distances, perc_low, perc_high):
    lower_quantile = np.quantile(distances["kill_distance"], perc_low)
    upper_quantile = np.quantile(distances["kill_distance"], perc_high)
    distances2 = distances[(distances["kill_distance"] >= lower_quantile) & (distances["kill_distance"] <= upper_quantile)]

    weapon_counts = distances2.groupby("killed_by").size().sort_values(ascending = False).head(10)

    distances2["weapon_prop_filtered"] = distances2["killed_by"].map(prop_list(distances2["killed_by"]), distances2["killed_by"])
    distances2["conditional_prob"] = (distances2["weapon_prop_filtered"] - distances2["weapon_prop"])
    distinct_props = distances2[["killed_by", "conditional_prob"]].drop_duplicates().sort_values(by = "conditional_prob", ascending = False).head(10)

    plt.subplots(figsize = (10,6))
    plt.subplot(1,2,1)
    sns.barplot(weapon_counts.index.values, weapon_counts.values)
    plt.xticks(rotation = 90)
    plt.title(f"By Frequency ({perc_low} to {perc_high} Percentile)")
    plt.subplot(1,2,2)
    sns.barplot(distinct_props["killed_by"], distinct_props["conditional_prob"])
    plt.xticks(rotation = 90)
    plt.title(f"By Proportion Diff ({perc_low} to {perc_high} Percentile)")
    plt.xlabel(None)
    plt.ylabel(None)
    plt.show()

erangel = kills[kills["map"] == "ERANGEL"]
erangel_sample = erangel.sample(n = 1000, random_state = 1)
img = plt.imread("erangel.jpg")
plt.subplots(figsize = (12,12))
plt.imshow(img,aspect='auto', extent=[0, 800000, 0, 800000])
plt.scatter(erangel_sample["killer_position_x"], erangel_sample["killer_position_y"], c = "r", s = 100)
plt.legend(["Killer"], loc = "upper right")
plt.show()

miramar = kills[kills["map"] == "MIRAMAR"]
miramar_sample = miramar.sample(n = 1000, random_state = 1)
img = plt.imread("miramar.jpg")
plt.subplots(figsize = (12,12))
plt.imshow(img, aspect='auto', extent=[0, 800000, 0, 800000])
plt.scatter(miramar_sample["killer_position_x"], miramar_sample["killer_position_y"], c = "r", s = 100)
plt.legend(["Killer"], loc = "upper right")
plt.show()


get_weapons_range(distances, 0, 0.1)

