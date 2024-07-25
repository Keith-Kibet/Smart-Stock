import streamlit as st
from streamlit_option_menu import option_menu
import Home
import News
import Comparison
import Prediction
import Risk
import Finances
import Technical_Indicators

# Set page configuration once at the top of the main script
st.set_page_config(
    page_title="SMART FORESIGHT",
    layout="wide"  # Optional: You can specify layout as 'wide' if needed
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        # Use st.sidebar for navigation menu only
        with st.sidebar:
            app = option_menu(
                menu_title="Smart Foresight",
                options=['Home', 'News', 'Comparison', 'Prediction', 'Risk', 'Finances', 'Technical Indicators'],
                icons=['house-fill', 'newspaper', 'columns-gap', 'graph-up-arrow', 'shield-shaded', 'currency-exchange', 'card-checklist'],
                menu_icon='menu-button-wide',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "#333"},
                    "icon": {"color": "white", "font-size": "12px"}, 
                    "nav-link": {"color": "white", "font-size": "12px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
            
        # Display the selected page
        if app == 'Home':
            Home.main()
        elif app == 'News':
            News.main()
        elif app == 'Comparison':
            Comparison.main()
        elif app == 'Prediction':
            Prediction.main()
        elif app == 'Risk':
            Risk.main()
        elif app == 'Finances':
            Finances.main()
        elif app == 'Technical Indicators':
            Technical_Indicators.main()

if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.run()
