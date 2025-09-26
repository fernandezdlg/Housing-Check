import streamlit as st
from PIL import Image
import random


def main():
    st.title("Housing Check")

    uploaded_files = st.file_uploader(
        "Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True
    )

    if uploaded_files:
        # Create a horizontal scrollable container for images
        st.write("### Uploaded Images")
        images_container = st.container()
        with images_container:
            cols = st.columns(len(uploaded_files))
            for col, uploaded_file in zip(cols, uploaded_files):
                image = Image.open(uploaded_file)
                col.image(
                    image, caption=f"{uploaded_file.name}", use_container_width=True
                )

        # Placeholder for processing results
        st.write("### Processing Results")
        results = []
        for uploaded_file in uploaded_files:
            # Simulate processing with random outputs
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
                }
            )

        # Display all results in a single table
        st.table(results)


if __name__ == "__main__":
    main()
