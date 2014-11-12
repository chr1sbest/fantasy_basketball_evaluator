from json import load
from math import sqrt
from copy import deepcopy
from os import system

class Evaluator(object):
    def __init__(self, view_limit=45):
        self.view_limit = view_limit
        self.load_categories()
        self.load_data()
        self.evaluate()

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
                if value in ['-2', '-1', '0', '1', '2', '']:
                    break
                print "Invalid Entry. Value must be in range of -2 to 2"
            self.cats[cat] = 0 if value == "" else int(value)
        points = {k: v for (k, v) in self.cats.iteritems() if v is not 0}
        sure = raw_input("\n{0} \n\nCorrect? y/n\n".format(points))
        if sure in ['n', 'N', 'no', 'No']:
            self.load_categories()

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

    def evaluate(self, cats=None, player_data=None):
        """
        Evaluate player SCORE and DIFF.
        SCORE = Total sum of ((Value - Mean) / STDEV * Weight) for all cats.
        Optionally can evaluate a subset of categories or other player_data.
        """
        cats = cats or self.cats
        player_data = player_data or self.player_data
        # Calculate SCORE
        for player in player_data:
            totals = {x: (player[x] - self.means[x]) / self.stds[x] * \
                cats.get(x, 0) for x in player.keys() if x in cats}
            player['SCORE'] = sum(totals.values())
        # Re-sort according to SCORE.
        player_data.sort(key=lambda x: x['SCORE'], reverse=True)
        for index, player in enumerate(player_data): 
            #Calculate Difference between ESPN rank.
            player['NEW'] = index + 1
            player['DIFF'] = player['RNK'] - player['NEW']
        self.display(player_data=player_data)

    def display(self, player_data=None, *args):
        """
        Display columns titles and values for *args.
        NEW  NAME             RNK  DIFF  SCORE
        1    Kevin Durant*    22   21    23.220
        """
        player_data = player_data or self.player_data
        args = args or ['RNK', 'DIFF', 'SCORE']
        base = "{0: <3} {1: <24} "                  # Build base column layout
        for index, category in enumerate(args):
            base += "{" + str(index + 2) + ": <4} "
        columns = base.format('NEW', 'NAME', *args)
        # Clear screen and display new details.
        system('clear')
        print columns
        print '\n'.join([\
            base.format(\
            player['NEW'], player['NAME'], *[player[arg] for arg in args]) \
                for player in player_data[:self.view_limit]])

    def punt(self, *args):
        """
        Zero out categories for a copy of player_data and re-evaluate.
        Punting is a strategy to maximize gains and minimize losses by
        forfeiting a few categories to focus on others.
        """
        print "Punting {0}".format(args)
        cats = {k: v for (k,v) in self.cats.iteritems() if k not in args}
        player_data = deepcopy(self.player_data)
        self.evaluate(cats=cats, player_data=player_data)

    def sort(self, key, reverse=False):
        """
        Sort player data according to key and then display.
        Reverse the reverse! Display descending by default.
        """
        self.player_data.sort(key=lambda x: x[key], reverse=not reverse)
        self.display()


#Helper Functions
def mean(*args):
    return sum(float(x) for x in args) / len(args)

def stdev(*args):
    avg = mean(*args)
    deviance = mean(*[(x - avg)**2 for x in args])
    return sqrt(deviance)

if __name__ == "__main__":
    a = Evaluator()
