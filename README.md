# shapes

shapes is a Python package for traditional and geometric morphometrics.

It can be used in a Python interpretator, or in a GUI online at [PhyloNimbus.com](http://www.phylonimbus.com/morphometrics/), where you can also digitize landmarks.

Uses include:

* Procrustes superimposition.
* Missing landmark estimation.

## Installation

shapes can be installed from the Python Package Index:

`pip install shapes`

## Usage

Read files from Landmark editor:

```
import shapes
lms = shapes.read('/path/to/file')
```

This returns a Shape object for that specimen.

Shape objects can be combined into ShapeSets:

```
shapeset = shapes.ShapeSet(name="Theropod skulls")
shapeset.append_shape(lms)
```

Once you've added all relevant Shapes to a ShapeSet, the landmarks can be
aligned using 
[Procrustes Analysis](https://en.wikipedia.org/wiki/Procrustes_analysis):

```
aligned_shapeset = shapes.procrustes_align(shapeset)
```

Note that this Procrustes alignment will work even if some landmarks are missing
 (in which case alignment will be based solely on the non-missing landmarks). 
This could lead to systematic biases in your dataset depending on the 
distribution of missing data. *Caveat emptor...*

Once the data set has been aligned as in the previous step, missing data can 
be interpolated using one of two methods.

Using symmetry (for landmarks that are part of symmetrical pairs):

```
paired_landmarks = [(1,4),(2,5),(3,6)]
symmetrically_reconstructed = shapes.missing.estimate_from_symmetry(
                                aligned_shapeset,
                                paired_landmarks)
```

Or using the mean of the aligned homologous landmark in specimens where it is 
present:

```
mean_reconstructed = shapes.missing.estimate_from_mean(aligned_shapeset)
```

Landmarks from all Shapes in a ShapeSet can be exported to csv:

```
aligned_shapeset.export('output_file.csv')
```

## License

shapes is available under the MIT license.

## More information and citation

White, D.E. (2016) Chapter 3 *of* The Evolution and Phylogenetic Analysis of 
the Dinosaur Axial Skeleton. PhD Dissertation, George Washington University.