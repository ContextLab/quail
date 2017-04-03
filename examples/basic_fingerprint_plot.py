#import
import pyrec as pyr

# presentation data
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]

# recall data
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]

# presentation data features
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

# analysis
analyzed_data = pyr.analyze(pyro, analysis='fingerprint')

# plot
pyr.plot(analyzed_data)
