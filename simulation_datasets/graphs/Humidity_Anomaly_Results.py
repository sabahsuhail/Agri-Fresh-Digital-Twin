import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CSV     = "/mnt/user-data/uploads/O1_Humidity_Cybersecurity_Results_old.csv"
OUT_PDF = "/mnt/user-data/outputs/Humidity_Anomaly_Detection.pdf"
OUT_PNG = "/mnt/user-data/outputs/Humidity_Anomaly_Detection.png"

df = pd.read_csv(CSV)
start = pd.Timestamp("2026-01-01 08:00:00")
df["Time"] = start + pd.to_timedelta(df["TimeMinutes"], unit="m")
det = df[df["AnomalyDetected"] == 1]
missed = df[(df["AttackActive"] == 1) & (df["AnomalyDetected"] == 0)]   # attacks the detector did not flag

BLUE, ORANGE, RED = "#1F4E79", "#E67E22", "#C62828"

fig, ax = plt.subplots(figsize=(11.5, 5.5))

ax.plot(df["Time"], df["ReferenceHumidity"], color=BLUE, linewidth=2.4,
        label="Simulated environmental humidity", zorder=3)
ax.plot(df["Time"], df["ReportedHumidity"], color=ORANGE, linewidth=2.4,
        label="Sensor-reported humidity", zorder=4)

ax.scatter(det["Time"], det["ReportedHumidity"], marker="X", s=130, color=RED,
           edgecolor="white", linewidth=0.9, zorder=6, label="Detected anomaly")

if len(missed):
    ax.scatter(missed["Time"], missed["ReportedHumidity"], marker="o", s=120,
               facecolor="white", edgecolor=RED, linewidth=2.0, zorder=6,
               label="Undetected attack")

ax.set_xlabel("Time", fontsize=13, fontweight="bold", labelpad=10)
ax.set_ylabel("Relative humidity (% RH)", fontsize=13, fontweight="bold", labelpad=10)
ax.set_ylim(82, 104)
from matplotlib.ticker import MultipleLocator
ax.yaxis.set_major_locator(MultipleLocator(2))

ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.set_xlim(start, start + pd.Timedelta(minutes=300))

ax.tick_params(axis="both", which="major", labelsize=11, direction="out")
ax.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.30, zorder=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend = ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=(2 if len(missed) else 3),
                   frameon=True, fancybox=False, framealpha=1.0, edgecolor="#666666",
                   fontsize=10.5, borderpad=0.8, columnspacing=1.8, handlelength=2.2)
legend.get_frame().set_facecolor("white")

fig.subplots_adjust(left=0.09, right=0.98, bottom=0.15, top=(0.87 if len(missed) else 0.90))
plt.savefig(OUT_PDF, bbox_inches="tight")
plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
