import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random


def generate_user_data():
    """Generate synthetic user data for the matching exercise"""
    random.seed(42)
    np.random.seed(42)

    all_users = []

    # Generate many Premium users for initial display (show confounding)
    premium_configs_full = [
        {"age": 45, "income": 85000, "churned": False},  # Older, High
        {"age": 52, "income": 95000, "churned": True},  # Older, High
        {"age": 38, "income": 65000, "churned": False},  # Middle, Medium
        {"age": 41, "income": 75000, "churned": False},  # Middle, High
        {"age": 29, "income": 45000, "churned": True},  # Young, Medium
        {"age": 48, "income": 90000, "churned": False},  # Older, High
        {"age": 43, "income": 72000, "churned": True},  # Middle, Medium
        {"age": 55, "income": 105000, "churned": False},  # Older, High
        {"age": 35, "income": 58000, "churned": False},  # Middle, Medium
        {"age": 27, "income": 42000, "churned": True},  # Young, Medium
    ]

    for i, config in enumerate(premium_configs_full):
        user = {
            "id": f"P{i+1}",
            "type": "premium",
            "age": config["age"],
            "income": config["income"],
            "churned": config["churned"],
            "color": "red",
        }
        all_users.append(user)

    # Generate many Free users for initial display
    free_configs_full = [
        {"age": 26, "income": 35000, "churned": True},  # Young, Low
        {"age": 31, "income": 42000, "churned": True},  # Young, Medium
        {"age": 44, "income": 68000, "churned": False},  # Middle, Medium
        {"age": 28, "income": 38000, "churned": True},  # Young, Low
        {"age": 50, "income": 82000, "churned": False},  # Older, High
        {"age": 39, "income": 55000, "churned": True},  # Middle, Medium
        {"age": 24, "income": 32000, "churned": True},  # Young, Low
        {"age": 33, "income": 48000, "churned": True},  # Young, Medium
        {"age": 47, "income": 78000, "churned": False},  # Middle, High
        {"age": 29, "income": 41000, "churned": True},  # Young, Medium
        {"age": 36, "income": 52000, "churned": False},  # Middle, Medium
        {"age": 53, "income": 88000, "churned": False},  # Older, High
        {"age": 25, "income": 36000, "churned": True},  # Young, Low
        {"age": 42, "income": 64000, "churned": True},  # Middle, Medium
        {"age": 49, "income": 76000, "churned": False},  # Middle, High
    ]

    for i, config in enumerate(free_configs_full):
        user = {
            "id": f"F{i+1}",
            "type": "free",
            "age": config["age"],
            "income": config["income"],
            "churned": config["churned"],
            "color": "blue",
        }
        all_users.append(user)

    return all_users


def get_matching_subset():
    """Get a smaller subset designed for 1:1 matching with guaranteed matches"""
    # 5 Premium users that need matches - carefully designed buckets
    premium_subset = [
        {
            "id": "P1",
            "type": "premium",
            "age": 52,
            "income": 85000,
            "churned": False,
        },  # Older, High
        {
            "id": "P2",
            "type": "premium",
            "age": 38,
            "income": 55000,
            "churned": False,
        },  # Middle, Medium
        {
            "id": "P3",
            "type": "premium",
            "age": 28,
            "income": 45000,
            "churned": True,
        },  # Young, Medium
        {
            "id": "P4",
            "type": "premium",
            "age": 41,
            "income": 35000,
            "churned": True,
        },  # Middle, Low
        {
            "id": "P5",
            "type": "premium",
            "age": 25,
            "income": 38000,
            "churned": True,
        },  # Young, Low
    ]

    # 8 Free users - ensuring each premium has at least one clear match
    free_subset = [
        # Matches for P1 (Older, High)
        {
            "id": "F1",
            "type": "free",
            "age": 53,
            "income": 88000,
            "churned": False,
        },  # Older, High
        {
            "id": "F2",
            "type": "free",
            "age": 51,
            "income": 92000,
            "churned": True,
        },  # Older, High
        # Matches for P2, P4 (Middle, Medium/Low)
        {
            "id": "F3",
            "type": "free",
            "age": 42,
            "income": 55000,
            "churned": False,
        },  # Middle, Medium
        {
            "id": "F4",
            "type": "free",
            "age": 39,
            "income": 35000,
            "churned": True,
        },  # Middle, Low
        {
            "id": "F5",
            "type": "free",
            "age": 44,
            "income": 32000,
            "churned": True,
        },  # Middle, Low
        # Matches for P3, P5 (Young, Medium/Low)
        {
            "id": "F6",
            "type": "free",
            "age": 29,
            "income": 42000,
            "churned": True,
        },  # Young, Medium
        {
            "id": "F7",
            "type": "free",
            "age": 27,
            "income": 38000,
            "churned": False,
        },  # Young, Low
        {
            "id": "F8",
            "type": "free",
            "age": 26,
            "income": 35000,
            "churned": True,
        },  # Young, Low
    ]

    all_subset = []
    for config in premium_subset + free_subset:
        all_subset.append(
            {
                "id": config["id"],
                "type": config["type"],
                "age": config["age"],
                "income": config["income"],
                "churned": config["churned"],
                "color": "red" if config["type"] == "premium" else "blue",
            }
        )

    return all_subset


