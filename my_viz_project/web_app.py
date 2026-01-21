"""
⚽ Soccer Team Evolution - Interactive Web App
==============================================
Run: streamlit run web_app.py
"""

import streamlit as st
import soccerdata as sd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Soccer Team Evolution",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("⚽ Soccer Team Evolution Dashboard")
st.markdown("### Analyze and compare team Elo ratings over time")

# Sidebar
st.sidebar.header("🎛️ Controls")

# Cache data loading
@st.cache_data(ttl=3600)
def load_current_elo():
    """Load current ClubElo data"""
    elo = sd.ClubElo()
    current_elo = elo.read_by_date()
    return current_elo

@st.cache_data(ttl=3600)
def get_team_history(team_name):
    """Get historical data for a team"""
    elo = sd.ClubElo()
    return elo.read_team_history(team_name)

# Load data
with st.spinner('Loading team data...'):
    current_elo = load_current_elo()
    
# Extract team names properly
team_names = []
for idx in current_elo.index:
    if isinstance(idx, tuple):
        team_names.append(idx[1] if len(idx) > 1 else str(idx))
    else:
        team_names.append(str(idx))

# Sidebar - Top Teams Display
st.sidebar.subheader("🏆 Current Top 10")
top_10 = current_elo.head(10)
for i, (idx, row) in enumerate(top_10.iterrows(), 1):
    team = team_names[i-1]
    st.sidebar.write(f"{i}. **{team}**: {int(row['elo'])}")

st.sidebar.markdown("---")

# Main content - Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Single Team Analysis",
    "🔥 Compare Teams",
    "📈 Top Teams Evolution",
    "🎯 Recent Form"
])

