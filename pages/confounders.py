import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def generate_classroom_data(n_students=500):
    """Generate classroom hours vs grades data with confounders"""
    np.random.seed(42)

    # Generate confounders
    motivation = np.random.normal(50, 15, n_students)  # 0-100 scale
    teacher_quality = np.random.choice(
        [30, 50, 70, 90], n_students
    )  # Different teachers
    family_support = np.random.normal(60, 20, n_students)  # 0-100 scale

    # Motivation affects both class attendance AND grades
    # Family support affects both class attendance AND grades
    # Teacher quality affects both (students seek out good teachers AND good teachers improve grades)

    # Class hours influenced by confounders
    base_hours = 15  # Base hours per week
    hours_from_motivation = motivation * 0.3  # More motivated = more hours
    hours_from_family = family_support * 0.2  # More support = more hours
    hours_from_teacher = (teacher_quality - 50) * 0.1  # Good teachers = more attendance

    classroom_hours = (
        base_hours
        + hours_from_motivation
        + hours_from_family
        + hours_from_teacher
        + np.random.normal(0, 3, n_students)
    )
    classroom_hours = np.clip(classroom_hours, 5, 40)  # Reasonable bounds

    # Grades influenced by confounders AND class hours
    base_grade = 50
    grade_from_motivation = motivation * 0.4  # Motivation directly improves grades
    grade_from_family = family_support * 0.3  # Family support directly improves grades
    grade_from_teacher = (
        teacher_quality - 50
    ) * 0.2  # Good teachers directly improve grades
    grade_from_hours = classroom_hours * 0.5  # Class hours have some effect, but small

    grades = (
        base_grade
        + grade_from_motivation
        + grade_from_family
        + grade_from_teacher
        + grade_from_hours
        + np.random.normal(0, 5, n_students)
    )
    grades = np.clip(grades, 0, 100)

    return pd.DataFrame(
        {
            "classroom_hours": classroom_hours,
            "grades": grades,
            "motivation": motivation,
            "teacher_quality": teacher_quality,
            "family_support": family_support,
        }
    )


def generate_treated_data(n_students=500):
    """Generate data for students affected by the new school rule"""
    np.random.seed(43)  # Different seed for variation

    # Same confounders as before
    motivation = np.random.normal(50, 15, n_students)
    teacher_quality = np.random.choice([30, 50, 70, 90], n_students)
    family_support = np.random.normal(60, 20, n_students)

    # The rule FORCES extra hours, independent of motivation/family
    base_hours = 15
    hours_from_motivation = motivation * 0.3  # Same relationship
    hours_from_family = family_support * 0.2  # Same relationship
    hours_from_teacher = (teacher_quality - 50) * 0.1  # Same relationship

    # NEW: Add forced extra hours from the rule (independent of confounders)
    forced_extra_hours = np.random.uniform(3, 8, n_students)  # Rule adds 3-8 hours

    classroom_hours = (
        base_hours
        + hours_from_motivation
        + hours_from_family
        + hours_from_teacher
        + forced_extra_hours
        + np.random.normal(0, 2, n_students)
    )
    classroom_hours = np.clip(classroom_hours, 5, 45)

    # Grades: same confounder effects + smaller causal effect from extra hours
    base_grade = 50
    grade_from_motivation = motivation * 0.4  # Same as before
    grade_from_family = family_support * 0.3  # Same as before
    grade_from_teacher = (teacher_quality - 50) * 0.2  # Same as before

    # TRUE CAUSAL EFFECT: much smaller than correlation suggests
    grade_from_hours = classroom_hours * 0.2  # Smaller effect than before (0.2 vs 0.5)

    grades = (
        base_grade
        + grade_from_motivation
        + grade_from_family
        + grade_from_teacher
        + grade_from_hours
        + np.random.normal(0, 5, n_students)
    )
    grades = np.clip(grades, 0, 100)

    return pd.DataFrame(
        {
            "classroom_hours": classroom_hours,
            "grades": grades,
            "motivation": motivation,
            "teacher_quality": teacher_quality,
            "family_support": family_support,
            "forced_extra_hours": forced_extra_hours,
        }
    )


