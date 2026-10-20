import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# ------------------------------------------------------------
# Paths (edit these)
# ------------------------------------------------------------
UTIL_CSV = "/mnt/user-data/uploads/Resource_Utilization_Results__3_.csv"
OUT_CSV  = "/mnt/user-data/outputs/workerThroughput_generated.csv"
OUT_PDF  = "/mnt/user-data/outputs/Worker_Throughput_generated.pdf"
OUT_PNG  = "/mnt/user-data/outputs/Worker_Throughput_generated.png"

INTERVAL = 15               # minutes per reporting interval
WORKER_MIN_PER_BATCH = 10   # ASSUMPTION: busy worker-minutes needed to finish one batch

# ------------------------------------------------------------
# 1. Busy / idle worker-minutes per 15-min interval (from utilization only)
#    = sum of the one-minute samples in (t-15, t]
# ------------------------------------------------------------
util = pd.read_csv(UTIL_CSV)
times = np.arange(0, util["TimeMinutes"].max() + INTERVAL, INTERVAL)

def window_sum(col, t):
    m = (util.TimeMinutes > t - INTERVAL) & (util.TimeMinutes <= t)
    return util.loc[m, col].sum()

busy = np.array([window_sum("BusyWorkers", t) for t in times])
idle = np.array([window_sum("IdleWorkers", t) for t in times])
utilization = np.divide(busy, busy + idle, out=np.zeros(len(busy)), where=(busy + idle) > 0)

# ------------------------------------------------------------
# 2. Throughput from worker state
#    Only busy workers produce batches; idle workers produce nothing.
#    batches in interval = busy worker-minutes / WORKER_MIN_PER_BATCH
#    Cumulative rounding keeps the running total consistent.
# ------------------------------------------------------------
cum_batches = np.rint(np.cumsum(busy / WORKER_MIN_PER_BATCH)).astype(int)

out = pd.DataFrame({
    "TimeMinutes": times.astype(float),
    "BusyWorkerSamples": busy,
    "IdleWorkerSamples": idle,
    "AvgBusyWorkers": (busy / INTERVAL).round(2),   # average number of busy workers in the interval
    "Utilization": utilization.round(3),
    "BatchesProcessed": cum_batches,
})
out.to_csv(OUT_CSV, index=False)

# ------------------------------------------------------------
# 3. Plot: batches processed only
# ------------------------------------------------------------
df = out.copy()
start_time = pd.Timestamp("2026-01-01 08:00:00")
df["Time"] = start_time + pd.to_timedelta(df["TimeMinutes"], unit="m")
df["IntervalThroughput"] = df["BatchesProcessed"].diff().fillna(0)

fig, ax = plt.subplots(figsize=(11.5, 5.5))

bar_width = 10 / (24 * 60)
bars = df[df["IntervalThroughput"] > 0]   # skip zero-height bars (avoids stray edge lines)
ax.bar(bars["Time"], bars["IntervalThroughput"], width=-bar_width, align="edge",
       color="#C9823A", edgecolor="#8B5A2B", linewidth=0.8, zorder=3, clip_on=False,
       label="Batches processed")

ax.set_xlabel("Time", fontsize=13, fontweight="bold", labelpad=10)
ax.set_ylabel("Batches processed per 15 min", fontsize=13, fontweight="bold", labelpad=10)

# Busy workers as a COUNT (average number of busy workers in each 15-min interval)
ax2 = ax.twinx()
ax2.plot(df["Time"], df["AvgBusyWorkers"], color="#1F4E79", linewidth=2.2, marker="o",
         markersize=5, zorder=4, clip_on=False, label="Busy workers")
ax2.set_ylabel("Number of busy workers", fontsize=13, fontweight="bold", labelpad=10)
ax2.set_ylim(0, 12)
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
ax2.tick_params(axis="y", which="major", labelsize=11, direction="out")
ax2.spines["top"].set_visible(False)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.set_xlim(start_time, start_time + pd.Timedelta(minutes=300))
ax.set_ylim(bottom=0)

ax.tick_params(axis="both", which="major", labelsize=11, direction="out")
ax.grid(True, which="major", axis="both", linestyle="--", linewidth=0.7, alpha=0.30)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
legend = ax.legend(h1 + h2, l1 + l2, loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2,
                   frameon=True, fancybox=False, framealpha=1.0, edgecolor="#666666",
                   fontsize=10.5, borderpad=0.8, columnspacing=2.0, handlelength=2.6)
legend.get_frame().set_facecolor("white")

fig.subplots_adjust(left=0.09, right=0.91, bottom=0.17, top=0.90)
plt.savefig(OUT_PDF, bbox_inches="tight")
plt.savefig(OUT_PNG, dpi=200, bbox_inches="tight")

print(out.assign(IntervalThroughput=df["IntervalThroughput"].astype(int)).to_string(index=False))
print("\nTotal batches:", int(out["BatchesProcessed"].iloc[-1]))
