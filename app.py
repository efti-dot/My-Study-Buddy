import streamlit as st
from prompt import OpenAIConfig
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please check the OPENAI_API_KEY.")

ai = OpenAIConfig(api_key=api_key)

def naive_bar():
    with st.sidebar:
        st.title("My-Study-Buddy")
        page = st.selectbox("Select an option", ["Talk with AI", "ViTT", "VoTT"])
    
    return page

def talk_with_AI():
    st.title("My Study Buddy")
    st.write("Feel free to ask anything about your study guide!")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("You: ", key="input")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        response = ai.get_response(user_input, st.session_state.messages)
        
        with st.chat_message("assistant"):
            st.markdown(response)


def ViTT():
    st.title("VTT - Video to Text")
    st.write("This is a simple Video to Text generation application.")
    st.write("Upload your video file below:")

    
    
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "m4a"])

    if uploaded_file is not None:
        file_size = len(uploaded_file.getvalue())
        max_size = 50 * 1024 * 1024  # 50 MB

        if file_size > max_size:
            st.error("File too large! Please upload a video smaller than 50 MB.")
        else:
            st.video(uploaded_file)

        
        transcribed_text = "--- Slide 1 --- Nursing Exam Review EHR • Body Mechanics • Workplace Violence • Interprofessional Collaboration --- Slide 2 --- Electronic Health Records (EHR) A lifetime digital record of a patient’s health. Contains history, diagnoses, treatments, provider visits. Improves communication between providers. Can be used in court/legal cases. --- Slide 3 --- EHR vs EMR Electronic Health Record: Lifetime record, across all visits. Electronic Medical Record: Record for one healthcare visit. EHR = Bigger picture | EMR = One event. --- Slide 4 --- EHR Advantages & Challenges Advantages: standardized, accurate, private, fast access. Multiple users can see info at once. Challenges: learning the system, fixing errors, keeping security strong. --- Slide 5 --- EHR Documentation Examples Admission nursing history, care plans, discharge forms. Telephone calls & verbal orders. Incident/occurrence reports. Acuity rating system = hours of care + staff needed. --- Slide 6 --- Body Mechanics Basics Using muscles safely to move, lift, and care for patients. Keeps balance, posture, and body alignment. Prevents injury for nurse + patient. Always assess patient’s ability before moving them. --- Slide 7 --- Center of Gravity & Stability Center of gravity = pelvis (when standing). Closer line of gravity to base = more stable. Lower center of gravity = bend hips/knees. Widen stance = better balance. --- Slide 8 --- Safe Lifting Rules Use legs, not back. Hold object close to body. Avoid twisting while lifting. Use assistive devices if >35 lbs. Ask for help if needed! --- Slide 9 --- Pushing & Pulling Pull toward your body when possible. Widen stance for balance. Face direction of movement. Sliding/rolling = safer than lifting. --- Slide 10 --- Patient Positions (Examples) Semi-Fowler’s (30°): prevents aspiration, helps breathing. Fowler’s (45-60°): procedures, better lung expansion. High Fowler’s (60-90°): severe dyspnea, prevents aspiration. Supine: flat on back, pillow for support. Prone: on stomach, helps drainage but not for lungs. --- Slide 11 --- More Positions Lateral (side-lying): pressure ulcer prevention. Orthopneic: leaning forward on pillow for COPD. Trendelenburg: head lower, helps venous return. Reverse Trendelenburg: head higher, reduces reflux. Modified Trendelenburg: legs elevated, treats shock. --- Slide 12 --- Workplace Violence - Risks Nurses face risk of verbal/physical violence. Often underreported → less resources provided. Warning signs: yelling, glaring, mumbling, swearing, pacing. Causes: pain, transfers, restraints, staff behavior, dissatisfaction. --- Slide 13 --- Workplace Violence - Prevention Stand 1.5–3 ft away from escalating patient. Respect personal space. Use calm, nonthreatening body language. Do not overreact, stay professional. Set simple, clear limits. Use silence & allow patient time to decide. --- Slide 14 --- Interprofessional Collaboration Different professionals working together for patient safety. Important because conditions & treatments are complex. Examples: grief support groups, therapy, spiritual advisors. Helps with safer, better care. --- Slide 15 --- Collaboration Barriers Miscommunication or lack of respect. Distrust between professions. Not understanding each other’s roles. Different levels of perceived importance. --- Slide 16 --- NCLEX Practice Questions EHR • Body Mechanics • Workplace Violence • Collaboration --- Slide 17 --- EHR Question 1 Which statement best describes an Electronic Health Record (EHR)? A. Record of one visit only B. Lifetime digital record of patient health history C. Handwritten notes stored in a chart D. A billing sheet used by providers --- Slide 18 --- Answer & Rationale Correct Answer: B Rationale: The EHR is a lifetime computerized record including history, diagnoses, and treatments. An EMR is for a single visit. --- Slide 19 --- Body Mechanics Question 1 A nurse is preparing to lift a box. Which action is INCORRECT? A. Bending at the knees B. Holding the box close to the body C. Twisting the waist while lifting D. Using leg muscles for support --- Slide 20 --- Answer & Rationale Correct Answer: C Rationale: Twisting at the waist while lifting increases the risk of back injury. Always keep back straight and use legs. --- Slide 21 --- Body Mechanics Question 2 Select all the actions that promote safe body mechanics: A. Widening stance before lifting B. Keeping load close to body C. Bending at the waist D. Using assistive devices when needed E. Facing the direction of movement --- Slide 22 --- Answer & Rationale Correct Answer: A, B, D, E Rationale: Safe body mechanics include a wide base of support, holding load close, using devices, and facing the direction of movement. --- Slide 23 --- Workplace Violence Question 1 A patient begins yelling, glaring, and pacing. What is the nurse’s PRIORITY? A. Leave the patient alone B. Stand 1.5–3 feet away, stay calm, use nonthreatening communication C. Call security immediately without trying to de-escalate D. Tell the patient to stop being disrespectful --- Slide 24 --- Answer & Rationale Correct Answer: B Rationale: Best action is maintaining safe space and calm, nonthreatening communication. This reduces escalation. --- Slide 25 --- Workplace Violence Question 2 Select all strategies for preventing workplace violence: A. Respect personal space B. Use neutral tone and expressions C. Set clear, simple limits D. Rush patient to decide quickly E. Allow silence for reflection --- Slide 26 --- Answer & Rationale Correct Answer: A, B, C, E Rationale: These actions de-escalate violence. Rushing increases patient stress. --- Slide 27 --- Interprofessional Collaboration Question 1 Which is a common barrier to effective interprofessional collaboration? A. Shared respect B. Miscommunication C. Team meetings D. Shared decision-making --- Slide 28 --- Answer & Rationale Correct Answer: B Rationale: Miscommunication is a common barrier, along with lack of respect or misunderstanding roles. --- Slide 29 --- Interprofessional Collaboration Question 2 Select all examples of interprofessional collaboration: A. Referring a patient to grief counseling B. Nurses and physicians planning care together C. Ignoring team input D. Contacting a spiritual advisor at patient request E. Attending support group referrals --- Slide 30 --- Answer & Rationale Correct Answer: A, B, D, E Rationale: Collaboration includes coordinated care across disciplines and respecting patient needs."
        st.text_area("Transcribed Text", transcribed_text, height=400)


        
        num_of_mcq = st.selectbox("Select number of MCQs to generate", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], index=0)
        additional_instructions = st.text_area("Additional Instructions (optional)", height=100)
        quiz_btn = st.button("Generate Quiz")

        if quiz_btn and transcribed_text:
            try:
                num = int(num_of_mcq)
                st.subheader(f"Generated {num} MCQs")

                mcqs = ai.generate_mcqs_from_text(transcribed_text, num, additional_instructions)
                st.markdown(mcqs)
            except ValueError:
                st.error("Please enter a valid number for MCQs.")


        num_of_true_false = st.selectbox("Select number of True/False questions to generate", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=0)
        additional_instructions_tf = st.text_area("Additional Instructions for True/False (optional)", height=100)
        tf_quiz_btn = st.button("Generate True/False Questions")

        if tf_quiz_btn and transcribed_text:
            try:
                num_tf = int(num_of_true_false)
                st.subheader(f"Generated {num_tf} True/False Questions")

                true_false_questions = ai.generate_true_false_from_text(transcribed_text, num_tf, additional_instructions_tf)
                st.markdown(true_false_questions)
            except ValueError:
                st.error("Please enter a valid number for True/False questions.")


def VoTT():
    st.title("VoTT - Voice to Text")
    st.write("This is a simple Voice to Text generation application.")
    st.write("Upload your audio file below:")

    
    
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

    if uploaded_file is not None:
        st.audio(uploaded_file)
        st.write("File uploaded successfully!")

        
        transcribed_text = OpenAIConfig.transcribe_audio_to_text(uploaded_file)
        st.text_area("Transcribed Text", transcribed_text, height=400)

        
        num_of_mcq = st.selectbox("Select number of MCQs to generate", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], index=0)
        quiz_btn = st.button("Generate Quiz")

        if quiz_btn and transcribed_text:
            try:
                num = int(num_of_mcq)
                st.subheader(f"Generated {num} MCQs")
                mcqs = ai.generate_mcqs_from_text(transcribed_text, num)
                st.markdown(mcqs)
            except ValueError:
                st.error("Please enter a valid number for MCQs.")



def main():
    page = naive_bar()
    
    if page == "Talk with AI":
        talk_with_AI()
    elif page == "ViTT":
        ViTT()
    elif page == "VoTT":
        VoTT()
    


main()
