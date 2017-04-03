#import
import pyrec as pyr


presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]

features = [
    [
        [
            {
                'category' : 'animal',
                'wordLength' : 3
            },
            {
                'category' : 'object',
                'wordLength' : 3
            },
            {
                'category' : 'object',
                'wordLength' : 3
            },
            {
                'category' : 'animal',
                'wordLength' : 4
            },
        ],
        [
            {
                'category' : 'place',
                'wordLength' : 3
            },
            {
                'category' : 'animal',
                'wordLength' : 6
            },
            {
                'category' : 'animal',
                'wordLength' : 5
            },
            {
                'category' : 'animal',
                'wordLength' : 5
            },
        ],
    ]
]

# create pyro object
pyro = pyr.Pyro(pres=presented,rec=recalled, features=features)

print(pyro.pres)
