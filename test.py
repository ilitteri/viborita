import re
import numpy as np
import pandas as pd

def create_title_array(file):
    array = file.values[:, 0]
    arrayLength = array.shape[0]
    return array

def filter_data(array):
    seriesList = []
    moviesList = []
    shitList = []
    for titleData in array:
        if len(titleData.split(":")) >= 3:
            seriesList.append(titleData.split(":"))
        elif len(titleData.split(":")) < 3:
            moviesList.append(titleData.split(":"))
        else:
            shitList.append(titleData.split(":"))
    return seriesList, moviesList, shitList

def create_dataframe(list):
    DataFrame = pd.DataFrame(list)
    return DataFrame
    
def sort_data(array):
    sortData = lambda l: sorted(list(set(list(zip(*l))[0])))
    seriesData, moviesData, shitData = filter_data(array)
    sorted_series = sortData(seriesData)
    sorted_movies = sortData(moviesData)
    return sorted_series, sorted_movies

def create_csv(file):
    titleArray = create_title_array(file)
    seriesNames, moviesNames = sort_data(titleArray)
    dataframe1, dataframe2 = create_dataframe(seriesNames), create_dataframe(moviesNames)
    dataframe1.to_csv(r"Series", index=False, header=True)
    dataframe2.to_csv(r"Movies", index=False, header=True)

def func(par1, par2):
    return

ivan_file = pd.read_csv("IvanNetflixViewingHistory.csv")
santi_file = pd.read_csv("SantiNetflixViewingHistory.csv")
vicky_file = pd.read_csv("VickyNetflixViewingHistory.csv")
lucho_file = pd.read_csv("LuchoNetflix.csv")

create_csv(ivan_file)

#messi sabe bastante
