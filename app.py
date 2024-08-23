import os
import streamlit as st
import google.generativeai as genai

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyD-3x7f8QbPDTfAhDJqSvDp2brTb44kawA'  # Replace with your actual API key
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Email Generator")

    # User input for email content description
    user_input = st.text_area(
        "Please describe the email content below (e.g., 'I need to write an email to my manager requesting leave')",
        height=200
    )

    # Button to generate email
    if st.button("Generate Email"):
        if user_input.strip():
            # Create a prompt for generating the email content
            prompt = f"""
            Based on the following description, please generate a professional email:

            "{user_input}"

            The email should include a recipient name, subject, main content, and a closing signature.
            """

            try:
                # Use the Gemini generative model to generate the email content
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                email_body = response.text

                # Store the generated email in the session state to keep it persistent
                st.session_state.generated_email = email_body
                st.session_state.copy_status = "Copy Email to Clipboard"  # Reset the copy button text

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("We couldn't generate the email. Please try again later.")
        else:
            st.warning("Please provide a description of the email content.")

    # Check if the generated email is in session state
    if 'generated_email' in st.session_state:
        st.subheader("Your Generated Email:")
        email_text_area = st.text_area("Generated Email:", st.session_state.generated_email, height=400, key="email_content")

        # Button to copy email to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Email to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var emailContent = document.querySelector('#email_content');
                    var range = document.createRange();
                    range.selectNode(emailContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
