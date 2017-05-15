
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
5. **Temporal Clustering** - a measure of recall clustering by temporal
   proximity during encoding

If we have a set of features for the stimuli, we can also compute a
**Memory Fingerprint**, which is an estimate of how a subject clusters
their recall responses with respect to features of a stimulus (see the
fingerprint tutorial for more on this).

Let's get to analyzing some ``eggs``. First, we'll load in some example
data:

.. code:: ipython2

    import quail
    egg = quail.load_example_data()

This dataset is comprised of 30 subjects, who each performed 8
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
          <td>POMEGRANATE</td>
          <td>FLORIDA</td>
          <td>TOOTH</td>
          <td>ANTELOPE</td>
          <td>PANCREAS</td>
          <td>PEAR</td>
          <td>CLEMENTINE</td>
          <td>LEMON</td>
          <td>TONGUE</td>
          <td>MICHIGAN</td>
          <td>RIB</td>
          <td>MOOSE</td>
          <td>RACOON</td>
          <td>IOWA</td>
          <td>MONKEY</td>
          <td>KANSAS</td>
        </tr>
        <tr>
          <th>1</th>
          <td>GRIDDLE</td>
          <td>DAHLIA</td>
          <td>ONION</td>
          <td>PICKLE</td>
          <td>AZALEA</td>
          <td>LOG</td>
          <td>SAUCER</td>
          <td>FLOOR</td>
          <td>FOUNDATION</td>
          <td>BUTTERCUP</td>
          <td>STRAINER</td>
          <td>CAULIFLOWER</td>
          <td>ELEVATOR</td>
          <td>BROCCOLI</td>
          <td>CARPET</td>
          <td>DISH</td>
        </tr>
        <tr>
          <th>2</th>
          <td>AUSTRALIA</td>
          <td>ETHIOPIA</td>
          <td>CELERY</td>
          <td>ITALY</td>
          <td>BASS</td>
          <td>MARACAS</td>
          <td>YAMS</td>
          <td>PIG</td>
          <td>LION</td>
          <td>LETTUCE</td>
          <td>ZEBRA</td>
          <td>ELEPHANT</td>
          <td>POLAND</td>
          <td>VIOLA</td>
          <td>CARROT</td>
          <td>TROMBONE</td>
        </tr>
        <tr>
          <th>3</th>
          <td>PINE</td>
          <td>SCREWS</td>
          <td>TRIANGLE</td>
          <td>WEDGE</td>
          <td>HICKORY</td>
          <td>WIRE</td>
          <td>CELLO</td>
          <td>HONEYDEW</td>
          <td>RASPBERRY</td>
          <td>ELM</td>
          <td>HAMMER</td>
          <td>SAXOPHONE</td>
          <td>MAPLE</td>
          <td>PLUM</td>
          <td>FIG</td>
          <td>VIOLIN</td>
        </tr>
        <tr>
          <th>4</th>
          <td>DAISY</td>
          <td>DRESS</td>
          <td>SUNFLOWER</td>
          <td>KNIFE</td>
          <td>GIRDLE</td>
          <td>TOASTER</td>
          <td>FORK</td>
          <td>PANTS</td>
          <td>SKILLET</td>
          <td>UTAH</td>
          <td>MAINE</td>
          <td>LILY</td>
          <td>UNDERWEAR</td>
          <td>NARCISSUS</td>
          <td>MONTANA</td>
          <td>ARIZONA</td>
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
          <th>...</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
          <th>16</th>
          <th>17</th>
          <th>18</th>
          <th>19</th>
          <th>20</th>
          <th>21</th>
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
          <th rowspan="5" valign="top">0</th>
          <th>0</th>
          <td>KANSAS</td>
          <td>POMEGRANATE</td>
          <td>CLEMENTINE</td>
          <td>TOOTH</td>
          <td>FLORIDA</td>
          <td>RIB</td>
          <td>MICHIGAN</td>
          <td>LEMON</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
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
          <td>GRIDDLE</td>
          <td>ONION</td>
          <td>DAHLIA</td>
          <td>CAULIFLOWER</td>
          <td>BUTTERCUP</td>
          <td>AZALEA</td>
          <td>BROCCOLI</td>
          <td>ELEVATOR</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
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
          <td>AUSTRALIA</td>
          <td>MARACAS</td>
          <td>POLAND</td>
          <td>TROMBONE</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
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
          <td>HONEYDEW</td>
          <td>RASPBERRY</td>
          <td>ELM</td>
          <td>SAXOPHONE</td>
          <td>PLUM</td>
          <td>PINE</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>None</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
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
          <td>UTAH</td>
          <td>MONTANA</td>
          <td>NARCISSUS</td>
          <td>ARIZONA</td>
          <td>DAISY</td>
          <td>DRESS</td>
          <td>SUNFLOWER</td>
          <td>LILY</td>
          <td>KNIFE</td>
          <td>GIRDLE</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
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
    <p>5 rows × 22 columns</p>
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
          <td>0.500</td>
        </tr>
        <tr>
          <th>1</th>
          <td>0.500</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0.250</td>
        </tr>
        <tr>
          <th>3</th>
          <td>0.375</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0.625</td>
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

    accuracy_avg = quail.analyze(egg, analysis='accuracy', listgroup=['average']*8)
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
          <td>0.476562</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.960938</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.546875</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.757812</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.406250</td>
        </tr>
      </tbody>
    </table>
    </div>



