import streamlit as st
from openai_service import generate_text
from templates import system_roles
from docx import Document


# Main App
def main():
    # Set the CSS style for the app
    st.markdown(f'<style>{open("styles.css").read()}</style>', unsafe_allow_html=True)

    # Initialize the session state
    if "page" not in st.session_state:
        st.session_state.page = "Home"
        st.session_state.generated_texts = []

    # Home page
    if st.session_state.page == "Home":
        # Center align the title and information on the home page
        st.markdown(
            "<h1 style='text-align: center;'>Doc Engine</h1>", unsafe_allow_html=True
        )
        st.markdown(
            "<h5 style='text-align: center;'>Welcome to Doc Engine. This app will help you generate documents faster than ever using AI. Choose the type of document you want to generate and enter the prompts. The AI will generate the rest of the document for you. The goal of Doc Engine is to help you generate the first draft of your document faster so you can spend more time on the more important content.</h5>",
            unsafe_allow_html=True,
        )

        # Get started button
        if st.button("Get Started"):
            st.session_state.page = "Options"
            st.experimental_rerun()

    elif st.session_state.page == "Options":
        options_page()

    elif st.session_state.page == "Generate Text":
        generate_text_section()
    # Sidebar
    # Home button
    if st.session_state.page != "Home":
        home_button()

    # Mode Selection
    if st.session_state.page == "Generate Text":
        st.sidebar.subheader("Mode Selection")
        temperature_modes = {"Creative": 1.5, "Neutral": 1.0, "Precise": 0.3}
        selected_mode = st.sidebar.selectbox(
            "Select a mode for the prompt:", list(temperature_modes.keys())
        )
        temperature = temperature_modes[selected_mode]

    # Max Word Selection
    if st.session_state.page == "Generate Text":
        st.sidebar.subheader("Max Words for Output")
        max_words: int = st.sidebar.slider(
            "Select the approximate maximum number of words for the output:",
            50,
            1000,
            200,
            50,
        )

    # Export to Word button
    if st.session_state.page == "Generate Text":
        st.sidebar.subheader("Export to Word")
        st.sidebar.button("Export to Word")
        if st.session_state.generated_texts:
            # Create a new Word document
            document = Document()

            # Add the generated texts to the Word document
            for text in st.session_state.generated_texts:
                document.add_paragraph(text)

            # Save the Word document
            document.save("generated_document.docx")
            st.success("Document exported successfully.")

        else:
            st.warning("Please generate text first.")

    # About
    sidebar()


def generate_text_section():
    if "document_type" not in st.session_state:
        # If document type is not selected, show a warning message
        st.warning("Please select a document type on the 'Options' page.")
        st.stop()

    document_type = st.session_state.document_type
    # Get the role template for the selected document type
    system_role = system_roles[document_type]
    print(system_role)

    st.markdown(f"## Template for {document_type}:")
    subtitle_list = list(system_role.keys())
    selected_subtitle = st.selectbox("Select a subtitle:", subtitle_list)
    prompt = system_role[selected_subtitle]

    # Display the template
    key = f"prompt_{selected_subtitle.replace(' ', '_')}"
    placeholder = f"Enter your prompt for {selected_subtitle} here"
    user_input = st.text_area(
        label="", value="", placeholder=placeholder, key=key, height=100
    )
    print(user_input)

    generate_key = f"generate_{selected_subtitle}"
    if st.button("Generate", key=generate_key):
        if user_input:
            # Combine the template prompt with the user's prompt
            prompt = (
                f"You will write {prompt} for a {document_type} with the following in mind:"
                + "\n"
                + user_input
            )
            generated_text = generate_text(prompt)
            st.session_state.generated_texts.append(generated_text)
            st.session_state.generated_texts = st.session_state.generated_texts[
                -10:
            ]  # Limit to last 10 generated texts
        else:
            st.warning("Please enter a prompt.")

    # Display the generated texts
    if st.session_state.generated_texts:
        st.markdown("### Generated Texts:")
        for text in st.session_state.generated_texts:
            st.write(text)

    # Delete button
    if st.button("Delete All"):
        if st.session_state.generated_texts:
            delete_confirmation = st.warning(
                "Are you sure you want to delete all the generated texts?"
            )
            if delete_confirmation.button("Confirm"):
                st.session_state.generated_texts = []


def options_page():
    st.markdown("<h1 style='text-align: center;'>Options</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h5 style='text-align: center;'> You can now choose two different methods to generate your document. You can either choose a template and enter the prompts for each subtitle, or you can upload the whole case description and make prompts with more freely without the subtitle restrictions. </h5>",
        unsafe_allow_html=True,
    )

    # Document Options
    if st.session_state.page == "Options":
        st.header("Document Options")
        document_type = st.selectbox(
            "Choose the type of documentation:", list(system_roles.keys())
        )

        # Template Options
    if st.button("Go to template"):
        # Store the selected document type in the session state
        st.session_state.document_type = document_type
        st.session_state.page = "Generate Text"
        st.experimental_rerun()


def sidebar():
    st.sidebar.header("About")
    st.sidebar.write(
        "Doc Engine is developed using Streamlit and OpenAI's GPT-3 model. It aims to simplify the document generation process and save time by automating the initial drafting phase."
    )

    # How to Use
    st.sidebar.header("How to Use")
    st.sidebar.write("1. Select the type of document you want to generate.")
    st.sidebar.write(
        "2. Make sure the mode and maximum words for output are set to your preference."
    )
    st.sidebar.write(
        "3. Enter your prompt in the text box below the template and press the 'Generate' button."
    )
    st.sidebar.write("4. Review the generated text and regenerate if necessary.")
    st.sidebar.write(
        "5. Use the 'Export to Word' button to export the generated text to a Word document. You find it at the bottom of the sidebar."
    )

    # FAQ
    st.sidebar.header("FAQ")
    st.sidebar.write("What is Doc Engine?")
    st.sidebar.write(
        "Doc Engine is an AI-powered app that helps you generate documents by providing prompts and generating the rest of the content using OpenAI's GPT-3 model."
    )
    st.sidebar.write("Can I trust the generated text 100%?")
    st.sidebar.write(
        "No. The generated text is meant to be used as a starting point for your document. You should always review the generated text and make any necessary changes to ensure the accuracy of the content."
    )
    st.sidebar.write("How do I use the mode selection?")
    st.sidebar.write(
        "The mode selection allows you to choose the tone of the generated text. The 'Creative' mode will generate more creative text, while the 'Precise' mode will generate more precise text. The 'Neutral' mode is a balance between the two."
    )
    st.sidebar.write("How do I use the maximum words for output selection?")
    st.sidebar.write(
        "The maximum words for output selection allows you to choose the approximate maximum number of words for the generated text. The actual number of words may be slightly higher or lower than the selected number since the model actually generates tokens instead of words."
    )


def home_button():
    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
        st.experimental_rerun()


if __name__ == "__main__":
    main()
