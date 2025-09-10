import streamlit as st
import plotly.graph_objects as go
import numpy as np


def create_city_map(selected_location=None):
    """Create interactive city map with pin placement"""
    fig = go.Figure()

    # Add city background
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=10,
        y1=10,
        fillcolor="lightgreen",
        opacity=0.3,
        line=dict(width=0),
    )

    # Add locations
    locations = {
        "mcdonalds": {
            "x": 2,
            "y": 8,
            "color": "red",
            "symbol": "square",
            "name": "McDonald's",
        },
        "gym": {"x": 8, "y": 8, "color": "blue", "symbol": "diamond", "name": "Gym"},
        "hospital": {
            "x": 5,
            "y": 2,
            "color": "green",
            "symbol": "cross",
            "name": "Hospital",
        },
    }

    for loc_id, loc in locations.items():
        fig.add_trace(
            go.Scatter(
                x=[loc["x"]],
                y=[loc["y"]],
                mode="markers+text",
                marker=dict(
                    size=20,
                    color=loc["color"],
                    symbol=loc["symbol"],
                ),
                text=[loc["name"]],
                textposition="bottom center",
                name=loc["name"],
                showlegend=False,
            )
        )

    # Add big pin if location is selected
    if selected_location and selected_location in locations:
        loc = locations[selected_location]
        fig.add_trace(
            go.Scatter(
                x=[loc["x"]],
                y=[loc["y"] + 0.5],  # Slightly above the location
                mode="markers+text",
                marker=dict(
                    size=30,
                    color="orange",
                    symbol="triangle-down",
                    line=dict(width=3, color="black"),
                ),
                text=["📍 SIGN HERE"],
                textposition="top center",
                name="Your Sign",
                showlegend=False,
            )
        )

    fig.update_layout(
        title="City Map - Where Will You Place Your Sign?",
        xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
        width=600,
        height=500,
        plot_bgcolor="white",
    )

    return fig


def get_location_message(location):
    """Get message based on sign placement location"""
    messages = {
        "mcdonalds": {
            "signup": "25 people signed up from McDonald's!",
            "result": "❌ **Experiment Failed!**\n\nYour 25 McDonald's volunteers actually GAINED weight during the running program!\n\n**Control group:** No change in weight\n**Treatment group:** +2 lbs average weight gain",
            "prompt": "This doesn't make sense... running should help with weight loss! Maybe try a different location?",
        },
        "gym": {
            "signup": "30 people signed up from the Gym!",
            "result": "❌ **Experiment Failed!**\n\nNeither group lost any weight!\n\n**Control group:** No change in weight\n**Treatment group:** No change in weight",
            "prompt": "Strange... nobody lost weight at all! Maybe try another location?",
        },
        "hospital": {
            "signup": "15 people signed up from the Hospital!",
            "result": "❌ **Experiment Failed!**\n\nMany volunteers got injured and couldn't complete the program!\n\n**Control group:** No change in weight\n**Treatment group:** +3 lbs average (due to injuries preventing exercise)",
            "prompt": "This is getting worse! The running program is backfiring. Maybe a different location will work better?",
        },
    }
    return messages.get(location, {})


