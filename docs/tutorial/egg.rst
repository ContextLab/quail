
The Egg data object
===================

This tutorial will go over the basics of the ``Egg`` data object, the
essential quail data structure that contains all the data you need to
run analyses and plot the results. An egg is made up of two primary
pieces of data:

1. ``pres`` data - words/stimuli that were presented to a subject

2. ``rec`` data - words/stimuli that were recalled by the subject.

You cannot create an ``egg`` without both of these components.
Additionally, there are a few optional fields:

1. ``features`` data - features that describe each of the stimuli (for
   example, the category of the word, word length, etc.). This field is
   required for fingerprint analysis (see the fingerprint tutorial).

2. ``dist_funcs`` dictionary - this field allows you to control the
   distance functions for each of the stimulus features. For more on
   this, see the fingerprint tutorial.

3. ``meta`` dictionary - this is an optional field that allows you to
   store custom meta data about the dataset, such as the date collected,
   experiment version etc.

There are also a few other fields and functions to make organizing and
modifying ``eggs`` easier (discussed at the bottom). Now, lets dive in
and create an ``egg`` from scratch.

Load in the library
-------------------

.. code:: ipython2

    import quail

The ``pres`` data structure
---------------------------

The first piece of an ``egg`` is the ``pres`` data, or in other words
the words/stimuli that were presented to the subject. For a single
subject's data, the form of the input will be a list of lists, where
each list is comprised of the words presented to the subject during a
particular study block. Let's create a fake dataset of one subject who
saw two encoding lists:

