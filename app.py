import streamlit as st
import utils

st.set_page_config(layout="wide")

st.title("AI/ML Research Agent for Business Growth 🚀")

st.markdown("""
Enter a company name, and the agent will conduct research to generate a report containing:
- A company overview.
- Top 5 AI/ML use case recommendations with implementation steps.
- Links to relevant datasets, GitHub repositories, and research papers.
""")

company_name = st.text_input("Enter the company name:", "Nvidia")

if st.button("Generate Report"):
    if company_name:
        with st.spinner("Conducting research and building your report... This may take a moment."):
            try:
                # Unpack all the data returned from the main processing function
                overview, use_cases, pdf_bytes, pdf_filename, error = utils.process_company_request(company_name)

                if error:
                    st.error(f"An error occurred: {error}")
                
                elif overview and use_cases:
                    st.success("Report Generated Successfully!")

                    # --- Display the full report in the Streamlit UI ---
                    st.header("Company Overview")
                    st.write(overview)

                    st.header("Top 5 AI/ML Use Cases")
                    for case in use_cases:
                        with st.container():
                            st.subheader(case["heading"])
                            st.write(case["description"])

                            st.markdown("**Implementation Steps:**")
                            for step in case["implementation_steps"]:
                                st.markdown(f"- {step}")

                            with st.expander("Explore Suggested Resources"):
                                st.markdown("##### **Top Datasets (from Kaggle)**")
                                if case["datasets"]:
                                    for ds in case["datasets"]:
                                        st.markdown(f"- [{ds['title']}]({ds['url']})")
                                else:
                                    st.write("No relevant datasets found.")

                                st.markdown("---") # Visual separator
                                st.markdown("##### **Top Repositories (from GitHub)**")
                                if case["repos"]:
                                    for repo in case["repos"]:
                                        st.markdown(f"- [{repo['name']}]({repo['url']}) - ⭐ {repo['stars']}")
                                else:
                                    st.write("No relevant repositories found.")
                                
                                st.markdown("---")
                                st.markdown("##### **Top Research Papers (from ArXiv)**")
                                if case["papers"]:
                                    for paper in case["papers"]:
                                        st.markdown(f"- [{paper['title']}]({paper['url']})")
                                else:
                                    st.write("No relevant research papers found.")
                    
                    # --- Provide the PDF Download Button at the end ---
                    st.download_button(
                        label="Download Full Report as PDF",
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                else:
                    st.error("An unknown error occurred while generating the report.")

            except Exception as e:
                st.error(f"An unexpected application error occurred: {e}")
    else:
        st.warning("Please enter a company name.")

