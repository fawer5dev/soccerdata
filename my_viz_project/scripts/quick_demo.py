"""
Quick Demo: Team Evolution Analysis
Run this to see a simple example!
"""

import soccerdata as sd
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

print("="*70)
print("🏆 QUICK TEAM EVOLUTION DEMO")
print("="*70)

# Step 1: Get top teams
print("\n📊 Fetching current top teams...")
elo = sd.ClubElo()
current_elo = elo.read_by_date()
top_5 = current_elo.head(5)

print("\n✅ Current Top 5 Teams:")
for i, (idx, row) in enumerate(top_5.iterrows(), 1):
    team_name = idx[1]
    print(f"   {i}. {team_name}: {int(row['elo'])} Elo")

# Step 2: Get history for top team
print(f"\n📈 Analyzing historical data...")
top_team = top_5.index[0][1]
history = elo.read_team_history(top_team)

print(f"\n📊 {top_team} Statistics:")
print(f"   Current: {int(history['elo'].iloc[-1])}")
print(f"   All-time high: {int(history['elo'].max())}")
print(f"   All-time low: {int(history['elo'].min())}")
print(f"   Data points: {len(history)}")

# Step 3: Create simple chart
print(f"\n🎨 Creating visualization...")
plt.figure(figsize=(14, 6))

# Plot with smoothing
smoothed = history['elo'].rolling(window=30, center=True).mean()
plt.plot(history.index, smoothed, linewidth=2.5, color='darkblue', label=top_team)

plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Elo Rating', fontsize=12, fontweight='bold')
plt.title(f'{top_team} - Elo Rating Evolution', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save chart
output_path = '../output/quick_demo_chart.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"   ✅ Saved to: {output_path}")

# Step 4: Compare top 3 teams
print(f"\n📊 Comparing top 3 teams...")
top_3_teams = [top_5.index[i][1] for i in range(3)]

plt.figure(figsize=(16, 7))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

for team, color in zip(top_3_teams, colors):
    history = elo.read_team_history(team)
    smoothed = history['elo'].rolling(window=50, center=True).mean()
    plt.plot(smoothed.index, smoothed, linewidth=3, label=team, color=color, alpha=0.8)
    print(f"   ✅ {team}: {len(history)} games analyzed")

plt.xlabel('Year', fontsize=13, fontweight='bold')
plt.ylabel('Elo Rating', fontsize=13, fontweight='bold')
plt.title('Top 3 Teams - Historical Evolution', fontsize=15, fontweight='bold')
plt.legend(fontsize=12, loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()

output_path = '../output/top_3_comparison.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"   ✅ Saved to: {output_path}")

print("\n" + "="*70)
print("🎉 DEMO COMPLETE!")
print("="*70)
print(f"\n📁 Check these files in my_viz_project/output/:")
print("   - quick_demo_chart.png")
print("   - top_3_comparison.png")
print(f"\n💡 Teams analyzed: {', '.join(top_3_teams)}")
print("\n⚡ To customize with YOUR teams, edit this file and change:")
print(f"   Line 54: top_3_teams = ['YourTeam1', 'YourTeam2', 'YourTeam3']")
print("\n⚽ Happy analyzing!")