.. code:: ipython2

    presented_words = [['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]

The ``rec`` data structure
--------------------------

The second fundamental component of an egg is the ``rec`` data, or the
words/stimuli that were recalled by the subject. Now, let's create the
recall lists:

.. code:: ipython2

    recalled_words = [['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]

We now have the two components necessary to build an ``egg``, so let's
do that and then take a look at the result.

.. code:: ipython2

    egg = quail.Egg(pres=presented_words, rec=recalled_words)

That's it! We've created our first ``egg``. Let's take a closer look at
how the ``egg`` is setup. We can use the ``info`` method to get a quick
snapshot of the ``egg``:

.. code:: ipython2

    egg.info()


.. parsed-literal::

    Number of subjects: 1
    Number of lists per subject: 2
    Number of words per list: 4
    Date created: Mon May 15 14:33:36 2017
    Meta data: {}


Now, let's take a closer look at how the ``egg`` is structured. First,
we will check out the ``pres`` field:

.. code:: ipython2

    egg.pres




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
we consider larger datasets with more subjects. Next, let's take a look
at the ``rec`` data:

.. code:: ipython2

    egg.rec




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
          <td>None</td>
        </tr>
      </tbody>
    </table>
    </div>



The ``rec`` data is also stored as a DataFrame. Notice that if the
number of recalled words is shorter than the number of presented words
(as it typically will be), those columns are filled with a ``None``
value. Now, let's create an ``egg`` with two subject's data and take a
look at the result.

Multisubject ``eggs``
---------------------

.. code:: ipython2

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
    multisubject_egg = quail.Egg(pres=presented_words,rec=recalled_words)

As you can see above, in order to create an ``egg`` with more than one
subject's data, all you do is create a list of subjects. Let's see how
the ``pres`` data is organized in the egg with more than one subject:

.. code:: ipython2

    multisubject_egg.pres




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

.. code:: ipython2

    multisubject_egg.rec




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
          <td>None</td>
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

The ``features`` data structure
-------------------------------

The ``features`` data structure is an optional field that can be added
to an egg. It contains features of the presented words that are required
for the fingerprint analysis. The ``features`` data is set up like the
``pres`` and ``rec`` data, but instead of a single word, there is a
dictionary of features. For example take the word "cat". A ``features``
dictionary for this word might look something like this:

.. code:: ipython2

    cat_features = {
        'category' : 'animal',
        'word_length' : 3,
        'starting_letter' : 'c',
    }

You can include any stimulus feature you want in this dictionary, such
as the position of the word on the screen, the color, or perhaps the
font of the word. To create the ``features`` data structure in an
``egg``, use the format of the ``pres`` structure, but replace the words
with dictionaries:

.. code:: ipython2

    # presented words
    presented_words=[['cat', 'bat', 'hat', 'goat'],['zoo', 'donkey', 'zebra', 'horse']]
    
    # presentation features
    presented_words_features = [
        [
            {
                'category' : 'animal',
                'word_length' : 3,
                'starting_letter' : 'c'
            },
            {
                'category' : 'object',
                'word_length' : 3,
                'starting_letter' : 'b'
            },
            {
                'category' : 'object',
                'word_length' : 3,
                'starting_letter' : 'h'
            },
            {
                'category' : 'animal',
                'word_length' : 4,
                'starting_letter' : 'g'
            },
        ],
        [
            {
                'category' : 'place',
                'word_length' : 3,
                'starting_letter' : 'z'
            },
            {
                'category' : 'animal',
                'word_length' : 6,
                'starting_letter' : 'd'
            },
            {
                'category' : 'animal',
                'word_length' : 5,
                'starting_letter' : 'z'
            },
            {
                'category' : 'animal',
                'word_length' : 5,
                'starting_letter' : 'h'
            },
        ],
    ]
    
    # recalled words
    recalled_words=[['bat', 'cat', 'goat', 'hat'],['donkey', 'horse', 'zoo']]

Then, simply pass the features to the ``Egg`` class using the
``features`` key word argument:

.. code:: ipython2

    # create egg object
    egg = quail.Egg(pres=presented_words, rec=recalled_words, features=presented_words_features)
    egg.features




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
          <td>{u'category': u'animal', u'starting_letter': u...</td>
          <td>{u'category': u'object', u'starting_letter': u...</td>
          <td>{u'category': u'object', u'starting_letter': u...</td>
          <td>{u'category': u'animal', u'starting_letter': u...</td>
        </tr>
        <tr>
          <th>1</th>
          <td>{u'category': u'place', u'starting_letter': u'...</td>
          <td>{u'category': u'animal', u'starting_letter': u...</td>
          <td>{u'category': u'animal', u'starting_letter': u...</td>
          <td>{u'category': u'animal', u'starting_letter': u...</td>
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
"dog", and then the next word you recall is "cat", your clustering by
category score would increase because the two recalled words are in the
same category. Similarly, if after you recall "cat" you recall the word
"can", your clustering by starting letter score would increase, since
both words share the first letter "c". This logic can be extended to any
number of feature dimensions.

Similarity between the words can be computed in a number of ways. By
default, the distance function for all textual features (like category,
starting letter) is binary. In other words, if the words are in the same
category (cat, dog), there similarity would be 1, whereas if they are in
different categories (cat, can) their similarity would be 0. For
numerical features (such as word length), by default similarity between
words is computed using Euclidean distance. However, the point of this
digression is that you can define your own distance functions by passing
a ``dist_func`` dictionary to the ``Egg`` class. This could be for all
feature dimensions, or only a subset. Let's see an example:

.. code:: ipython2

    dist_funcs = {
        'word_length' : lambda x,y: (x-y)**2
    }
    
    egg = quail.Egg(pres=presented_words, rec=recalled_words, features=presented_words_features, dist_funcs=dist_funcs)

In the example code above, similarity between words for the word\_length
feature dimension will now be computed using this custom distance
function, while all other feature dimensions will be set to the default.

Adding meta data to an ``egg``
------------------------------

Lastly, we can add meta data to the ``egg``. We added this field to help
researchers keep their eggs organized by adding custom meta data to the
``egg`` object. The data is added to the ``egg`` by passing the ``meta``
key word argument when creating the ``egg``:

.. code:: ipython2

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
    Date created: Mon May 15 14:33:36 2017
    Meta data: {'Researcher': 'Andy Heusser', 'Study': 'Egg Tutorial'}


Adding ``listgroup`` and ``subjgroup`` to an ``egg``
----------------------------------------------------

While the ``listgroup`` and ``subjgroup`` arguments can be used within
the ``analyze`` function, they can also be attached directly to the
``egg``, allowing you to save condition labels for easy organization and
easy data sharing.

To do this, simply pass one or both of the arguments when creating the
``egg``:

.. code:: ipython2

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

    multisubject_egg.save('myegg.p')

This will save you ``egg`` using the package ``pickle``. The result? A
pickled egg! To load this egg later, simply call the ``load_egg``
function with the path of the egg:

::

    egg = quail.load('myegg.p')

Stacking ``eggs``
-----------------

We now have two separate eggs, each with a single subject's data. Let's
combine them by passing a ``list`` of ``eggs`` to the ``stack_eggs``
function:

.. code:: ipython2

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

.. code:: ipython2

    stacked_eggs = quail.stack_eggs([subject1_egg, subject2_egg])
    stacked_eggs.pres




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

.. code:: ipython2

    cracked_egg = quail.crack_egg(stacked_eggs, subjects=[1], lists=[0])
    cracked_egg.pres




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

.. code:: ipython2

    stacked_eggs.crack(subjects=[0,1], lists=[1]).pres




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


