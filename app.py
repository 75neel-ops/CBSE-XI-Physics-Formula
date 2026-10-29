import random
import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(
    page_title="একাদশ শ্রেণির গণিত ফর্মুলা কুইজ", page_icon="📐", layout="centered"
)

# ফর্মুলার ডেটাবেস
FORMULAS = {
    "Sets & Relations": [
        {
            "prompt": "Number of elements in power set P(A) where n(A) = m",
            "answer": "2^m",
        },
        {"prompt": "n(A ∪ B) = n(A) + n(B) - ?", "answer": "n(A ∩ B)"},
        {"prompt": "De Morgan's Law: (A ∪ B)' =", "answer": "A' ∩ B'"},
    ],
    "Trigonometric Functions": [
        {"prompt": "sin²(x) + cos²(x) =", "answer": "1"},
        {"prompt": "cos(2x) in terms of cos(x) =", "answer": "2cos²(x) - 1"},
        {"prompt": "sin(A + B) =", "answer": "sinA cosB + cosA sinB"},
        {"prompt": "tan(2x) =", "answer": "2tan(x) / (1 - tan²(x))"},
    ],
    "Permutations & Combinations": [
        {"prompt": "nPr formula =", "answer": "n! / (n - r)!"},
        {"prompt": "nCr formula =", "answer": "n! / (r! * (n - r)!)"},
        {"prompt": "nCr + nC(r-1) =", "answer": "n+1Cr"},
    ],
    "Limits & Derivatives": [
        {"prompt": "lim (x->0) [sin(x) / x] =", "answer": "1"},
        {"prompt": "Derivative of x^n d/dx(x^n) =", "answer": "n*x^(n-1)"},
        {"prompt": "Derivative of sin(x) =", "answer": "cos(x)"},
    ],
    "Straight Lines & Conics": [
        {
            "prompt": "Slope of line through (x1, y1) and (x2, y2) =",
            "answer": "(y2 - y1) / (x2 - x1)",
        },
        {
            "prompt": "Equation of circle with center (h,k) and radius r =",
            "answer": "(x-h)² + (y-k)² = r²",
        },
        {"prompt": "Eccentricity (e) of a parabola =", "answer": "1"},
    ],
}


# কুইজ শুরু বা রিসেট করার ফাংশন
def reset_quiz():
  all_questions = []
  for topic, items in FORMULAS.items():
    for item in items:
      all_questions.append((topic, item))
  random.shuffle(all_questions)
  st.session_state.questions = all_questions[:5]  # ৫টি প্রশ্ন নির্বাচন
  st.session_state.current_step = 0
  st.session_state.score = 0
  st.session_state.game_over = False


# সাইডবার মেনু
st.sidebar.title("📌 মেনু (Menu)")
mode = st.sidebar.radio(
    "একটি মোড বেছে নিন:",
    ["📚 Study All Formulas", "🎮 Play Formula Quiz Game"],
)

st.title("📐 Class 11 Math Formula Master")
st.write("একাদশ শ্রেণির গণিতের সূত্ৰ রিভিশন এবং প্র্যাকটিস করার অ্যাপ।")
st.divider()

# --- ১. STUDY MODE ---
if mode == "📚 Study All Formulas":
  st.header("📚 Formula Cheat Sheet")

  for topic, items in FORMULAS.items():
    with st.expander(f"🔹 {topic}", expanded=True):
      for item in items:
        st.markdown(f"• **{item['prompt']}** ➡️ `{item['answer']}`")

# --- ২. QUIZ GAME MODE ---
elif mode == "🎮 Play Formula Quiz Game":
  st.header("🎮 Formula Quiz Game")

  # সেসন স্টেট ইনিশিয়ালাইজ করা
  if "questions" not in st.session_state:
    reset_quiz()

  if not st.session_state.game_over:
    q_index = st.session_state.current_step
    total_q = len(st.session_state.questions)

    if q_index < total_q:
      topic, item = st.session_state.questions[q_index]

      st.caption(f"প্রশ্ন {q_index + 1} / {total_q} | বিষয়: **{topic}**")
      st.subheader(f"Fill in the blank: `{item['prompt']} = ?`")

      # ইউজার ইনপুট
      user_ans = st.text_input(
          "আপনার উত্তর লিখুন:", key=f"user_ans_{q_index}"
      )

      if st.button("জমা দিন (Submit)"):
        # স্পেস এবং কেস বাদ দিয়ে যাচাই করা
        clean_user = user_ans.lower().replace(" ", "")
        clean_correct = item["answer"].lower().replace(" ", "")

        if clean_user == clean_correct:
          st.success("✅ সঠিক উত্তর! (Correct!)")
          st.session_state.score += 1
        else:
          st.error(f"❌ ভুল উত্তর! সঠিক উত্তর: **{item['answer']}**")

        st.session_state.current_step += 1
        if st.session_state.current_step >= total_q:
          st.session_state.game_over = True
        st.rerun()

    else:
      st.session_state.game_over = True

  # কুইজ শেষ হলে ফলাফল দেখানো
  if st.session_state.game_over:
    st.balloons()
    st.subheader("🏆 Game Over!")
    st.metric(
        label="আপনার মোট স্কোর:",
        value=f"{st.session_state.score} / {len(st.session_state.questions)}",
    )

    if st.button("আবার খেলুন (Play Again)"):
      reset_quiz()
      st.rerun()
