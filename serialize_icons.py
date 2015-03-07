import clr
clr.AddReference('System.Drawing')

from System.Drawing import Bitmap, Icon
from System.IO import Directory, File, Path
from System.Runtime.Serialization.Formatters.Binary import BinaryFormatter

from argparse import ArgumentParser


def convert_all(path, ext):

    formatter = BinaryFormatter()
    iconDirectory = path

    for fpath in Directory.GetFiles(iconDirectory):
        
        if fpath[-4:] not in ext:
            continue

        name = Path.GetFileNameWithoutExtension(fpath)
        out = Path.Combine(iconDirectory, name + '.dat')

        try:
            image = Bitmap(fpath)
        except ValueError as e:
            raise ValueError(
                "Error loading Bitmap('{0}').\nError Msg: {1}".format(fpath, e)
            )

        stream = File.Create(out)
        formatter.Serialize(stream, image)
        stream.Close()


def main():

    usage = "python serialize_icons.py --path './icons', --extensions .ico .gif"
    description = 'Script to serialize icons/gifs into binary format'
    
    parser = ArgumentParser(usage=usage, description=description)
    parser.add_argument(
        '--path', type=str, help='Valid directory path', 
    )
    parser.add_argument(
        '--extensions', type=str, nargs='+'
    )

    args = parser.parse_args()
    path = args.path
    ext = args.extensions

    if path is None:
        path = __file__
    if ext is None:
        ext = ('.ico', '.gif')

    convert_all(path, ext)


if __name__ == '__main__':
    
    main()