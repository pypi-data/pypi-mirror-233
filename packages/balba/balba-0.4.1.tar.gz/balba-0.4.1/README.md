# balba
Automatically generate a website showcasing Kicad projects. The website makes it easy to review multiple aspects
of a project from any device without the need to download any files or install KiCad.

Project named after [Bidens alba](https://wikipedia.org/wiki/Bidens_alba).

## Getting started
This program assumes the following:

1. All your KiCad projects are stored in a single directory, each one in its own subdirectory.
2. There exists a `balba.yaml` at the root.
3. Each project has a `README.md` at its root.
4. Said `README.md` has the appropriate front matter.

The structure should look something like:
```
├── balba.yaml
├── cocoro
│ ├── cocoro.kicad_pcb
│ ├── cocoro.kicad_prl
│ ├── cocoro.kicad_pro
│ ├── cocoro.kicad_sch
│ ├── ledc.kicad_sch
│ └── README.md
├── other_project
| ├── ...
```

Once that's done, all you have to do is `cd` into the root directory and run `balba`. By default, the output will
be stored on `./balba-build`.
