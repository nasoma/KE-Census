import plotly.graph_objects as go
import locale
from analysis import *

locale.setlocale(locale.LC_ALL, 'en_US.utf8')

voter_percentages = population_voter_analysis()
male_female_ratios = gender_ratios()

st.sidebar.markdown('#### Kenya 2019 Population Census Summary')

df = pd.read_csv('county_list.csv')


#or read_and_cache_csv = st.cache(pd.read_csv) then
#df = read_and_cache_csv("filename.csv")
#see implementation in analysis.py


counties = st.sidebar.selectbox('Select county', df['COUNTY'], index=29)
registered_voters = st.sidebar.checkbox("Compare With Voter Registration Data, (IEBC 2017)")

st.sidebar.markdown(' #### 📈  Parts Of Tens')
remittances_data_file = st.sidebar.file_uploader(label="Upload File")

parts_of_tens = st.sidebar.selectbox('', ('Select Option...', '10 Most Populous Counties', '10 Least Populous Counties',
                                            'Highest Male To Female Ratio', 'Highest Female To Male Ratio',
                                            'Highest % Of Registered Voters', 'Lowest % Of Registered Voters'))

if remittances_data_file is not None:
    remittances_data = pd.read_csv(remittances_data_file)
    st.write(remittances_data)

if '10 Most Populous Counties' in parts_of_tens:
    st.subheader('10 Most Populous Counties')
    st.table(male_female_ratios[2])
elif '10 Least Populous Counties' in parts_of_tens:
    st.subheader('10 Least Populous Counties')
    st.table(male_female_ratios[3])
elif 'Highest Male To Female Ratio' in parts_of_tens:
    st.subheader('Highest Male To Female ratio')
    st.table(male_female_ratios[0])
elif 'Highest Female To Male Ratio' in parts_of_tens:
    st.subheader('Highest Female To Male Ratio')
    st.table(male_female_ratios[1])
elif 'Highest % Of Registered Voters' in parts_of_tens:
    st.subheader('Highest % Of Registered Voters')
    st.table(voter_percentages[0])
elif 'Lowest % Of Registered Voters' in parts_of_tens:
    st.subheader('Lowest % Of Registered Voters')
    st.table(voter_percentages[1])
else:
    county_data = df.loc[df.COUNTY == counties]
    total = county_data['TOTAL'].values[0]
    voters = county_data['VOTERS'].values[0]
    male = county_data['MALE'].values[0]
    female = county_data['FEMALE'].values[0]
    intersex = county_data['INTERSEX'].values[0]

    st.subheader(counties + " County, Total Population: " + locale.format_string("%d", total, grouping=True))

    st.text("Male: " + locale.format_string("%d", male, grouping=True))
    st.text("Female: " + locale.format_string("%d", female, grouping=True))
    st.text("Intersex: " + locale.format_string("%d", intersex, grouping=True))

    if registered_voters:
        '''
        ### Voter Registration
        '''
        st.text('Total Voters: ' + locale.format_string("%d", voters, grouping=True))
        voters_percentage = (voters / total) * 100

        st.text("% of voters: " + str(round(voters_percentage, 2)))
        hover_text = "% of voters: " + str(round(voters_percentage, 2))
        voters_vs_pop = ['Population', 'Voters']
        colors = ['burlywood', 'chocolate']
        fig = go.Figure(data=[
        go.Bar(x=voters_vs_pop, y=[total, voters], hovertext=['', hover_text], marker_color=colors)])
        fig.update_layout(title_text='Population Against No. Of Registered Voters')
        st.plotly_chart(fig)
    else:
        labels = ['Male', 'Female']
        values = [male, female]
        colors = ['burlywood', 'chocolate']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#F5F5DC', width=1)))
        st.plotly_chart(fig)

st.sidebar.markdown(' #### About')
st.sidebar.info("This app uses data that is publicly available. It is not affiliated to IEBC or KNBS.")
st.sidebar.info("Email: tazamadata@gmail.com")

















