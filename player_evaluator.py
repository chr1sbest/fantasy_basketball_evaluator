from json import load
from math import sqrt

class Evaluator(object):
    def __init__(self):
        self.load_categories()
        self.load_data()
        self.evaluate()

    def load_data(self):
        """
        Load player_data and then calculate means and standard devations.
        """
        with open('player_data.json') as data:
            self.player_data = load(data)
        self.means, self.stds = {}, {}
        for key in self.cats.keys() + ['RNK']:
            self.means[key] = mean(*[x[key] for x in self.player_data])
            self.stds[key] = stdev(*[x[key] for x in self.player_data])

    def evaluate(self, cats=None):
        cats = cats or self.cats
        for player in self.player_data:
            totals = {x: (player[x] - self.means[x]) / self.stds[x] * \
                cats.get(x, 0) for x in player.keys() if x in cats}
            player['SCORE'] = sum(totals.values())
        self.player_data.sort(key=lambda x: x['SCORE'], reverse=True)

    def punt(self, *args):
        print "Punting {0}".format(args)
        cats = {k: v for (k,v) in self.cats.iteritems() if k not in args}
        self.evaluate(cats)

    def load_categories(self):
        """
        Prompt user for point value per category.
        """
        self.cats = {}
        categories = ['PTS', 'FGM', 'FGA', 'FG%', 'FTM', 'FTA','FT%', \
                '3PM', '3PA', 'REB', 'AST', 'A/TO', 'STL', 'BLK', 'TO']
        print "Please asign point values to each category"
        for cat in categories:
            while True:
                value = raw_input("{0} value? ".format(cat))
                if value in ['-2', '-1', '0', '1', '2']:
                    break
                print "Invalid Entry. Value must be in range of -2 to 2"
            self.cats[cat] = int(value)
        sure = raw_input("\n{0} \n\nCorrect? y/n\n".format(self.cats))
        if sure in ['n', 'N', 'no', 'No']:
            self.load_categories()

    def __str__(self):
        return '\n'.join([\
            "{0: <4} {1: <24} {2:.2f}".format(\
            x['RNK'] - y + 1, x['NAME'], x['SCORE']) \
            for y, x in enumerate(self.player_data)])

    def print(self, *args, sort_by='SCORE'):
        # Print specific arguments


#Helper Functions
def mean(*args):
    return sum(float(x) for x in args) / len(args)

def stdev(*args):
    avg = mean(*args)
    deviance = mean(*[(x - avg)**2 for x in args])
    return sqrt(deviance)

if __name__ == "__main__":
    a = Evaluator()
