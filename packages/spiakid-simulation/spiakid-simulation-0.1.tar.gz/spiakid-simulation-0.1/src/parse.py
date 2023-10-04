import os
import argparse
from pathlib import Path
import pathlib
import Photon_simulation as sim
import Functions.Yaml.Yaml_rw as write
import Image_process.Datacube_interface as Inter

def parse():

    parser = argparse.ArgumentParser(description='MKID phase simulation')
    parser.add_argument('--template', dest = 'save_link',help = 'Create a template of simulation data file')
    parser.add_argument('--yml', help ='Path to the simulation data file',dest ='yml')
    parser.add_argument('--output', help='Folder to store output', dest='output')
    parser.add_argument('--sim', help='Launch the simulation',dest = 'Launch')
    parser.add_argument('--image', help = 'Simulate an image', dest = 'Shape')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse()

    if args.save_link:
        link = args.save_link + '/template.yaml'
        write.write_template_image(link)

    if args.yml and args.output:
        print('yes')
    
    if args.Launch:
        print(sim.Photon_simulator(args.Launch))
    
    if args.Shape:
        Inter.Interface(int(eval(args.Shape)[0]),int(eval(args.Shape)[1]))