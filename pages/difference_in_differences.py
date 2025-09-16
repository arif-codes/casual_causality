import streamlit as st
import plotly.graph_objects as go
import numpy as np


def generate_territory_data():
    """Generate retention data for both territories"""
    # Territory A: gets feature at end of year 2
    # Territory B: control territory (no feature during period)

    years = [1, 2, 3, 4]

    # Base retention rates with natural upward trend
    base_trend_a = [65, 70, 75, 80]  # Natural trend
    base_trend_b = [63, 68, 73, 78]  # Similar natural trend

    # Feature effect starts after year 2 for Territory A
    feature_effect_a = [0, 0, 5, 10]  # Effect shows in years 3 and 4
    feature_effect_b = [0, 0, 0, 0]  # No feature in Territory B

    retention_a = [
        base + effect for base, effect in zip(base_trend_a, feature_effect_a)
    ]
    retention_b = [
        base + effect for base, effect in zip(base_trend_b, feature_effect_b)
    ]

    return years, retention_a, retention_b


def create_retention_plot(years, retention_a, retention_b, stage="parallel"):
    """Create retention trends plot based on stage"""
    fig = go.Figure()

    if stage == "parallel":
        # Show only years 1-2, both lines parallel
        display_years = years[:2]
        display_a = retention_a[:2]
        display_b = retention_b[:2]

        fig.add_trace(
            go.Scatter(
                x=display_years,
                y=display_a,
                mode="lines+markers",
                name="Territory A (Treatment)",
                line=dict(color="red", width=3),
                marker=dict(size=8),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=display_years,
                y=display_b,
                mode="lines+markers",
                name="Territory B (Control)",
                line=dict(color="blue", width=3),
                marker=dict(size=8),
            )
        )

        title = "Before Period: Parallel Trends"

    elif stage == "spike":
        # Show Territory A extending to year 4, Territory B stops at year 2
        display_years = years[:4]
        display_a = retention_a[:4]  # Show A's full trend including year 4
        display_b = retention_b[:2]  # Keep B at year 2

        fig.add_trace(
            go.Scatter(
                x=display_years,
                y=display_a,
                mode="lines+markers",
                name="Territory A (Treatment)",
                line=dict(color="red", width=3),
                marker=dict(size=8),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=years[:2],
                y=display_b,
                mode="lines+markers",
                name="Territory B (Control)",
                line=dict(color="blue", width=3),
                marker=dict(size=8),
            )
        )

        # Add feature line
        fig.add_vline(
            x=2.5,
            line_dash="dash",
            line_color="green",
            annotation_text="Feature Introduced",
            annotation_position="top",
        )

        # Show naive estimate (year 2 to year 4)
        naive_effect = retention_a[3] - retention_a[1]  # Year 4 - Year 2
        fig.add_annotation(
            x=3.2,
            y=retention_a[3] + 2,
            text=f"Naive Effect: +{naive_effect}",
            showarrow=False,
            bgcolor="orange",
            bordercolor="black",
            borderwidth=1,
            font=dict(size=12),
        )

        title = "Territory A Spikes After Feature"

    elif stage == "reveal_trend":
        # Show both territories extending to year 4
        display_years = years[:4]
        display_a = retention_a[:4]  # Show A's full trend
        display_b = retention_b[:4]  # Show B's full trend

        fig.add_trace(
            go.Scatter(
                x=display_years,
                y=display_a,
                mode="lines+markers",
                name="Territory A (Treatment)",
                line=dict(color="red", width=3),
                marker=dict(size=8),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=display_years,
                y=display_b,
                mode="lines+markers",
                name="Territory B (Control)",
                line=dict(color="blue", width=3),
                marker=dict(size=8),
            )
        )

        fig.add_vline(
            x=2.5,
            line_dash="dash",
            line_color="green",
            annotation_text="Feature Introduced",
            annotation_position="top",
        )

        title = "Territory B Also Trending Up!"

    elif stage == "full_did":
        # Show full period with DiD calculation
        fig.add_trace(
            go.Scatter(
                x=years,
                y=retention_a,
                mode="lines+markers",
                name="Territory A (Treatment)",
                line=dict(color="red", width=3),
                marker=dict(size=8),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=years,
                y=retention_b,
                mode="lines+markers",
                name="Territory B (Control)",
                line=dict(color="blue", width=3),
                marker=dict(size=8),
            )
        )

        fig.add_vline(
            x=2.5,
            line_dash="dash",
            line_color="green",
            annotation_text="Feature Introduced",
            annotation_position="top",
        )

        fig.add_annotation(
            x=2.8,  # Slightly left of year 3
            y=retention_a[2],  # Arrow tip points exactly at Year 3 data point for A
            text="A: +15",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red",
            arrowwidth=2,
            bgcolor="white",
            bordercolor="red",
            borderwidth=1,
            font=dict(size=11, color="red"),
            ax=-50,  # Text positioned 50 pixels left of arrow tip
            ay=-30,  # Text positioned 30 pixels above arrow tip
        )

        # Territory B annotation - positioned to the right
        fig.add_annotation(
            x=3.2,  # Slightly right of year 3
            y=retention_b[2],  # Arrow tip points exactly at Year 3 data point for B
            text="B: +10",
            showarrow=True,
            arrowhead=2,
            arrowcolor="blue",
            arrowwidth=2,
            bgcolor="white",
            bordercolor="blue",
            borderwidth=1,
            font=dict(size=11, color="blue"),
            ax=50,  # Text positioned 50 pixels right of arrow tip
            ay=-30,  # Text positioned 30 pixels above arrow tip
        )

        # DiD result annotation - positioned higher up to avoid collision
        fig.add_annotation(
            x=3,
            y=87,  # Moved higher up
            text="DiD = 15 - 10 = +5",
            showarrow=False,
            bgcolor="yellow",
            bordercolor="black",
            borderwidth=2,
            font=dict(size=14, color="black", weight="bold"),
        )

        title = "Difference-in-Differences Calculation"

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Retention Rate (%)",
        xaxis=dict(range=[0.5, 4.5], dtick=1),
        yaxis=dict(range=[60, 95]),
        width=700,
        height=500,
        showlegend=True,
    )

    return fig


