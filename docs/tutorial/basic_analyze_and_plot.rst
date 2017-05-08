
Basic analyzing and plotting
============================

This tutorial will go over the basics of analyzing ``eggs``, the primary
data structure used in ``quail``. To learn about how an egg is set up,
see the egg tutorial.

An egg is made up of (at minimum) the words presented to a subject and
the words recalled by the subject. With these, two components we can
perform a number of analyses:

1. **Recall Accuracy** - the proportion of words presented that were
   later recalled
2. **Serial Position Curve** - recall accuracy as a function of the
   encoding position of the word
3. **Probability of First Recall** - the probability that a word will be
   recalled first as a function of its encoding position
4. **Lag-CRP** - given the recall of word n, the probability of
   recalling words at neighboring positions (n+/-1, 2, 3 etc).

If we have a set of features for the stimuli, we can also compute a
**Memory Fingerprint**, which is an estimate of how a subject clusters
their recall responses with respect to features of a stimulus (see the
fingerprint tutorial for more on this).

Let's get to analyzing some ``eggs``. First, we'll load in some example
data:

.. code:: ipython2

    import quail
    egg = quail.load_example_data()

This dataset is comprised of 19 subjects, who each performed 16
study/test blocks of 16 words each. Here are some of the presented
words:

.. code:: ipython2

    egg.pres.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>10</th>
          <th>11</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">0</th>
          <th>0</th>
          <td>HARMONICA</td>
          <td>UKULELE</td>
          <td>COTTONWOOD</td>
          <td>BLENDER</td>
          <td>CUP</td>
          <td>JUMPER</td>
          <td>MIXER</td>
          <td>ROBE</td>
          <td>OAK</td>
          <td>COLANDER</td>
          <td>SPRUCE</td>
          <td>SHIRT</td>
          <td>MARIMBA</td>
          <td>BELT</td>
          <td>BANJO</td>
          <td>EVERGREEN</td>
        </tr>
        <tr>
          <th>1</th>
          <td>LARVA</td>
          <td>WILLOW</td>
          <td>GUITAR</td>
          <td>FINGER</td>
          <td>XYLOPHONE</td>
          <td>POPLAR</td>
          <td>HAND</td>
          <td>SCORPION</td>
          <td>ANKLE</td>
          <td>MONARCH</td>
          <td>EUCALYPTUS</td>
          <td>ASH</td>
          <td>ACCORDION</td>
          <td>BONGOS</td>
          <td>LIP</td>
          <td>WORM</td>
        </tr>
        <tr>
          <th>2</th>
          <td>BARN</td>
          <td>HIPPOPOTAMUS</td>
          <td>KNUCKLE</td>
          <td>DONKEY</td>
          <td>DOG</td>
          <td>KITCHEN</td>
          <td>PETUNIA</td>
          <td>CARNATION</td>
          <td>ROSE</td>
          <td>GAZEBO</td>
          <td>TIGER</td>
          <td>HEART</td>
          <td>ALCOVE</td>
          <td>FACE</td>
          <td>EAR</td>
          <td>TULIP</td>
        </tr>
        <tr>
          <th>3</th>
          <td>CAMISOLE</td>
          <td>FURNACE</td>
          <td>ARTICHOKE</td>
          <td>IRAN</td>
          <td>EGYPT</td>
          <td>CHIMNEY</td>
          <td>CUBA</td>
          <td>POTATO</td>
          <td>LOBBY</td>
          <td>SPINACH</td>
          <td>GARLIC</td>
          <td>GERMANY</td>
          <td>CLOSET</td>
          <td>BLOUSE</td>
          <td>JACKET</td>
          <td>SUIT</td>
        </tr>
        <tr>
          <th>4</th>
          <td>OVEN</td>
          <td>TRUMPET</td>
          <td>MONTREAL</td>
          <td>PARIS</td>
          <td>TUBA</td>
          <td>ARMS</td>
          <td>STOMACH</td>
          <td>PELVIS</td>
          <td>THERMOMETER</td>
          <td>BROILER</td>
          <td>HIP</td>
          <td>ROME</td>
          <td>DALLAS</td>
          <td>MUG</td>
          <td>TAMBOURINE</td>
          <td>PICCOLO</td>
        </tr>
      </tbody>
    </table>
    </div>



