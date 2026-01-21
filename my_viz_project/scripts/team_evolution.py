"""
🏆 Team Evolution Timeline - Interactive Script
===============================================

This script creates beautiful visualizations of team Elo ratings over time.
Run this to see how top soccer teams have evolved!
"""

import soccerdata as sd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta

# Configure plotting
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("notebook", font_scale=1.2)
plt.rcParams['figure.figsize'] = (14, 7)

print("="*60)
print("🏆 TEAM EVOLUTION TIMELINE PROJECT")
print("="*60)
print()

# Step 1: Get current rankings
print("📊 Step 1: Fetching current team rankings...")
elo = sd.ClubElo()
current_elo = elo.read_by_date()
top_10 = current_elo.head(10)

print(f"\n✅ Top 10 Teams (Current Elo):")
for i, (idx, row) in enumerate(top_10.iterrows(), 1):
    team_name = idx[1]  # Get team name from multi-index
    print(f"   {i}. {team_name}: {int(row['elo'])}")

# Visualize current top 10
print("\n📈 Creating visualization 1: Current Top 10...")
plt.figure(figsize=(12, 6))
colors = plt.cm.RdYlGn(np.linspace(0.5, 0.9, len(top_10)))
bars = plt.bar(range(len(top_10)), top_10['elo'], color=colors, edgecolor='black', linewidth=1.5)

plt.xticks(range(len(top_10)), [idx[1] for idx in top_10.index], rotation=45, ha='right')
plt.ylabel('Elo Rating', fontsize=14, fontweight='bold')
plt.title('Current Top 10 Teams by Elo Rating', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='y', alpha=0.3)

for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('../output/current_top_10.png', dpi=300, bbox_inches='tight')
print("   ✅ Saved: output/current_top_10.png")
plt.show()

# Step 2: Compare top 5 teams over time
print("\n📊 Step 2: Analyzing historical evolution of top 5 teams...")
NUM_TEAMS = 5
teams_to_compare = [idx[1] for idx in current_elo.head(NUM_TEAMS).index]

team_histories = {}
for team in teams_to_compare:
    try:
        history = elo.read_team_history(team)
        team_histories[team] = history
        print(f"   ✅ {team}: {len(history)} data points")
    except Exception as e:
        print(f"   ⚠️  Could not fetch {team}: {e}")

if len(team_histories) > 0:
    # Multi-team comparison chart
    print("\n📈 Creating visualization 2: Multi-team comparison...")
    plt.figure(figsize=(18, 9))
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(team_histories)))
    smoothing_window = 50
    
    for (team, history), color in zip(team_histories.items(), colors):
        smoothed = history['elo'].rolling(window=smoothing_window, center=True).mean()
        plt.plot(smoothed.index, smoothed, linewidth=3, label=team, color=color, alpha=0.8)
    
    plt.xlabel('Year', fontsize=14, fontweight='bold')
    plt.ylabel('Elo Rating', fontsize=14, fontweight='bold')
    plt.title(f'Evolution of Top {len(team_histories)} Teams - Elo Ratings Over Time', 
              fontsize=18, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=12, framealpha=0.9)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../output/team_evolution_comparison.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: output/team_evolution_comparison.png")
    plt.show()
    
    # Recent form (last 5 years)
    print("\n📈 Creating visualization 3: Recent form (last 5 years)...")
    five_years_ago = datetime.now() - timedelta(days=5*365)
    
    plt.figure(figsize=(16, 8))
    colors = plt.cm.tab10(np.linspace(0, 1, len(team_histories)))
    
    for (team, history), color in zip(team_histories.items(), colors):
        recent = history[history.index >= five_years_ago]
        if len(recent) > 0:
            smoothed = recent['elo'].rolling(window=10, center=True).mean()
            plt.plot(smoothed.index, smoothed, linewidth=3.5, label=team, 
                    color=color, marker='o', markersize=2, alpha=0.9)
    
    plt.xlabel('Date', fontsize=14, fontweight='bold')
    plt.ylabel('Elo Rating', fontsize=14, fontweight='bold')
    plt.title('Recent Form: Last 5 Years Performance', fontsize=18, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=11, framealpha=0.95)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../output/recent_form_5_years.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: output/recent_form_5_years.png")
    plt.show()
    
    # Trend analysis
    print("\n📊 Step 3: Calculating team momentum (1-year trends)...")
    one_year_ago = datetime.now() - timedelta(days=365)
    
    trends = {}
    for team, history in team_histories.items():
        current = history['elo'].iloc[-1]
        year_ago_data = history[history.index <= one_year_ago]
        if len(year_ago_data) > 0:
            year_ago = year_ago_data['elo'].iloc[-1]
            change = current - year_ago
            trends[team] = {
                'current': current,
                'year_ago': year_ago,
                'change': change,
                'pct_change': (change / year_ago) * 100
            }
    
    trends_df = pd.DataFrame(trends).T
    trends_df = trends_df.sort_values('change', ascending=False)
    
    print("\n📈 Team Momentum (1-Year Change):")
    for team, row in trends_df.iterrows():
        arrow = "🔥" if row['change'] > 0 else "📉"
        print(f"   {arrow} {team}: {row['change']:+.1f} pts ({row['pct_change']:+.1f}%)")
    
    # Visualize momentum
    print("\n📈 Creating visualization 4: Team momentum...")
    plt.figure(figsize=(12, 6))
    colors = ['green' if x > 0 else 'red' for x in trends_df['change']]
    plt.barh(trends_df.index, trends_df['change'], color=colors, alpha=0.7, edgecolor='black')
    
    plt.xlabel('Elo Point Change (1 Year)', fontsize=13, fontweight='bold')
    plt.title('Team Momentum: Rising vs Falling', fontsize=16, fontweight='bold', pad=15)
    plt.axvline(x=0, color='black', linestyle='-', linewidth=1)
    plt.grid(axis='x', alpha=0.3)
    
    for i, (idx, row) in enumerate(trends_df.iterrows()):
        plt.text(row['change'], i, f" {row['change']:+.0f} ({row['pct_change']:+.1f}%)",
                va='center', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('../output/team_momentum.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved: output/team_momentum.png")
    plt.show()
    
    # Save data
    print("\n💾 Saving data to CSV...")
    combined_data = pd.DataFrame()
    for team, history in team_histories.items():
        temp = history[['elo']].copy()
        temp.columns = [team]
        combined_data = pd.concat([combined_data, temp], axis=1)
    
    combined_data.to_csv('../output/team_evolution_data.csv')
    print("   ✅ Saved: output/team_evolution_data.csv")

print("\n" + "="*60)
print("🎉 ANALYSIS COMPLETE!")
print("="*60)
print("\n📁 All outputs saved in: my_viz_project/output/")
print("   - current_top_10.png")
print("   - team_evolution_comparison.png")
print("   - recent_form_5_years.png")
print("   - team_momentum.png")
print("   - team_evolution_data.csv")
print("\n💡 Next steps:")
print("   - Check the output folder for your visualizations")
print("   - Modify this script to analyze your favorite teams")
print("   - Share your charts on social media!")
print("\n⚽ Happy analyzing!")
