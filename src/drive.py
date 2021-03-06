#!/usr/bin/env/python3

import argparse
from derp.inferer import Inferer
from derp.state import State
import derp.util

def main(args):

    # Load configs
    hw_config = derp.util.load_config(args.hw)
    sw_config = derp.util.load_config(args.sw)

    # Prepare variables
    state = State()
    components = derp.util.load_components(hw_config, state)
    inferer = Inferer(hw_config, sw_config, args.path, state)

    # Event loop
    print("Ready")
    while True:

        # Sense Plan Act loop
        for component in components:
            component.sense(state)
        inferer.plan(state)
        for component in components:
            component.act(state)

        # Write out state and each component buffer
        if state['record']:
            state.scribe(args.hw)
            state.write()
            inferer.scribe(state)
            inferer.write()
            for component in components:
                component.scribe(state)
                component.write()

        # Print to the screen for verbose mode
        if args.verbose:
            print("%.3f %3s %4s %.3f %4s %.3f" % (state['timestamp'] / 1E6,
                                                  'REC' if state['record'] else 'off',
                                                  'Aspd' if state['auto_speed'] else '!spd',
                                                  state['speed'],
                                                  'Astr' if state['auto_steer'] else '!str',
                                                  state['steer']))

        # Exit
        if 'exit' in state and state['exit']:
            return
            

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--hw', type=str, required=True, help="physical configuration path")
    parser.add_argument('--sw', type=str, default=None, help="inferer configuration path")
    parser.add_argument('--path', type=str, default=None, help="folder where models are stored")
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    
    main(args)