and some of the recalled words:

.. code:: ipython2

    egg.rec.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>10</th>
          <th>11</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
          <th>16</th>
          <th>17</th>
          <th>18</th>
          <th>19</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">0</th>
          <th>0</th>
          <td>EVERGREEN</td>
          <td>COTTONWOOD</td>
          <td>MARIMBA</td>
          <td>CUP</td>
          <td>MIXER</td>
          <td>BELT</td>
          <td>UKULELE</td>
          <td>HARMONICA</td>
          <td>MIXER</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td>XYLOPHONE</td>
          <td>LARVA</td>
          <td>WILLOW</td>
          <td>EUCALYPTUS</td>
          <td>BONGOS</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2</th>
          <td>BARN</td>
          <td>HIPPOPOTAMUS</td>
          <td>ALCOVE</td>
          <td>TULIP</td>
          <td>ROSE</td>
          <td>CHRYSANTHEMUM</td>
          <td>TIGER</td>
          <td>FACE</td>
          <td>EAR</td>
          <td>HEART</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3</th>
          <td>BLOUSE</td>
          <td>CAMISOLE</td>
          <td>JACKET</td>
          <td>SUIT</td>
          <td>LOBBY</td>
          <td>KITCHEN</td>
          <td>FURNACE</td>
          <td>EGYPT</td>
          <td>IRAN</td>
          <td>GERMANY</td>
          <td>SPINACH</td>
          <td>POTATO</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>4</th>
          <td>PICCOLO</td>
          <td>MIAMI</td>
          <td>PELVIS</td>
          <td>HIP</td>
          <td>STOMACH</td>
          <td>THERMOMETER</td>
          <td>MONTREAL</td>
          <td>ROME</td>
          <td>PARIS</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



We can start with the simplest analysis - recall accuracy - which is
just the proportion of words recalled that were in the encoding lists.
To compute accuracy, simply call the ``analyze`` function, with the
``analysis`` key word argument set to ``accuracy``:

Recall Accuracy
---------------

.. code:: ipython2

    accuracy = quail.analyze(egg, analysis='accuracy')
    accuracy.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">0</th>
          <th>0</th>
          <td>0.533333</td>
        </tr>
        <tr>
          <th>1</th>
          <td>0.333333</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0.600000</td>
        </tr>
        <tr>
          <th>3</th>
          <td>0.733333</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0.533333</td>
        </tr>
      </tbody>
    </table>
    </div>



The result is a multi-index Pandas DataFrame where the first-level index
is the subject identifier and the second level index is the list number.
By default, note that each list is analyzed separately. However, you can
easily return the average over lists using the ``listgroup`` kew word
argument:

.. code:: ipython2

    accuracy_avg = quail.analyze(egg, analysis='accuracy', listgroup=['average']*16)
    accuracy_avg.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <th>average</th>
          <td>0.495833</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.933333</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.587500</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.500000</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.529167</td>
        </tr>
      </tbody>
    </table>
    </div>



Now, the result is a single value for each subject representing the
average accuracy across the 16 lists. The ``listgroup`` kwarg can also
be used to do some fancier groupings, like splitting the data into the
first and second half of the experiment:

.. code:: ipython2

    accuracy_split = quail.analyze(egg, analysis='accuracy', listgroup=['First Half']*8+['Second Half']*8)
    accuracy_split.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2" valign="top">0</th>
          <th>Second Half</th>
          <td>0.475000</td>
        </tr>
        <tr>
          <th>First Half</th>
          <td>0.516667</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">1</th>
          <th>Second Half</th>
          <td>0.950000</td>
        </tr>
        <tr>
          <th>First Half</th>
          <td>0.916667</td>
        </tr>
        <tr>
          <th>2</th>
          <th>Second Half</th>
          <td>0.508333</td>
        </tr>
      </tbody>
    </table>
    </div>



These analysis results can be passed directly into the plot function
like so:

.. code:: ipython2

    ax = quail.plot(accuracy_split)



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_14_0.png


