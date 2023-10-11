import streamlit as st
import pandas as pd
import numpy as np

# st.title('Uber pickups in NYC')

def main():
    # Create two smaller boxes on the right
    col1, col2 = st.columns(2)

    # Top box on the right (takes most of the height)
    with col1:
        st.title("Top Box on the Right")
        st.write("This box takes most of the height.")
        st.write("You can add more content here.")
 
    # Bottom box on the right (takes one line for input)
    with col2:
        st.title("Bottom Box on the Right")
        user_input = st.text_input("Enter your chat here:", "")

        if user_input:
            st.write(f"User: {user_input}")
            # Here, you can add your chatbot logic to generate responses and display them.

if __name__ == "__main__":
    main()