# TAB 1: Single Team Analysis
with tab1:
    st.header("📊 Single Team Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Team selection
        selected_team = st.selectbox(
            "Select a team:",
            options=team_names[:50],  # Top 50 teams
            index=0
        )
    
    with col2:
        smoothing = st.slider(
            "Smoothing (matches):",
            min_value=10,
            max_value=150,
            value=30,
            step=10
        )
    
    if selected_team:
        with st.spinner(f'Loading {selected_team} data...'):
            history = get_team_history(selected_team)
            
            # Statistics
            st.subheader(f"📈 {selected_team} Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Elo", f"{int(history['elo'].iloc[-1])}")
            with col2:
                st.metric("All-time Peak", f"{int(history['elo'].max())}")
            with col3:
                st.metric("All-time Low", f"{int(history['elo'].min())}")
            with col4:
                st.metric("Total Matches", f"{len(history):,}")
            
            # Interactive Chart with Plotly
            st.subheader("📉 Elo Rating Evolution")
            
            fig = go.Figure()
            
            # Raw data (light)
            fig.add_trace(go.Scatter(
                x=history.index,
                y=history['elo'],
                mode='lines',
                name='Raw Elo',
                line=dict(color='lightblue', width=1),
                opacity=0.3
            ))
            
            # Smoothed data
            smoothed = history['elo'].rolling(window=smoothing, center=True).mean()
            fig.add_trace(go.Scatter(
                x=history.index,
                y=smoothed,
                mode='lines',
                name=f'{smoothing}-Match Average',
                line=dict(color='darkblue', width=3)
            ))
            
            fig.update_layout(
                title=f'{selected_team} Elo Rating Over Time',
                xaxis_title='Date',
                yaxis_title='Elo Rating',
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional stats
            st.subheader("📊 Historical Milestones")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Peak Performance:**")
                peak_date = history['elo'].idxmax()
                st.write(f"- Date: {peak_date.strftime('%Y-%m-%d')}")
                st.write(f"- Elo: {int(history['elo'].max())}")
            
            with col2:
                st.write("**Lowest Point:**")
                low_date = history['elo'].idxmin()
                st.write(f"- Date: {low_date.strftime('%Y-%m-%d')}")
                st.write(f"- Elo: {int(history['elo'].min())}")

# TAB 2: Compare Teams
with tab2:
    st.header("🔥 Compare Multiple Teams")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        compare_teams = st.multiselect(
            "Select teams to compare (max 6):",
            options=team_names[:50],
            default=team_names[:3],
            max_selections=6
        )
    
    with col2:
        compare_smoothing = st.slider(
            "Smoothing:",
            min_value=20,
            max_value=100,
            value=50,
            step=10,
            key="compare_smooth"
        )
    
    if compare_teams:
        with st.spinner('Loading comparison data...'):
            fig = go.Figure()
            
            colors = px.colors.qualitative.Set2
            
            for i, team in enumerate(compare_teams):
                history = get_team_history(team)
                smoothed = history['elo'].rolling(window=compare_smoothing, center=True).mean()
                
                fig.add_trace(go.Scatter(
                    x=history.index,
                    y=smoothed,
                    mode='lines',
                    name=team,
                    line=dict(color=colors[i % len(colors)], width=3)
                ))
            
            fig.update_layout(
                title='Team Comparison - Elo Ratings Over Time',
                xaxis_title='Date',
                yaxis_title='Elo Rating',
                hovermode='x unified',
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Current standings table
            st.subheader("📊 Current Standings")
            standings_data = []
            for team in compare_teams:
                history = get_team_history(team)
                standings_data.append({
                    'Team': team,
                    'Current Elo': int(history['elo'].iloc[-1]),
                    'Peak Elo': int(history['elo'].max()),
                    'Matches': len(history)
                })
            
            standings_df = pd.DataFrame(standings_data)
            standings_df = standings_df.sort_values('Current Elo', ascending=False)
            st.dataframe(standings_df, use_container_width=True)

# TAB 3: Top Teams Evolution
with tab3:
    st.header("📈 Top Teams Historical Evolution")
    
    num_top_teams = st.slider(
        "Number of top teams to display:",
        min_value=3,
        max_value=10,
        value=5
    )
    
    with st.spinner(f'Loading top {num_top_teams} teams...'):
        fig = go.Figure()
        
        colors = px.colors.qualitative.Plotly
        
        for i in range(num_top_teams):
            team = team_names[i]
            history = get_team_history(team)
            smoothed = history['elo'].rolling(window=50, center=True).mean()
            
            fig.add_trace(go.Scatter(
                x=history.index,
                y=smoothed,
                mode='lines',
                name=team,
                line=dict(color=colors[i % len(colors)], width=3)
            ))
        
        fig.update_layout(
            title=f'Top {num_top_teams} Teams - Historical Evolution',
            xaxis_title='Date',
            yaxis_title='Elo Rating',
            hovermode='x unified',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

# TAB 4: Recent Form
with tab4:
    st.header("🎯 Recent Form Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        recent_teams = st.multiselect(
            "Select teams:",
            options=team_names[:30],
            default=team_names[:5],
            key="recent_teams"
        )
    
    with col2:
        years_back = st.selectbox(
            "Time period:",
            options=[1, 2, 3, 5, 10],
            index=2,
            format_func=lambda x: f"Last {x} year{'s' if x > 1 else ''}"
        )
    
    if recent_teams:
        cutoff_date = datetime.now() - timedelta(days=years_back*365)
        
        with st.spinner('Analyzing recent form...'):
            fig = go.Figure()
            colors = px.colors.qualitative.Set1
            
            for i, team in enumerate(recent_teams):
                history = get_team_history(team)
                recent = history[history.index >= cutoff_date]
                
                if len(recent) > 0:
                    smoothed = recent['elo'].rolling(window=10, center=True).mean()
                    
                    fig.add_trace(go.Scatter(
                        x=recent.index,
                        y=smoothed,
                        mode='lines+markers',
                        name=team,
                        line=dict(color=colors[i % len(colors)], width=3),
                        marker=dict(size=3)
                    ))
            
            fig.update_layout(
                title=f'Recent Form - Last {years_back} Year{"s" if years_back > 1 else ""}',
                xaxis_title='Date',
                yaxis_title='Elo Rating',
                hovermode='x unified',
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Momentum analysis
            st.subheader("📊 Momentum Analysis")
            momentum_data = []
            
            for team in recent_teams:
                history = get_team_history(team)
                recent = history[history.index >= cutoff_date]
                
                if len(recent) > 10:
                    current = recent['elo'].iloc[-1]
                    start = recent['elo'].iloc[0]
                    change = current - start
                    pct_change = (change / start) * 100
                    
                    momentum_data.append({
                        'Team': team,
                        'Start Elo': int(start),
                        'Current Elo': int(current),
                        'Change': int(change),
                        'Change %': f"{pct_change:+.1f}%",
                        'Trend': '🔥' if change > 0 else '📉'
                    })
            
            momentum_df = pd.DataFrame(momentum_data)
            momentum_df = momentum_df.sort_values('Change', ascending=False)
            st.dataframe(momentum_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>⚽ Built with Streamlit & SoccerData | Data from ClubElo</p>
        <p><small>Refresh data by reloading the page</small></p>
    </div>
""", unsafe_allow_html=True)