def create_scatter_plot(data, show_confounders=False):
    """Create scatter plot of classroom hours vs grades"""
    fig = go.Figure()

    if not show_confounders:
        # Simple scatter plot
        fig.add_trace(
            go.Scatter(
                x=data["classroom_hours"],
                y=data["grades"],
                mode="markers",
                marker=dict(color="blue", size=6, opacity=0.6),
                name="Students",
                text=[
                    f"Hours: {h:.1f}<br>Grade: {g:.1f}"
                    for h, g in zip(data["classroom_hours"], data["grades"])
                ],
                hovertemplate="%{text}<extra></extra>",
            )
        )

        # Add trendline
        z = np.polyfit(data["classroom_hours"], data["grades"], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(
            data["classroom_hours"].min(), data["classroom_hours"].max(), 100
        )
        fig.add_trace(
            go.Scatter(
                x=x_trend,
                y=p(x_trend),
                mode="lines",
                line=dict(color="red", width=2),
                name="Trend Line",
            )
        )

        title = "Classroom Hours vs Grades - Strong Positive Correlation!"

    else:
        # Color by motivation level
        fig.add_trace(
            go.Scatter(
                x=data["classroom_hours"],
                y=data["grades"],
                mode="markers",
                marker=dict(
                    color=data["motivation"],
                    colorscale="RdYlBu_r",
                    size=6,
                    opacity=0.7,
                    colorbar=dict(title="Motivation Level"),
                ),
                name="Students",
                text=[
                    f"Hours: {h:.1f}<br>Grade: {g:.1f}<br>Motivation: {m:.1f}"
                    for h, g, m in zip(
                        data["classroom_hours"], data["grades"], data["motivation"]
                    )
                ],
                hovertemplate="%{text}<extra></extra>",
            )
        )

        title = "Same Data, Colored by Motivation - See the Confounder!"

    fig.update_layout(
        title=title,
        xaxis_title="Weekly Classroom Hours",
        yaxis_title="Final Grade (%)",
        width=700,
        height=500,
        showlegend=False,
    )

    return fig


def create_instrumental_comparison_plot(original_data, treated_data):
    """Create comparison plot showing original vs treated groups"""
    fig = go.Figure()

    # Original group (red)
    fig.add_trace(
        go.Scatter(
            x=original_data["classroom_hours"],
            y=original_data["grades"],
            mode="markers",
            marker=dict(color="red", size=6, opacity=0.6),
            name="Original Group (Before Rule)",
            text=[
                f"Hours: {h:.1f}<br>Grade: {g:.1f}"
                for h, g in zip(
                    original_data["classroom_hours"], original_data["grades"]
                )
            ],
            hovertemplate="%{text}<extra></extra>",
        )
    )

    # Treated group (blue)
    fig.add_trace(
        go.Scatter(
            x=treated_data["classroom_hours"],
            y=treated_data["grades"],
            mode="markers",
            marker=dict(color="blue", size=6, opacity=0.6),
            name="Treated Group (After Rule)",
            text=[
                f"Hours: {h:.1f}<br>Grade: {g:.1f}"
                for h, g in zip(treated_data["classroom_hours"], treated_data["grades"])
            ],
            hovertemplate="%{text}<extra></extra>",
        )
    )

    # Add trendlines
    # Original group trendline (steeper - confounded)
    z1 = np.polyfit(original_data["classroom_hours"], original_data["grades"], 1)
    p1 = np.poly1d(z1)
    x_trend1 = np.linspace(
        original_data["classroom_hours"].min(),
        original_data["classroom_hours"].max(),
        100,
    )
    fig.add_trace(
        go.Scatter(
            x=x_trend1,
            y=p1(x_trend1),
            mode="lines",
            line=dict(color="darkred", width=2),
            name="Original Trend (Confounded)",
            showlegend=False,
        )
    )

    # Treated group trendline (less steep - true causal effect)
    z2 = np.polyfit(treated_data["classroom_hours"], treated_data["grades"], 1)
    p2 = np.poly1d(z2)
    x_trend2 = np.linspace(
        treated_data["classroom_hours"].min(),
        treated_data["classroom_hours"].max(),
        100,
    )
    fig.add_trace(
        go.Scatter(
            x=x_trend2,
            y=p2(x_trend2),
            mode="lines",
            line=dict(color="darkblue", width=2),
            name="Treated Trend (True Causal Effect)",
            showlegend=False,
        )
    )

    fig.update_layout(
        title="Instrumental Variables: Original vs Rule-Affected Students",
        xaxis_title="Weekly Classroom Hours",
        yaxis_title="Final Grade (%)",
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
    if "lesson3_step" not in st.session_state:
        st.session_state.lesson3_step = 1
        st.session_state.show_confounders = False

    # Lesson Title
    st.title("🧩 Understanding Confounders")

    # Step 1: What Are We Trying to Answer?
    st.header("🎯 The Core Question in Causality")
    st.markdown(
        """
    In causality we are trying to answer:

    **If we apply a treatment (i.e., change something in the world), what is the effect of that treatment on an outcome?**
    
    Sometimes, this can be straightforward (we hope): *Turning on a light makes the room brighter.*
    
    But what happens if that treatment is highly linked to other things (the other things we can call **confounders**)?
    """
    )

    # Step 2: The Classroom Example
    if st.session_state.lesson3_step >= 2:
        st.header("📚 Example: Classroom Hours → Grades")

        st.markdown("Imagine we want to know:")
        st.info("**If students spend more hours in class, do their grades improve?**")

        # Generate and show the data
        data = generate_classroom_data()

        st.markdown(
            "At first glance, if we plot classroom hours against grades, it might look like a nice upward-sloping line — more hours, better grades."
        )

        fig = create_scatter_plot(data, show_confounders=False)
        st.plotly_chart(fig, use_container_width=True)

        # Calculate correlation
        correlation = np.corrcoef(data["classroom_hours"], data["grades"])[0, 1]
        st.success(
            f"📈 **Strong positive correlation: {correlation:.3f}** - More hours, better grades!"
        )

    # Step 3: But Is That The Full Story?
    if st.session_state.lesson3_step >= 3:
        st.header("🤔 But Is That The Full Story?")

        st.markdown(
            """
        Students who attend more classes might also be:
        - More **motivated**
        - Have better **teachers** 
        - Come from more supportive **families**
        
        These factors (motivation, teacher quality, family support) are **confounders** because they affect **both** classroom hours **and** grades.
        
        So, the observed relationship might not reflect the true causal effect of classroom hours — it's mixed up with these other influences.
        """
        )

    # Step 4: What Can We Do About Confounders?
    if st.session_state.lesson3_step >= 4:
        st.header("✅ What Can We Do About Confounders?")

        st.markdown(
            """
        If we just compare students who attend more classes with those who attend fewer, we can't be sure whether the difference in grades is due to classroom hours or due to motivation, teacher quality, or family support.

        So, how do we isolate the true causal effect of classroom hours?
        """
        )

        st.header("🛠 Enter the Instrument")
        st.markdown(
            """
        An instrument is something that:

        1. **Affects the treatment** (in this case, classroom hours).
        2. **Does NOT directly affect the outcome** (grades), except through the treatment.
        """
        )

    # Step 5: Pick an Instrument
    if st.session_state.lesson3_step >= 5:
        st.header("Pick an instrument we could use:")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("A) Student motivation", use_container_width=True):
                st.error(
                    "❌ **Incorrect!** Motivation is a confounder - it affects both classroom hours AND grades directly."
                )

        with col2:
            if st.button(
                "B) A new school rule requiring extra class hours",
                use_container_width=True,
            ):
                st.success("✅ **Correct!** This is a good instrument because:")
                st.markdown(
                    """
                - It changes classroom hours (treatment)
                - It doesn't directly make students smarter or change their family background (so it doesn't directly affect grades)
                """
                )

        with col3:
            if st.button("C) Teacher quality", use_container_width=True):
                st.error(
                    "❌ **Incorrect!** Teacher quality is a confounder - it affects both classroom hours AND grades directly."
                )

        if st.session_state.lesson3_step >= 6:
            st.info(
                "**A and C are confounders, not instruments, because they affect both classroom hours and grades.**"
            )

    # Step 6: Before and After Comparison
    if st.session_state.lesson3_step >= 6:
        st.header("📊 Before-and-After Comparison")

        st.markdown("**Before the rule:**")
        st.markdown(
            "Students decide how many hours to attend. This choice is influenced by motivation, teacher quality, and family support — all confounders."
        )

        st.markdown("**After the rule:**")
        st.markdown(
            "Some students are forced to attend more hours because of the new law. Their classroom hours increase, even though their motivation or family background stays the same."
        )

    # Step 7: Visual Comparison
    if st.session_state.lesson3_step >= 7:
        st.header("How would this look visually?")
        st.markdown(
            "Let's plot Classroom Hours vs Grades AFTER the law in blue and the ORIGINAL class in red."
        )

        # Generate and show the comparison data
        original_data = generate_classroom_data()
        treated_data = generate_treated_data()

        fig = create_instrumental_comparison_plot(original_data, treated_data)
        st.plotly_chart(fig, use_container_width=True)

    # Step 8: What Does the Scatter Plot Show?
    if st.session_state.lesson3_step >= 8:
        st.header("✅ What Does the Scatter Plot Show?")

        st.markdown(
            "**Red points:** The original group of students (before the rule), showing the natural variation in classroom hours and grades. This line looks strongly positive because motivated students both attend more and score higher."
        )

        st.markdown(
            '**Blue points:** The group affected by the new rule. They were "pushed" to attend more hours, so their classroom hours increase (shift to the right), but their grades only improve by the true causal effect — not as much as the red trend suggests.'
        )

    # Navigation
    st.divider()

    if st.session_state.lesson3_step >= 8:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Start Over", use_container_width=True):
                st.session_state.lesson3_step = 1
                st.session_state.show_math = False
                st.rerun()
        with col2:
            st.info("🚧 More lessons coming soon!")
        with col3:
            if st.button("♾️ Optional Maths", use_container_width=True):
                st.session_state.show_math = True
                st.rerun()

        # Optional Math Section
        if getattr(st.session_state, "show_math", False):
            st.divider()
            st.header("🔢 Calculating the Average Treatment Effect (ATE)")

            st.subheader("Naive Approach (Before Instrument)")
            st.markdown("If we just compare students who attend more vs fewer hours:")

            st.latex(
                r"""
            \text{Effect}_{\text{naive}} = \frac{\text{Average Grades (High Hours)} - \text{Average Grades (Low Hours)}}{\text{Average Hours (High)} - \text{Average Hours (Low)}}
            """
            )

            st.markdown("**Example:**")
            st.markdown(
                """
            - High-attendance students: 85 points, 10 hours/week
            - Low-attendance students: 70 points, 5 hours/week
            """
            )

            st.latex(
                r"""
            \text{Effect}_{\text{naive}} = \frac{85 - 70}{10 - 5} = 3 \text{ points per extra hour}
            """
            )

            st.error(
                "**Looks huge! But this is biased because motivated students both attend more and score higher.**"
            )

            st.subheader("Instrument-Based Approach (After Adding the Rule)")
            st.markdown("Now, use the variation caused by the rule:")

            st.latex(
                r"""
            \text{Effect}_{\text{IV}} = \frac{\text{Average Grades (Rule Group)} - \text{Average Grades (No Rule Group)}}{\text{Average Hours (Rule Group)} - \text{Average Hours (No Rule Group)}}
            """
            )

            st.markdown("**Example:**")
            st.markdown(
                """
            - Rule group: 78 points, 8 hours/week
            - No-rule group: 74 points, 6 hours/week
            """
            )

            st.latex(
                r"""
            \text{Effect}_{\text{IV}} = \frac{78 - 74}{8 - 6} = 2 \text{ points per extra hour}
            """
            )

            st.success(
                """
            **✅ Key Insight:**
            
            - **Naive estimate:** 3 points/hour (inflated by confounders)
            - **Instrument-based estimate:** 2 points/hour (closer to the true causal effect)
            """
            )
    else:
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state.lesson3_step += 1
            st.rerun()
