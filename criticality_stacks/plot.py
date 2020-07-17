import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def run(tid_list, ans, total):

    # plot
    pre = []
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    pre.append(0)
    sub_tid = []
    sub_total = 0
    for i in range(len(tid_list)):
        if ans[i] == 0:
            continue

        if ans[i]/total < 0.2:
            sub_tid.append(i)
            sub_total += ans[i]

        print("ans %d ::: total %d ::: ans/total %.2f" % (ans[i], total, ans[i]/total))
        label = "thread " + str(tid_list[i]) + ": " + str(round(ans[i], 0)) + "/" + str(round(total,0)) + "=" + str(round(ans[i]/total,4))
        width = 0.35

        now = []
        now.append(pre[0] + ans[i]/total)
        now.append(0)
        now.append(0)
        now.append(0)
        now.append(0)
        plt.bar((1,2,3,4,5), now, width, bottom=pre, label=label)

        pre = now

    plt.ylim(0,1)
    plt.legend()
    path = "out/critical.png"
    plt.savefig(path)

