import streamlit as st
from openai_service import generate_text
from templates import document_templates
from docx import Document


# Main App
def main():
    # Set the CSS style for the app
    st.markdown('<style>{}</style>'.format(open('styles.css').read()), unsafe_allow_html=True)

    # Initialize the session state
    if "page" not in st.session_state:
        st.session_state.page = "Options"

    # Home page
    if st.session_state.page != "Generate Text":
        # Center align the title and information on the home page
        st.markdown("<h1 style='text-align: center;'>Doc Engine</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Welcome to Doc Engine. This app will help you generate documents faster than ever using AI. Choose the type of document you want to generate and enter the prompts. The AI will generate the rest of the document for you. The goal of Doc Engine is to help you generate the first draft of your document faster so you can spend more time on the more important content.</p>", unsafe_allow_html=True)

    # Sidebar
    if st.sidebar.button("Home"):
        st.session_state.page = "Options"

    # Mode Selection
    if st.session_state.page == "Generate Text":
        st.sidebar.subheader("Mode Selection")
        temperature_modes = {
            "Creative": 1.5,
            "Neutral": 1.0,
            "Precise": 0.3
        }
        selected_mode = st.sidebar.selectbox("Select a mode for the prompt:", list(temperature_modes.keys()))
        temperature = temperature_modes[selected_mode]
    
    # Max Word Selection
    if st.session_state.page == "Generate Text":
        st.sidebar.subheader("Max Words for Output")
        max_words = st.sidebar.slider("Select the maximum number of words for the output:", 50, 500, 250, 50)


    # Options page
    if st.session_state.page == "Options":
        st.header("Document Options")
        document_type = st.selectbox("Choose the type of documentation:", list(document_templates.keys()))

        if st.button("Go to template"):
            # Store the selected document type in the session state
            st.session_state.document_type = document_type
            st.session_state.page = "Generate Text"

    # Generate Text page
    elif st.session_state.page == "Generate Text":
        if "document_type" not in st.session_state:
            # If document type is not selected, show a warning message
            st.warning("Please select a document type on the 'Options' page.")
            st.stop()

        document_type = st.session_state.document_type
        document_template = document_templates[document_type]

        st.markdown(f"## Template for {document_type}:")
        for subtitle, prompt in document_template.items():
            st.text(subtitle + ":")
            key = f"prompt_{subtitle}"
            placeholder = f"Enter your prompt for {subtitle} here"
            with st.empty():
                # Create a text area for the user to enter the prompt
                user_prompt = st.text_area(label="", value="", placeholder=placeholder, key=key, height=100)

            generate_key = f"generate_{subtitle}"
            if st.button("Generate", key=generate_key):
                if user_prompt:
                    # Combine the template prompt with the user's prompt
                    prompt = prompt + "\n" + user_prompt
                    generated_text = generate_text(prompt)
                    st.markdown(f"### Generated Text for {subtitle}:")
                    st.write(generated_text)
                    st.session_state.generated_text = generated_text
                else:
                    st.warning("Please enter a prompt.")

        # Export to Word button
        if st.sidebar.button("Export to Word"):
            if "generated_text" in st.session_state and st.session_state.generated_text:
                # Create a new Word document
                document = Document()

                # Add the generated text to the Word document
                document.add_paragraph(st.session_state.generated_text)

                # Save the Word document
                document.save("generated_document.docx")
                st.success("Document exported successfully.")
            else:
                st.warning("Please generate text first.")

if __name__ == "__main__":
    main()
