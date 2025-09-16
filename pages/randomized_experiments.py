import streamlit as st
import plotly.graph_objects as go
import numpy as np


def create_engagement_bar_chart(no_feature_avg, feature_avg, rollout_type="baseline"):
    """Create bar chart showing engagement comparison"""
    fig = go.Figure()

    ate = feature_avg - no_feature_avg

    # Add bars
    fig.add_trace(
        go.Bar(
            x=["No Feature", "Feature"],
            y=[no_feature_avg, feature_avg],
            marker_color=["lightcoral", "lightblue"],
            text=[f"{no_feature_avg} min/day", f"{feature_avg} min/day"],
            textposition="inside",
            name="Average Engagement",
        )
    )

    # Add ATE annotation
    fig.add_annotation(
        x=0.5,
        y=max(no_feature_avg, feature_avg) + 15,
        text=f"ATE = +{ate} min/day",
        showarrow=False,
        font=dict(size=16, color="black"),
        bgcolor=(
            "yellow"
            if rollout_type == "randomized"
            else "orange" if rollout_type == "baseline" else "red"
        ),
        bordercolor="black",
        borderwidth=1,
    )

    fig.update_layout(
        title="Daily Engagement: Feature vs No Feature",
        xaxis_title="Group",
        yaxis_title="Average Minutes per Day",
        yaxis=dict(range=[0, max(no_feature_avg, feature_avg) + 30]),
        showlegend=False,
        height=400,
        width=600,
    )

    return fig


def get_rollout_info(rollout_type):
    """Get information for each rollout strategy"""
    info = {
        "baseline": {
            "title": "Initial Observation",
            "body": "Feature users appear more engaged, but is this causal? Try different rollout strategies to find out.",
            "color": "info",
        },
        "power_user": {
            "title": "Power-user rollout → HIGHLY BIASED",
            "body": "You gave early access via a signup link. Only your most engaged users opted-in. That makes the feature group look great — but it's confounded by selection: these users were already high-engagement. The observed +40 min/day is an overestimate of the feature's true effect.",
            "color": "error",
        },
        "self_selection": {
            "title": "Self-selection → PARTIAL BIAS",
            "body": "Some users choose the feature and they tend to be more motivated/curious. This still biases results because those traits affect engagement independent of the feature. They may not be power users, necessarily, but are not representative of our base as they are more curious and engaged with the app.",
            "color": "warning",
        },
        "randomized": {
            "title": "Randomised rollout → UNBIASED",
            "body": "Randomisation balances hidden traits (power-user propensity, baseline engagement). The +10 min/day is the most reliable estimate of the feature's causal effect.",
            "color": "success",
        },
    }
    return info.get(rollout_type, info["baseline"])


