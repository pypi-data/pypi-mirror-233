# yolo2labelme

Tool to convert yolo format dataset to labelme json format.

## Installation
```bash
pip install yolo-to-labelme
```
## Usage
Arguments:

`--yolo-annotation-dir` : path to dataset directory

`--labelme-output-dir` : path to output directory.
 
`--image-width` default value is 1024.

`--image-height` default value is 1024.

`--class-mapping-file` classes name file.
### CLI Usage:

Specify yolo-labels-directory, output directory and classes file.

```bash
yolo-to-labelme --yolo-annotation-dir path/to/yoloDataset --labelme-output-dir path/to/labelmeJsonDir --class-mapping-file path/to/classes-file
```

## Useful links
https://github.com/adeel-maker/yolo-to-labelme

Lableme to yolo : https://pypi.org/project/labelme2yolo/