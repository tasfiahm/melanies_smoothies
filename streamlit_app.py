# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    f"""Choose the fruits you want in your custom Smoothie!

    """
)



#option = st.selectbox(
 #   "What is your favorite fruit?",
  #  ("Banana", "Strawberry", "Peaches"),
#)

#st.write("Your favorite fruit is:", option)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on smoothie will be: ", name_on_order)



#session = get_active_session()
cnx = st.connection("snowflake") #adding snowflake session
session = cnx.session() #adding snowflake session
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Define options
#options = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]

# Create multiselect dropdown
ingredients_list  = st.multiselect("Choose up to 5 ingrenents:", my_dataframe, max_selections=5)

# Display selected options
if ingredients_list:
 #   st.write(ingredients_list)
  #  st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