def render(navigate_to):
    # Back button
    if st.button("← Back to Home"):
        navigate_to("home")

    # Initialize session state
    if "lesson4_rollout" not in st.session_state:
        st.session_state.lesson4_rollout = "baseline"

    if "lesson4_tried_rollouts" not in st.session_state:
        st.session_state.lesson4_tried_rollouts = set()

    # Lesson Title and Introduction
    st.title("🎯 Randomised Experiments for Product Teams")
    st.subheader("Does this feature actually cause higher engagement?")

    st.info(
        """
    **The Scenario**: You're a PM at a tech company. Your team built a shiny new feature — the Smart Recommendation Feed. 
    
    On the surface, users that use it look much more engaged. But did the feature *cause* that engagement, or did already-engaged users just try the feature first?
    
    **Recall**: We previously established in Lesson 2 that how we target and get people to sign up to trials can effect the final outcome.
    
    **Your Mission**: Try different rollout strategies and watch how the average treatment effect (ATE) estimate changes.
    """
    )

    # Step-by-step progression
    if "lesson4_step" not in st.session_state:
        st.session_state.lesson4_step = 1

    if st.session_state.lesson4_step >= 2:
        st.header("🎮 Mini-Game Instructions")
        st.markdown(
            """
        **Goal**: Choose one of the rollout strategies and observe how the bars and ATE label update. 
        Then read the explanation to discover whether the observed difference tells the true causal story.
        """
        )

    # Main interactive section (only show if step 2 or later)
    if st.session_state.lesson4_step >= 2:
        # Main Layout
        col1, col2 = st.columns([2, 1])

        # Left Column: Graph
        with col1:
            # Determine current values based on rollout type
            rollout_values = {
                "baseline": (65, 90),
                "power_user": (60, 100),
                "self_selection": (65, 90),
                "randomized": (70, 80),
            }

            no_feature, feature = rollout_values[st.session_state.lesson4_rollout]

            if st.session_state.lesson4_rollout == "baseline":
                st.markdown(
                    "**Observed difference looks like:** Feature users are +25 minutes/day more engaged."
                )

            # Create and display chart
            fig = create_engagement_bar_chart(
                no_feature, feature, st.session_state.lesson4_rollout
            )
            st.plotly_chart(fig, use_container_width=True)

        # Right Column: Rollout Buttons and Info
        with col2:
            st.subheader("🎮 Pick a Rollout Strategy")

            # Rollout Strategy Buttons
            if st.button(
                "🔗 Give it to power users\n(link signup)",
                use_container_width=True,
                key="power_user_btn",
            ):
                st.session_state.lesson4_rollout = "power_user"
                st.session_state.lesson4_tried_rollouts.add("power_user")
                st.rerun()

            if st.button(
                "👤 Let users choose\n(pop up when they open app)",
                use_container_width=True,
                key="self_selection_btn",
            ):
                st.session_state.lesson4_rollout = "self_selection"
                st.session_state.lesson4_tried_rollouts.add("self_selection")
                st.rerun()

            if st.button(
                "🎲 Choose users at random to receive the update",
                use_container_width=True,
                key="randomized_btn",
            ):
                st.session_state.lesson4_rollout = "randomized"
                st.session_state.lesson4_tried_rollouts.add("randomized")
                st.rerun()

            # Info Box
            st.divider()
            info = get_rollout_info(st.session_state.lesson4_rollout)

            if info["color"] == "success":
                st.success(f"**{info['title']}**")
            elif info["color"] == "error":
                st.error(f"**{info['title']}**")
            elif info["color"] == "warning":
                st.warning(f"**{info['title']}**")
            else:
                st.info(f"**{info['title']}**")

            st.markdown(info["body"])

        # Check if all rollouts have been tried
        if len(st.session_state.lesson4_tried_rollouts) >= 3:
            st.session_state.lesson4_step = 3

    # Show key takeaways after completing mini-game
    if st.session_state.lesson4_step >= 3:
        st.divider()
        st.header("🎓 Key Takeaways")
        st.success(
            """
        **If you care about cause, HOW you roll out matters more than the raw uplift.**
        
        Randomised experiments are the simplest, most reliable way to measure causal impact in product teams.

        Life is not always that easy, however, and we will cover later what you can do when you cannot perform a randomised trial.

        """
        )

    # Navigation
    st.divider()

    if st.session_state.lesson4_step < 2:
        # Initial next button
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state.lesson4_step = 2
            st.rerun()
    elif st.session_state.lesson4_step == 2:
        # During mini-game, show next button if completed
        if len(st.session_state.lesson4_tried_rollouts) >= 3:
            if st.button("Next →", type="primary", use_container_width=True):
                st.session_state.lesson4_step = 3
                st.rerun()
    else:
        # Final navigation
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Start Over", use_container_width=True):
                st.session_state.lesson4_step = 1
                st.session_state.lesson4_rollout = "baseline"
                st.session_state.lesson4_tried_rollouts = set()
                st.rerun()

        with col2:
            if st.button("📈 Next: Lesson 5", use_container_width=True, type="primary"):
                navigate_to("difference_in_differences")

        with col3:
            if st.button("♾️ Optional Maths", use_container_width=True):
                st.session_state.show_math = True
                st.rerun()

        # Optional Math Section
        if getattr(st.session_state, "show_math", False):
            st.divider()
            st.header("📚 Optional Math Corner")
            st.subheader("Average Treatment Effect (ATE) Formula")
            st.latex(
                r"\text{ATE} = \text{mean}(Y | \text{Feature}) - \text{mean}(Y | \text{No Feature})"
            )
            st.markdown(
                "**Key insight**: If assignment is random, ATE is an unbiased estimate of the causal effect."
            )

            st.subheader("Why Randomisation Works")
            st.markdown(
                """
            - **Balances observed traits**: Age, gender, usage history
            - **Balances unobserved traits**: Motivation, tech-savviness, time availability  
            - **Creates comparable groups**: Any difference in outcomes is likely due to the feature
            """
            )
