#!/usr/bin/env python
# coding: utf-8

# ## # Introduction
# <p><img src="https://assets.datacamp.com/production/project_981/img/lego_unsplash.jpg" alt="A picture of Lego characters!"></p>
# <h3 id="letslookatlegosets">Let's look at Lego sets!</h3>
# <p>Lego is a household name across the world, supported by a diverse toy line, hit movies, and a series of successful video games. In this project, we are going to explore a key development in the history of Lego: the introduction of licensed sets such as Star Wars, Super Heroes, and Harry Potter.</p>
# <p>It may not be widely known, but Lego has had its share of ups and downs since its inception in the early 20th century. This includes a particularly rough period in the late 90s. As described in <a href="https://www.businessinsider.com/how-lego-made-a-huge-turnaround-2014-2?r=US&IR=T">this article</a>, Lego was only able to survive due to a successful internal brand (Bionicle) and the introduction of its first licensed series: Star Wars. In the instructions panel are the two questions you will need to answer to complete this project.</p>
# <p>Before diving into our analysis though, let's become familiar with the two datasets that will help you with this project:<br><br></p>
# <div style="background-color: #ebf4f7; color: #595959; text-align:left; vertical-align: middle; padding: 15px 25px 15px 25px; line-height: 1.6;">
#     <div style="font-size:20px"><b>datasets/lego_sets.csv</b></div>
# <ul>
#     <li><b>set_num:</b> A code that is unique to each set in the dataset. <b><i>This column is critical, and a missing value indicates the set is a duplicate or invalid!</i></b></li>
#     <li><b>set_name:</b> A name for every set in the dataset (note that this can be the same for different sets).</li>
#     <li><b>year:</b> The date the set was released.</li>
#     <li><b>num_parts:</b> The number of parts contained in the set.<b><i> This column is not central to our analyses, so missing values are acceptable.</i></b></li>
#         <li><b>theme_name:</b> The name of the sub-theme of the set.</li>
#     <li><b>parent_theme:</b> The name of the parent theme the set belongs to. Matches the `name` column of the `parent_themes` csv file.</li>
# </ul>
# 
# <div style="font-size:20px"><b>datasets/parent_themes.csv</b></div>
# <ul>
#     <li><b>id:</b> A code that is unique to every theme.</li>
#     <li><b>name:</b> The name of the parent theme.</li>
#     <li><b>is_licensed:</b> A Boolean column specifying whether the theme is a licensed theme.</li>
# </ul>
#     </div>
# <p>From here on out, it will be your task to explore and manipulate the existing data until you are able to answer the two questions described in the instructions panel. Feel free to add as many cells as necessary. Finally, remember that you are only tested on your answer, not on the methods you use to arrive at the answer!</p>
# <p><em><strong>Note:</strong> If you haven't completed a DataCamp project before you should check out the <a href="https://projects.datacamp.com/projects/33">Intro to Projects</a> first to learn about the interface. In this project, you also need to know your way around <code>pandas</code> DataFrames and it's recommended that you take a look at the course <a href="https://www.datacamp.com/courses/data-manipulation-with-pandas">Data Manipulation with pandas</a>.</em></p>

# In[35]:


# Import the relevant modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the csv datasets as pandas dataframes
lego_sets = pd.read_csv("datasets/lego_sets.csv")
parent_themes = pd.read_csv("datasets/parent_themes.csv")


# In[36]:


# Display the head, info, and description of lego_sets
display(lego_sets.head())
lego_sets.info()

# Remove duplicates and check info
lego_sets = lego_sets.drop_duplicates(subset = ["set_num"])
lego_sets.info()

# Remove null values and check info
lego_sets = lego_sets.dropna(subset = ["set_num"])
lego_sets.info()


# In[37]:


#Display the head and info of parent_themes dataset
display(parent_themes.head())
display(parent_themes.info())


# In[42]:


# subset parent_themes to find the themes that are licensed
licensed_themes = parent_themes[parent_themes["is_licensed"] == True] 

# extract the names of all licensed themes
licensed_theme_names = licensed_themes["name"]

# select rows of lego_sets that are licensed themes
lego_sets = lego_sets.loc[lego_sets["parent_theme"].isin(licensed_theme_names)]

# find total number of licensed Star Wars themed releases by subsetting lego_sets 
Total_SW_Releases = len(lego_sets[lego_sets["parent_theme"] == "Star Wars"])

# find total number of licensed theme releases
Total_Releases = len(lego_sets["parent_theme"])

# find percentage of all licensed releases that were Star Wars themed
the_force = int((Total_SW_Releases / Total_Releases) * 100)

# display the_force 
the_force


# In[39]:


# group the licensed sets by year and parent_theme
lego_sets_by_year = lego_sets.groupby(["year", "parent_theme"])

# count the number of unique parent_themes released every year and reset the index 
theme_counts = lego_sets_by_year.size().reset_index(name="counts")

# group counts df by year and find the idx of the maximum counts, then compare with original counts df to get true/false series
idx = theme_counts.groupby("year")["counts"].transform(max) == theme_counts["counts"]

# subset the original counts df with the idx of the maximum counts and assign to new max_counts df
max_theme_counts = theme_counts[idx]

# display max_theme_counts
display(max_theme_counts)


# In[40]:


# iterrate through rows of max_theme_counts to find the year where Star Wars was not the most popular theme
not_SW_year = [row[0] for index, row in max_theme_counts.iterrows() if "Star Wars" not in row[1]] 

# assign this year to new_era and convert to integer
new_era = int(not_SW_year[0])

# display the year
new_era


# In[41]:


get_ipython().run_cell_magic('nose', '', '\ndef test_force():\n    assert(int(the_force) != 45), \\\n        "Have you properly inspected your data and dealt with missing values appropriately?"\n    assert(int(the_force) != 50), \\\n        "Have you dropped the relevant missing rows? Remember, not all rows with missing values need to be dropped!"\n    assert int(the_force) == 51 or int(the_force) == 52, \\\n        "Have you correctly calculated the percentage of licensed sets that belonged to the Star Wars theme?"\n\ndef test_new_era():\n    assert((type(new_era)==int) & (len(str(new_era))==4)), \\\n        "Have you entered the year in which Star Wars was not the most popular theme as a four digit integer?"\n    assert int(new_era) == 2017, \\\n        "Have you correctly calculated the year in which Star Wars was no longer the most popular set?"')

