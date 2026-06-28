import matplotlib.pyplot as plt 
import streamlit as st
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from io import BytesIO


def create_pdf(score, found_skills, missing_skills):

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "AI Resume Analysis Report")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 760, f"Resume Score : {score}/100")

    pdf.drawString(50, 730, "Skills Found:")

    y = 710

    for skill in found_skills:
        pdf.drawString(70, y, f"- {skill}")
        y -= 20

    pdf.drawString(50, y-10, "Missing Skills:")

    y -= 30

    for skill in missing_skills:
        pdf.drawString(70, y, f"- {skill}")
        y -= 20

    pdf.save()

    buffer.seek(0)

    return buffer

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#081b29,#0f3460,#16213e);
}

h1,h2,h3,h4,h5,h6,
p,
label,
div,           
li {
    color: white !important;
}

div[data-testid="stMetric"]{
    background:rgba(255,255,255,0.08);
    border:1px solid #00c8ff;        
    border-radius:18px;
    padding:18px;
    text-align:center;
}

textarea{
    background:#102542 !important;
    color:white !important;
}

div[data-testid="stFileUploader"]{
    background:rgba(255,255,255,.05);
    border-radius:15px;
    padding:15px;
}

section[data-testid="stSidebar"]{
    background:#09131f;
}
            
[data-baseweb="select"] div {
    color: black !important;
}
            
[data-baseweb="select"] input {
    color: black !important;
    -webkit-text-fill-color: black !important;
}

[data-baseweb="select"] span {
    color: black !important;
}

div[role="listbox"] {
    background-color: black !important;
}
            
div[role="option"] {
    color: black !important;
    background-color: white !important;
}
/* Selected value */
[data-baseweb="select"] input {
    color: black !important;
    -webkit-text-fill-color: black !important;
}

/* Selected value */
[data-baseweb="select"] {
    color: black !important;
}

/* Dropdown popup */
[data-baseweb="popover"] {
    background-color: white !important;
}

/* Dropdown list */
[data-baseweb="menu"] {
    background-color: white !important;
}

/* All options */
[data-baseweb="menu"] [role="option"] {
    color: black !important;
    background-color: white !important;
}

/* Hover */
[data-baseweb="menu"] [role="option"]:hover {
    background-color: #E6F4FF !important;
    color: black !important;
}

/* Download button */
.stDownloadButton > button {
    background-color: #00c8ff !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    border: 2px solid #00c8ff !important;
    padding: 12px 20px !important;

    /* ✨ Glow */
    box-shadow: 0 0 10px #00c8ff,
                0 0 20px rgba(0,200,255,0.6) !important;

    transition: all 0.3s ease;
}

/* Hover */
.stDownloadButton > button:hover {
    background-color: #0099cc !important;
    color: white !important;

    box-shadow: 0 0 15px #00e5ff,
                0 0 30px rgba(0,229,255,0.9) !important;

    transform: scale(1.03);
}

.stDownloadButton > button:hover {
    background-color: #0099cc !important;
    color: white !important;
}    

/* Browse files button */
div[data-testid="stFileUploader"] button {
    color: black !important;
    background-color: #315399 !important;
    font-weight: bold !important;
    border-radius: 8px !important;
}

/* Hover effect */
div[data-testid="stFileUploader"] button:hover {
    color: white !important;
    background-color: #0099cc !important;
}

/* Upload box */
div[data-testid="stFileUploader"] {
    border: 2px solid #00c8ff !important;
    border-radius: 18px !important;
    padding: 18px !important;
    background: rgba(255,255,255,0.05) !important;

    /* Glow effect */
    box-shadow: 0 0 12px rgba(0,200,255,0.5) !important;
}

/* Hover glow */
div[data-testid="stFileUploader"]:hover {
    box-shadow: 0 0 20px rgba(0,200,255,0.9) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]{
    border:2px solid #00c8ff !important;
    border-radius:18px !important;
    box-shadow:0 0 15px rgba(0,200,255,0.7) !important;
}

/* Selectbox glow */
div[data-baseweb="select"] {
    border: 4px solid #00c8ff !important;
    border-radius: 12px !important;
    box-shadow: 0 0 20px rgba(0,200,255,0.7) !important;
    transition: all 0.3s ease;
}

/* Hover glow */
div[data-baseweb="select"]:hover {
    box-shadow: 0 0 18px rgba(0,200,255,1) !important;
}                                                                                              

</style>
""",unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.markdown("""
<div style="
background: rgba(255,255,255,0.05);
border: 2px solid #00c8ff;
border-radius: 20px;
padding: 20px;
margin-bottom: 20px;
box-shadow: 0 0 20px rgba(0,200,255,0.8);
text-align: center;
">

