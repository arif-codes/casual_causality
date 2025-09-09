import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def generate_target_data(
    time_of_day, hangover_severity, theory="hangover", theory_value=0
):
    """Generate rifle accuracy data based on time and hangover level"""
    # Use theory_value to create different random seeds for visual variety
    np.random.seed(42 + int(theory_value * 10))  # Changes based on slider value

    # Base accuracy (distance from bullseye center)
    base_accuracy = 2.0  # inches from center

    # Hangover effect - only real cause of poor accuracy
    hangover_effect = hangover_severity * 3.0

    # Add small visual variations for other theories (but don't improve accuracy)
    if theory == "warmup":
        # Work start time: slight variation but no real improvement
        visual_variation = (theory_value - 9) * 0.1  # Minimal effect
        base_accuracy += abs(visual_variation) * 0.2  # Still poor accuracy
    elif theory == "food":
        # Breakfast amount: slight variation but no real improvement
        visual_variation = (theory_value - 2.5) * 0.1  # Minimal effect
        base_accuracy += abs(visual_variation) * 0.2  # Still poor accuracy
    elif theory == "fatigue":
        # Coffee cups: slight variation but no real improvement
        visual_variation = (theory_value - 2.5) * 0.1  # Minimal effect
        base_accuracy += abs(visual_variation) * 0.2  # Still poor accuracy

    # Time effect - minimal impact
    time_effect = 0.2 if time_of_day == "Morning" else 0.0

    # Generate shot coordinates (x, y from bullseye center)
    n_shots = 10
    accuracy_std = base_accuracy + hangover_effect + time_effect

    x_coords = np.random.normal(0, accuracy_std, n_shots)
    y_coords = np.random.normal(0, accuracy_std, n_shots)

    return x_coords, y_coords


def create_target_plot(morning_shots, afternoon_shots):
    """Create interactive target visualization"""
    fig = go.Figure()

    # Draw target rings
    for radius in [2, 4, 6, 8, 10]:
        fig.add_shape(
            type="circle",
            x0=-radius,
            y0=-radius,
            x1=radius,
            y1=radius,
            line=dict(color="black", width=1),
            fillcolor="rgba(0,0,0,0)",
        )

    # Add center bullseye
    fig.add_shape(
        type="circle",
        x0=-0.5,
        y0=-0.5,
        x1=0.5,
        y1=0.5,
        fillcolor="red",
        line=dict(color="red"),
    )

    # Morning shots (red)
    fig.add_trace(
        go.Scatter(
            x=morning_shots[0],
            y=morning_shots[1],
            mode="markers",
            marker=dict(color="red", size=8, symbol="x"),
            name="Morning Shots",
            text=["Morning"] * len(morning_shots[0]),
        )
    )

    # Afternoon shots (blue)
    fig.add_trace(
        go.Scatter(
            x=afternoon_shots[0],
            y=afternoon_shots[1],
            mode="markers",
            marker=dict(color="blue", size=8, symbol="circle"),
            name="Afternoon Shots",
            text=["Afternoon"] * len(afternoon_shots[0]),
        )
    )

    fig.update_layout(
        title="Lee Enfield Rifle Test Results",
        xaxis_title="Distance from Center (inches)",
        yaxis_title="Distance from Center (inches)",
        width=500,
        height=500,
        xaxis=dict(range=[-12, 12], dtick=2, showgrid=True),
        yaxis=dict(range=[-12, 12], dtick=2, showgrid=True),
        showlegend=True,
        plot_bgcolor="white",
    )

    return fig


def calculate_accuracy_score(shots):
    """Calculate average distance from bullseye"""
    x_coords, y_coords = shots
    distances = np.sqrt(x_coords**2 + y_coords**2)
    return np.mean(distances)