For more details on plotting, see the plot tutorial. Next, lets take a
look at the serial position curve analysis. As stated above the serial
position curve (or spc) computes recall accuracy as a function of the
encoding position of the word. To use it, use the same ``analyze``
function illustrated above, but set the ``analysis`` kwarg to ``spc``.
Let's also average across lists within subject:

Serial Position Curve
---------------------

.. code:: ipython2

    spc = quail.analyze(egg, analysis='spc', listgroup=['average']*16)
    spc.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>10</th>
          <th>11</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
          <th>16</th>
          <th>17</th>
          <th>18</th>
          <th>19</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <th>average</th>
          <td>0.7500</td>
          <td>0.6875</td>
          <td>0.3125</td>
          <td>0.3750</td>
          <td>0.3125</td>
          <td>0.1875</td>
          <td>0.4375</td>
          <td>0.3125</td>
          <td>0.3750</td>
          <td>0.1875</td>
          <td>0.5625</td>
          <td>0.5000</td>
          <td>0.5625</td>
          <td>0.5625</td>
          <td>0.5000</td>
          <td>0.8125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.8125</td>
          <td>0.9375</td>
          <td>0.8750</td>
          <td>0.9375</td>
          <td>0.8125</td>
          <td>0.9375</td>
          <td>1.0000</td>
          <td>0.6875</td>
          <td>0.9375</td>
          <td>0.8125</td>
          <td>0.6875</td>
          <td>0.8125</td>
          <td>0.9375</td>
          <td>0.9375</td>
          <td>0.9375</td>
          <td>0.9375</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.8125</td>
          <td>0.6875</td>
          <td>0.5000</td>
          <td>0.6875</td>
          <td>0.5000</td>
          <td>0.5000</td>
          <td>0.4375</td>
          <td>0.5000</td>
          <td>0.5625</td>
          <td>0.5000</td>
          <td>0.4375</td>
          <td>0.5000</td>
          <td>0.5625</td>
          <td>0.3125</td>
          <td>0.5625</td>
          <td>0.7500</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.6250</td>
          <td>0.4375</td>
          <td>0.4375</td>
          <td>0.3125</td>
          <td>0.4375</td>
          <td>0.3750</td>
          <td>0.2500</td>
          <td>0.3125</td>
          <td>0.2500</td>
          <td>0.5625</td>
          <td>0.5625</td>
          <td>0.3125</td>
          <td>0.3750</td>
          <td>0.6875</td>
          <td>0.8125</td>
          <td>0.7500</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.9375</td>
          <td>0.6250</td>
          <td>0.6875</td>
          <td>0.6250</td>
          <td>0.3750</td>
          <td>0.3125</td>
          <td>0.3750</td>
          <td>0.5000</td>
          <td>0.2500</td>
          <td>0.3750</td>
          <td>0.3125</td>
          <td>0.3750</td>
          <td>0.5000</td>
          <td>0.4375</td>
          <td>0.4375</td>
          <td>0.8125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    </div>



The result is a df where each row is a subject and each column is the
encoding position of the word. To plot, simply pass the result of the
analysis function to the plot function:

.. code:: ipython2

    ax = quail.plot(spc)



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_19_0.png


Probability of First Recall
---------------------------

The next analysis we'll take a look at is the probability of first
recall, which is the probability that a word will be recalled first as a
function of its encoding position. To compute this, call the ``analyze``
function with the ``analysis`` kwarg set to ``pfr``. Again, we'll
average over lists:

.. code:: ipython2

    pfr = quail.analyze(egg, analysis='pfr', listgroup=['average']*16)
    pfr.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>10</th>
          <th>11</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
          <th>16</th>
          <th>17</th>
          <th>18</th>
          <th>19</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <th>average</th>
          <td>0.2500</td>
          <td>0.0</td>
          <td>0.0000</td>
          <td>0.0625</td>
          <td>0.0625</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0000</td>
          <td>0.0625</td>
          <td>0.0625</td>
          <td>0.0625</td>
          <td>0.0625</td>
          <td>0.0625</td>
          <td>0.1875</td>
          <td>0.1250</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.0000</td>
          <td>0.0</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.1250</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0000</td>
          <td>0.0625</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0625</td>
          <td>0.1250</td>
          <td>0.1875</td>
          <td>0.4375</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.2500</td>
          <td>0.0</td>
          <td>0.1250</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0625</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0625</td>
          <td>0.0000</td>
          <td>0.5000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.1875</td>
          <td>0.0</td>
          <td>0.0625</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0625</td>
          <td>0.1875</td>
          <td>0.1875</td>
          <td>0.1875</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.4375</td>
          <td>0.0</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0000</td>
          <td>0.0625</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0000</td>
          <td>0.0625</td>
          <td>0.1875</td>
          <td>0.1875</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    </div>



