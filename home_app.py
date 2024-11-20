import base64

import streamlit as st
import numpy as np
import json
from os import path
from datetime import date
import time
from streamlit_extras.streaming_write import write
from streamlit_extras.badges import badge

INFO_FILE_PATH = path.join(path.dirname(path.abspath(__file__)), 'info.json')
ASSETS_DIR_PATH = path.join(path.dirname(path.abspath(__file__)), 'assets')


def load_projects(info_projects):
    st.divider()
    st.subheader(f":orange[**Projects**]")
    st.write("Below you can see my Machine Learning projects and interact with them 🤩!")

    for category_key in info_projects:
        category = info_projects[category_key]
        category_name = category["category_name"]

        with st.expander(category_name, expanded=True):
            projects = np.array(category["projects"])
            qty_project_columns = 4
            rows = int(np.ceil(len(projects) / qty_project_columns))
            projects.resize(rows, qty_project_columns)

            for row in range(rows):
                columns = st.columns(qty_project_columns)
                project_rows = zip(columns, projects[row, :])

                for col, project in project_rows:
                    if project:
                        container = col.container(border=True)
                        with container:
                            st.page_link(project["app_path"], label=project["name"], icon=project["icon"],
                                         use_container_width=True)
                            # st.write(project["description"])


def load_experiences(info_experiences):
    st.divider()
    st.subheader(f":orange[**Professional Experiences**]")

    for experience in info_experiences:

        expander = st.expander(f"💼 {experience['role']} @ {experience['company']}")

        start_date = date.fromisoformat(experience['start_date']).strftime('%B %Y')
        end_date = date.fromisoformat(experience['end_date']).strftime('%B %Y')

        expander.subheader(f":orange[{experience['role']}]")

        expander.write(f"**{experience['company']}** ({start_date} – {end_date})")

        for topic in experience["topics"]:
            expander.write(f"- {topic}")


def load_educations(info_educations):
    st.divider()

    with st.container():
        left_column, right_column = st.columns(2)

        left_column.subheader(":orange[**Education**]")

        for education in info_educations:
            expander = st.expander(f"📚 {education['course_name']} @ {education['institution_name']}")
            expander.subheader(f":orange[{education['level']} in {education['course_name']}]")
            expander.write(f"**{education['institution_name']}** ({education['start_date']} – {education['end_date']})")


def load_certifications():
    st.divider()
    st.subheader(":orange[**Certifications**]")

    with st.container():
        left_column, right_column = st.columns(2)

        left_column.write("🧠 **Machine Learning Specialization**")
        left_column.image('./assets/img/machine-learning-specialization-certificate-bruno-sudre.png', caption='',
                          use_column_width='auto')

        # right_column.write("🇫🇷 TCF Canada - B2")
        # right_column.image('./assets/img/tcf-canada-example.jpg', caption='', use_column_width='auto')


def load_skills(tech_skills):
    with st.container():
        st.subheader(":orange[**Tech Skills**]")

        programming_languages = tech_skills["programming_languages"]
        machine_learning = tech_skills["machine_learning"]
        data_analysis_visualization = tech_skills["data_analysis_visualization"]
        databases = tech_skills["databases"]
        cloud_computing = tech_skills["cloud_computing"]

        background_color = "green"
        styled_programming_languages = " ".join(
            [f":{background_color}-background[{pl}]" for pl in programming_languages])
        styled_machine_learning = " ".join([f":{background_color}-background[{ml}]" for ml in machine_learning])
        styled_data_analysis_visualization = " ".join(
            [f":{background_color}-background[{da}]" for da in data_analysis_visualization])
        styled_databases = " ".join([f":{background_color}-background[{db}]" for db in databases])
        styled_cloud_computing = " ".join([f":{background_color}-background[{cp}]" for cp in cloud_computing])

        st.write(f"👨🏻‍💻 Programming Languages: {styled_programming_languages}")
        st.write(f"🧠 Machine Learning: {styled_machine_learning}")
        st.write(f"🧮 Data Analysis & Visualization: {styled_data_analysis_visualization}")
        st.write(f"💾 Databases: {styled_databases}")
        st.write(f"☁️ Cloud Computing: {styled_cloud_computing}")


def load_intro(info_social_media, spoken_languages):
    def stream_data():
        message = "Hi 👋, I'm :orange[Bruno Sudré]!"
        for word in message.split(" "):
            yield word + " "
            time.sleep(0.3)

    with st.container():
        left_column, right_column = st.columns(2)

        left_column.title("Hi 👋, I'm :orange[Bruno Sudré]!")
        # st.write_stream(stream_data)
        left_column.write(
            """
                Final-year AI & Machine Learning student, at Collège LaSalle, with five years of experience as a 
                Software Engineer. Currently seeking an internship in Machine Learning or Data Science to apply AI 
                expertise to solve real-world challenges.                  
            """)

        styled_spoken_languages = " ".join([f":green-background[{sl}]" for sl in spoken_languages])
        left_column.write(f"Languages: {styled_spoken_languages}")

        right_columns = right_column.columns(5)
        right_columns[1].image(f'{ASSETS_DIR_PATH}/img/bruno_automne.png', caption='', clamp=True, width=200)
        columns = right_column.columns(5)
        for i, social_media in enumerate(info_social_media):
            if i + 1 < len(columns):
                image = base64.b64encode(open(social_media["logo_path"], "rb").read()).decode()
                columns[i + 1].markdown(
                    f"""
                    <a href="{social_media['url']}">
                        <img src="data:image/png;base64,{image}" width="40">
                    </a>
                    """,
                    unsafe_allow_html=True,
                )

        right_column.markdown("<br />", unsafe_allow_html=True)
        with right_column.popover("📄 Download my resume", use_container_width=True):
            with open(f"{ASSETS_DIR_PATH}/doc/resume-bruno-sudre-en.pdf", "rb") as english_resume:
                st.download_button(
                    label="🇨🇦 English",
                    data=english_resume,
                    file_name="resume-bruno-sudre-en.pdf",
                    mime="doc",
                    use_container_width=True
                )

            with open(f"{ASSETS_DIR_PATH}/doc/resume-bruno-sudre-en.pdf", "rb") as french_resume:
                st.download_button(
                    label="🇫🇷 Français",
                    data=french_resume,
                    file_name="resume-bruno-sudre-en.pdf",
                    mime="doc",
                    use_container_width=True
                )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Bruno Sudré",
        page_icon=":gem:",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Bruno Sudré's Portfolio"
        }
    )

    with open(INFO_FILE_PATH) as config_file:
        info = json.load(config_file)

        info_projects = info["projects"]
        info_experiences = info["experiences"]
        info_educations = info["educations"]
        info_social_media = info["social_media"]
        info_spoken_languages = info["spoken_languages"]
        info_tech_skills = info["tech_skills"]

        load_intro(info_social_media, info_spoken_languages)
        load_skills(info_tech_skills)
        load_projects(info_projects)
        load_experiences(info_experiences)
        load_educations(info_educations)
        load_certifications()