def create_age_bucket(age):
    """Convert exact age to coarse bucket"""
    if age < 30:
        return "Young"
    elif age < 50:
        return "Middle-aged"
    else:
        return "Older"


def create_income_bucket(income):
    """Convert exact income to coarse bucket"""
    if income < 40000:
        return "Low"
    elif income < 80000:
        return "Medium"
    else:
        return "High"


def render_stickman(user_type, user_id, selected=False):
    """Create a simple stick figure representation"""
    color = "red" if user_type == "premium" else "blue"
    style = "border: 3px solid gold;" if selected else ""

    return f"""
    <div style="text-align: center; cursor: pointer; padding: 10px; {style}">
        <div style="font-size: 40px; color: {color};">🚶</div>
        <div style="font-size: 12px; font-weight: bold;">{user_id}</div>
    </div>
    """


def calculate_naive_effect(users):
    """Calculate naive treatment effect without matching"""
    premium_users = [u for u in users if u["type"] == "premium"]
    free_users = [u for u in users if u["type"] == "free"]

    premium_churn_rate = sum(u["churned"] for u in premium_users) / len(premium_users)
    free_churn_rate = sum(u["churned"] for u in free_users) / len(free_users)

    return free_churn_rate - premium_churn_rate


def find_matches(users, selected_premium_id, selected_free_id):
    """Find exact matches based on coarsened attributes"""
    premium_user = next(u for u in users if u["id"] == selected_premium_id)
    free_user = next(u for u in users if u["id"] == selected_free_id)

    premium_age_bucket = create_age_bucket(premium_user["age"])
    premium_income_bucket = create_income_bucket(premium_user["income"])

    free_age_bucket = create_age_bucket(free_user["age"])
    free_income_bucket = create_income_bucket(free_user["income"])

    return {
        "premium_user": premium_user,
        "free_user": free_user,
        "age_match": premium_age_bucket == free_age_bucket,
        "income_match": premium_income_bucket == free_income_bucket,
        "perfect_match": premium_age_bucket == free_age_bucket
        and premium_income_bucket == free_income_bucket,
        "premium_buckets": (premium_age_bucket, premium_income_bucket),
        "free_buckets": (free_age_bucket, free_income_bucket),
    }


