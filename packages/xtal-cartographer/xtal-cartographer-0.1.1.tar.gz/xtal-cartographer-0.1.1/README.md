Example Usage:

```
cartographer -i PDB.mtz -o PDB.map -intensity FWT -phase PHWT
```


```
usage: cartographer [-h] [-m M] -i I -o O [-r [R]] [-intensity [INTENSITY]] [-phase [PHASE]]

options:
  -h, --help              show this help message and exit
  -m M, -model_path M     Path to model
  -i I, -input I          Input mtz path
  -o O, -output O         Output map path 
  -r [R], -resolution [R] Resolution cutoff to apply to mtz
  -intensity [INTENSITY]  Name of intensity column in MTZ
  -phase [PHASE]          Name of phase column in MTZ
```
