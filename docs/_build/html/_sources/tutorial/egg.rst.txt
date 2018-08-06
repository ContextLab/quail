
The Egg data object
===================

This tutorial will go over the basics of the ``Egg`` data object, the
essential ``quail`` data structure that contains all the data you need
to run analyses and plot the results. An egg is made up of two primary
pieces of data:

1. ``pres`` data - stimuli/features that were presented to a subject

2. ``rec`` data - stimuli/features that were recalled by the subject.

You cannot create an ``egg`` without both of these components.
Additionally, there are a few optional fields:

1. ``dist_funcs`` dictionary - this field allows you to control the
   distance functions for each of the stimulus features. For more on
   this, see the fingerprint tutorial.

2. ``meta`` dictionary - this is an optional field that allows you to
   store custom meta data about the dataset, such as the date collected,
   experiment version etc.

There are also a few other fields and functions to make organizing and
modifying ``eggs`` easier (discussed at the bottom). Now, lets dive in
and create an ``egg`` from scratch.

Load in the library
-------------------

.. code:: ipython3

    import quail
    %matplotlib inline


.. parsed-literal::

    /usr/local/lib/python3.6/site-packages/pydub/utils.py:165: RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
      warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning)


The ``pres`` data structure
---------------------------

The first piece of an ``egg`` is the ``pres`` data, or in other words
the stimuli that were presented to the subject. For a single subject’s
data, the form of the input will be a list of lists, where each list is
comprised of the words presented to the subject during a particular
study block. Let’s create a fake dataset of one subject who saw two
encoding lists:

