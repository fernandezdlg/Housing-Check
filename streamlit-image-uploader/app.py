import os
import streamlit as st
from PIL import Image
import random

from process_image import analyze_image_


def main():
    st.title("Housing Check")
    api_key = os.getenv("GOOGLE_AI_API_KEY")

    uploaded_files = st.file_uploader(
        "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
    )
    # Section for property description
    st.write("### Property Description")
    property_description = st.text_area(
        "Add a description of the property (e.g., location, size, condition, etc.):"
    )
    if property_description:
        st.write("#### Your Description:")
        st.write(property_description)
    if uploaded_files:
        # Create a horizontal scrollable container for images

        st.write("### Uploaded Images")
        images_container = st.container()
        with images_container:
            cols = st.columns(len(uploaded_files))
            for col, uploaded_file in zip(cols, uploaded_files):
                image = Image.open(uploaded_file)
                analysis = analyze_image_(image, api_key)
                print(analysis)
                col.image(
                    image, caption=f"{uploaded_file.name}", use_container_width=True
                )

        # Placeholder for processing results
        st.write("### Processing Results")
        results = []
        for uploaded_file in uploaded_files:
            # Simulate processing with random outputs
            image = Image.open(uploaded_file)
            analysis = analyze_image_(image, api_key)
            state_of_building = random.choice(["Very Good", "Good", "Medium", "Bad"])
            comments = random.choice(
                [
                    "No issues detected",
                    "Minor cracks observed",
                    "Severe damage detected",
                ]
            )
            grade = random.randint(1, 10)

            # Append results for the table
            results.append(
                {
                    "Image Name": uploaded_file.name,
                    "State of Building": state_of_building,
                    "Comments": comments,
                    "Replacement Cost per Unit": grade,
                    "Analysis Results": analysis,
                }
            )

        # Display all results in a single table
        st.table(results)


if __name__ == "__main__":
    main()
