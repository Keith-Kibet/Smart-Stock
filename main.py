import streamlit as st
from streamlit_option_menu import option_menu
import Home
import News
import Comparison
import Prediction
import Risk
import Finances
import Technical_Indicators
import Login  # Import the login module
import chat

# Set page configuration once at the top of the main script
st.set_page_config(
    page_title="SMART FORESIGHT",
    layout="wide"
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
        # Show login page if not logged in
        if "logged_in" not in st.session_state or not st.session_state.logged_in:
            Login.main()
            return

        # Show logout button in sidebar
        with st.sidebar:
           # if st.button("Logout"):
             ##   st.session_state.logged_in = False
             #   st.rerun()  # Reload to show login page

            selected_page = option_menu(
                menu_title="Smart Foresight",
                options=['Home', 'News', 'Comparison', 'Risk', 'Finances', 'Technical Indicators', 'Prediction', 'Chat', 'Logout'],
                icons=['house-fill', 'newspaper', 'pie-chart', "shield-shaded", "currency-exchange", "card-checklist", 'graph-up-arrow', 'chat-dots', 'box-arrow-right'],
                menu_icon='menu-button-wide',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "#333"},
                    "icon": {"color": "white", "font-size": "13px"}, 
                    "nav-link": {"color": "white", "font-size": "13px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Display the selected page's content
        if selected_page == 'Home':
            Home.main()
        elif selected_page == 'News':
            News.main()
        elif selected_page == 'Comparison':
            Comparison.main()
        elif selected_page == 'Prediction':
            Prediction.main()
        elif selected_page == 'Risk':
            Risk.main()
        elif selected_page == 'Finances':
            Finances.main()
        elif selected_page == 'Technical Indicators':
            Technical_Indicators.main()
        elif selected_page == 'Chat':
            chat.main()
        elif selected_page == 'Logout':
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.run()
