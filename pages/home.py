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
        
        **This is about causation - and it changes everything.**
        """
        )

    # What You'll Learn
    st.header("🎓 What You'll Learn")

    learning_goals = [
        "🕵️ **Become a causality detective** - spot the difference between correlation and causation",
        "⚖️ **Understand when to trust causal claims** - and when to be skeptical",
        "🎮 **Play with real scenarios** - see how hidden factors fool us",
        "🎲 **Discover why randomisation is magic** - the gold standard of causal inference",
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
        **Hi! My name is Arif** and I'm a Data Scientist at Sky. I'm interested in Causality and Product Data Science, which is what led me to build this web app.
        
        **Connect with me:**
        - 💼 [LinkedIn](https://uk.linkedin.com/in/arif-ahmed-1205bb191)
        - 📧 Contact me through LinkedIn for questions or feedback!
        
        *I built this app in a few hours for curious minds who want to understand the world better.*
        """
        )

    # Call to Action
    st.divider()
    st.header("🚀 Ready to Start?")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🎯 Start Your Causal Journey", type="primary", use_container_width=True
        ):
            navigate_to("what_is_causality")

    st.divider()
    st.caption("*Estimated completion: 20 minutes | No math background required*")