def render(navigate_to):
    # Back button
    if st.button("← Back to Home"):
        navigate_to("home")

    # Initialize session state
    if "lesson2_step" not in st.session_state:
        st.session_state.lesson2_step = 1
        st.session_state.current_location = None
        st.session_state.tested_locations = set()
        st.session_state.experiment_phase = "select"  # select, signup, experiment, results

    # Lesson Step 1: Introduction
    st.title("🏃‍♂️ The Running Weight Loss Experiment")

    st.info(
        """
    **The Argument**: You're an avid runner arguing with colleagues about whether running helps with weight loss.
    
    **The Wager**: $100 says running will help people lose significantly more weight than not running.
    
    **The Plan**: Run a 1-month experiment with a control group (your colleagues who won't run) and a treatment group (volunteers who will start running).
    """
    )

    # Lesson Step 2: The Challenge
    if st.session_state.lesson2_step >= 2:
        st.header("🎯 The Challenge")

        st.markdown(
            """
        **Control Group**: ✅ Your colleagues volunteered (they won't run)
        
        **Treatment Group**: ❓ You need to recruit volunteers who will run
        
        **Your Solution**: Place signs around the city asking people to sign up for your running experiment!
        """
        )

    # Lesson Step 3: Interactive Map
    if st.session_state.lesson2_step >= 3:
        st.header("🗺️ Choose Your Sign Location")

        st.markdown(
            "**Click a button** to place your recruitment sign at that location:"
        )

        # Show the map with current selection
        fig = create_city_map(st.session_state.current_location)
        st.plotly_chart(fig, use_container_width=True)

        # Location selection buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🍟 Place at McDonald's", use_container_width=True, key="mcdonalds_btn"):
                st.session_state.current_location = "mcdonalds"
                st.session_state.experiment_phase = "placed"
                st.rerun()
        
        with col2:
            if st.button("💪 Place at Gym", use_container_width=True, key="gym_btn"):
                st.session_state.current_location = "gym"
                st.session_state.experiment_phase = "placed"
                st.rerun()
        
        with col3:
            if st.button("🏥 Place at Hospital", use_container_width=True, key="hospital_btn"):
                st.session_state.current_location = "hospital"
                st.session_state.experiment_phase = "placed"
                st.rerun()

        # Show location-specific content based on phase
        if st.session_state.current_location and st.session_state.experiment_phase == "placed":
            location_data = get_location_message(st.session_state.current_location)
            
            st.info(f"📍 **Sign placed at {st.session_state.current_location.title()}**")
            
            if st.button("⏳ Wait for Sign-ups", type="primary", use_container_width=True, key="signup_btn"):
                st.session_state.experiment_phase = "signup"
                st.rerun()
        
        elif st.session_state.current_location and st.session_state.experiment_phase == "signup":
            location_data = get_location_message(st.session_state.current_location)
            
            st.info(f"📍 **Sign placed at {st.session_state.current_location.title()}**")
            st.success(location_data["signup"])
            
            if st.button("🧪 Run Experiment", use_container_width=True, key="experiment_btn"):
                st.session_state.experiment_phase = "results"
                st.rerun()
        
        elif st.session_state.current_location and st.session_state.experiment_phase == "results":
            location_data = get_location_message(st.session_state.current_location)
            
            st.info(f"📍 **Sign placed at {st.session_state.current_location.title()}**")
            st.success(location_data["signup"])
            
            st.error("**Results after 1 month:**")
            st.error(location_data["result"])
            st.warning(location_data["prompt"])
            
            # Add to tested locations
            if st.session_state.current_location not in st.session_state.tested_locations:
                st.session_state.tested_locations.add(st.session_state.current_location)
            
            # Show appropriate next action
            if len(st.session_state.tested_locations) < 3:
                if st.button("🔄 Try a Different Site", use_container_width=True, key="retry_btn"):
                    st.session_state.current_location = None
                    st.session_state.experiment_phase = "select"
                    st.rerun()
            else:
                st.info("💡 You've tried all locations... something seems wrong with your approach!")

    # Show "What's Going On?" when all locations tested
    if len(st.session_state.tested_locations) >= 3:
        st.divider()
        if st.button(
            "🤔 Huh, What's Going On?", type="primary", use_container_width=True
        ):
            st.session_state.lesson2_step = 4
            st.rerun()

    # Lesson Step 4: Selection Bias Explanation
    if st.session_state.lesson2_step >= 4:
        st.header("🎯 The Problem: Selection Bias!")

        st.error(
            """
        **You Lost $100 Because of Selection Bias!**
        
        The problem wasn't your hypothesis (running does help with weight loss).
        The problem was **WHERE** you recruited your treatment group!
        """
        )

        st.subheader("🧠 What is Selection Bias?")
        st.markdown(
            """
        **Selection bias** occurs when your sample is not representative of the population you want to study.
        
        **What happened at each location:**
        """
        )

        # Show the explanations now
        col1, col2, col3 = st.columns(3)

        with col1:
            st.error("**🍟 McDonald's**")
            st.markdown(
                "People who eat unhealthily. Even with running, their diet sabotaged the results!"
            )

        with col2:
            st.error("**💪 Gym**")
            st.markdown(
                "Health-conscious people who would have lost weight anyway - with or without your study!"
            )

        with col3:
            st.error("**🏥 Hospital**")
            st.markdown(
                "People with health conditions that made running counterproductive!"
            )

        st.markdown("**None of these represented 'average people'!**")

        st.success(
            """
        🎓 **Key Lesson**: 
        
        Where and how you recruit participants can dramatically bias your results, 
        even if your hypothesis is correct!
        
        **Better approach**: Random sampling from the general population, not convenience sampling from biased locations.
        """
        )

    # Navigation
    st.divider()

    if st.session_state.lesson2_step >= 4:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start Over", use_container_width=True):
                st.session_state.lesson2_step = 1
                st.session_state.current_location = None
                st.session_state.tested_locations = set()
                st.session_state.experiment_phase = "select"
                st.rerun()
        with col2:
            st.info("🚧 More lessons coming soon!")
    elif st.session_state.lesson2_step == 3:
        # During interactive map phase - no next button until all experiments done
        # The "What's Going On?" button will appear when all 3 locations tested
        pass
    else:
        # Regular navigation for steps 1-2
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state.lesson2_step += 1
            st.rerun()
