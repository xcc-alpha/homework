import matplotlib.pyplot as plt,config
def draw_year_pic(df):
    y=df["年份"].value_counts().sort_index()
    plt.figure(figsize=(9,4))
    plt.plot(y.index,y.values,marker="o",c="#1967d2")
    plt.title("光子计算-年度发文趋势")
    plt.savefig(f"{config.FIG_OUT}/year_trend.png",dpi=200)
    plt.close()
