"""
🎯 QUICK REFERENCE GUIDE - Soccer Data Visualization
====================================================

This file contains quick code snippets for common tasks.
"""

# ============================================
# 1. IMPORTING AND SETUP
# ============================================

import soccerdata as sd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configure plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("notebook")


# ============================================
# 2. DATA SOURCES - HOW TO FETCH DATA
# ============================================

# FBref - Comprehensive statistics
fbref = sd.FBref('ENG-Premier League', '2023-24')
player_stats = fbref.read_player_season_stats(stat_type="standard")
team_stats = fbref.read_team_season_stats(stat_type="standard")
schedule = fbref.read_schedule()

# ClubElo - Team ratings
elo = sd.ClubElo()
current_elo = elo.read_by_date()
team_history = elo.read_team_history("Manchester City")

# Understat - Expected goals (xG)
understat = sd.Understat('EPL', '2023')
shot_data = understat.read_shot_data()
match_results = understat.read_match_results()

# WhoScored - Detailed match data
whoscored = sd.WhoScored('ENG-Premier League', '2023-24')
# Note: WhoScored requires browser automation

# SoFIFA - FIFA ratings and player values
sofifa = sd.SoFIFA(version='23')
players_info = sofifa.read_players()


# ============================================
# 3. COMMON DATA FILTERS
# ============================================

# Top scorers
top_scorers = player_stats.nlargest(10, 'goals')

# Players with minimum games
active_players = player_stats[player_stats['games'] >= 10]

# Specific team players
team_players = player_stats[player_stats.index.get_level_values('team') == 'Arsenal']

# Date range filtering
recent_matches = schedule[schedule['date'] >= '2024-01-01']


# ============================================
# 4. BASIC VISUALIZATIONS
# ============================================

def plot_top_scorers(data, n=10):
    """Bar chart of top scorers"""
    top = data.nlargest(n, 'goals')
    plt.figure(figsize=(12, 6))
    plt.barh(range(len(top)), top['goals'])
    plt.yticks(range(len(top)), top.index.get_level_values('player'))
    plt.xlabel('Goals')
    plt.title(f'Top {n} Scorers')
    plt.tight_layout()
    return plt


def scatter_goals_assists(data):
    """Scatter plot of goals vs assists"""
    plt.figure(figsize=(10, 6))
    plt.scatter(data['goals'], data['assists'], alpha=0.6)
    plt.xlabel('Goals')
    plt.ylabel('Assists')
    plt.title('Goals vs Assists')
    plt.grid(True, alpha=0.3)
    return plt


def plot_elo_evolution(team_name, smoothing=30):
    """Plot team Elo rating over time"""
    elo = sd.ClubElo()
    history = elo.read_team_history(team_name)
    
    plt.figure(figsize=(14, 6))
    plt.plot(history.index, history['elo'].rolling(smoothing).mean())
    plt.xlabel('Date')
    plt.ylabel('Elo Rating')
    plt.title(f'{team_name} - Elo Rating Evolution')
    plt.grid(True, alpha=0.3)
    return plt


def heatmap_team_stats(team_stats):
    """Heatmap of team statistics"""
    # Select numeric columns
    numeric_cols = team_stats.select_dtypes(include=['float64', 'int64']).columns
    correlation = team_stats[numeric_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
    plt.title('Team Statistics Correlation')
    plt.tight_layout()
    return plt


# ============================================
# 5. INTERACTIVE PLOTLY VISUALIZATIONS
# ============================================

def interactive_scatter(data):
    """Interactive scatter plot with Plotly"""
    fig = px.scatter(
        data.reset_index(),
        x='goals',
        y='assists',
        hover_data=['player', 'team', 'games'],
        title='Goals vs Assists (Interactive)',
        size='games',
        color='team'
    )
    return fig


def interactive_bar(data, n=15):
    """Interactive bar chart"""
    top = data.nlargest(n, 'goals').reset_index()
    fig = px.bar(
        top,
        x='player',
        y='goals',
        color='team',
        title=f'Top {n} Scorers',
        hover_data=['assists', 'games']
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


# ============================================
# 6. USEFUL FUNCTIONS
# ============================================

def save_data(dataframe, filename):
    """Save dataframe to CSV"""
    dataframe.to_csv(f'../output/{filename}')
    print(f"✅ Saved to output/{filename}")


def save_plot(filename, dpi=300):
    """Save current plot to file"""
    plt.savefig(f'../output/{filename}', dpi=dpi, bbox_inches='tight')
    print(f"✅ Plot saved to output/{filename}")


def get_player_info(player_stats, player_name):
    """Get all stats for a specific player"""
    return player_stats[
        player_stats.index.get_level_values('player').str.contains(player_name, case=False)
    ]


def compare_players(player_stats, player_names):
    """Compare multiple players"""
    players = []
    for name in player_names:
        player = get_player_info(player_stats, name)
        if not player.empty:
            players.append(player)
    return pd.concat(players)


# ============================================
# 7. AVAILABLE LEAGUES
# ============================================

LEAGUES = {
    'Premier League': 'ENG-Premier League',
    'La Liga': 'ESP-La Liga',
    'Bundesliga': 'GER-Bundesliga',
    'Serie A': 'ITA-Serie A',
    'Ligue 1': 'FRA-Ligue 1',
    'Champions League': 'INT-Champions League',
    'Europa League': 'INT-Europa League',
}


# ============================================
# 8. STAT TYPES (FBref)
# ============================================

STAT_TYPES = [
    'standard',      # Goals, assists, cards
    'shooting',      # Shots, xG, accuracy
    'passing',       # Pass completion, key passes
    'passing_types', # Pass types and distances
    'defense',       # Tackles, interceptions
    'possession',    # Touches, dribbles, carries
    'playing_time',  # Minutes played, starts
    'misc',          # Miscellaneous stats
    'keeper',        # Goalkeeper specific
    'keeper_adv',    # Advanced keeper stats
]


# ============================================
# 9. EXAMPLE WORKFLOW
# ============================================

def example_analysis():
    """Complete analysis example"""
    
    # 1. Fetch data
    fbref = sd.FBref('ENG-Premier League', '2023-24')
    players = fbref.read_player_season_stats(stat_type="standard")
    
    # 2. Filter
    top_players = players[players['games'] >= 10].nlargest(20, 'goals')
    
    # 3. Visualize
    plt.figure(figsize=(12, 6))
    plt.barh(range(len(top_players)), top_players['goals'])
    plt.yticks(range(len(top_players)), 
               top_players.index.get_level_values('player'))
    plt.xlabel('Goals')
    plt.title('Top 20 Scorers - Premier League 2023-24')
    plt.tight_layout()
    
    # 4. Save
    save_plot('top_20_scorers.png')
    save_data(top_players, 'top_20_scorers.csv')
    
    return top_players


if __name__ == "__main__":
    print("📚 Quick Reference Guide Loaded!")
    print("\nTip: Import functions from this file in your notebooks:")
    print("  from scripts.quick_reference import *")
