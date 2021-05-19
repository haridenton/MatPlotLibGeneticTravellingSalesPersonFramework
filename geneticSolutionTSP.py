import math
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# No of Cities and number of individuals must be even
NO_OF_CITIES = 40
NO_OF_INDIVIDUALS = 100
RANDOM_ROUTE_LENGTH = 0
SHORTEST_ROUTE = 0
GENERATION = 1


def getRandomPath(no_of_cities):
    random_path = [item for item in range(no_of_cities)]
    random.shuffle(random_path)
    return random_path


def getPathX(path):
    X_path = []
    for i in range(NO_OF_CITIES):
        X_path.append(X[path[i]])
    return X_path


def getPathY(path):
    Y_path = []
    for i in range(NO_OF_CITIES):
        Y_path.append(Y[path[i]])
    return Y_path


def getEuclideanDistance(test_path):
    euclidean_distance = 0
    for i in range(len(test_path) - 1):
        current_city = test_path[i]
        next_city = test_path[i + 1]
        x1 = X[current_city]
        y1 = Y[current_city]
        x2 = X[next_city]
        y2 = Y[next_city]
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        hyp = math.sqrt(width ** 2 + height ** 2)
        euclidean_distance = euclidean_distance + hyp
    return euclidean_distance


fig, ax = plt.subplots()
plt.title("Genetic Algorithm Solution For Travelling Salesman")
plt.subplots_adjust(bottom=0.2)
X = [random.triangular() for i in range(NO_OF_CITIES)]
Y = [random.triangular() for i in range(NO_OF_CITIES)]
current_route, = plt.plot(X, Y, lw=2, marker='o')
ax.xaxis.set_label_position('top')
ax.set_title("Random Distance: " + str(getEuclideanDistance(range(NO_OF_CITIES))))
gene_pool = [getRandomPath(NO_OF_CITIES) for i in range(NO_OF_INDIVIDUALS)]
euclidean_distances = [getEuclideanDistance(p) for p in gene_pool]



class Index(object):
    ind = 0

    def next(self, event):
        if self.ind < NO_OF_INDIVIDUALS - 1: self.ind += 1
        ydata = getPathY(gene_pool[self.ind])
        xdata = getPathX(gene_pool[self.ind])
        current_route.set_ydata(ydata)
        current_route.set_xdata(xdata)
        ax.xaxis.set_label_position('top')
        ax.set_xlabel("Path Travelled Distance: " + str(euclidean_distances[self.ind]))
        plt.draw()

    def prev(self, event):
        if self.ind > 0: self.ind -= 1
        ydata = getPathY(gene_pool[self.ind])
        xdata = getPathX(gene_pool[self.ind])
        current_route.set_ydata(ydata)
        current_route.set_xdata(xdata)
        ax.xaxis.set_label_position('top')
        ax.set_xlabel("Path Travelled Distance: " + str(euclidean_distances[self.ind]))
        plt.draw()

    def find_shortest(self, event):
        pos_of_min = euclidean_distances.index(min(euclidean_distances))
        shortest_current_path = gene_pool[pos_of_min]
        ydata = getPathY(shortest_current_path)
        xdata = getPathX(shortest_current_path)
        current_route.set_ydata(ydata)
        current_route.set_xdata(xdata)
        ax.xaxis.set_label_position('top')
        ax.set_xlabel("Current Shortest Distance: " + str(euclidean_distances[pos_of_min]))
        plt.draw()

    def breed(self, event):
        # get the top 10% "fittest" routes
        global gene_pool, euclidean_distances
        working_gene_pool = gene_pool.copy()
        shortest_ten_percent = []
        next_generation = []
        for i in range(NO_OF_INDIVIDUALS // 10):
            pos_of_min = euclidean_distances.index(min(euclidean_distances))
            shortest_ten_percent.append(working_gene_pool[pos_of_min])
            working_gene_pool.remove(working_gene_pool[pos_of_min])
        # copy best routes into next generation
        next_generation = next_generation + shortest_ten_percent
        # cross over between the best routes
        for i in range(NO_OF_INDIVIDUALS // 10 // 2):
            bottom = shortest_ten_percent[len(shortest_ten_percent)-1].copy()
            top = shortest_ten_percent[0].copy()
            shortest_ten_percent.remove(top)
            shortest_ten_percent.remove(bottom)
            child1 = top[: NO_OF_CITIES // 2]
            child2 = bottom[: NO_OF_CITIES // 2]
            for each_city in child1:
                bottom.remove(each_city)
            for each_city in child2:
                top.remove(each_city)
            child1 = child1 + bottom
            child2 = child2 + top
            next_generation.append(child1)
            next_generation.append(child2)
        plt.draw()
        next_generation = next_generation * 5
        # now we randomly mutate the paths
        for x in range(10,len(next_generation)):
            if random.randint(1,12) >= 4:
                print("bootsy")
                path = next_generation[x]
                for i in range(NO_OF_CITIES-1):
                    if random.randint(1, 12) >= 4:
                        print("collins")
                        temp = path[i]
                        path[i] = path[-i]
                        path[-i] = temp

        gene_pool = next_generation.copy()
        euclidean_distances = []
        euclidean_distances = [getEuclideanDistance(p) for p in gene_pool]
        print("Breeded")
        self.find_shortest(event)



callback = Index()
axbreed = plt.axes([0.2, 0.05, 0.17, 0.075])
axgenerate = plt.axes([0.5, 0.05, 0.17, 0.075])
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bbreed = Button(axbreed, 'Breed')
bbreed.on_clicked(callback.breed)
bgenerate = Button(axgenerate, 'Find Shortest')
bgenerate.on_clicked(callback.find_shortest)
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()
