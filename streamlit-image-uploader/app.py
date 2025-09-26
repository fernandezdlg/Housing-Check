import os
import streamlit as st
from PIL import Image
import random
import json

from process_image import analyze_image_


def load_prompt(prompt_file):
    """Load the prompt from a text file."""
    with open(prompt_file, "r") as file:
        return file.read()


def main():
    st.title("Housing Check")
    api_key = os.getenv("GOOGLE_AI_API_KEY")

    prompt_file = "streamlit-image-uploader/prompt.txt"
    prompt = load_prompt(prompt_file)

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
                # analysis = analyze_image_(image, api_key)
                # print(analysis)
                col.image(
                    image, caption=f"{uploaded_file.name}", use_container_width=True
                )

        # Placeholder for processing results
        st.write("### Processing Results")
        results = []
        for uploaded_file in uploaded_files:
            # Simulate processing with random outputs
            image = Image.open(uploaded_file)
            # downsample image
            image = image.resize((512, 512))

            analysis = analyze_image_(image, api_key, prompt=prompt)
            # state_of_building = random.choice(["Very Good", "Good", "Medium", "Bad"])
            # # comments = random.choice(
            # #     [
            # #         "No issues detected",
            # #         "Minor cracks observed",
            # #         "Severe damage detected",
            # #     ]
            # # )
            # grade = random.randint(1, 10)
            print("CHECKM1")
            print(analysis)
            print("CHECKM2")
            print(type(analysis))
            # analysis = json.loads(analysis)
            if isinstance(analysis, str):
                # Remove extra quotes and clean the string
                analysis = analysis.strip()  # Remove leading/trailing whitespace
                if analysis.startswith("```") and analysis.endswith("```"):
                    analysis = analysis[7:-3].strip()  # Remove surrounding triple backticks
                try:
                    analysis = json.loads(
                        analysis
                    )  # Parse the JSON string into a dictionary
                    print("CHECKM3")
                    print(type(analysis))
                    print(dict(analysis))
                    print("CHECKM4")
                except json.JSONDecodeError as e:
                    st.error(
                        f"Failed to parse analysis result for {uploaded_file.name}: {e}"
                    )
                    analysis = {}  # Use an empty dictionary if parsing fails
            # transform analysis into a dictionary
            # Append results for the table
            results.append(
                {
                    "Image Name": uploaded_file.name,
                    "Facade": analysis.get("facade", ""),
                    "Roof": analysis.get("roof", ""),
                    "Secondary Rooms": analysis.get("secondary_rooms", ""),
                    "Electrical": analysis.get("electrical", ""),
                    "Sanitary": analysis.get("sanitary", ""),
                    "Heating": analysis.get("heating", ""),
                    "Moisture": analysis.get("moisture", ""),
                    "Elevators": analysis.get("elevators", ""),
                    "Overall Grade": analysis.get("overall_grade", ""),
                }
            )

        # Display all results in a single table
        st.table(results)


if __name__ == "__main__":
    main()
