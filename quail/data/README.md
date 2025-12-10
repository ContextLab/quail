# Example data

This folder contains example datasets for use with the quail package.

## Datasets

### Ziman et al. (2018) - Free recall with automatic speech transcription

The `automatic.egg` and `manual.egg` files contain data from:

> Ziman, K., Heusser, A. C., Fitzpatrick, P. C., Field, C. E., & Manning, J. R. (2018). Is automatic speech-to-text transcription ready for use in psychological experiments? *Behavior Research Methods*, 50(6), 2597-2605. https://doi.org/10.3758/s13428-018-1037-4

A description of the data format, along with documentation for loading in the data and carrying out the analyses from the paper may be found [here](http://cdl-quail.readthedocs.io/en/latest/tutorial.html).

### Polyn et al. (2009) - Context Maintenance and Retrieval (CMR) model data

The `cmr.egg` file contains behavioral data from:

> Polyn, S. M., Norman, K. A., & Kahana, M. J. (2009). A context maintenance and retrieval model of organizational processes in free recall. *Psychological Review*, 116(1), 129-156. https://doi.org/10.1037/a0014420

This dataset contains 45 subjects who studied lists of 24 words each using either SIZE or ANIMACY encoding tasks. List types include:
- **Control (Size)**: All items studied using the SIZE task
- **Control (Animacy)**: All items studied using the ANIMACY task
- **Shift**: Items alternated between SIZE and ANIMACY encoding tasks

Features include: `item` (word), `task` (Size or Animacy), `temporal` (serial position), `wordpool_idx` (index into original wordpool), and `condition` (list type).

Load this dataset with:
```python
import quail
egg = quail.load_example_data('cmr')
```

### Murdock (1962) - Serial position effect in free recall

The `murd62.egg` file contains behavioral data from:

> Murdock, B. B. (1962). The serial position effect of free recall. *Journal of Experimental Psychology*, 64(5), 482-488. https://doi.org/10.1037/h0045106

This classic dataset contains 7200 trials across 6 experimental conditions varying in list length and presentation rate:

| Condition | List Length | Presentation Rate | Trials |
|-----------|-------------|-------------------|--------|
| LL10-2s   | 10 items    | 2 sec/item        | 1200   |
| LL15-2s   | 15 items    | 2 sec/item        | 1200   |
| LL20-1s   | 20 items    | 1 sec/item        | 1200   |
| LL20-2s   | 20 items    | 2 sec/item        | 1200   |
| LL30-1s   | 30 items    | 1 sec/item        | 1200   |
| LL40-1s   | 40 items    | 1 sec/item        | 1200   |

Features include: `item`, `temporal` (serial position), `list_length`, `rate` (presentation rate in seconds), and `condition`.

Load this dataset with:
```python
import quail
egg = quail.load_example_data('murd62')
```
