import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Hiragino Sans"


def simulate_family():
  """1家族をシミュレート。男の子が生まれるまで子供を作り続ける。"""
  girls = 0
  while True:
    if random.random() < 0.5:
      return 1, girls
    else:
      girls += 1


def simulate_country(num_families=100_000):
  """国全体をシミュレート。各家族の子供数リストも返す。"""
  total_boys = 0
  total_girls = 0
  children_per_family = []
  for _ in range(num_families):
    boys, girls = simulate_family()
    total_boys += boys
    total_girls += girls
    children_per_family.append(boys + girls)
  return total_boys, total_girls, children_per_family


def main():
  num_families = 100_000
  num_trials = 10

  print("=== 男の子が生まれるまで子供を作り続ける国のシミュレーション ===")
  print(f"家族数: {num_families:,}  試行回数: {num_trials}")
  print()

  trial_boys = []
  trial_girls = []
  cumulative_boy_pcts = []
  last_children_per_family = []

  cum_boys = 0
  cum_girls = 0

  for i in range(1, num_trials + 1):
    boys, girls, children_per_family = simulate_country(num_families)
    total = boys + girls
    boy_pct = boys / total * 100
    girl_pct = girls / total * 100
    print(
      f"試行 {i:2d}: 男の子 {boys:>7,} / 女の子 {girls:>7,} "
      f"(男 {boy_pct:.2f}% / 女 {girl_pct:.2f}%)"
    )

    trial_boys.append(boys)
    trial_girls.append(girls)
    cum_boys += boys
    cum_girls += girls
    cumulative_boy_pcts.append(cum_boys / (cum_boys + cum_girls) * 100)
    last_children_per_family = children_per_family

  print()
  total = cum_boys + cum_girls
  avg_boy_pct = cum_boys / total * 100
  avg_girl_pct = cum_girls / total * 100
  print("--- 全試行の合計 ---")
  print(f"男の子: {cum_boys:>10,}")
  print(f"女の子: {cum_girls:>10,}")
  print(f"男女比: 男 {avg_boy_pct:.2f}% / 女 {avg_girl_pct:.2f}%")
  print()
  print("理論値: 男 50.00% / 女 50.00%")
  print("※ 各出産の確率は常に50%なので、")
  print("  「いつ止めるか」の戦略は全体の男女比に影響しません。")

  # --- グラフ描画 ---
  fig, axes = plt.subplots(1, 3, figsize=(18, 5))
  fig.suptitle(
    "男の子が生まれるまで子供を作り続ける国のシミュレーション",
    fontsize=14,
  )

  # (a) 棒グラフ: 各試行の男の子・女の子数
  ax = axes[0]
  x = range(1, num_trials + 1)
  width = 0.35
  ax.bar([i - width / 2 for i in x], trial_boys, width, label="男の子", color="#5B9BD5")
  ax.bar([i + width / 2 for i in x], trial_girls, width, label="女の子", color="#ED7D31")
  ax.set_xlabel("試行")
  ax.set_ylabel("人数")
  ax.set_title("(a) 各試行の男女数")
  ax.set_xticks(list(x))
  ax.legend()

  # (b) 折れ線グラフ: 累積男児比率の推移
  ax = axes[1]
  ax.plot(list(x), cumulative_boy_pcts, marker="o", color="#5B9BD5", linewidth=2)
  ax.axhline(y=50, color="gray", linestyle="--", label="理論値 (50%)")
  ax.set_xlabel("試行")
  ax.set_ylabel("累積男児比率 (%)")
  ax.set_title("(b) 累積男児比率の収束")
  ax.set_xticks(list(x))
  ax.set_ylim(48, 52)
  ax.legend()

  # (c) ヒストグラム: 家族ごとの子供数の分布
  ax = axes[2]
  max_children = max(last_children_per_family)
  bins = range(1, min(max_children + 2, 16))
  ax.hist(
    last_children_per_family, bins=bins, align="left",
    color="#70AD47", edgecolor="white", rwidth=0.8,
  )
  ax.set_xlabel("子供の人数")
  ax.set_ylabel("家族数")
  ax.set_title("(c) 家族ごとの子供数の分布 (幾何分布)")
  ax.set_xticks(list(bins)[:-1])

  plt.tight_layout()
  output_path = "result.png"
  plt.savefig(output_path, dpi=150)
  print(f"\nグラフを {output_path} に保存しました。")


if __name__ == "__main__":
  main()
