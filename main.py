import argparse, chalk
import sounddevice as sd

DEVICE = 8
DIFF = 0.5

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args = parser.parse_args()

def main():

    if args.list_devices:
        print('#' * 40)
        print('Inputs!')
        print('#' * 40)
        print(sd.query_devices('input'))
        parser.exit(0)

    def callback(indata, frames, time, status):
        if status:
            print(status)

        indata.shape = -1,2
        indata = indata.T

        Zero = indata[0]
        One = indata[1]

        #try mean
        l = Zero.__abs__().sum()
        r = One.__abs__().sum()
        
        if l > r:
            if l-DIFF >= r:
                print(chalk.red('LEFT'))
            else:
                print(chalk.yellow('CENTER'))
        else:
            if l <= r-DIFF:
                print(chalk.blue('RIGHT'))
            else:
                print(chalk.yellow('CENTER'))

    with sd.InputStream(device=DEVICE, channels=2, callback=callback):
        while True:
            continue





if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print('#' * 40)
        print('Program Ended!')
        print('#' * 40)
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))