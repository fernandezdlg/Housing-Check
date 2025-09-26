import os
import streamlit as st
from PIL import Image
import random
import json
from geopy.geocoders import Nominatim
import pandas as pd
import altair as alt



from process_image import analyze_image_
from real_estate_problem_analyzer import analyze_image_problems
from image_room_clasify import clasify_image
from price_analasys import RenovationAnalyzer



def extract_cost_rows(analysis_json):
    """
    Turns the LLM analysis JSON into tidy rows for plotting.
    Supports multiple top-level categories, each with a list of entries.
    """
    rows = []
    if not isinstance(analysis_json, dict):
        return rows

    for category, entries in analysis_json.items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            cat = entry.get("category", category)
            rp = entry.get("renovation_prediction", {}) or {}
            years_until = rp.get("years_until_renovation_needed")
            urgency = rp.get("urgency_level")

            cost = (entry.get("cost_analysis") or {})
            # Immediate repairs (single lump sum + optional items)
            imm = (cost.get("immediate_repairs") or {})
            imm_cost = imm.get("estimated_cost_chf", 0) or 0
            imm_desc = imm.get("description", "Immediate repairs")
            imm_items = imm.get("items") or []
            # If items are provided, plot each; else plot the lump sum if > 0
            if imm_items:
                for it in imm_items:
                    rows.append({
                        "category": cat,
                        "label": f"Immediate · {it.get('item','Item')}",
                        "description": imm_desc,
                        "cost": float(it.get("cost", 0) or 0),
                        "years_until": 0,
                        "urgency": "immediate"
                    })
            elif imm_cost > 0:
                rows.append({
                    "category": cat,
                    "label": "Immediate · Repairs",
                    "description": imm_desc,
                    "cost": float(imm_cost),
                    "years_until": 0,
                    "urgency": "immediate"
                })

            # Future renovation (lump sum + items)
            fut = (cost.get("future_renovation") or {})
            fut_desc = fut.get("description", "Future renovation")
            fut_items = fut.get("items") or []
            fut_lump = float(fut.get("estimated_cost_chf", 0) or 0)

            # If itemized, prefer item rows (avoid double counting lump sum)
            if fut_items:
                for it in fut_items:
                    rows.append({
                        "category": cat,
                        "label": f"Future · {it.get('item','Item')}",
                        "description": fut_desc,
                        "cost": float(it.get("cost", 0) or 0),
                        "years_until": years_until,
                        "urgency": urgency
                    })
            elif fut_lump > 0:
                rows.append({
                    "category": cat,
                    "label": "Future · Renovation",
                    "description": fut_desc,
                    "cost": fut_lump,
                    "years_until": years_until,
                    "urgency": urgency
                })
    return rows


def build_cost_chart(analysis_json, width=800, bar_height=42):
    """
    Returns an Altair horizontal stacked bar chart with tooltips.
    One bar per category; segments per cost item.
    """
    rows = extract_cost_rows(analysis_json)
    if not rows:
        return None

    df = pd.DataFrame(rows)

    # Format CHF in tooltip via calculated field (keeps axis numeric)
    df["cost_chf"] = df["cost"].map(lambda x: f"CHF {int(x):,}".replace(",", "'"))

    # Height scales with number of categories
    n_categories = df["category"].nunique()
    chart_height = max(bar_height * n_categories, bar_height + 10)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            y=alt.Y("category:N", title=None, sort="-x"),
            x=alt.X("cost:Q", title="Estimated cost (CHF)", stack="zero"),
            color=alt.Color("label:N", title="Segment"),
            tooltip=[
                alt.Tooltip("category:N", title="Category"),
                alt.Tooltip("label:N", title="Item"),
                alt.Tooltip("description:N", title="Description"),
                alt.Tooltip("cost_chf:N", title="Cost"),
                alt.Tooltip("urgency:N", title="Urgency"),
                alt.Tooltip("years_until:Q", title="Years until renovation", format=".0f"),
            ],
        )
        .properties(width=width, height=chart_height)
        .interactive()  # enables hover & legend interactions
    )

    return chart





def load_prompt(prompt_file):
    """Load the prompt from a text file."""
    with open(prompt_file, "r") as file:
        return file.read()


def main():

    st.title("Housing Check")
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    analyzer = RenovationAnalyzer(api_key)

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
        counter = 0
        for uploaded_file in uploaded_files:
            # Simulate processing with random outputs
            image = Image.open(uploaded_file)
            # downsample image
            image = image.resize((512, 512))

            # Clasify the image
            clasify_image(image, api_key, counter)
            counter += 1
            analysis = analyze_image_(image, api_key, prompt=prompt)
            problems = analyze_image_problems(image, api_key)

            # big results

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

        # Price analysis section
        print("Starting renovation analysis with Gemini 2.0-flash...")
        print(f"Found {len(analyzer.category_data)} categories in CSV")
        print(
            f"Will analyze folders: {list(analyzer.folder_to_category_mapping.keys())}"
        )

        # Run analysis
        results = analyzer.analyze_all_categories()

        # Save results
        analyzer.save_results(results)

        # Generate and save summary report
        summary = analyzer.generate_summary_report(results)
        with open("renovation_analysis_summary.md", "w", encoding="utf-8") as f:
            f.write(summary)

        print("\nAnalysis complete!")
        print(f"Results saved to: renovation_analysis_results.json")
        print(f"Summary report saved to: renovation_analysis_summary.md")


        # Here the horizontal bar chart for renovation costs is displayed
        st.write("#### Cost Breakdown (interactive)")
        with open("/Users/fernandez/Documents/collab_repos/Housing-Check/renovation_analysis_results.json", "r") as f:
            cost_analysis = json.load(f)
            chart = build_cost_chart(cost_analysis)
            
            # streamlit embed chart box
            if chart is not None:
                st.container()
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No renovation expected 🤠👍.")


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
