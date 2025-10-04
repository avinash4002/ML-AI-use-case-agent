import streamlit as st
import utils

st.set_page_config(layout="wide")

st.title("AI/ML Research Agent for Business Growth 🚀")

st.markdown("""
This agent helps you discover AI/ML use cases to accelerate your company's growth. 
Enter a company name, and the agent will generate a report with:
- A company overview.
- Top 5 AI/ML use case recommendations with implementation steps.
- Relevant datasets, GitHub repositories, and research papers.
""")

company_name = st.text_input("Enter the company name:", "Google")

if st.button("Generate Report"):
    if company_name:
        with st.spinner("Conducting research and building your report... This may take a moment."):
            try:
                # This function now correctly unpacks the expected 3 return values
                pdf_bytes, pdf_filename, error_message = utils.process_company_request(company_name)

                if error_message:
                    # If an error occurred, display it directly in the UI
                    st.error(error_message)
                elif pdf_bytes:
                    # If successful, show the success message and download button
                    st.success("Report Generated Successfully!")
                    
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                else:
                    # A fallback for any unexpected case where there's no PDF and no error
                    st.error("An unknown error occurred while generating the report.")

            except Exception as e:
                # This will catch any other unexpected errors in the application
                st.error(f"An unexpected application error occurred: {e}")
    else:
        st.warning("Please enter a company name.")

