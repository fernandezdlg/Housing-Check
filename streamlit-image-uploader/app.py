import os
import streamlit as st
from PIL import Image
import random
import json
from geopy.geocoders import Nominatim
from process_image import analyze_image_
from real_estate_problem_analyzer import analyze_image_problems
import pandas as pd


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

    st.write("### Property Address")
    address = st.text_input("Enter the property address (street, city, country)")

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
            problems = analyze_image_problems(image, api_key)
            # state_of_building = random.choice(["Very Good", "Good", "Medium", "Bad"])
            # # comments = random.choice(
            # #     [
            # #         "No issues detected",
            # #         "Minor cracks observed",
            # #         "Severe damage detected",
            # #     ]
            # # )
            # grade = random.randint(1, 10)

            # analysis = json.loads(analysis)
            if isinstance(analysis, str):
                # Remove extra quotes and clean the string
                analysis = analysis.strip()  # Remove leading/trailing whitespace
                if analysis.startswith("```") and analysis.endswith("```"):
                    analysis = analysis[
                        7:-3
                    ].strip()  # Remove surrounding triple backticks
                try:
                    analysis = json.loads(
                        analysis
                    )  # Parse the JSON string into a dictionary

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
                    "Problems": problems,
                }
            )

        # Display all results in a single table
        # st.table(results)
        df_results = pd.DataFrame(results)  # Convert the results list to a DataFrame

        # Apply custom styles to the DataFrame
        styled_df = df_results.style.set_properties(
            **{"width": "150px"}
        )  # Set column width

        # Display the styled DataFrame
        st.dataframe(styled_df, use_container_width=True)

    if address:
        st.write("### Property Location on Map")
        geolocator = Nominatim(user_agent="housing-check")
        location = geolocator.geocode(address)

        if location:
            df = pd.DataFrame(
                [[location.latitude, location.longitude]], columns=["lat", "lon"]
            )
            st.map(df, zoom=15)
        else:
            st.error("Could not find that address. Try a different format.")


if __name__ == "__main__":
    main()
