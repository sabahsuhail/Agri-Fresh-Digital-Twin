import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

UTIL_CSV = "/mnt/user-data/uploads/Resource_Utilization_Results__3_.csv"
OUT_PDF  = "/mnt/user-data/outputs/Busy_Idle_Workers.pdf"
OUT_PNG  = "/mnt/user-data/outputs/Busy_Idle_Workers.png"

df = pd.read_csv(UTIL_CSV)
start_time = pd.Timestamp("2026-01-01 08:00:00")
df["Time"] = start_time + pd.to_timedelta(df["TimeMinutes"], unit="m")

fig, ax = plt.subplots(figsize=(11.5, 5.5))

ax.step(df["Time"], df["BusyWorkers"], where="post", color="#1F4E79",
        linewidth=2.2, label="Busy workers", zorder=4)
ax.step(df["Time"], df["IdleWorkers"], where="post", color="#7F7F7F",
        linewidth=2.0, linestyle="--", label="Idle workers", zorder=3)

ax.set_xlabel("Time", fontsize=13, fontweight="bold", labelpad=10)
ax.set_ylabel("Number of workers", fontsize=13, fontweight="bold", labelpad=10)

ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.set_xlim(start_time, start_time + pd.Timedelta(minutes=300))
ax.set_ylim(0, 12.5)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

ax.tick_params(axis="both", which="major", labelsize=11, direction="out")
ax.grid(True, which="major", axis="both", linestyle="--", linewidth=0.7, alpha=0.30)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

legend = ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=True, fancybox=False, framealpha=1.0,
                   edgecolor="#666666", fontsize=10.5, borderpad=0.9,
                   labelspacing=0.8, handlelength=2.8)
legend.get_frame().set_facecolor("white")

fig.subplots_adjust(left=0.08, right=0.97, bottom=0.17, top=0.90)
plt.savefig(OUT_PDF, bbox_inches="tight")
plt.savefig(OUT_PNG, dpi=200, bbox_inches="tight")
