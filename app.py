import random
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Class 11 Physics Formula Quiz",
    page_icon="⚡",
    layout="centered",
)

# Class 11 Physics Formula Database
PHYSICS_FORMULAS = {
    "Mechanics & Motion": [
        {
            "prompt": "Equation of motion: v =",
            "answer": "u + at",
        },
        {
            "prompt": "Displacement in time t: s =",
            "answer": "ut + 1/2at^2",
        },
        {
            "prompt": "Newton's Second Law force: F =",
            "answer": "ma",
        },
        {
            "prompt": "Centripetal acceleration: a_c =",
            "answer": "v^2/r",
        },
    ],
    "Work, Energy & Power": [
        {
            "prompt": "Work done (W) in terms of force (F) and displacement (s) =",
            "answer": "F.s",
        },
        {
            "prompt": "Kinetic Energy (K) =",
            "answer": "1/2mv^2",
        },
        {
            "prompt": "Potential Energy (U) =",
            "answer": "mgh",
        },
        {
            "prompt": "Power (P) =",
            "answer": "W/t",
        },
    ],
    "Gravitation": [
        {
            "prompt": "Universal Gravitational Law force: F =",
            "answer": "G*m1*m2/r^2",
        },
        {
            "prompt": "Acceleration due to gravity: g =",
            "answer": "GM/R^2",
        },
        {
            "prompt": "Orbital velocity of satellite: v_0 =",
            "answer": "sqrt(GM/R)",
        },
    ],
    "Thermodynamics": [
        {
            "prompt": "First Law of Thermodynamics: dQ =",
            "answer": "dU + dW",
        },
        {
            "prompt": "Ideal Gas Law equation: PV =",
            "answer": "nRT",
        },
    ],
    "Oscillations & Waves": [
        {
            "prompt": "Time period of a simple pendulum: T =",
            "answer": "2*pi*sqrt(l/g)",
        },
        {
            "prompt": "Frequency (f) in terms of time period (T) =",
            "answer": "1/T",
        },
    ],
}


# Function to reset or initialize the quiz
def reset_quiz():
  all_questions = []
  for topic, items in PHYSICS_FORMULAS.items():
    for item in items:
      all_questions.append((topic, item))
  random.shuffle(all_questions)
  st.session_state.questions = all_questions[:5]  # Select 5 questions
  st.session_state.current_step = 0
  st.session_state.score = 0
  st.session_state.game_over = False


# Sidebar Menu
st.sidebar.title("📌 Menu")
mode = st.sidebar.radio(
    "Select Mode:", ["📚 Study All Physics Formulas", "🎮 Play Physics Quiz Game"]
)

st.title("⚡ Class 11 Physics Formula Master")
st.write(
    "An interactive web app to revise and test your Class 11 Physics formulas."
)
st.divider()

# --- 1. STUDY MODE ---
if mode == "📚 Study All Physics Formulas":
  st.header("📚 Physics Formula Cheat Sheet")

  for topic, items in PHYSICS_FORMULAS.items():
    with st.expander(f"🔹 {topic}", expanded=True):
      for item in items:
        st.markdown(f"• **{item['prompt']}** ➡️ `{item['answer']}`")

# --- 2. QUIZ GAME MODE ---
elif mode == "🎮 Play Physics Quiz Game":
  st.header("🎮 Physics Quiz Game")

  if "questions" not in st.session_state:
    reset_quiz()

  if not st.session_state.game_over:
    q_index = st.session_state.current_step
    total_q = len(st.session_state.questions)

    if q_index < total_q:
      topic, item = st.session_state.questions[q_index]

      st.caption(f"Question {q_index + 1} / {total_q} | Topic: **{topic}**")
      st.subheader(f"Fill in the blank: `{item['prompt']} ?`")

      # User input field
      user_ans = st.text_input(
          "Enter your answer:", key=f"user_ans_{q_index}"
      )

      if st.button("Submit Answer"):
        clean_user = user_ans.lower().replace(" ", "")
        clean_correct = item["answer"].lower().replace(" ", "")

        if clean_user == clean_correct:
          st.success("✅ Correct Answer!")
          st.session_state.score += 1
        else:
          st.error(
              f"❌ Incorrect! The correct answer is: **{item['answer']}**"
          )

        st.session_state.current_step += 1
        if st.session_state.current_step >= total_q:
          st.session_state.game_over = True
        st.rerun()

    else:
      st.session_state.game_over = True

  # Display final results when game is over
  if st.session_state.game_over:
    st.balloons()
    st.subheader("🏆 Game Over!")
    st.metric(
        label="Your Final Score:",
        value=f"{st.session_state.score} / {len(st.session_state.questions)}",
    )

    if st.button("Play Again"):
      reset_quiz()
      st.rerun()
