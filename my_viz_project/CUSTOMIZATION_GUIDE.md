# 🎓 TEAM EVOLUTION - CUSTOMIZATION GUIDE

## 📝 How to Customize for Your Favorite Teams

### 🎯 Option 1: Change Number of Teams (Quick)

Open `scripts/team_evolution.py` and find **Line 64**:

```python
NUM_TEAMS = 5  # Currently analyzing top 5 teams
```

**Change it to:**
```python
NUM_TEAMS = 10  # Analyze top 10 teams
NUM_TEAMS = 3   # Just top 3 teams
```

---

### 🎯 Option 2: Specify Exact Teams (Recommended)

Find **Line 65** in the script:

```python
teams_to_compare = [idx[1] for idx in current_elo.head(NUM_TEAMS).index]
```

**Replace it with your chosen teams:**
```python
# Premier League rivals:
teams_to_compare = ["Manchester City", "Liverpool", "Arsenal", "Manchester United"]

# Spanish giants:
teams_to_compare = ["Real Madrid", "Barcelona", "Atletico Madrid"]

# European powerhouses:
teams_to_compare = ["Bayern Munich", "Real Madrid", "Manchester City", "Liverpool", "PSG"]

# Historical comparison:
teams_to_compare = ["AC Milan", "Juventus", "Inter"]

# Your custom selection:
teams_to_compare = ["TEAM1", "TEAM2", "TEAM3"]  # Add your teams here!
```

---

### 🎯 Option 3: Change Time Period

**Line 119** - Adjust recent form period:

```python
# Currently shows last 5 years
five_years_ago = datetime.now() - timedelta(days=5*365)

# Change to:
ten_years_ago = datetime.now() - timedelta(days=10*365)  # Last decade
three_years_ago = datetime.now() - timedelta(days=3*365) # Last 3 years
twenty_years_ago = datetime.now() - timedelta(days=20*365) # 20 years
```

---

### 🎯 Option 4: Adjust Chart Smoothing

**Line 78** - Change how smooth the lines are:

```python
smoothing_window = 50  # Current smoothing

# More detail (less smooth):
smoothing_window = 20

# Smoother lines:
smoothing_window = 100
```

---

### 🎯 Option 5: Change Chart Colors

**Line 76** - Modify color scheme:

```python
# Current:
colors = plt.cm.Set2(np.linspace(0, 1, len(team_histories)))

# Try these:
colors = plt.cm.tab10(np.linspace(0, 1, len(team_histories)))  # Bright colors
colors = plt.cm.viridis(np.linspace(0, 1, len(team_histories)))  # Purple-green
colors = plt.cm.plasma(np.linspace(0, 1, len(team_histories)))  # Pink-yellow
colors = plt.cm.rainbow(np.linspace(0, 1, len(team_histories)))  # Rainbow!
```

---

## 💡 QUICK CUSTOMIZATION EXAMPLE

Here's a complete example for analyzing Premier League top 6:

1. Open `scripts/team_evolution.py`
2. Find **Line 64-65**
3. Replace with:

```python
# Analyze Premier League Big 6
teams_to_compare = [
    "Manchester City",
    "Liverpool", 
    "Arsenal",
    "Chelsea",
    "Manchester United",
    "Tottenham"
]
```

4. Save the file
5. Run: `python my_viz_project/scripts/team_evolution.py`

That's it! 🎉

---

## 🔍 Finding Team Names

Not sure of the exact team name? Run this quick check:

```python
import soccerdata as sd
elo = sd.ClubElo()
current = elo.read_by_date()

# Search for a team (e.g., "Milan")
teams = [team for team in current.index.get_level_values('team') if 'Milan' in team]
print(teams)
```

---

## 🎨 COMPLETE CUSTOMIZATION TEMPLATE

Copy this into a NEW file `scripts/my_custom_analysis.py`:

```python
import soccerdata as sd
import matplotlib.pyplot as plt
import numpy as np

# ===== CUSTOMIZE HERE =====
MY_TEAMS = ["Real Madrid", "Barcelona", "Bayern Munich"]  # Your teams
SMOOTHING = 50  # How smooth (20=detailed, 100=very smooth)
COLOR_SCHEME = plt.cm.Set2  # Color palette
TIME_PERIOD_YEARS = 5  # Recent form window
# ==========================

print(f"Analyzing: {', '.join(MY_TEAMS)}")

elo = sd.ClubElo()
plt.figure(figsize=(16, 8))
colors = COLOR_SCHEME(np.linspace(0, 1, len(MY_TEAMS)))

for team, color in zip(MY_TEAMS, colors):
    history = elo.read_team_history(team)
    smoothed = history['elo'].rolling(window=SMOOTHING, center=True).mean()
    plt.plot(smoothed.index, smoothed, linewidth=3, label=team, color=color)

plt.legend(fontsize=12)
plt.title(f'Evolution: {", ".join(MY_TEAMS)}', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Elo Rating', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../output/my_custom_chart.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Chart saved to output/my_custom_chart.png")
```

Run it: `python my_viz_project/scripts/my_custom_analysis.py`

---

## 🆘 Common Issues

**"Team not found"** → Check exact spelling with the search code above  
**"Too many teams"** → Reduce number or increase figure size  
**"Empty chart"** → Team might not have historical data  

---

**Ready to customize? Pick an option above and I'll help you implement it!** 🎨⚽
