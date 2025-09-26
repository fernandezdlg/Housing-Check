import streamlit as st
from PIL import Image
import random


def main():
    st.title("Housing Check")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open and display the image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_container_width=True)
        st.write("")
        st.success("Image uploaded successfully!")

        # Placeholder for image processing
        st.write("Processing the image...")
        # Simulate processing with random outputs
        state_of_building = random.choice(["Good", "Average", "Poor"])
        comments = random.choice(
            ["No issues detected", "Minor cracks observed", "Severe damage detected"]
        )
        grade = random.randint(1, 10)

        # Display results in a table
        st.subheader("Building Analysis Results")
        st.table(
            {
                "State of Building": [state_of_building],
                "Comments": [comments],
                "Grade": [grade],
            }
        )


if __name__ == "__main__":
    main()
