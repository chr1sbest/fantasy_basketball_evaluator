from json import load
from math import sqrt

class Evaluator(object):
    def __init__(self):
        #self.load_data()
        self.load_categories()

    def load_categories(self):
        """
        Prompt user for point value per category.
        """
        self.cats = {}
        categories = ['PTS', 'REB', 'AST'] 
        print "Please asign point values to each category"
        for cat in categories:
            value = raw_input("{0} value? ".format(cat))
            assert value in ['-2', '-1', '0', '1', '2'], \
                    'Invalid Entry. Value must be in range of -2 to 2'
            self.cats[cat] = int(value)
        correct = raw_input("{0} correct? y/n\n".format(self.cats))
        if correct not in ['y', 'Y', 'yes', 'Yes']:
            self.load_categories()

    def load_data(self):
        """
        Load player_data and then calculate means and standard devations.
        """
        with open('player_data.json') as data:
            self.player_data = load(data)
        player_data = array(self.player_data)
        self.means = {k: mean(x[k] for x in player_data) for (k, v) in self.cats}
        self.stds = {k: stdev(x[k] for x in player_data) for (k, v) in self.cats}

    def evaluate(self, cats=None):
        cats = cats or self.categories
        for player in self.player_data:
            totals = {x: (player[x] - self.mean[x]) / self.std[x] * cats.get(x, 0)\
                      for x in player.cats}
            player['evaluation'] = sum(totals.values())
        self.player_data.sort(lambda x: x['evaluation'])
        print self.player_data

    def punt(self, *args):
        print "Punting {0}".format(args)
        cats = {k: v for (k,v) in self.categories.iteritems() if k not in args}
        self.evaluate(cats)


#Helper Functions

def mean(*args):
    return sum(float(x) for x in args) / len(args)

def stdev(*args):
    avg = mean(*args)
    deviance = mean(*[(x - avg)**2 for x in args])
    return sqrt(deviance)