Now, the result is a single value for each subject representing the
average accuracy across the 16 lists. The ``listgroup`` kwarg can also
be used to do some fancier groupings, like splitting the data into the
first and second half of the experiment:

.. code:: ipython2

    accuracy_split = quail.analyze(egg, analysis='accuracy', listgroup=['First Half']*4+['Second Half']*4)
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
          <td>0.546875</td>
        </tr>
        <tr>
          <th>First Half</th>
          <td>0.406250</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">1</th>
          <th>Second Half</th>
          <td>0.937500</td>
        </tr>
        <tr>
          <th>First Half</th>
          <td>0.984375</td>
        </tr>
        <tr>
          <th>2</th>
          <th>Second Half</th>
          <td>0.625000</td>
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

    spc = quail.analyze(egg, analysis='spc', listgroup=['average']*8)
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
          <th>...</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
          <th>16</th>
          <th>17</th>
          <th>18</th>
          <th>19</th>
          <th>20</th>
          <th>21</th>
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
          <td>1.0</td>
          <td>0.750</td>
          <td>0.750</td>
          <td>0.375</td>
          <td>0.500</td>
          <td>0.125</td>
          <td>0.250</td>
          <td>0.375</td>
          <td>0.375</td>
          <td>0.500</td>
          <td>...</td>
          <td>0.375</td>
          <td>0.625</td>
          <td>0.25</td>
          <td>0.500</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>1.0</td>
          <td>1.000</td>
          <td>1.000</td>
          <td>1.000</td>
          <td>0.875</td>
          <td>0.875</td>
          <td>0.875</td>
          <td>1.000</td>
          <td>0.875</td>
          <td>1.000</td>
          <td>...</td>
          <td>1.000</td>
          <td>1.000</td>
          <td>1.00</td>
          <td>1.000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.5</td>
          <td>0.500</td>
          <td>0.375</td>
          <td>0.500</td>
          <td>0.625</td>
          <td>0.500</td>
          <td>0.625</td>
          <td>0.500</td>
          <td>0.500</td>
          <td>0.500</td>
          <td>...</td>
          <td>0.750</td>
          <td>0.625</td>
          <td>0.75</td>
          <td>0.625</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>1.0</td>
          <td>0.875</td>
          <td>0.875</td>
          <td>0.625</td>
          <td>0.625</td>
          <td>0.875</td>
          <td>1.000</td>
          <td>0.750</td>
          <td>0.875</td>
          <td>0.375</td>
          <td>...</td>
          <td>0.625</td>
          <td>0.875</td>
          <td>0.50</td>
          <td>0.875</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.5</td>
          <td>0.250</td>
          <td>0.625</td>
          <td>0.250</td>
          <td>0.375</td>
          <td>0.375</td>
          <td>0.375</td>
          <td>0.250</td>
          <td>0.250</td>
          <td>0.125</td>
          <td>...</td>
          <td>0.500</td>
          <td>0.625</td>
          <td>0.75</td>
          <td>0.875</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 22 columns</p>
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

    pfr = quail.analyze(egg, analysis='pfr', listgroup=['average']*8)
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
          <th>...</th>
          <th>12</th>
          <th>13</th>
          <th>14</th>
          <th>15</th>
          <th>16</th>
          <th>17</th>
          <th>18</th>
          <th>19</th>
          <th>20</th>
          <th>21</th>
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
          <td>0.625</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.125</td>
          <td>0.000</td>
          <td>0.125</td>
          <td>...</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>...</td>
          <td>0.625</td>
          <td>0.125</td>
          <td>0.125</td>
          <td>0.125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>...</td>
          <td>0.125</td>
          <td>0.000</td>
          <td>0.125</td>
          <td>0.375</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.125</td>
          <td>0.000</td>
          <td>...</td>
          <td>0.125</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.250</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.125</td>
          <td>0.000</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>...</td>
          <td>0.125</td>
          <td>0.375</td>
          <td>0.250</td>
          <td>0.125</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 22 columns</p>
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

    lagcrp = quail.analyze(egg, analysis='lagcrp', listgroup=['average']*8)
    lagcrp.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>-16</th>
          <th>-15</th>
          <th>-14</th>
          <th>-13</th>
          <th>-12</th>
          <th>-11</th>
          <th>-10</th>
          <th>-9</th>
          <th>-8</th>
          <th>-7</th>
          <th>...</th>
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
          <td>0.0</td>
          <td>0.250</td>
          <td>0.0000</td>
          <td>0.125000</td>
          <td>0.00000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.02500</td>
          <td>0.000000</td>
          <td>...</td>
          <td>0.062500</td>
          <td>0.000000</td>
          <td>0.156250</td>
          <td>0.03125</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.0000</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.0</td>
          <td>0.125</td>
          <td>0.0625</td>
          <td>0.000000</td>
          <td>0.09375</td>
          <td>0.041667</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.03125</td>
          <td>0.097222</td>
          <td>...</td>
          <td>0.000000</td>
          <td>0.025000</td>
          <td>0.000000</td>
          <td>0.00000</td>
          <td>0.062500</td>
          <td>0.062500</td>
          <td>0.0000</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.2500</td>
          <td>0.000000</td>
          <td>0.06250</td>
          <td>0.031250</td>
          <td>0.000000</td>
          <td>0.031250</td>
          <td>0.08125</td>
          <td>0.108333</td>
          <td>...</td>
          <td>0.087500</td>
          <td>0.087500</td>
          <td>0.025000</td>
          <td>0.00000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.0625</td>
          <td>0.000</td>
          <td>0.125</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.0</td>
          <td>0.000</td>
          <td>0.1875</td>
          <td>0.166667</td>
          <td>0.06250</td>
          <td>0.062500</td>
          <td>0.125000</td>
          <td>0.114583</td>
          <td>0.09375</td>
          <td>0.133333</td>
          <td>...</td>
          <td>0.140625</td>
          <td>0.020833</td>
          <td>0.072917</td>
          <td>0.06250</td>
          <td>0.041667</td>
          <td>0.145833</td>
          <td>0.0000</td>
          <td>0.125</td>
          <td>0.125</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.0</td>
          <td>0.375</td>
          <td>0.0000</td>
          <td>0.166667</td>
          <td>0.00000</td>
          <td>0.000000</td>
          <td>0.083333</td>
          <td>0.000000</td>
          <td>0.03125</td>
          <td>0.041667</td>
          <td>...</td>
          <td>0.031250</td>
          <td>0.062500</td>
          <td>0.041667</td>
          <td>0.00000</td>
          <td>0.062500</td>
          <td>0.000000</td>
          <td>0.1250</td>
          <td>0.000</td>
          <td>0.000</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 33 columns</p>
    </div>



