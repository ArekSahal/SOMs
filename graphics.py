import matplotlib.pyplot as plt
import numpy as np 

class Presenter:

    def __init__(self,color_pallet=False):
        self.model = None
        self.data = []
        self.labels = []
        self.label_titles = []
        if color_pallet:
            self.color_pallet = color_pallet
        else:
            self.color_pallet = ["#d73027", "#4575b4","#ffffbf", "#91bfdb","#fc8d59", "#fee090", "#e0f3f8"]


    def set_model(self, m):
        self.model = m

    def set_data(self, data, labels, label_titles, legend_labels):
        self.data = data
        self.labels = labels
        self.label_titles = label_titles
        self.legend_labels = legend_labels
    

    def show(self):
        color_map = "RdYlBu"
        a = 0.8
        xs = []
        ys = []
        colors = []
        
        fig, axs = plt.subplots(ncols=len(self.label_titles), figsize=(4*len(self.label_titles) + 1,4))
        if len(self.label_titles) ==1:
            axs = [axs]
        #fig.suptitle("2D mapping of MPs", fontsize=20, verticalalignment="bottom")
        #fig.patch.set_visible(False)
        # [["male", "Female"], ["District 1", "District not 1"]]

        for i in range(len(self.label_titles)):
            axs[i].set_title(self.label_titles[i])
            axs[i].axis('off')

        for i in range(len(self.legend_labels)):
            dummy_colors = []
            dummy_xs = []
            dummy_ys = []
            for j in range(len(self.legend_labels[i])):
                dummy_colors.append(self.color_pallet[j])
                dummy_xs.append([])
                dummy_ys.append([])
                
            colors.append(dummy_colors)
            xs.append(dummy_xs)
            ys.append(dummy_ys)

        for i in range(self.data.shape[0]):
            winner = self.model.find_winner(self.data[i,:])
            s = np.sqrt(self.model.n_nodes)
            row = (winner % s) + (np.random.rand() - 0.5 )*1
            col = ((winner - row)/s) +  (np.random.rand() - 0.5 )*1
            for j in range(len(self.legend_labels)):
                if len(self.legend_labels[j]) <1:
                    xs[j].append(row)
                    ys[j].append(col)
                else:
                    xs[j][int(self.labels[j][i])].append(row)
                    ys[j][int(self.labels[j][i])].append(col)

        for i in range(len(self.label_titles)):
            if len(self.legend_labels[i]) == 0:
                axs[i].scatter(xs[i], ys[i], c=[int(k) for k in self.labels[i]], alpha=a, cmap=color_map)
            else:
                for j in range(len(self.legend_labels[i])):
                    axs[i].scatter(xs[i][j], ys[i][j], c=colors[i][j],label=self.legend_labels[i][j], alpha=a)
                    axs[i].legend(bbox_to_anchor=(1,1))

        fig.tight_layout()
        return fig