<h1 style="
color:#00d4ff;
font-size:52px;
margin:0;
text-shadow:0 0 15px #00c8ff;
">
🤖 AI Resume Analyzer
</h1>

</div>
""", unsafe_allow_html=True)

st.markdown(
"<p style='text-align:center;color:white;font-size:18px;'>Upload your resume and receive an AI-powered analysis.</p>",
unsafe_allow_html=True
)
st.image(
    "ai resume banner.png",
    use_container_width=True
)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("📌 About")

    st.write("""
This project analyzes your resume,
detects technical skills,
shows missing skills,
calculates resume score
and provides suggestions.
""")

    st.markdown("---")

    st.success("Python")
    st.success("Streamlit")
    st.success("PyPDF2")

# ---------------- ROLE ----------------

st.container(border=True)

st.markdown("""
<div style="
background:rgba(255,255,255,0.08);
border:1px solid #00c8ff;
border-radius:18px;
padding:20px;
margin-bottom:15px;
">
<h3 style="color:white;text-align:center;">
💼 Select Job Role
</h3>
""", unsafe_allow_html=True)

role = st.selectbox(
    "",
    [
        "Python Developer",
        "Frontend Developer",
        "Data Analyst"
    ]
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FILE ----------------

with st.container(border=True):

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "",
        type=["pdf"]
    )

# ==================================================

if uploaded_file is not None:

    st.success("Resume Uploaded Successfully ✅")

    reader = PdfReader(uploaded_file)

    resume_text=""

    for page in reader.pages:
        text=page.extract_text()
        if text:
            resume_text+=text

    with st.expander("📄 View Resume Content"):
     st.text_area(
        "",
        resume_text,
        height=220
    )

    # ---------------- Skills ----------------

    skills=[

        "Python",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "SQL",
        "Git",
        "GitHub",
        "Java",
        "C++",
        "Excel"

    ]

    found_skills=[]

    for skill in skills:

        if skill.lower() in resume_text.lower():

            found_skills.append(skill)

    # ---------------- Required Skills ----------------

    if role=="Python Developer":

        required_skills=[
            "Python",
            "SQL",
            "Git",
            "GitHub"
        ]

    elif role=="Frontend Developer":

        required_skills=[
            "HTML",
            "CSS",
            "JavaScript",
            "React"
        ]

    else:

        required_skills=[
            "Python",
            "SQL",
            "Excel"
        ]

    missing_skills=[]

    for skill in required_skills:

        if skill not in found_skills:

            missing_skills.append(skill)
    # ---------------- Dashboard Metrics ----------------

    score = len(found_skills) * 10

    if score > 100:
        score = 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("✅ Skills Detected", len(found_skills))

    with col2:
        st.metric("❌ Missing Skills", len(missing_skills))

    with col3:
        st.metric("📊 Resume Score", f"{score}/100")
    st.markdown("---")

    col1, col2 = st.columns([1.5,1.7])

    with col1:

        st.subheader("🎯 Job Match")

        matched = len(required_skills) - len(missing_skills)
        match_percent = int((matched / len(required_skills)) * 100)

        st.progress(match_percent/100)

        st.metric("Job Match", f"{match_percent}%")
    
    with col2:

      
     with st.container(border=True):

        st.markdown("""           
        <h3 style='text-align:center;color:white;'>
        📊 Skills Overview
        </h3>
        """, unsafe_allow_html=True)

        labels = ["Skills Found", "Missing Skills"]
        sizes = [len(found_skills), len(missing_skills)]

        fig, ax = plt.subplots(figsize=(3.2,3.2))

        colors = ["#40719E", "#1F1769"]

        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor":"white","linewidth":0},
            textprops={"color":"white"}
        )

        ax.set_facecolor("#1B1D7A")
        fig.patch.set_facecolor("#1B1D7A")
        ax.axis("equal")

        st.pyplot(fig)

    st.markdown("""
    <div style="
    background: rgba(255,255,255,0.08);
    border:1px solid #00c8ff;
    border-radius:18px;
    padding:20px;
    margin-top:15px;
    margin-bottom:20px;
    ">
    <h3 style="color:white;text-align:center;">📊 Overall Resume Score</h3>
    </div>
    """, unsafe_allow_html=True)

    st.progress(score/100)

    st.markdown(
     f"<h2 style='text-align:center;color:white;'>{score}% Match</h2>",
     unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------- Skills & Missing Skills ----------------

    left, right = st.columns(2)

    with left:

     st.markdown("""
     <div style="
     background:rgba(255,255,255,0.08);
     border:1px solid #00c8ff;
     border-radius:18px;
     padding:18px;
     ">
     <h3 style="color:white;text-align:center;">
     ✅ Skills Found
     </h3>
     </div>
     """, unsafe_allow_html=True) 

     if found_skills:
         for skill in found_skills:
            st.markdown(f"""
            <div style="
            background:rgba(255,255,255,0.08);
            border:1px solid #00c8ff;
            border-radius:12px;
            padding:12px;
            margin-bottom:10px;
            box-shadow:0 0 10px rgba(0,200,255,0.7);
            color:white;
            font-weight:bold;
            ">
           ✅ {skill}
           </div>
           """, unsafe_allow_html=True)
     else:
         st.warning("No skills detected.")

    with right:

     st.markdown("""
     <div style="
     background:rgba(255,255,255,0.08);
      border:1px solid #ff4b6e;
     border-radius:18px;
     padding:18px;
     ">
     <h3 style="color:white;text-align:center;">
     ❌ Missing Skills
     </h3>
     </div>
     """, unsafe_allow_html=True)

     if missing_skills:
         for skill in missing_skills:
            st.markdown(f"""
            <div style="
            background:rgba(255,255,255,0.08);
            border:1px solid #00c8ff;
            border-radius:12px;
            padding:12px;
            margin-bottom:10px;
            box-shadow:0 0 10px rgba(0,200,255,0.7);
            color:white;
            font-weight:bold;
            ">
            ✅ {skill}
            </div>
            """, unsafe_allow_html=True)
     else:
         st.success("No missing skills!")

    st.markdown("---")

    # ---------------- Analysis ----------------

    st.markdown("""
 <div style="
 background:rgba(255,255,255,0.08);
 border:1px solid #00c8ff;
 border-radius:18px;
 padding:18px;
 margin-bottom:15px;
 ">
 <h3 style="color:white;text-align:center;">  
 📋 Analysis Summary
 </h3>
 </div>
 """, unsafe_allow_html=True)

    if score >= 80:
        st.success("Excellent Resume! Your resume is highly suitable for the selected role.")

    elif score >= 60:
        st.info("Good Resume. Add a few more relevant skills to improve your profile.")

    elif score >= 40:
        st.warning("Average Resume. Try adding projects, certifications, and technical skills.")

    else:
        st.error("Resume needs significant improvement for this role.")

    # ---------------- Suggestions ----------------

    st.markdown("""
 <div style="
 background:rgba(255,255,255,0.08);
 border:1px solid #00c8ff;
 border-radius:18px;
 padding:18px;
 margin-bottom:15px;
 ">
 <h3 style="color:white;text-align:center;">
 💡 Suggestions
 </h3>
 </div>
 """, unsafe_allow_html=True)

    suggestions = []

    if "GitHub" not in found_skills:
        suggestions.append("Add your GitHub profile.")

    if "SQL" not in found_skills:
        suggestions.append("Learn and mention SQL.")

    if "Git" not in found_skills:
        suggestions.append("Mention Git version control experience.")

    if len(found_skills) < 5:
        suggestions.append("Add more technical skills.")

    suggestions.append("Include 2–3 real-world projects.")
    suggestions.append("Add certifications.")
    suggestions.append("Keep your resume to one page.")
    suggestions.append("Use action verbs in project descriptions.")

    for item in suggestions:
        st.markdown(f"""
        <div style="
        background:rgba(255,255,255,0.08);
        border:1px solid #00c8ff;
        border-radius:12px;
        padding:12px;
        margin-bottom:10px;
        box-shadow:0 0 10px rgba(0,200,255,0.7);
        color:white;
        font-weight:bold;
        transition:0.3s;
        ">
        ✔️ {item}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="
    background:rgba(255,255,255,0.08);
    border:1px solid #00c8ff;
    border-radius:18px;
    padding:18px;
    margin-bottom:15px;
    ">
    <h3 style="color:white;text-align:center;">
    📥 Download Analysis Report
    </h3>
    </div>
    """, unsafe_allow_html=True)

    pdf_file = create_pdf(score, found_skills, missing_skills)

    st.download_button(
    "📄 Download PDF Report",
    data=pdf_file,
    file_name="AI_Resume_Report.pdf",
    mime="application/pdf",
    use_container_width=True
    )
    st.markdown("---")

    # ---------------- Footer ---------------

st.markdown("---")

st.markdown(
 """
 <div style="text-align:center;color:white;">
 Developed by <b>Pari Pal</b> ❤️ <br>
 Python • Streamlit • PyPDF2
 </div>
 """,    
 unsafe_allow_html=True
 )