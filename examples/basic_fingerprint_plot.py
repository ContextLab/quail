#import
import quail

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

# create egg object
egg = quail.Egg(pres=presented,rec=recalled, features=features)

# analysis
analyzed_data = quail.analyze(egg, analysis='fingerprint')

# plot
quail.plot(analyzed_data)