def render(navigate_to):
    # Back button
    if st.button("← Back to Home"):
        navigate_to("home")

    # Initialize session state
    if "lesson5_step" not in st.session_state:
        st.session_state.lesson5_step = 1
        st.session_state.did_stage = "parallel"
        st.session_state.show_math = False

    # Step 1: Introduction
    st.title("📈 Difference-in-Differences")

    st.markdown(
        """
    So far we've seen:
    - **Selection bias**: the wrong users sign up first.
    - **Confounders**: hidden traits create spurious effects.
    - **Randomised trials**: the gold standard to isolate cause.
    - **Instruments**: clever tricks when randomisation isn't possible.
    
    Randomised trials are great — but life isn't always that simple.
    """
    )

    if st.session_state.lesson5_step >= 2:
        st.markdown(
            """
        What happens if:
        - You can't split users individually,
        - Or business/legislation forces a rollout in one territory first,
        - Or you have staggered launches across regions?
        
        Imagine our company runs in multiple territories. In Territory A, the government passes a law forcing us to roll out a new feature **two years earlier** than in Territory B.
        
        We want to see: will this feature affect customer retention? If yes, we can plan ahead for Territory B.
        
        We didn't randomise! The timing was forced. Can we still estimate the effect?
        
        Yes — by using **Difference-in-Differences (DiD)**.
        """
        )

    # Step 2: Scenario Setup
    if st.session_state.lesson5_step >= 3:
        st.header("🎯 Scenario Setup")

        st.markdown(
            """
        Here's the plan:
        
        - Territory A gets the feature first (due to the law).
        - Territory B is delayed by 2 years.
        - Both territories were already trending upward in retention before the feature.
        
        The key idea:
        We compare **how much each territory changes over time**.
        - Change in A = observed effect + general trend
        - Change in B = general trend alone
        - DiD = Change in A − Change in B → isolates the feature's causal effect
        """
        )

    # Step 3: Mini-Game Instructions
    if st.session_state.lesson5_step >= 4:
        st.header("🎮 Mini-Game Instructions")

        st.info(
            """
        **Goal:**
        1. Explore retention trends in both territories.
        2. Observe how A and B trend over time.
        3. Use the Difference-in-Differences idea to compute the causal effect.
        
        **Your task:**
        Step through the graph year by year, and uncover the "extra bump" caused by the feature.
        """
        )

    # Step 4: Interactive Mini-Game
    if st.session_state.lesson5_step >= 5:
        st.header("📊 Interactive Analysis")

        # Generate data
        years, retention_a, retention_b = generate_territory_data()

        # Stage progression buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button(
                "1. Show Parallel Trends\n(Years 1-2)", use_container_width=True
            ):
                st.session_state.did_stage = "parallel"
                st.rerun()

        with col2:
            if st.button(
                "2. Territory A Spikes\n(Feature Effect?)", use_container_width=True
            ):
                st.session_state.did_stage = "spike"
                st.rerun()

        with col3:
            if st.button(
                "3. Territory B Trends Too\n(General Trend!)", use_container_width=True
            ):
                st.session_state.did_stage = "reveal_trend"
                st.rerun()

        with col4:
            if st.button("4. Calculate DiD\n(True Effect)", use_container_width=True):
                st.session_state.did_stage = "full_did"
                st.rerun()

        # Display the plot
        fig = create_retention_plot(
            years, retention_a, retention_b, st.session_state.did_stage
        )
        st.plotly_chart(fig, use_container_width=True)

        # Contextual explanations based on current stage
        if st.session_state.did_stage == "parallel":
            st.info(
                "**Stage 1 - Parallel Trends:** Both territories show similar upward trends before any intervention. This suggests they're comparable."
            )

        elif st.session_state.did_stage == "spike":
            st.warning(
                """
            **Stage 2 - Naive Analysis:** Territory A jumps up after the feature! 
            
            🤔 **If we stopped here, we might think:** "The feature caused a +10 point increase!"
            
            But wait... we have a comparison group that used to trend similarly. Let's see what happened to them.
            """
            )

        elif st.session_state.did_stage == "reveal_trend":
            st.warning(
                """
            **Stage 3 - The Plot Thickens:** Territory B ALSO increased over the same period!
            
            🧠 **Key Insight:** Maybe both territories were naturally trending upward due to:
            - Market conditions
            - Seasonal effects  
            - Company-wide improvements
            
            The naive +10 estimate is **confounded** by this general trend.
            """
            )

        elif st.session_state.did_stage == "full_did":
            st.success(
                """
            **Stage 4 - DiD Analysis:** Now we can isolate the true causal effect!
            
            - Territory A change (Year 2 → Year 4): **+15 points**
            - Territory B change (Year 2 → Year 4): **+10 points**  
            - **Difference-in-Differences**: 15 - 10 = **+5 points**
            
            The feature's true causal effect is +5 points, not the naive +10 estimate.
            """
            )

            # Show numerical breakdown
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Territory A Change", "+15 pp", help="Feature + general trend"
                )
            with col2:
                st.metric("Territory B Change", "+10 pp", help="General trend only")
            with col3:
                st.metric(
                    "True Feature Effect", "+5 pp", help="DiD isolates causal effect"
                )

    # Step 5: Key Takeaways
    if st.session_state.lesson5_step >= 6:
        st.header("🎓 Key Takeaways")

        st.success(
            """
        - **Randomised trials** are still gold standard.
        - When you can't randomise, **DiD** allows you to estimate causal effects from staggered rollouts.
        - Works by comparing **changes over time**, not raw levels.
        - Assumes **parallel trends**: both groups would have trended similarly without the feature.
        """
        )

        st.warning(
            """
        **⚠️ Key Assumption: Parallel Trends**
        
        DiD only works if Territory A and B would have followed similar trends without the feature. 
        If A was naturally accelerating faster than B anyway, our estimate would be biased.
        """
        )

    # Optional Math Section
    if st.session_state.lesson5_step >= 6 and st.session_state.show_math:
        st.divider()
        st.header("📚 Optional Math Corner")

        st.subheader("Difference-in-Differences Formula")

        st.latex(
            r"""
        \text{ATE}_{\text{DiD}} = (Y_{\text{After,A}} - Y_{\text{Before,A}}) - (Y_{\text{After,B}} - Y_{\text{Before,B}})
        """
        )

        st.markdown(
            """
        - **First difference**: Change in treatment group (A)
        - **Second difference**: Change in control group (B)  
        - **Subtracting B's change** removes background trends
        """
        )

        st.subheader("Our Example")
        st.latex(
            r"""
        \begin{align}
        \text{Territory A change} &= 85 - 70 = 15 \\
        \text{Territory B change} &= 78 - 68 = 10 \\
        \text{DiD} &= 15 - 10 = 5
        \end{align}
        """
        )

        st.success(
            """
        **Key Insight:**
        If parallel trends hold, DiD provides an unbiased causal estimate even without individual randomisation.
        """
        )

    # Navigation
    st.divider()

    if st.session_state.lesson5_step < 6:
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state.lesson5_step += 1
            st.rerun()
    else:
        # Final navigation options
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Start Over", use_container_width=True):
                st.session_state.lesson5_step = 1
                st.session_state.did_stage = "parallel"
                st.session_state.show_math = False
                st.rerun()

        with col2:
            st.info("🚧 More lessons coming soon!")

        with col3:
            if st.button("♾️ Optional Maths", use_container_width=True):
                st.session_state.show_math = not st.session_state.show_math
                st.rerun()