def render(navigate_to):
    # Back button
    if st.button("← Back to Home"):
        navigate_to("home")

    # Initialize session state for story progression
    if "story_step" not in st.session_state:
        st.session_state.story_step = 1
    if "active_theory" not in st.session_state:
        st.session_state.active_theory = None

    # Story Step 1: Introduction
    st.title("🕵️ The Lee Enfield Mystery")

    st.info(
        """
    **WWII Britain, 1943**: Factories are mass-producing Lee Enfield rifles to support the war effort.
    
    A quality control marksman tests each rifle by shooting a 10-round group at 100 yards. Rifles with tight groupings get sniper scopes, loose groupings get iron sights.
    
    **But there's a strange pattern...**
    """
    )

    # Story Step 2: The Pattern
    if st.session_state.story_step >= 2:
        st.header("🔍 The Pattern")

        col1, col2 = st.columns(2)
        with col1:
            st.error("**Morning Rifles:** Always poor accuracy ❌")
        with col2:
            st.info("**Afternoon Rifles:** Mixed results - some good, some bad ✅❌")

        st.markdown(
            "So it appears that rifles tested in the **afternoon** are more accurate than rifles tested in the **morning**?!"
        )

    # Story Step 3: The Questions
    if st.session_state.story_step >= 3:
        st.subheader("The Questions:")

        st.markdown(
            """
        - **Same marksman** ✓
        - **Same rifles** ✓  
        - **Same targets** ✓
        - **Same distance** ✓
        
        **So why the difference?** 🤔
        """
        )

    # Story Step 4: Test Theories Section
    if st.session_state.story_step >= 4:
        st.header("🧪 Test Your Theories")
        st.markdown(
            "**What do you think is causing the morning rifles to be inaccurate?**"
        )

        # Theory Controllers Row
        col1, col2, col3, col4 = st.columns(4)

        # Theory 1: Not Warmed Up
        with col1:
            if st.session_state.story_step >= 5:
                if st.button(
                    "🤸 Not Warmed Up", use_container_width=True, key="theory1"
                ):
                    st.session_state.active_theory = "warmup"
                    st.rerun()
            else:
                st.button(
                    "🔒 Locked", disabled=True, use_container_width=True, key="locked1"
                )

        # Theory 2: Needs Breakfast
        with col2:
            if st.session_state.story_step >= 6:
                if st.button(
                    "🍳 Needs Breakfast", use_container_width=True, key="theory2"
                ):
                    st.session_state.active_theory = "food"
                    st.rerun()
            else:
                st.button(
                    "🔒 Locked", disabled=True, use_container_width=True, key="locked2"
                )

        # Theory 3: Getting Tired
        with col3:
            if st.session_state.story_step >= 7:
                if st.button(
                    "😴 Getting Tired", use_container_width=True, key="theory3"
                ):
                    st.session_state.active_theory = "fatigue"
                    st.rerun()
            else:
                st.button(
                    "🔒 Locked", disabled=True, use_container_width=True, key="locked3"
                )

        # Theory 4: Hangover
        with col4:
            if st.session_state.story_step >= 8:
                if st.button(
                    "🍺 Hangover Effect", use_container_width=True, key="theory4"
                ):
                    st.session_state.active_theory = "hangover"
                    st.rerun()
            else:
                st.button(
                    "🔒 Locked", disabled=True, use_container_width=True, key="locked4"
                )

        # Active Theory Details
        hangover_severity = 0.8  # Default hangover level
        pints_last_night = 6  # Default for logic checking
        theory_value = 0  # Default slider value
        current_theory = "hangover"  # Default theory

        if st.session_state.active_theory == "warmup":
            current_theory = "warmup"
            st.subheader("🤸 Theory: Not Warmed Up")
            st.markdown("*Maybe the marksman needs to warm up his shooting muscles?*")

            work_start_time = st.slider(
                "Work Start Time",
                min_value=6,
                max_value=9,
                value=9,
                step=1,
                format="%d AM",
                help="What time does the marksman start work?",
            )

            theory_value = work_start_time

            if work_start_time < 9:
                st.error("**Tried starting at 6 AM instead of 9 AM**")
                st.error("**Result:** Still terrible morning accuracy! ❌")
            else:
                st.warning("**Current:** Starting at 9 AM - poor morning accuracy")

            hangover_severity = 0.8  # Still hungover regardless

        elif st.session_state.active_theory == "food":
            current_theory = "food"
            st.subheader("🍳 Theory: Needs Breakfast")
            st.markdown("*Perhaps low blood sugar affects his aim?*")

            breakfast_amount = st.slider(
                "Breakfast Amount",
                min_value=0,
                max_value=5,
                value=2,
                step=1,
                format="%d items",
                help="How many breakfast items did he eat?",
            )

            theory_value = breakfast_amount

            if breakfast_amount >= 4:
                st.error("**Tried heavy breakfast before work**")
                st.error("**Result:** Morning still bad, afternoon still mixed! ❌")
            elif breakfast_amount == 0:
                st.error("**Tried skipping breakfast entirely**")
                st.error("**Result:** Morning still bad, afternoon still mixed! ❌")
            else:
                st.warning("**Current:** Normal breakfast - poor morning accuracy")

            hangover_severity = 0.8  # Still hungover regardless

        elif st.session_state.active_theory == "fatigue":
            current_theory = "fatigue"
            st.subheader("😴 Theory: Getting Tired")
            st.markdown("*Maybe he gets tired as the day goes on?*")

            coffee_cups = st.slider(
                "Cups of Coffee Before Shooting",
                min_value=0,
                max_value=5,
                value=2,
                step=1,
                format="%d cups",
                help="How many cups of coffee before shooting?",
            )

            theory_value = coffee_cups

            st.error(
                "**Problem:** If fatigue was the issue, morning should be BETTER than afternoon!"
            )
            st.error("**Result:** This theory doesn't match the pattern! ❌")

            hangover_severity = 0.8  # Still hungover regardless

        elif st.session_state.active_theory == "hangover":
            current_theory = "hangover"
            st.subheader("🍺 Theory: Hangover Effect")
            st.markdown("*What if he drinks heavily the night before?*")

            pints_last_night = st.slider(
                "Pints Last Night",
                min_value=0,
                max_value=8,
                value=6,
                step=1,
                format="%d pints",
                help="How many pints did he drink the night before?",
            )

            theory_value = pints_last_night

            # Calculate hangover severity (0-1 scale)
            hangover_severity = min(pints_last_night / 6.0, 1.0)

            if pints_last_night == 0:
                st.success("**Result:** Both morning AND afternoon accurate! ✅")
                st.success(
                    "🎯 **Both sessions accurate!** The hangover theory explains the mystery!"
                )
            else:
                st.warning(
                    f"**Heavy drinking ({pints_last_night} pints):** Poor morning accuracy due to hangover"
                )

        # Target Visualization (always show when theories are available)
        if st.session_state.story_step >= 5:
            st.subheader("🎯 Target Results")

            # Generate shot data based on current theory and slider value
            morning_shots = generate_target_data(
                "Morning", hangover_severity, current_theory, theory_value
            )
            afternoon_shots = generate_target_data(
                "Afternoon", hangover_severity * 0.3, current_theory, theory_value
            )

            col1, col2 = st.columns([2, 1])
            with col1:
                fig = create_target_plot(morning_shots, afternoon_shots)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                morning_score = calculate_accuracy_score(morning_shots)
                afternoon_score = calculate_accuracy_score(afternoon_shots)
                st.metric(
                    "🌅 Morning Average", f"{morning_score:.1f} inches from center"
                )
                st.metric(
                    "🌅 Afternoon Average", f"{afternoon_score:.1f} inches from center"
                )

                if (
                    st.session_state.active_theory == "hangover"
                    and pints_last_night == 0
                ):
                    st.success("🎯 Perfect accuracy!")

    # Story Step 9: The Big Lesson
    if st.session_state.story_step >= 9:
        st.header("🎯 The Big Lesson")

        st.success(
            """
        **This is causality detective work!**
        
        - ❌ **Time of day** was correlated with accuracy, but didn't *cause* the problem
        - ❌ **Warmup, food, fatigue** seemed plausible but weren't the real cause  
        - ✅ **Alcohol hangover** was the hidden factor actually *causing* poor morning accuracy
        
        **The real cause was hidden** - time of day was just correlation and the other "confounders" were red herrings!
        """
        )

        st.markdown("**🎓 Key Insight:** *Causation = X actually makes Y happen*")
        st.markdown("Note to self: Avoid drinking before important tasks! 🍺🚫")

    # Single Next button at the bottom
    st.divider()

    # Determine what the button should say and do
    if st.session_state.story_step == 9:
        # Final step - show restart option
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start Over", use_container_width=True, key="restart"):
                st.session_state.story_step = 1
                st.session_state.active_theory = None
                st.rerun()
        with col2:
            st.info("🚧 More lessons coming soon!")
    elif st.session_state.story_step == 8:
        # Only allow progression if they've solved the mystery (pints = 0)
        if st.session_state.active_theory == "hangover" and pints_last_night == 0:
            if st.button(
                "Next → See the Big Lesson",
                type="primary",
                use_container_width=True,
                key="final_next",
            ):
                st.session_state.story_step = 9
                st.rerun()
        else:
            st.info(
                "💡 **Hint:** Try the 'Hangover Effect' theory and adjust the slider to solve the mystery!"
            )
    else:
        # Regular progression
        if st.button(
            "Next →", type="primary", use_container_width=True, key="main_next"
        ):
            st.session_state.story_step += 1
            st.rerun()