Unlike the previous two analyses, the result of this analysis returns a
df where the number of columns are double the length of the lists. To
view the results:

.. code:: ipython2

    ax=quail.plot(lagcrp)



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_27_0.png


Temporal clustering
-------------------

Another way to evaluate temporal clustering is to measure the temporal
distance of each transition made with respect to where on a list the
subject could have transitioned. This 'temporal clustering score' is a
good summary of how strongly participants are clustering their responses
according to temporal proximity during encoding.

.. code:: ipython2

    temporal = quail.analyze(egg, analysis='temporal', listgroup=['average']*8)
    ax = quail.plot(temporal, plot_style='violin', ylim=[0,1])



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_29_0.png


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
          <td>{u'category': u'FRUITS', u'color': [98, 233, 7...</td>
          <td>{u'category': u'STATES', u'color': [98, 193, 1...</td>
          <td>{u'category': u'BODY PARTS', u'color': [204, 9...</td>
          <td>{u'category': u'MAMMALS', u'color': [7, 121, 8...</td>
          <td>{u'category': u'BODY PARTS', u'color': [210, 2...</td>
          <td>{u'category': u'FRUITS', u'color': [220, 38, 3...</td>
          <td>{u'category': u'FRUITS', u'color': [95, 236, 9...</td>
          <td>{u'category': u'FRUITS', u'color': [179, 134, ...</td>
          <td>{u'category': u'BODY PARTS', u'color': [171, 1...</td>
          <td>{u'category': u'STATES', u'color': [170, 6, 83...</td>
          <td>{u'category': u'BODY PARTS', u'color': [205, 8...</td>
          <td>{u'category': u'MAMMALS', u'color': [126, 183,...</td>
          <td>{u'category': u'MAMMALS', u'color': [13, 125, ...</td>
          <td>{u'category': u'STATES', u'color': [235, 27, 8...</td>
          <td>{u'category': u'MAMMALS', u'color': [116, 201,...</td>
          <td>{u'category': u'STATES', u'color': [237, 220, ...</td>
        </tr>
        <tr>
          <th>1</th>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'FLOWERS', u'color': [239, 61, ...</td>
          <td>{u'category': u'VEGETABLES', u'color': [71, 23...</td>
          <td>{u'category': u'VEGETABLES', u'color': [121, 2...</td>
          <td>{u'category': u'FLOWERS', u'color': [38, 240, ...</td>
          <td>{u'category': u'FLOWERS', u'color': [231, 35, ...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [2...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'FLOWERS', u'color': [177, 210,...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [2...</td>
          <td>{u'category': u'VEGETABLES', u'color': [200, 7...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'VEGETABLES', u'color': [45, 24...</td>
          <td>{u'category': u'BUILDING RELATED', u'color': [...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
        </tr>
        <tr>
          <th>2</th>
          <td>{u'category': u'COUNTRIES', u'color': [102, 19...</td>
          <td>{u'category': u'COUNTRIES', u'color': [199, 20...</td>
          <td>{u'category': u'VEGETABLES', u'color': [241, 2...</td>
          <td>{u'category': u'COUNTRIES', u'color': [37, 124...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [158, ...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [15, 1...</td>
          <td>{u'category': u'VEGETABLES', u'color': [30, 15...</td>
          <td>{u'category': u'MAMMALS', u'color': [104, 148,...</td>
          <td>{u'category': u'MAMMALS', u'color': [168, 132,...</td>
          <td>{u'category': u'VEGETABLES', u'color': [148, 6...</td>
          <td>{u'category': u'MAMMALS', u'color': [47, 42, 1...</td>
          <td>{u'category': u'MAMMALS', u'color': [8, 84, 10...</td>
          <td>{u'category': u'COUNTRIES', u'color': [150, 19...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [112, ...</td>
          <td>{u'category': u'VEGETABLES', u'color': [154, 6...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [201, ...</td>
        </tr>
        <tr>
          <th>3</th>
          <td>{u'category': u'TREES', u'color': [113, 117, 9...</td>
          <td>{u'category': u'TOOLS', u'color': [92, 78, 186...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [48, 7...</td>
          <td>{u'category': u'TOOLS', u'color': [170, 142, 2...</td>
          <td>{u'category': u'TREES', u'color': [204, 46, 25...</td>
          <td>{u'category': u'TOOLS', u'color': [36, 101, 20...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [149, ...</td>
          <td>{u'category': u'FRUITS', u'color': [118, 190, ...</td>
          <td>{u'category': u'FRUITS', u'color': [47, 113, 1...</td>
          <td>{u'category': u'TREES', u'color': [117, 158, 2...</td>
          <td>{u'category': u'TOOLS', u'color': [168, 72, 18...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [113, ...</td>
          <td>{u'category': u'TREES', u'color': [221, 227, 2...</td>
          <td>{u'category': u'FRUITS', u'color': [104, 251, ...</td>
          <td>{u'category': u'FRUITS', u'color': [208, 173, ...</td>
          <td>{u'category': u'INSTRUMENTS', u'color': [245, ...</td>
        </tr>
        <tr>
          <th>4</th>
          <td>{u'category': u'FLOWERS', u'color': [117, 200,...</td>
          <td>{u'category': u'CLOTHING', u'color': [141, 251...</td>
          <td>{u'category': u'FLOWERS', u'color': [80, 14, 1...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [3...</td>
          <td>{u'category': u'CLOTHING', u'color': [143, 104...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [2...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'CLOTHING', u'color': [8, 170, ...</td>
          <td>{u'category': u'KITCHEN-RELATED', u'color': [1...</td>
          <td>{u'category': u'STATES', u'color': [54, 189, 5...</td>
          <td>{u'category': u'STATES', u'color': [217, 17, 3...</td>
          <td>{u'category': u'FLOWERS', u'color': [29, 169, ...</td>
          <td>{u'category': u'CLOTHING', u'color': [189, 224...</td>
          <td>{u'category': u'FLOWERS', u'color': [246, 77, ...</td>
          <td>{u'category': u'STATES', u'color': [221, 52, 2...</td>
          <td>{u'category': u'STATES', u'color': [157, 60, 3...</td>
        </tr>
      </tbody>
    </table>
    </div>



Like the other analyses, computing the memory fingerprint can be done
using the ``analyze`` function with the ``analysis`` kwarg set to
``fingerprint``:

.. code:: ipython2

    fingerprint = quail.analyze(egg, analysis='fingerprint', listgroup=['average']*8)
    fingerprint.head()




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
          <td>0.513880</td>
          <td>0.525987</td>
          <td>0.490013</td>
          <td>0.511757</td>
          <td>0.476129</td>
          <td>0.513928</td>
        </tr>
        <tr>
          <th>1</th>
          <th>average</th>
          <td>0.564096</td>
          <td>0.474935</td>
          <td>0.499726</td>
          <td>0.500558</td>
          <td>0.491788</td>
          <td>0.536853</td>
        </tr>
        <tr>
          <th>2</th>
          <th>average</th>
          <td>0.657864</td>
          <td>0.541949</td>
          <td>0.481426</td>
          <td>0.505036</td>
          <td>0.470425</td>
          <td>0.603982</td>
        </tr>
        <tr>
          <th>3</th>
          <th>average</th>
          <td>0.765421</td>
          <td>0.489243</td>
          <td>0.478731</td>
          <td>0.493680</td>
          <td>0.492727</td>
          <td>0.638130</td>
        </tr>
        <tr>
          <th>4</th>
          <th>average</th>
          <td>0.536066</td>
          <td>0.440451</td>
          <td>0.504046</td>
          <td>0.497356</td>
          <td>0.474537</td>
          <td>0.572010</td>
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

    ax = quail.plot(fingerprint, ylim=[0,1.2])



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_35_0.png


This result suggests that subjects in this example dataset tended to
cluster their recall responses by category as well as the size (bigger
or smaller than a shoebox) of the word. List length and other properties
of your experiment can bias these clustering scores. To help with this,
we implemented a permutation clustering procedure which shuffles the
order of each recall list and recomputes the clustering score with
respect to that distribution. Note: this also works with the temporal
clustering analysis.

.. code:: ipython2

    # warning: this can take a little while.  Setting parallel=True will help speed up the permutation computation
    # fingerprint = quail.analyze(egg, analysis='fingerprint', listgroup=['average']*8, permute=True, n_perms=100)
    # ax = quail.plot(fingerprint, ylim=[0,1.2])

Finally, the fingerprint can be plotted along side of the temporal
clustering score:

.. code:: ipython2

    fingerprint_temporal = quail.analyze(egg, analysis='fingerprint_temporal', listgroup=['average']*8)
    ax = quail.plot(fingerprint_temporal)



.. image:: basic_analyze_and_plot_files/basic_analyze_and_plot_39_0.png

