import streamlit as st


def render(navigate_to):
    # Hero Section
    st.title("🎯 Casual Causality")
    st.subheader("Learn causal inference casually - no PhD required!")

    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏱️ Time to Complete", "~20 mins")
    with col2:
        st.metric("🧠 Prerequisites", "Curiosity")
    with col3:
        st.metric("📊 Math Required", "Minimal")

    st.divider()

    # Why This Matters
    st.header("🤔 Why This Matters")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        **We see correlations everywhere:**
        - 📱 "People who use our app score higher on tests"
        - ☕ "Coffee drinkers are more productive" 
        - 🏥 "Patients who take this drug recover faster"
        
        **But correlation ≠ causation!**
        """
        )

    with col2:
        st.markdown(
            """
        **What we really want to know:**
        - 🎯 Does the app actually *make* people smarter?
        - ⚡ Does coffee actually *cause* productivity?
        - 💊 Does the drug actually *cure* patients?
        
        **Causation is determing if one thing causes change in another thing.**
        """
        )

    # What You'll Learn
    st.header("🎓 What You'll Learn")

    learning_goals = [
        "🕵️ **Become a causality detective** - spot the difference between correlation and causation",
        "⚖️ **Understand when to trust causal claims** - and when to be skeptical",
        "🎮 **Learn with simple mini games** - I've added some maths, but minimal",
    ]

    for goal in learning_goals:
        st.markdown(f"- {goal}")

    # About Section
    st.header("👨‍💻 About")

    col1, col2 = st.columns([1, 3])
    with col1:
        # Try to load actual headshot, fallback to message
        try:
            st.image("assets/headshot.jpg", width=200)
        except:
            st.info("📷 Add your headshot.jpg to the assets folder")

    with col2:
        st.markdown(
            """
        **Hi! My name is Arif** and I'm a Data Scientist at Sky. I'm interested in Causality and Product Data Science but most resources online are very maths heavy, which is what led me to build this web app.
        
        **Connect with me:**
        - 💼 [LinkedIn](https://uk.linkedin.com/in/arif-ahmed-1205bb191)
        - 📧 Contact me through LinkedIn for questions or feedback!
        
        *This is a WIP project so please be prepared for things to change as I improve it :)*
        """
        )

    # Call to Action
    st.divider()
    st.header("🚀 Ready to Start?")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(
            "🎯 Lesson 1: What is Causality?", type="primary", use_container_width=True
        ):
            navigate_to("what_is_causality")

    with col2:
        if st.button(
            "🏃‍♂️ Lesson 2: Selection Bias", type="primary", use_container_width=True
        ):
            navigate_to("selection_bias")

    with col3:
        if st.button(
            "🧩 Lesson 3: Confounders", type="primary", use_container_width=True
        ):
            navigate_to("confounders")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(
            "🎲 Lesson 4: Randomized Experiments",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("randomized_experiments")

    with col2:
        if st.button(
            "📈 Lesson 5: Difference-in-Differences",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("difference_in_differences")

    with col3:
        if st.button(
            "⚖️ Lesson 6: Coarsened Exact Matching",
            type="primary",
            use_container_width=True,
        ):
            navigate_to("coarsened_exact_matching")

    st.divider()
    st.caption(
        "*Estimated completion: 5-10 minutes each | No math background required*"
    )
