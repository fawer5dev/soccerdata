#!/usr/bin/env python3
"""
🚀 INSTANT RUN - Team Evolution Quick Analysis
==============================================
Just run: python run_now.py
"""

import sys
sys.path.insert(0, '/Users/fawer5/Documents/fawer5dev/soccerdata')

print("\n" + "="*70)
print("🏆 TEAM EVOLUTION ANALYSIS")
print("="*70 + "\n")

try:
    # Import libraries
    print("📦 Loading libraries...")
    import soccerdata as sd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    print("   ✅ All libraries loaded!\n")
    
    # Fetch data
    print("🔄 Fetching team data from ClubElo...")
    elo = sd.ClubElo()
    current_elo = elo.read_by_date()
    top_5 = current_elo.head(5)
    print("   ✅ Data fetched!\n")
    
    # Display top 5
    print("🏆 Current Top 5 Teams:\n")
    for i, (idx, row) in enumerate(top_5.iterrows(), 1):
        if isinstance(idx, tuple):
            team_name = idx[1] if len(idx) > 1 else idx[0]
        else:
            team_name = str(idx)
        print(f"   {i}. {team_name}: {int(row['elo'])} Elo")
    
    # Get top team history
    print(f"\n📊 Analyzing top team...")
    idx = top_5.index[0]
    top_team = idx[1] if isinstance(idx, tuple) and len(idx) > 1 else str(idx)
    history = elo.read_team_history(top_team)
    
    print(f"\n📈 {top_team} Stats:")
    print(f"   • Current: {int(history['elo'].iloc[-1])}")
    print(f"   • Peak: {int(history['elo'].max())}")
    print(f"   • Low: {int(history['elo'].min())}")
    print(f"   • Matches: {len(history)}")
    
    # Create chart
    print(f"\n🎨 Creating chart...")
    plt.figure(figsize=(14, 6))
    smoothed = history['elo'].rolling(window=30, center=True).mean()
    plt.plot(history.index, smoothed, linewidth=2.5, color='darkblue')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Elo Rating', fontsize=12)
    plt.title(f'{top_team} - Elo Evolution', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output = 'my_viz_project/output/team_chart.png'
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Chart saved: {output}")
    
    # Compare top 3
    print(f"\n📊 Comparing top 3 teams...")
    plt.figure(figsize=(16, 7))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, color in zip(range(3), colors):
        idx = top_5.index[i]
        team = idx[1] if isinstance(idx, tuple) and len(idx) > 1 else str(idx)
        history = elo.read_team_history(team)
        smoothed = history['elo'].rolling(window=50, center=True).mean()
        plt.plot(smoothed.index, smoothed, linewidth=3, label=team, color=color)
        print(f"   ✅ {team}")
    
    plt.xlabel('Year', fontsize=13)
    plt.ylabel('Elo Rating', fontsize=13)
    plt.title('Top 3 Teams Comparison', fontsize=15, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output = 'my_viz_project/output/comparison_chart.png'
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Chart saved: {output}")
    
    print("\n" + "="*70)
    print("🎉 SUCCESS!")
    print("="*70)
    print("\n📁 Check these files:")
    print("   • my_viz_project/output/team_chart.png")
    print("   • my_viz_project/output/comparison_chart.png")
    print("\n⚽ Open them to see your visualizations!\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTry running:")
    print("  source venv_soccer_viz/bin/activate")
    print("  python run_now.py")
