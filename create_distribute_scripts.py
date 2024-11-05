import itertools as itt
from pathlib import Path
import csv


ROOT = Path('C:/Users/dominic/Downloads/IAU Poster Test')
path = ROOT / 'Posters_paid.csv'


def iter_data(csvfile):
    with Path(csvfile).open() as fp:
        for row in csv.reader(fp):
            if row:
                yield row


def load_screen_ids(csvfile, date, time):
    # division, date, time, screen, id, presenter, title
    for division, d, t, screen, id_, presenter, title in iter_data(csvfile):
        if time == t and date == d and screen.isdigit() and id_.isdigit():
            yield screen, id_


def create_ssh_script(date, time):
    output = ROOT / f'scripts/load-posters-aug{int(date):>02d}-{int(time):<02d}00.sh'
    # print( f'Aug {int(date):<02d}', f'{int(time):<02d}:00')

    screens, ids = zip(*load_screen_ids(path, f'Aug {int(date):>02d}', f'{int(time):<02d}:00'))
    with output.open('w') as file:
        for screen, id_ in zip(screens, ids):
            file.write(
                # f'scp {path.with_name("launch.py")} iau@pi{screen}:~/Desktop/Posters/launch.py',
                f"ssh iau@pi{screen} 'export DISPLAY=:0.0; python Desktop/Posters/launch.py {id_}'\n"
            )
            file.truncate()


if __name__ == '__main__':
    for date, time in itt.product(range(12, 16), (10, 15)):
        create_ssh_script(date, time)
#create_distribute_scripts.py
#Displaying create_distribute_scripts.py