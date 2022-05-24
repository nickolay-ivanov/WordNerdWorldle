import shelve
d = shelve.open('stats.txt')


def add_stats(win, num_of_turns):
    d['Wordle_Played'] = d['Wordle_Played'] + 1
    if win:
        d['Wordle_Wins'] = d['Wordle_Wins'] + 1
        d['Wordle_WinStreak'] = d['Wordle_WinStreak'] + 1
        if num_of_turns == 1:
            d['Wordle_win_in_one'] = d['Wordle_win_in_one'] + 1
        elif num_of_turns == 2:
            d['Wordle_win_in_two'] = d['Wordle_win_in_two'] + 1
        elif num_of_turns == 3:
            d['Wordle_win_in_three'] = d['Wordle_win_in_three'] + 1
        elif num_of_turns == 4:
            d['Wordle_win_in_four'] = d['Wordle_win_in_four'] + 1
        elif num_of_turns == 5:
            d['Wordle_win_in_five'] = d['Wordle_win_in_five'] + 1
        elif num_of_turns == 6:
            d['Wordle_win_in_six'] = d['Wordle_win_in_six'] + 1
    else:
        d['Wordle_WinStreak'] = 0
    d['Wordle_WinPerc'] = d['Wordle_Wins'] / d['Wordle_Played'] * 100


def print_score():
    print("Played: {}".format(d['Played']))
    print("Wins: {}".format(d['Wins']))
    print("WinPerc: {}".format(round(d['WinPerc'])))
    print("Win in 1: {}".format(d['win_in_one']))
    print("Win in 2: {}".format(d['win_in_two']))
    print("Win in 3: {}".format(d['win_in_three']))
    print("Win in 4: {}".format(d['win_in_four']))
    print("Win in 5: {}".format(d['win_in_five']))
    print("Win in 6: {}".format(d['win_in_six']))


add_stats(True, 5)
print_score()
