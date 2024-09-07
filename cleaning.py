import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
url = 'https://www.sharkattackfile.net/spreadsheets/GSAF5.xls'

df = pd.read_excel(url)


# Load the DataFrame from URL
url = 'https://www.sharkattackfile.net/spreadsheets/GSAF5.xls'
df = pd.read_excel(url)



def delete_columns(df):
    """
    Function to delete unnecessary columns from a DataFrame.
    The columns to be deleted are specified in the list passed to the drop method.
    The drop method returns a new DataFrame without that columns.
    """
    df_dropped_multiple = df.drop(['Year', 'Type', 'Location', 'Name', 'Sex', 'Age', 'Injury',
                                   'Unnamed: 11', 'Time', 'Species ', 'Source', 'pdf', 'href formula',
                                   'href', 'Case Number', 'Case Number.1', 'original order',
                                   'Unnamed: 21', 'Unnamed: 22'], axis=1)
    return df_dropped_multiple



def clean_data(df):
    """
    Function to standarize column names and remove duplicates and missing values.
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.drop_duplicates(inplace=True)
    df = df.dropna()
    return df




def remove_prefix(date):
    """
    This function removes the prefix "Reported " from a given date string, if present.
    Takes a string as argument and return the string without "Reported " or the original string if it doesn't start with "Reported ".
    """
    if isinstance(date, str) and date.startswith("Reported "):
        return date[len("Reported "):]
    return date



def fix_format_date(date):
    """
    This function fixes the format of a given date string.
    Takes a string as argument and return the string in the format "dd-mm-yyyy" if it is in a date format, or None if it is not.
    """
    if isinstance(date, str):
        try:
            correct_date_format = pd.to_datetime(date, format='%d-%b-%Y', errors='coerce')
            return correct_date_format.strftime('%d-%m-%Y') if correct_date_format else None
        except ValueError:
            return None
    return None



def filter_date(df):
    """
    This function filters the DataFrame to include only attacks after 2000-01-01.
    Takes a DataFrame as argument and return a new DataFrame with only attacks after 2000-01-01.
    """
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_filtered = df[df['date'] >= pd.to_datetime('2000-01-01')]
    return df_filtered



def get_mode_of_attacks(df):
    """
    Function to calculate the most common values for the columns specified in the dataframe.
    Returns a dictionary with the mode for each column.
    """
    moda_country = df['country'].mode()[0]
    moda_state = df['state'].mode()[0]
    moda_activity = df['activity'].mode()[0]

    return {
        'most_attacked_country': moda_country,
        'most_attacked_state': moda_state,
        'most_common_activity': moda_activity
    }




def top_country_state_activity(df, n=10):
    """
    Function to calculate the top (default 10) combinations of 'country', 'state' and 'activity' that have the most attacks.
    Takes a DataFrame and an integer n as arguments.
    Group the data by these columns, count the occurrences, and print the top n combinations
    """
    country_state_activity = df.groupby(['country', 'state', 'activity']).size().sort_values(ascending=False).head(n)
    print(f"Top {n} combinaciones país-estado-actividad más frecuentes:")
    return country_state_activity



def plot_top_countries_attacks(df_filtered, top_n=10):
    """
    Function that groups attacks by country, 
    and generates a bar graph with the main affected countries.
    
    Parameters:
    df_filtered (DataFrame): Filtered and cleaned DataFrame.
    top_n (int): Number of countries to display in the chart. By default it is 10.
    """
    
    # Count the number of attacks per country
    attacks_per_country = df_filtered.groupby('country').size().reset_index(name='count')

    # Get the top countries with the most attacks
    top_countries = attacks_per_country.sort_values(by='count', ascending=False).head(top_n)
    
    # Create the bar chart
    plt.figure(figsize=(14, 8))
    bars = plt.bar(top_countries['country'], top_countries['count'], color='lightblue')

    # Add numbers inside the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center', color='black')

    # Chart settings
    plt.xlabel('Country')
    plt.ylabel('Number of Attacks')
    plt.title(f'Top {top_n} Countries with the Most Shark Attacks (from 2000)')
    plt.gca().invert_xaxis()  # Invertir el eje X para que el país con más ataques esté al principio
    plt.tight_layout()

    # Show the graph
    return plt.show()



def plot_top_activties (df_filtered):
    """
    Function that groups attacks by activities,
    and generates a bar graph with the 7 most common
    activities when the attacks occurred.
    
    Parameters:
    df_filtered (DataFrame): Filtered and cleaned DataFrame.
    """

    attacks_per_activity = df_filtered.groupby('activity').size().reset_index(name='count')

    # Sort the activities by the number of attacks in descending order and select the first 7
    top_7_activities = attacks_per_activity.sort_values(by='count', ascending=False).head(7)

    # Create a bar graph with the 7 activities with the most attacks
    plt.figure(figsize=(14, 8))
    bars = plt.bar(top_7_activities['activity'], top_7_activities['count'], color='lightblue')

    # Add the numbers inside the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center', color='black')
    
    # Chart settings
    plt.xlabel('Activity')
    plt.ylabel('Number of Attacks')
    plt.title('Top 5 Activities with the Most Shark Attacks (from 2000)')
    plt.xticks(rotation=45, ha='right')  # Rotar las etiquetas para mejor legibilidad
    plt.tight_layout()

    # Mostrar el gráfico
    return plt.show()



def plot_attacks_per_month(df_filtered):
    """
    Funtion that groups attacks by month and generates a
    bar graph with the attacks per month.
    Parameters: the filtered DataFrame
    """

    # Extract the month from the 'date' column
    df['month'] = df_filtered['date'].dt.month

    # Group by month and count attacks
    attacks_per_month = df.groupby('month').size().reset_index(name='count')

    # Create a bar chart of attacks by month
    plt.figure(figsize=(14, 8))
    bars = plt.bar(attacks_per_month['month'], attacks_per_month['count'], color='lightblue')

    # Add the numbers inside the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center', color='black')

    # Chart settings
    plt.xlabel('Month')
    plt.ylabel('Number of Attacks')
    plt.title('Total Number of Shark Attacks by Month (From 2000)')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    # Mostrar el gráfico
    plt.tight_layout()
    return plt.show()



def plot_top_states_activities(df_filtered):
    """
    Function that groups attacks by states and activities,
    and generates a bar graph with the top 5 combination of
    states and activities with the most attacks.
    Parameters: the filtered DataFrame
    """

    # Select the states with the most attacks
    top_states = df_filtered['state'].value_counts().head(5).index
    # Filter by those states
    filtered_data = df_filtered[df_filtered['state'].isin(top_states)]
    # Select the activities with the most attacks
    top_activities = df_filtered['activity'].value_counts().head(5).index
    # Filter by those activities
    filtered_data = df_filtered[df_filtered['activity'].isin(top_activities)]
    
    # Create the stacked bar chart
    plt.figure(figsize=(14, 8))
    barplot = sns.countplot(data=filtered_data, x='state', hue='activity', order=top_states)

    # Add the numbers on the bars
    for p in barplot.patches:
        height = p.get_height()
        if height > 0:  # Only add text if height is greater than zero
            barplot.text(p.get_x() + p.get_width() / 2, height + 0.1, int(height), ha="center")

    # Adjust the graph
    plt.title('Frecuencia de actividades por estado (Top 5 estados)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.show()



def plot_top_states(df_filtered):
    """
    Function that groups attacks by states and generates a
    bar graph with the top 10 states with the most attacks.
    Parameters: the filtered DataFrame
    """
    
    # Separate the data by states and count how many attacks occurred in each one
    attacks_per_state = df_filtered.groupby('state').size().reset_index(name='count')

    # Get the 10 states/provinces with the most attacks
    top_10_states = attacks_per_state.sort_values(by='count', ascending=False).head(10)

    # Create the bar chart
    plt.figure(figsize=(14, 8))
    bars = plt.bar(top_10_states['state'], top_10_states['count'], color='lightblue')

    # Add the numbers inside the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center', color='black')

    # Chart settings
    plt.xlabel('State/Province')
    plt.ylabel('Number of Attacks')
    plt.title('Top 10 States/Provinces with Most Shark Attacks (From 2020)')
    plt.tight_layout()
    return plt.show()