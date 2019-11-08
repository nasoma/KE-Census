import pandas as pd
import streamlit as st


@st.cache()
def population_voter_analysis():
    df = pd.read_csv('county_list.csv').set_index('COUNTY').drop(['code', 'MALE', 'FEMALE', 'INTERSEX'], axis=1)
    percentage_of_voters = df['VOTERS'] / df["TOTAL"] * 100
    df.insert(0, "% Voters", percentage_of_voters)

    highest_voters_percentage = df.sort_values(by=['% Voters'], ascending=False).rename(
        columns={'TOTAL': 'TOTAL POPULATION', 'VOTERS': 'REGISTERED VOTERS'}).head(10)

    lowest_voters_percentage = df.sort_values(by=['% Voters'], ascending=True).rename(
        columns={'TOTAL': 'TOTAL POPULATION', 'VOTERS': 'REGISTERED VOTERS'}).head(10)
    return highest_voters_percentage, lowest_voters_percentage


@st.cache()
def gender_ratios():
    df = pd.read_csv('county_list.csv')
    male_to_female = df['MALE'] / df['FEMALE']
    df.insert(1, "Male To Female Ratio", male_to_female)
    m_f = df.sort_values(by=['Male To Female Ratio'], ascending=False).drop(['code', 'VOTERS', 'INTERSEX'
                                                                             ], axis=1).set_index('COUNTY').head(10)
    female_to_male = df['FEMALE'] / df['MALE']
    df.insert(1, "Female To Male Ratio", female_to_male)
    f_m = df.sort_values(by=['Female To Male Ratio'], ascending=False).drop(['code', 'VOTERS', 'INTERSEX',
                                                                             'Male To Female Ratio'], axis=1).set_index(
        'COUNTY').head(10)
    top_population = df.sort_values(by=['TOTAL'], ascending=False).drop(['code', 'VOTERS',
                                                                         'Female To Male Ratio',
                                                                         'Male To Female Ratio'], axis=1).set_index(
        'COUNTY').head(10)
    least_population = df.sort_values(by=['TOTAL'], ascending=False).drop(['code', 'VOTERS',
                                                                           'Female To Male Ratio',
                                                                           'Male To Female Ratio'], axis=1).set_index(
        'COUNTY').tail(10)

    return m_f, f_m, top_population, least_population