def render(navigate_to):
    # Back button
    if st.button("← Back to Home"):
        navigate_to("home")

    # Initialize session state
    if "lesson6_step" not in st.session_state:
        st.session_state.lesson6_step = 1
        st.session_state.all_users = generate_user_data()
        st.session_state.matching_users = get_matching_subset()
        st.session_state.selected_premium = None
        st.session_state.selected_free = None
        st.session_state.matches_found = []
        st.session_state.show_naive = False
        st.session_state.show_matching = False
        st.session_state.show_buckets = False
        st.session_state.use_subset = False

    users = (
        st.session_state.matching_users
        if st.session_state.use_subset
        else st.session_state.all_users
    )

    # Step 1: Introduction
    st.title("🎯 Coarsened Exact Matching")

    st.markdown(
        """
    So far we've learned about randomised experiments and difference-in-differences. These are powerful tools!
    
    But what happens when **the treatment itself would be biased** if we applied it randomly?
    """
    )

    if st.session_state.lesson6_step >= 2:
        st.header("🏢 Real-World Scenario")

        st.markdown(
            """
        Imagine you work at a tech company. You want to find out: 
        
        **"Do users who pay for our Premium Analytics Dashboard churn less than free users?"**
        
        This could help you decide whether to invest more in premium features.
        """
        )

    if st.session_state.lesson6_step >= 3:
        st.header("🧪 Can We A/B Test This?")

        st.markdown(
            """
        Let's think about running an A/B test:
        - **Group A**: Give premium features for free
        - **Group B**: Keep them on free tier
        
        **What's the problem here? 🤔**
        """
        )

        if st.button("🤔 Click to reveal the issue"):
            st.error(
                """
            **The Problem:** If we give premium features for free, that's not real user behavior! 
            
            People who *choose* to pay are fundamentally different from people who get it free.
            This would massively bias our results.
            """
            )

    if st.session_state.lesson6_step >= 4:
        st.header("💡 Alternative Approach")

        st.markdown(
            """
        Since we can't randomise, let's look at **observational data**:
        - Compare existing premium users vs existing free users
        - See who churns more
        
        Simple correlation analysis, right? Let's see...
        """
        )

    if st.session_state.lesson6_step >= 5:
        st.header("👥 Meet Our Users")

        st.markdown("**Premium Users (🔴 Red) vs Free Users (🔵 Blue)**")
        st.caption("*Click on users to see their details*")

        # Display users in two columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔴 Premium Users")
            premium_users = [u for u in users if u["type"] == "premium"]

            for user in premium_users:
                if st.button(
                    f"🚶 {user['id']}",
                    key=f"preview_prem_{user['id']}",
                    help=f"Age: {user['age']}, Income: £{user['income']:,}, Churned: {'Yes' if user['churned'] else 'No'}",
                ):
                    st.info(
                        f"**{user['id']}**: Age {user['age']}, Income £{user['income']:,}, {'Churned' if user['churned'] else 'Stayed'}"
                    )

        with col2:
            st.subheader("🔵 Free Users")
            free_users = [u for u in users if u["type"] == "free"]

            for user in free_users:
                if st.button(
                    f"🚶 {user['id']}",
                    key=f"preview_free_{user['id']}",
                    help=f"Age: {user['age']}, Income: £{user['income']:,}, Churned: {'Yes' if user['churned'] else 'No'}",
                ):
                    st.info(
                        f"**{user['id']}**: Age {user['age']}, Income £{user['income']:,}, {'Churned' if user['churned'] else 'Stayed'}"
                    )

    if st.session_state.lesson6_step >= 6:
        st.header("📊 Naive Analysis")

        if st.button("🔍 Calculate Naive Treatment Effect"):
            st.session_state.show_naive = True
            st.rerun()

        if st.session_state.show_naive:
            naive_effect = calculate_naive_effect(users)

            premium_churn = sum(
                u["churned"] for u in users if u["type"] == "premium"
            ) / len([u for u in users if u["type"] == "premium"])
            free_churn = sum(u["churned"] for u in users if u["type"] == "free") / len(
                [u for u in users if u["type"] == "free"]
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Premium Churn Rate", f"{premium_churn:.1%}")
            with col2:
                st.metric("Free Churn Rate", f"{free_churn:.1%}")
            with col3:
                st.metric(
                    "Naive Effect",
                    f"{naive_effect:.1%}",
                    help="Free churn rate - Premium churn rate",
                )

            st.success(
                "🎉 Wow! Premium users churn much less! The premium feature must be amazing!"
            )

            st.warning(
                "**But wait...** Let's take a closer look at the user attributes..."
            )

    if st.session_state.lesson6_step >= 7:
        st.header("🔍 The Hidden Pattern")

        st.markdown(
            """
        Look closely at the premium vs free users:
        - **Premium users**: Tend to be older and wealthier
        - **Free users**: Tend to be younger and less wealthy
        
        Older, wealthier users probably churn less anyway - regardless of premium features!
        
        Our "treatment effect" is **confounded** by age and wealth.
        """
        )

    if st.session_state.lesson6_step >= 8:
        st.header("🎯 Coarsened Exact Matching")

        st.markdown(
            """
        **Solution**: Instead of comparing all premium vs all free users, let's compare users who are similar in other ways.
        
        **Step 1**: Convert exact attributes to coarse buckets:
        - **Age**: Young (<30), Middle-aged (30-49), Older (50+)  
        - **Income**: Low (<£40k), Medium (£40k-80k), High (>£80k)
        
        **Step 2**: Only compare users in the same buckets.
        """
        )

        if st.button("🪣 Apply Bucketing to Users"):
            st.session_state.show_buckets = True
            st.rerun()

        if st.session_state.show_buckets:
            st.success(
                "✅ **Bucketing Applied!** Users are now grouped into coarse categories:"
            )

            col1, col2 = st.columns(2)
            with col1:
                st.info(
                    """
                **Age Buckets:**
                - 🟢 Young: Under 30
                - 🟡 Middle-aged: 30-49  
                - 🔴 Older: 50+
                """
                )
            with col2:
                st.info(
                    """
                **Income Buckets:**
                - 💰 Low: Under £40k
                - 💰💰 Medium: £40k-80k
                - 💰💰💰 High: Over £80k
                """
                )

            st.markdown(
                "👇 **Notice how the user information now shows bucket categories instead of exact numbers!**"
            )

    if st.session_state.lesson6_step >= 9:
        st.header("🎮 Interactive Matching Game")

        st.markdown(
            """
        **Your task**: Select one premium user and one free user who are in the same buckets.
        Find all possible matches to get the true treatment effect!
        """
        )

        # Switch to the matching subset (5 premium + 8 free users with guaranteed matches)
        if not st.session_state.use_subset:
            st.session_state.use_subset = True
            users = st.session_state.matching_users

        # Display users in two columns with bucket info if bucketing is shown
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔴 Premium Users")
            premium_users = [u for u in users if u["type"] == "premium"]

            for i, user in enumerate(premium_users):
                # Check if this user is already matched
                already_matched = any(
                    match["premium_user"]["id"] == user["id"]
                    for match in st.session_state.matches_found
                )

                if not already_matched:
                    selected = st.session_state.selected_premium == user["id"]

                    if st.session_state.show_buckets:
                        age_bucket = create_age_bucket(user["age"])
                        income_bucket = create_income_bucket(user["income"])
                        button_text = f"🚶 {user['id']}"
                        help_text = f"{age_bucket}, {income_bucket}, Churned: {'Yes' if user['churned'] else 'No'}"
                    else:
                        button_text = f"🚶 {user['id']}"
                        help_text = f"Age: {user['age']}, Income: £{user['income']:,}, Churned: {'Yes' if user['churned'] else 'No'}"

                    if st.button(
                        button_text, key=f"match_prem_{user['id']}", help=help_text
                    ):
                        st.session_state.selected_premium = user["id"]
                        st.rerun()

                    if selected:
                        st.markdown("**🟡 SELECTED**")
                        if st.session_state.show_buckets:
                            st.caption(f"Age: {create_age_bucket(user['age'])}")
                            st.caption(
                                f"Income: {create_income_bucket(user['income'])}"
                            )
                        else:
                            st.caption(f"Age: {user['age']}")
                            st.caption(f"Income: £{user['income']:,}")
                        st.caption(f"Churned: {'Yes' if user['churned'] else 'No'}")
                else:
                    st.success(f"✅ {user['id']} - Already Matched")

        with col2:
            st.subheader("🔵 Free Users")
            free_users = [u for u in users if u["type"] == "free"]

            for i, user in enumerate(free_users):
                # Check if this user is already matched
                already_matched = any(
                    match["free_user"]["id"] == user["id"]
                    for match in st.session_state.matches_found
                )

                if not already_matched:
                    selected = st.session_state.selected_free == user["id"]

                    if st.session_state.show_buckets:
                        age_bucket = create_age_bucket(user["age"])
                        income_bucket = create_income_bucket(user["income"])
                        button_text = f"🚶 {user['id']}"
                        help_text = f"{age_bucket}, {income_bucket}, Churned: {'Yes' if user['churned'] else 'No'}"
                    else:
                        button_text = f"🚶 {user['id']}"
                        help_text = f"Age: {user['age']}, Income: £{user['income']:,}, Churned: {'Yes' if user['churned'] else 'No'}"

                    if st.button(
                        button_text, key=f"match_free_{user['id']}", help=help_text
                    ):
                        st.session_state.selected_free = user["id"]
                        st.rerun()

                    if selected:
                        st.markdown("**🟡 SELECTED**")
                        if st.session_state.show_buckets:
                            st.caption(f"Age: {create_age_bucket(user['age'])}")
                            st.caption(
                                f"Income: {create_income_bucket(user['income'])}"
                            )
                        else:
                            st.caption(f"Age: {user['age']}")
                            st.caption(f"Income: £{user['income']:,}")
                        st.caption(f"Churned: {'Yes' if user['churned'] else 'No'}")
                else:
                    st.success(f"✅ {user['id']} - Already Matched")

        # Show comparison if both users selected
        if st.session_state.selected_premium and st.session_state.selected_free:
            match_result = find_matches(
                users, st.session_state.selected_premium, st.session_state.selected_free
            )

            st.subheader("🔍 Comparison Results")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Premium User: {match_result['premium_user']['id']}**")
                if st.session_state.show_buckets:
                    st.caption(f"Age: {match_result['premium_buckets'][0]}")
                    st.caption(f"Income: {match_result['premium_buckets'][1]}")
                else:
                    st.caption(
                        f"Age: {match_result['premium_user']['age']} → {match_result['premium_buckets'][0]}"
                    )
                    st.caption(
                        f"Income: £{match_result['premium_user']['income']:,} → {match_result['premium_buckets'][1]}"
                    )
                st.caption(
                    f"Churned: {'Yes' if match_result['premium_user']['churned'] else 'No'}"
                )

            with col2:
                st.markdown(f"**Free User: {match_result['free_user']['id']}**")
                if st.session_state.show_buckets:
                    st.caption(f"Age: {match_result['free_buckets'][0]}")
                    st.caption(f"Income: {match_result['free_buckets'][1]}")
                else:
                    st.caption(
                        f"Age: {match_result['free_user']['age']} → {match_result['free_buckets'][0]}"
                    )
                    st.caption(
                        f"Income: £{match_result['free_user']['income']:,} → {match_result['free_buckets'][1]}"
                    )
                st.caption(
                    f"Churned: {'Yes' if match_result['free_user']['churned'] else 'No'}"
                )

            # Match quality assessment
            if match_result["perfect_match"]:
                st.success(
                    "✅ **Perfect Match!** Both users are in the same age and income buckets."
                )
                if st.button("💾 Save This Match"):
                    st.session_state.matches_found.append(match_result)
                    st.session_state.selected_premium = None
                    st.session_state.selected_free = None
                    st.success(
                        f"Match saved! You now have {len(st.session_state.matches_found)} matches."
                    )
                    st.rerun()
            else:
                match_issues = []
                if not match_result["age_match"]:
                    match_issues.append("different age buckets")
                if not match_result["income_match"]:
                    match_issues.append("different income buckets")

                st.error(
                    f"❌ **Poor Match**: These users have {' and '.join(match_issues)}. Try finding users in the same buckets."
                )

        # Show matched pairs table
        if len(st.session_state.matches_found) > 0:
            st.subheader("📋 Matched Pairs")

            for i, match in enumerate(st.session_state.matches_found):
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    premium_status = (
                        "❌ Churned"
                        if match["premium_user"]["churned"]
                        else "✅ Stayed"
                    )
                    st.info(
                        f"**{match['premium_user']['id']}** (Premium)\n{premium_status}"
                    )
                with col2:
                    st.markdown("**↔️ vs ↔️**")
                    st.caption(
                        f"{match['premium_buckets'][0]}, {match['premium_buckets'][1]}"
                    )
                with col3:
                    free_status = (
                        "❌ Churned" if match["free_user"]["churned"] else "✅ Stayed"
                    )
                    st.info(f"**{match['free_user']['id']}** (Free)\n{free_status}")

        # Check if all premium users are matched
        premium_users = [u for u in users if u["type"] == "premium"]
        unmatched_premium = [
            u
            for u in premium_users
            if not any(
                match["premium_user"]["id"] == u["id"]
                for match in st.session_state.matches_found
            )
        ]

        if len(unmatched_premium) == 0 and len(st.session_state.matches_found) > 0:
            if st.button(
                "🎉 Calculate Average Treatment Effect - All Premiums Matched!",
                type="primary",
            ):
                st.session_state.lesson6_step = 10
                st.rerun()
        else:
            st.info(
                f"🎯 **Progress**: {len(st.session_state.matches_found)}/{len(premium_users)} premium users matched. Match all premium users to unlock the final calculation!"
            )

    if st.session_state.lesson6_step >= 10 and len(st.session_state.matches_found) > 0:
        st.header("🎉 Final Results: Matched Analysis")

        st.markdown(
            f"**Congratulations! You matched all {len(st.session_state.matches_found)} premium users!**"
        )

        # Calculate effect from matches
        matched_premium_churn = sum(
            match["premium_user"]["churned"] for match in st.session_state.matches_found
        ) / len(st.session_state.matches_found)
        matched_free_churn = sum(
            match["free_user"]["churned"] for match in st.session_state.matches_found
        ) / len(st.session_state.matches_found)
        matched_effect = matched_free_churn - matched_premium_churn

        # Calculate naive effect from original large dataset
        naive_effect = calculate_naive_effect(st.session_state.all_users)

        st.subheader("📊 Compare the Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🤖 Naive Analysis",
                f"{naive_effect:.1%}",
                help="From original large dataset - biased by confounders",
            )
            st.caption("Used ALL users without controlling for age/income")

        with col2:
            st.metric(
                "🎯 Matched Analysis",
                f"{matched_effect:.1%}",
                help="From matched pairs - controlling for age & income",
            )
            st.caption("Used only matched pairs with same age/income buckets")

        # Show insight based on difference
        if abs(matched_effect) < abs(naive_effect):
            st.success(
                f"""
            🎉 **Key Insight**: The premium effect dropped from {naive_effect:.1%} to {matched_effect:.1%}!
            
            Much of what we thought was a "premium effect" was actually just older, wealthier users being less likely to churn anyway.
            
            **Coarsened Exact Matching revealed the true causal effect by controlling for confounders.**
            """
            )
        else:
            st.info(
                "The matched analysis shows the treatment effect remains strong even after controlling for confounders!"
            )

        # Show detailed breakdown
        with st.expander("🔍 See Detailed Breakdown"):
            st.markdown("**Your Matched Pairs:**")
            for i, match in enumerate(st.session_state.matches_found, 1):
                premium_result = (
                    "Churned" if match["premium_user"]["churned"] else "Stayed"
                )
                free_result = "Churned" if match["free_user"]["churned"] else "Stayed"
                buckets = (
                    f"{match['premium_buckets'][0]}, {match['premium_buckets'][1]}"
                )
                st.write(
                    f"{i}. **{match['premium_user']['id']}** ({premium_result}) vs **{match['free_user']['id']}** ({free_result}) | Both: {buckets}"
                )

            st.markdown(f"**Final Calculation:**")
            st.write(f"- Premium churn rate in matches: {matched_premium_churn:.1%}")
            st.write(f"- Free churn rate in matches: {matched_free_churn:.1%}")
            st.write(
                f"- Treatment effect: {matched_free_churn:.1%} - {matched_premium_churn:.1%} = **{matched_effect:.1%}**"
            )

    if st.session_state.lesson6_step >= 11:
        st.header("🎓 Key Takeaways")

        st.success(
            """
        - **When A/B testing would bias results**, use observational matching instead
        - **Coarsened Exact Matching** groups users by similar characteristics
        - **Compare like with like** to isolate the true treatment effect
        - **Confounders can make small effects look big** (or vice versa)
        """
        )

        st.info(
            """
        **💡 When to use CEM:**
        - Self-selection into treatment (people choose to pay)
        - Can't randomise ethically or practically  
        - Have rich data on potential confounders
        - Want to make fair comparisons
        """
        )

    # Navigation
    st.divider()

    if st.session_state.lesson6_step < 11:
        if st.button("Next →", type="primary", use_container_width=True):
            st.session_state.lesson6_step += 1
            st.rerun()
    else:
        # Final navigation options
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Start Over", use_container_width=True):
                st.session_state.lesson6_step = 1
                st.session_state.all_users = generate_user_data()
                st.session_state.matching_users = get_matching_subset()
                st.session_state.selected_premium = None
                st.session_state.selected_free = None
                st.session_state.matches_found = []
                st.session_state.show_naive = False
                st.session_state.show_matching = False
                st.session_state.show_buckets = False
                st.session_state.use_subset = False
                st.rerun()

        with col2:
            st.info("🚧 More lessons coming soon!")

    # Check if show_math state exists, if not initialize it
    if "show_cem_math" not in st.session_state:
        st.session_state.show_cem_math = False

    # Add the math button to the final navigation
    if st.session_state.lesson6_step >= 11:
        with col3:
            if st.button("📚 Optional Maths", use_container_width=True):
                st.session_state.show_cem_math = not st.session_state.show_cem_math
                st.rerun()

        # Show detailed math section if toggled
        if st.session_state.show_cem_math:
            st.divider()
            st.header("📚 Optional Math Corner")

            st.subheader("1. Coarsened Exact Matching Formula")

            st.markdown(
                """
            **Step 1: Coarsening Function**
            
            For each continuous variable, we define a coarsening function C(X):
            """
            )

            st.latex(
                r"""
            C(X_i) = \begin{cases}
            \text{"Young"} & \text{if } X_i < 30 \\
            \text{"Middle"} & \text{if } 30 \leq X_i < 50 \\
            \text{"Older"} & \text{if } X_i \geq 50
            \end{cases}
            """
            )

            st.markdown(
                """
            **Step 2: Exact Matching Within Strata**
            
            Units are matched if they belong to the same coarsened stratum:
            """
            )

            st.latex(
                r"""
            \text{Match}(i,j) = \mathbf{1}[C(X_i) = C(X_j)] \times \mathbf{1}[T_i \neq T_j]
            """
            )

            st.markdown(
                """
            Where:
            - i, j are different units
            - T_i is treatment status (1 = premium, 0 = free)
            - 𝟙[·] is the indicator function (1 if true, 0 if false)
            """
            )

            st.subheader("2. Average Treatment Effect Estimation")

            st.markdown(
                """
            **Within each matched stratum s, calculate the stratum-specific treatment effect:**
            """
            )

            st.latex(
                r"""
            \hat{\tau}_s = \frac{1}{n_{1s}} \sum_{i \in T_s} Y_i - \frac{1}{n_{0s}} \sum_{j \in C_s} Y_j
            """
            )

            st.markdown(
                """
            Where:
            - T_s = treated units in stratum s
            - C_s = control units in stratum s  
            - n_{1s}, n_{0s} = number of treated/control units in stratum s
            """
            )

            st.markdown(
                """
            **Overall Average Treatment Effect:**
            """
            )

            st.latex(
                r"""
            \hat{\tau}_{CEM} = \frac{\sum_{s} n_s \hat{\tau}_s}{\sum_{s} n_s}
            """
            )

            st.markdown(
                """
            Where n_s is the total number of matched units in stratum s.
            """
            )

            st.subheader("3. Why Coarsening Works")

            st.markdown(
                """
            **The Intuition:**
            
            Within each stratum, treated and control units have similar covariate distributions.
            If coarsening preserves the relevant variation, then the **selection bias is eliminated within each stratum**.
            
            This means we can compare users with similar characteristics and isolate the true treatment effect.
            """
            )

            st.subheader("4. Key Assumptions")

            st.warning(
                """
            **CEM relies on these critical assumptions:**
            
            1. **Conditional Independence**: Treatment assignment is independent of potential outcomes, conditional on observed covariates
            
            2. **Common Support**: For each stratum, there exist both treated and control units
            
            3. **Coarsening Preserves Balance**: The coarse buckets don't hide important heterogeneity
            """
            )

            st.success(
                """
            **Bottom Line:**
            CEM is easy to understand but is restricted in scope of application.
            """
            )