This df is set up just like the serial position curve. To plot:

.. code:: ipython2

    ax = quail.plot(pfr)



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_23_0.png


Lag-CRP
-------

The next analysis to consider is the lag-CRP, which again is a function
that given the recall of word n, returns the probability of recalling
words at neighboring positions (n+/-1, 2, 3 etc). To use it? You guessed
it: call the ``analyze`` function with the ``analysis`` kwarg set to
``lagcrp``:

.. code:: ipython2

    lagcrp = quail.analyze(egg, analysis='lagcrp', listgroup=['average']*16)
    lagcrp.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>-15</th>
          <th>-14</th>
          <th>-13</th>
          <th>-12</th>
          <th>-11</th>
          <th>-10</th>
          <th>-9</th>
          <th>-8</th>
          <th>-7</th>
          <th>-6</th>
          <th>...</th>
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>10</th>
          <th>11</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <th>average</th>
          <td>0.000</td>
          <td>0.00000</td>
          <td>0.135417</td>
          <td>0.041667</td>
          <td>0.062500</td>
          <td>0.028125</td>
          <td>0.062500</td>
          <td>0.097917</td>
          <td>0.056250</td>
          <td>0.010417</td>
          <td>...</td>
          <td>0.031250</td>
          <td>0.012500</td>
          <td>0.067708</td>
          <td>0.135417</td>
          <td>0.046875</td>
          <td>0.156250</td>
          <td>0.062500</td>
          <td>0.00000</td>
          <td>0.0625</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.000</td>
          <td>0.18750</td>
          <td>0.125000</td>
          <td>0.057292</td>
          <td>0.088542</td>
          <td>0.072917</td>
          <td>0.094792</td>
          <td>0.125000</td>
          <td>0.104315</td>
          <td>0.072470</td>
          <td>...</td>
          <td>0.075000</td>
          <td>0.080208</td>
          <td>0.119792</td>
          <td>0.083333</td>
          <td>0.135417</td>
          <td>0.145833</td>
          <td>0.031250</td>
          <td>0.06250</td>
          <td>0.0625</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.125</td>
          <td>0.03125</td>
          <td>0.125000</td>
          <td>0.031250</td>
          <td>0.031250</td>
          <td>0.041667</td>
          <td>0.052083</td>
          <td>0.083333</td>
          <td>0.075000</td>
          <td>0.050595</td>
          <td>...</td>
          <td>0.099554</td>
          <td>0.080208</td>
          <td>0.033333</td>
          <td>0.036458</td>
          <td>0.015625</td>
          <td>0.057292</td>
          <td>0.083333</td>
          <td>0.03125</td>
          <td>0.0625</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.000</td>
          <td>0.03125</td>
          <td>0.062500</td>
          <td>0.052083</td>
          <td>0.057292</td>
          <td>0.048958</td>
          <td>0.010417</td>
          <td>0.036458</td>
          <td>0.080208</td>
          <td>0.000000</td>
          <td>...</td>
          <td>0.107887</td>
          <td>0.000000</td>
          <td>0.093750</td>
          <td>0.125000</td>
          <td>0.093750</td>
          <td>0.000000</td>
          <td>0.031250</td>
          <td>0.00000</td>
          <td>0.0625</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.000</td>
          <td>0.21875</td>
          <td>0.125000</td>
          <td>0.041667</td>
          <td>0.098958</td>
          <td>0.052083</td>
          <td>0.020833</td>
          <td>0.036458</td>
          <td>0.015625</td>
          <td>0.046875</td>
          <td>...</td>
          <td>0.054167</td>
          <td>0.052083</td>
          <td>0.000000</td>
          <td>0.046875</td>
          <td>0.062500</td>
          <td>0.062500</td>
          <td>0.114583</td>
          <td>0.00000</td>
          <td>0.1875</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 31 columns</p>
    </div>



