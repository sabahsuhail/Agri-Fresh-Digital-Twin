import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CSV     = "/mnt/user-data/uploads/O1_Cybersecurity_Results__2_.csv"
OUT_PDF = "/mnt/user-data/outputs/Temperature_Anomaly_Detection.pdf"
OUT_PNG = "/mnt/user-data/outputs/Temperature_Anomaly_Detection.png"

df = pd.read_csv(CSV)
start = pd.Timestamp("2026-01-01 08:00:00")
df["Time"] = start + pd.to_timedelta(df["TimeMinutes"], unit="m")
det = df[df["AnomalyDetected"] == 1]

BLUE, ORANGE, RED = "#1F4E79", "#E67E22", "#C62828"

fig, ax = plt.subplots(figsize=(11.5, 5.5))

ax.plot(df["Time"], df["ReferenceTemp"], color=BLUE, linewidth=2.4,
        label="Simulated environmental temperature", zorder=3)
ax.plot(df["Time"], df["ReportedTemp"], color=ORANGE, linewidth=2.4,
        label="Sensor-reported temperature", zorder=4)

# faint guides at each detected anomaly
for t in det["Time"]:
    ax.axvline(t, color=RED, linewidth=1.0, linestyle=":", alpha=0.45, zorder=1)

ax.scatter(det["Time"], det["ReportedTemp"], marker="X", s=130, color=RED,
           edgecolor="white", linewidth=0.9, zorder=6, label="Detected anomaly")

ax.set_xlabel("Time", fontsize=13, fontweight="bold", labelpad=10)
ax.set_ylabel("Temperature (°C)", fontsize=13, fontweight="bold", labelpad=10)
ax.set_ylim(2.0, 6.0)

ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.set_xlim(start, start + pd.Timedelta(minutes=300))

ax.tick_params(axis="both", which="major", labelsize=11, direction="out")
ax.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.30, zorder=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend = ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3,
                   frameon=True, fancybox=False, framealpha=1.0, edgecolor="#666666",
                   fontsize=10.5, borderpad=0.8, columnspacing=1.8, handlelength=2.2)
legend.get_frame().set_facecolor("white")

fig.subplots_adjust(left=0.09, right=0.98, bottom=0.15, top=0.90)
plt.savefig(OUT_PDF, bbox_inches="tight")
plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
