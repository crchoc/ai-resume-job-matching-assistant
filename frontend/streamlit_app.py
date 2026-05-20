import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Resume & Job Matching Assistant",
    page_icon="📄",
    layout="wide",
)


def run_full_analysis(resume_file, job_description: str) -> dict:
    files = {
        "file": (
            resume_file.name,
            resume_file.getvalue(),
            "application/pdf",
        )
    }

    data = {
        "job_description": job_description,
    }

    response = requests.post(
        f"{API_BASE_URL}/api/analysis/run",
        files=files,
        data=data,
        timeout=180,
    )

    if not response.ok:
        raise RuntimeError(response.text)

    return response.json()


def show_skill_badges(skills: list[str], badge_type: str = "matched"):
    if not skills:
        st.write("None")
        return

    if badge_type == "missing":
        background_color = "#fff7ed"
        text_color = "#9a3412"
        border_color = "#fed7aa"
    else:
        background_color = "#ecfdf5"
        text_color = "#065f46"
        border_color = "#a7f3d0"

    badge_html = " ".join(
        [
            f"""
            <span style="
                display:inline-block;
                padding:6px 12px;
                margin:4px 4px 6px 0;
                border-radius:16px;
                background-color:{background_color};
                color:{text_color};
                font-size:14px;
                font-weight:500;
                border:1px solid {border_color};
            ">
                {skill}
            </span>
            """
            for skill in skills
        ]
    )

    st.markdown(badge_html, unsafe_allow_html=True)

def show_result(result: dict):
    st.subheader("Analysis Result")

    score = result.get("match_score", 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Match Score", f"{score}%")

    with col2:
        st.metric("Matched Skills", len(result.get("matched_skills", [])))

    with col3:
        st.metric("Missing Skills", len(result.get("missing_skills", [])))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.markdown("### Job Information")
        st.write(f"**Job Title:** {result.get('job_title', 'Unknown Position')}")
        st.write(f"**Company:** {result.get('company_name', 'Unknown Company')}")
        st.write(f"**Saved Result ID:** {result.get('result_id')}")

    with right:
        st.markdown("### Recommendation")
        st.info(result.get("recommendation", "No recommendation available."))

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Matched Skills")
        show_skill_badges(result.get("matched_skills", []), badge_type="matched")

    with col_b:
        st.markdown("### Missing Skills")
        show_skill_badges(result.get("missing_skills", []), badge_type="missing")

    with st.expander("Show all extracted skills"):
        st.markdown("#### Resume Skills")
        show_skill_badges(result.get("resume_skills", []), badge_type="matched")

        st.markdown("#### Job Skills")
        show_skill_badges(result.get("job_skills", []), badge_type="missing")
    st.divider()

    st.markdown("### Tailored Resume Bullet Points")

    bullets = result.get("tailored_bullets", [])

    if bullets:
        for bullet in bullets:
            st.write(f"- {bullet}")
    else:
        st.warning("No bullet points were generated.")

    st.divider()

    st.markdown("### Cover Letter Draft")

    cover_letter = result.get("cover_letter", "")

    st.text_area(
        label="Generated Cover Letter",
        value=cover_letter,
        height=280,
    )


def main():
    st.title("AI Resume & Job Matching Assistant")
    st.write(
        "Upload your resume PDF and paste a job description. "
        "The app will calculate a match score, identify matched and missing skills, "
        "and generate tailored resume bullet points and a cover letter draft."
    )

    with st.sidebar:
        st.header("Project Workflow")
        st.write("1. Upload resume PDF")
        st.write("2. Paste job description")
        st.write("3. Run full analysis")
        st.write("4. Review match score")
        st.write("5. Use generated bullets and cover letter")

        st.divider()

        st.caption("Backend API")
        st.code(f"{API_BASE_URL}/api/analysis/run")

    resume_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"],
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=280,
        placeholder=(
            "Example:\n"
            "Python Backend Developer\n"
            "Company: ABC Tech\n\n"
            "We are looking for a junior backend developer with Python, FastAPI, SQL, Docker..."
        ),
    )

    analyze_button = st.button(
        "Analyze Resume Match",
        type="primary",
        use_container_width=True,
    )

    if analyze_button:
        if resume_file is None:
            st.error("Please upload a resume PDF first.")
            return

        if not job_description.strip():
            st.error("Please paste a job description first.")
            return

        with st.spinner("Analyzing resume and job description..."):
            try:
                result = run_full_analysis(
                    resume_file=resume_file,
                    job_description=job_description,
                )

                st.session_state["analysis_result"] = result
                st.success("Analysis completed and saved to database.")

            except Exception as error:
                st.error("Analysis failed.")
                st.code(str(error))

    if "analysis_result" in st.session_state:
        show_result(st.session_state["analysis_result"])


if __name__ == "__main__":
    main()