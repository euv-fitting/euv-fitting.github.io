"""
/////   WIP  /////
This file is a supplement to calibrate_utils.md and generates the plots seen
in that document.

Author: Hunter Staiger
Last Updated: 7/23/2022
"""
from matplotlib import pyplot as plt

from euv_fitting.calibrate.utils import SpeReader

spe_loc = './example_data/270.spe'
plot_loc = './plots/'


def main():
    # SpeReader Section
    print('---------------')
    S = SpeReader(spe_loc)
    print('Loading SPE data')

    print(f'Image Shape: ({S.frame}, {S.xdim})')

    print('rawtime = ', S.metadata['rawtime'])

    S.print_metadata()
    img = S.load_img()
    f = plt.Figure()
    plt.plot(img[4])

    plt.xlabel('Channel')
    plt.ylabel('Intensity [ADU]')
    plt.title('Frame 1 of the .spe image')

    plt.show()
    plt.savefig(plot_loc + 'Single Unfiltered Frame.png')


if __name__ == '__main__':
    main()