Unlike the previous two analyses, the result of this analysis returns a
df where the number of columns are double the length of the lists. To
view the results:

.. code:: ipython2

    ax= quail.plot(lagcrp)



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_27_0.png


Memory Fingerprint
------------------

Last but not least is the memory fingerprint analysis. For a detailed
treatment of this analysis, see the fingerprint tutorial.

As described in the fingerprint tutorial, the ``features`` data
structure is used to estimate how subjects cluster their recall
responses with respect to the features of the encoded stimuli. Briefly,
these estimates are derived by computing the similarity of neighboring
recall words along each feature dimension. For example, if you recall
"dog", and then the next word you recall is "cat", your clustering by
category score would increase because the two recalled words are in the
same category. Similarly, if after you recall "cat" you recall the word
"can", your clustering by starting letter score would increase, since
both words share the first letter "c". This logic can be extended to any
number of feature dimensions.

To use this analysis function, you'll need to include a ``features``
field when you create your ``egg``. Our example data has this field
included. For more info on how to create this field, see the egg and
fingerprint tutorials.

Here is a glimpse of the features df:

.. code:: ipython2

    egg.features.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>10</th>
          <th>11</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="5" valign="top">0</th>
          <th>0</th>
          <td>{u'category': u'INSTRUMENTS', u'color': [76, 1...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [236, ...</td>
          <td>{u'category': u'TREES', u'color': [177, 159, 1...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [5...</td>
          <td>{u'category': u'CLOTHING', u'color': [173, 175...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'CLOTHING', u'color': [164, 251...</td>
          <td>{u'category': u'TREES', u'color': [41, 54, 36]...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [2...</td>
          <td>{u'category': u'TREES', u'color': [240, 4, 31]...</td>
          <td>{u'category': u'CLOTHING', u'color': [224, 224...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [25, 6...</td>
          <td>{u'category': u'CLOTHING', u'color': [241, 165...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [115, ...</td>
          <td>{u'category': u'TREES', u'color': [75, 128, 15...</td>
        </tr>
        <tr>
          <th>1</th>
          <td>{u'category': u'INSECTS', u'color': [4, 235, 2...</td>
          <td>{u'category': u'TREES', u'color': [228, 126, 9...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [220, ...</td>
          <td>{u'category': u'BODY PARTS', u'color': [54, 23...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [251, ...</td>
          <td>{u'category': u'TREES', u'color': [169, 107, 5...</td>
          <td>{u'category': u'BODY PARTS', u'color': [189, 2...</td>
          <td>{u'category': u'INSECTS', u'color': [132, 113,...</td>
          <td>{u'category': u'BODY PARTS', u'color': [231, 1...</td>
          <td>{u'category': u'INSECTS', u'color': [189, 191,...</td>
          <td>{u'category': u'TREES', u'color': [162, 214, 1...</td>
          <td>{u'category': u'TREES', u'color': [190, 18, 19...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [231, ...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [219, ...</td>
          <td>{u'category': u'BODY PARTS', u'color': [193, 8...</td>
          <td>{u'category': u'INSECTS', u'color': [169, 134,...</td>
        </tr>
        <tr>
          <th>2</th>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'MAMMALS', u'color': [236, 1, 3...</td>
          <td>{u'category': u'BODY PARTS', u'color': [10, 22...</td>
          <td>{u'category': u'MAMMALS', u'color': [38, 159, ...</td>
          <td>{u'category': u'MAMMALS', u'color': [163, 32, ...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'FLOWERS', u'color': [119, 83, ...</td>
          <td>{u'category': u'FLOWERS', u'color': [223, 233,...</td>
          <td>{u'category': u'FLOWERS', u'color': [183, 214,...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'MAMMALS', u'color': [151, 249,...</td>
          <td>{u'category': u'BODY PARTS', u'color': [209, 1...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'BODY PARTS', u'color': [161, 2...</td>
          <td>{u'category': u'BODY PARTS', u'color': [104, 2...</td>
          <td>{u'category': u'FLOWERS', u'color': [237, 26, ...</td>
        </tr>
        <tr>
          <th>3</th>
          <td>{u'category': u'CLOTHING', u'color': [69, 48, ...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'VEGETABLES', u'color': [246, 1...</td>
          <td>{u'category': u'COUNTRIES', u'color': [212, 17...</td>
          <td>{u'category': u'COUNTRIES', u'color': [12, 17,...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'COUNTRIES', u'color': [141, 17...</td>
          <td>{u'category': u'VEGETABLES', u'color': [16, 16...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'VEGETABLES', u'color': [235, 1...</td>
          <td>{u'category': u'VEGETABLES', u'color': [67, 46...</td>
          <td>{u'category': u'COUNTRIES', u'color': [250, 10...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'CLOTHING', u'color': [80, 195,...</td>
          <td>{u'category': u'CLOTHING', u'color': [176, 187...</td>
          <td>{u'category': u'CLOTHING', u'color': [137, 93,...</td>
        </tr>
        <tr>
          <th>4</th>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [160, ...</td>
          <td>{u'category': u'CITIES', u'color': [226, 253, ...</td>
          <td>{u'category': u'CITIES', u'color': [56, 22, 15...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [145, ...</td>
          <td>{u'category': u'BODY PARTS', u'color': [116, 1...</td>
          <td>{u'category': u'BODY PARTS', u'color': [206, 1...</td>
          <td>{u'category': u'BODY PARTS', u'color': [116, 1...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'BODY PARTS', u'color': [16, 23...</td>
          <td>{u'category': u'CITIES', u'color': [144, 96, 2...</td>
          <td>{u'category': u'CITIES', u'color': [198, 225, ...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [144, ...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [45, 7...</td>
        </tr>
      </tbody>
    </table>
    </div>



Like the other analyses, computing the memory fingerprint can be done
using the ``analyze`` function with the ``analysis`` kwarg set to
``fingerprint``:

.. code:: ipython2

    fingerprint = quail.analyze(egg, analysis='fingerprint', listgroup=['average']*16)
    fingerprint.head()


.. parsed-literal::

    /Users/andyheusser/Library/Enthought/Canopy_64bit/User/lib/python2.7/site-packages/numpy/core/fromnumeric.py:2889: RuntimeWarning: Mean of empty slice.
      out=out, **kwargs)
    /Users/andyheusser/Library/Enthought/Canopy_64bit/User/lib/python2.7/site-packages/numpy/core/_methods.py:80: RuntimeWarning: invalid value encountered in double_scalars
      ret = ret.dtype.type(ret / rcount)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>category</th>
          <th>color</th>
          <th>location</th>
          <th>firstLetter</th>
          <th>wordLength</th>
          <th>size</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <th>average</th>
          <td>0.632417</td>
          <td>0.483138</td>
          <td>0.502924</td>
          <td>0.506006</td>
          <td>0.514513</td>
          <td>0.596458</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.778671</td>
          <td>0.502356</td>
          <td>0.507287</td>
          <td>0.509048</td>
          <td>0.490684</td>
          <td>0.677017</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.638698</td>
          <td>0.484930</td>
          <td>0.500614</td>
          <td>0.505704</td>
          <td>0.448253</td>
          <td>0.636060</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.596828</td>
          <td>0.508649</td>
          <td>0.543621</td>
          <td>0.487804</td>
          <td>0.486110</td>
          <td>0.565875</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.565906</td>
          <td>0.507093</td>
          <td>0.496227</td>
          <td>0.510562</td>
          <td>0.511061</td>
          <td>0.573317</td>
        </tr>
      </tbody>
    </table>
    </div>



The result of this analysis is a df, where each row is a subject's
fingerprint and each column is a feature dimensions. The values
represent a subjects tendency to cluster their recall responses along a
particular feature dimensions. They are probability values, and thus,
greater values indicate more clustering along that feature dimension. To
plot, simply pass the result to the plot function:

.. code:: ipython2

    ax = quail.plot(fingerprint)



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_33_0.png


This result suggests that subjects in this example dataset tended to
cluster their recall responses by category as well as the size (bigger
or smaller than a shoebox) of the word.
