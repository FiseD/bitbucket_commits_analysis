import sys
import json
from datetime import datetime
from collections import defaultdict, Counter
import matplotlib.pyplot as plt


def create_bar_chart(author, x, y, tops=None):
    fig, ax = plt.subplots()
    ax.bar(x, y, 0.35)

    if tops:
        x = tops
    ax.set(xlabel='dates / words', ylabel='commits / words count',
           title='{} {} - {}'.format(author, x[0], x[-1]))
    ax.autoscale()
    plt.show()

def show_usage():
    print('\nUse python make_charts.py with args:')
    print('\t <User> - username from authors list')
    print('\t <Date from> - Start date commits with YYYY-MM-DD format')
    print('\t <Date to> - End date commits with YYYY-MM-DD format')
    print('\t <Top words count from> - First num from interaval of top words counts')
    print('\t <Top words count to> - Second num from interaval of top words counts')
    print('Like python make_charts.py <user> <date_from> <date_to> <top_from> <top_to>')


if __name__ == '__main__':
    try:
        user = sys.argv[1]
        date_from = sys.argv[2]
        date_to = sys.argv[3]
        top_words_from = int(sys.argv[4])
        top_words_to = int(sys.argv[5])
    except IndexError:
        show_usage()
        exit()

    with open('data.json', 'r') as f:
        data = json.loads(f.read())

    print('Authors list:')
    authors = sorted(list(data.keys()))
    print(', '.join(authors))

    commits_count_by_date = defaultdict(lambda: defaultdict(int))
    for author, dates in data.items():
        for date, commits in dates.items():
            date = date[:10]
            commits_count_by_date[author][date] += 1

    words_count_by_author = defaultdict(lambda: defaultdict(list))
    for author, dates in data.items():
        for date, message in dates.items():
            date = date[:10]
            words_count_by_author[author][date].extend([x.lower() for x in message.split()])

    if user in authors:
        commits_dates = []
        commits_count = []
        for date, count in commits_count_by_date[user].items():
            if date >= date_from and date <= date_to:
                commits_dates.append(date)
                commits_count.append(count)

        if not commits_dates:
            print('\nNo commits in select dates.')
            exit()

        words_count = defaultdict(int)
        for date, counts in words_count_by_author[user].items():
            if date >= date_from and date <= date_to:
                counts = Counter(counts)
                for word, count in counts.items():
                        words_count[word] += count

        filtered_words_count = {}
        for word, count in words_count.items():
            if count >= top_words_from and count <= top_words_to:
                filtered_words_count[word] = count

        create_bar_chart(user, commits_dates, commits_count)
        create_bar_chart(user, list(filtered_words_count.keys()), list(filtered_words_count.values()), (top_words_from, top_words_to))

    else:
        print('\nUser not found.')