.. code:: ipython3

    presented_words = [['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]

The ``rec`` data structure
--------------------------

The second fundamental component of an egg is the ``rec`` data, or the
words/stimuli that were recalled by the subject. Now, let’s create the
recall lists:

.. code:: ipython3

    recalled_words = [['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]

We now have the two components necessary to build an ``egg``, so let’s
do that and then take a look at the result.

.. code:: ipython3

    egg = quail.Egg(pres=presented_words, rec=recalled_words)

That’s it! We’ve created our first ``egg``. Let’s take a closer look at
how the ``egg`` is setup. We can use the ``info`` method to get a quick
snapshot of the ``egg``:

.. code:: ipython3

    egg.info()


.. parsed-literal::

    Number of subjects: 1
    Number of lists per subject: 2
    Number of words per list: 4
    Date created: Mon Aug  6 14:43:19 2018
    Meta data: {}


Now, let’s take a closer look at how the ``egg`` is structured. First,
we will check out the ``pres`` field:

.. code:: ipython3

    egg.get_pres_items()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2" valign="top">0</th>
          <th>0</th>
          <td>cat</td>
          <td>bat</td>
          <td>hat</td>
          <td>goat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>zoo</td>
          <td>animal</td>
          <td>zebra</td>
          <td>horse</td>
        </tr>
      </tbody>
    </table>
    </div>



As you can see above, the ``pres`` field was turned into a multi-index
Pandas DataFrame organized by subject and by list. This is how the
``pres`` data is stored within an egg, which will make more sense when
we consider larger datasets with more subjects. Next, let’s take a look
at the ``rec`` data:

.. code:: ipython3

    egg.get_rec_items()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2" valign="top">0</th>
          <th>0</th>
          <td>bat</td>
          <td>cat</td>
          <td>goat</td>
          <td>hat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>animal</td>
          <td>horse</td>
          <td>zoo</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



The ``rec`` data is also stored as a DataFrame. Notice that if the
number of recalled words is shorter than the number of presented words,
those columns are filled with a ``NaN`` value. Now, let’s create an
``egg`` with two subject’s data and take a look at the result.

Multisubject ``eggs``
---------------------

.. code:: ipython3

    # presented words
    sub1_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
    sub2_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
    
    # recalled words
    sub1_recalled=[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]
    sub2_recalled=[['cat', 'goat', 'bat', 'hat'],['horse', 'zebra', 'zoo', 'animal']]
    
    # combine subject data
    presented_words = [sub1_presented, sub2_presented]
    recalled_words = [sub1_recalled, sub2_recalled]
    
    # create Egg
    multisubject_egg = quail.Egg(pres=presented_words, rec=recalled_words)
    
    multisubject_egg.info()


.. parsed-literal::

    Number of subjects: 2
    Number of lists per subject: 2
    Number of words per list: 4
    Date created: Mon Aug  6 14:43:19 2018
    Meta data: {}


As you can see above, in order to create an ``egg`` with more than one
subject’s data, all you do is create a list of subjects. Let’s see how
the ``pres`` data is organized in the egg with more than one subject:

.. code:: ipython3

    multisubject_egg.get_pres_items()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2" valign="top">0</th>
          <th>0</th>
          <td>cat</td>
          <td>bat</td>
          <td>hat</td>
          <td>goat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>zoo</td>
          <td>animal</td>
          <td>zebra</td>
          <td>horse</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">1</th>
          <th>0</th>
          <td>cat</td>
          <td>bat</td>
          <td>hat</td>
          <td>goat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>zoo</td>
          <td>animal</td>
          <td>zebra</td>
          <td>horse</td>
        </tr>
      </tbody>
    </table>
    </div>



Looks identical to the single subject data, but now we have two unique
subject identifiers in the ``DataFrame``. The ``rec`` data is set up in
the same way:

.. code:: ipython3

    multisubject_egg.get_rec_items()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2" valign="top">0</th>
          <th>0</th>
          <td>bat</td>
          <td>cat</td>
          <td>goat</td>
          <td>hat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>animal</td>
          <td>horse</td>
          <td>zoo</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">1</th>
          <th>0</th>
          <td>cat</td>
          <td>goat</td>
          <td>bat</td>
          <td>hat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>horse</td>
          <td>zebra</td>
          <td>zoo</td>
          <td>animal</td>
        </tr>
      </tbody>
    </table>
    </div>



As you add more subjects, they are simply appended to the bottom of the
df with a unique subject identifier.

Adding features to the egg
--------------------------

Stimuli can also be passed as a dictionary containing the stimulus and
features of the stimulus. You can include any stimulus feature you want
in this dictionary, such as the position of the word on the screen, the
color, or perhaps the font of the word:

.. code:: ipython3

    cat_features = {
        'item': 'cat',
        'category': 'animal',
        'word_length': 3,
        'starting_letter': 'c',
    }

Let’s try creating an egg with additional stimulus features:

.. code:: ipython3

    # presentation features
    presented_words = [
        [
            {
                'item': 'cat',
                'category': 'animal',
                'word_length': 3,
                'starting_letter': 'c'
            },
            {
                'item': ' bat',
                'category': 'object',
                'word_length': 3,
                'starting_letter': 'b'
            },
            {
                'item': 'hat',
                'category': 'object',
                'word_length': 3,
                'starting_letter': 'h'
            },
            {
                'item': 'goat',
                'category': 'animal',
                'word_length': 4,
                'starting_letter': 'g'
            },
        ],
        [
            {
                'item': 'zoo', 
                'category': 'place',
                'word_length': 3,
                'starting_letter': 'z'
            },
            {
                'item': 'donkey',
                'category' : 'animal',
                'word_length' : 6,
                'starting_letter' : 'd'
            },
            {
                'item': 'zebra',
                'category': 'animal',
                'word_length': 5,
                'starting_letter': 'z'
            },
            {
                'item': 'horse',
                'category': 'animal',
                'word_length': 5,
                'starting_letter': 'h'
            },
        ],
    ]
    
    recalled_words = [
        [
            {
                'item': ' bat',
                'category': 'object',
                'word_length': 3,
                'starting_letter': 'b'
            },
            {
                'item': 'cat',
                'category': 'animal',
                'word_length': 3,
                'starting_letter': 'c'
            },
            {
                'item': 'goat',
                'category': 'animal',
                'word_length': 4,
                'starting_letter': 'g'
            },
            {
                'item': 'hat',
                'category': 'object',
                'word_length': 3,
                'starting_letter': 'h'
            },
        ],
        [
            {
                'item': 'donkey',
                'category' : 'animal',
                'word_length' : 6,
                'starting_letter' : 'd'
            },
            {
                'item': 'horse',
                'category': 'animal',
                'word_length': 5,
                'starting_letter': 'h'
            },
            {
                'item': 'zoo', 
                'category': 'place',
                'word_length': 3,
                'starting_letter': 'z'
            },
    
        ],
    ]
    
    # create egg object
    egg = quail.Egg(pres=presented_words, rec=recalled_words)

Like before, you can use the ``get_pres_items`` method to retrieve the
presented items:

.. code:: ipython3

    egg.get_pres_items()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2" valign="top">0</th>
          <th>0</th>
          <td>cat</td>
          <td>bat</td>
          <td>hat</td>
          <td>goat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>zoo</td>
          <td>donkey</td>
          <td>zebra</td>
          <td>horse</td>
        </tr>
      </tbody>
    </table>
    </div>



The stimulus features can be accessed by calling the
``get_pres_features`` method:

.. code:: ipython3

    egg.get_pres_features()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2" valign="top">0</th>
          <th>0</th>
          <td>{'category': 'animal', 'word_length': 3, 'star...</td>
          <td>{'category': 'object', 'word_length': 3, 'star...</td>
          <td>{'category': 'object', 'word_length': 3, 'star...</td>
          <td>{'category': 'animal', 'word_length': 4, 'star...</td>
        </tr>
        <tr>
          <th>1</th>
          <td>{'category': 'place', 'word_length': 3, 'start...</td>
          <td>{'category': 'animal', 'word_length': 6, 'star...</td>
          <td>{'category': 'animal', 'word_length': 5, 'star...</td>
          <td>{'category': 'animal', 'word_length': 5, 'star...</td>
        </tr>
      </tbody>
    </table>
    </div>



Defining custom distance functions for the stimulus feature dimensions
----------------------------------------------------------------------

As described in the fingerprint tutorial, the ``features`` data
structure is used to estimate how subjects cluster their recall
responses with respect to the features of the encoded stimuli. Briefly,
these estimates are derived by computing the similarity of neighboring
recall words along each feature dimension. For example, if you recall
“dog”, and then the next word you recall is “cat”, your clustering by
category score would increase because the two recalled words are in the
same category. Similarly, if after you recall “cat” you recall the word
“can”, your clustering by starting letter score would increase, since
both words share the first letter “c”. This logic can be extended to any
number of feature dimensions.

Similarity between stimuli can be computed in a number of ways. By
default, the distance function for all textual features (like category,
starting letter) is binary. In other words, if the words are in the same
category (cat, dog), there similarity would be 1, whereas if they are in
different categories (cat, can) their similarity would be 0. For
numerical features (such as word length), by default similarity between
words is computed using Euclidean distance. However, the point of this
digression is that you can define your own distance functions by passing
a ``dist_func`` dictionary to the ``Egg`` class. This could be for all
feature dimensions, or only a subset. Let’s see an example:

.. code:: ipython3

    dist_funcs = {
        'word_length' : lambda x,y: (x-y)**2
    }
    
    egg = quail.Egg(pres=presented_words, rec=recalled_words, dist_funcs=dist_funcs)

In the example code above, similarity between words for the word_length
feature dimension will now be computed using this custom distance
function, while all other feature dimensions will be set to the default.

Adding meta data to an ``egg``
------------------------------

Lastly, we can add meta data to the ``egg``. We added this field to help
researchers keep their eggs organized by adding custom meta data to the
``egg`` object. The data is added to the ``egg`` by passing the ``meta``
key word argument when creating the ``egg``:

.. code:: ipython3

    meta = {
        'Researcher' : 'Andy Heusser',
        'Study' : 'Egg Tutorial'
    }
    
    egg = quail.Egg(pres=presented_words, rec=recalled_words, meta=meta)
    egg.info()


.. parsed-literal::

    Number of subjects: 1
    Number of lists per subject: 2
    Number of words per list: 4
    Date created: Mon Aug  6 14:43:19 2018
    Meta data: {'Researcher': 'Andy Heusser', 'Study': 'Egg Tutorial'}


Adding ``listgroup`` and ``subjgroup`` to an ``egg``
----------------------------------------------------

While the ``listgroup`` and ``subjgroup`` arguments can be used within
the ``analyze`` function, they can also be attached directly to the
``egg``, allowing you to save condition labels for easy organization and
easy data sharing.

To do this, simply pass one or both of the arguments when creating the
``egg``:

.. code:: ipython3

    # presented words
    sub1_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
    sub2_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
    
    # recalled words
    sub1_recalled=[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]
    sub2_recalled=[['cat', 'goat', 'bat', 'hat'],['horse', 'zebra', 'zoo', 'animal']]
    
    # combine subject data
    presented_words = [sub1_presented, sub2_presented]
    recalled_words = [sub1_recalled, sub2_recalled]
    
    # create Egg
    multisubject_egg = quail.Egg(pres=presented_words,rec=recalled_words, subjgroup=['condition1', 'condition2'],
                                listgroup=['early','late'])

Saving an ``egg``
-----------------

Once you have created your egg, you can save it for use later, or to
share with colleagues. To do this, simply call the ``save`` method with
a filepath:

::

   multisubject_egg.save('myegg')

To load this egg later, simply call the ``load_egg`` function with the
path of the egg:

::

   egg = quail.load('myegg')

Stacking ``eggs``
-----------------

We now have two separate eggs, each with a single subject’s data. Let’s
combine them by passing a ``list`` of ``eggs`` to the ``stack_eggs``
function:

.. code:: ipython3

    # subject 1 data
    sub1_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
    sub1_recalled=[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]
    
    # create subject 2 egg
    subject1_egg = quail.Egg(pres=sub1_presented, rec=sub1_recalled)
    
    # subject 2 data
    sub2_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
    sub2_recalled=[['cat', 'goat', 'bat', 'hat'],['horse', 'zebra', 'zoo', 'animal']]
    
    # create subject 2 egg
    subject2_egg = quail.Egg(pres=sub2_presented, rec=sub2_recalled)

.. code:: ipython3

    stacked_eggs = quail.stack_eggs([subject1_egg, subject2_egg])
    stacked_eggs.get_pres_items()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th rowspan="2" valign="top">0</th>
          <th>0</th>
          <td>cat</td>
          <td>bat</td>
          <td>hat</td>
          <td>goat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>zoo</td>
          <td>animal</td>
          <td>zebra</td>
          <td>horse</td>
        </tr>
        <tr>
          <th rowspan="2" valign="top">1</th>
          <th>0</th>
          <td>cat</td>
          <td>bat</td>
          <td>hat</td>
          <td>goat</td>
        </tr>
        <tr>
          <th>1</th>
          <td>zoo</td>
          <td>animal</td>
          <td>zebra</td>
          <td>horse</td>
        </tr>
      </tbody>
    </table>
    </div>



Cracking ``eggs``
-----------------

You can use the ``crack_egg`` function to slice out a subset of subjects
or lists:

.. code:: ipython3

    cracked_egg = quail.crack_egg(stacked_eggs, subjects=[1], lists=[0])
    cracked_egg.get_pres_items()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <th>0</th>
          <td>cat</td>
          <td>bat</td>
          <td>hat</td>
          <td>goat</td>
        </tr>
      </tbody>
    </table>
    </div>



Alternatively, you can use the ``crack`` method, which does the same
thing:

.. code:: ipython3

    stacked_eggs.crack(subjects=[0,1], lists=[1]).get_pres_items()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
        </tr>
        <tr>
          <th>Subject</th>
          <th>List</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <th>0</th>
          <td>zoo</td>
          <td>animal</td>
          <td>zebra</td>
          <td>horse</td>
        </tr>
        <tr>
          <th>1</th>
          <th>0</th>
          <td>zoo</td>
          <td>animal</td>
          <td>zebra</td>
          <td>horse</td>
        </tr>
      </tbody>
    </table>
    </div>


