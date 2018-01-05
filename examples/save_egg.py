import quail

# generate some fake data
next_presented = ['CAT', 'DOG', 'SHOE', 'HORSE', 'SNAIL', 'FOOT', 'CAR', 'ARM', 'UTAH', 'NEW YORK', 'TRUCK', 'EAR', 'ARIZONA', 'BIKE', 'STROLLER', 'TOE']
next_recalled = ['HORSE', 'DOG', 'CAT', 'NEW YORK', 'UTAH', 'ARIZONA']

next_features = [{
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'C',
                    'length' : 3
                 },
                 {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'D',
                    'length' : 3
                 },
                 {
                    'category' : 'object',
                    'size' : 'smaller',
                    'starting letter' : 'S',
                    'length' : 4
                 },
                 {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'H',
                    'length' : 5
                 },
                 {
                    'category' : 'animal',
                    'size' : 'bigger',
                    'starting letter' : 'S',
                    'length' : 5
                 },
                 {
                    'category' : 'body part',
                    'size' : 'smaller',
                    'starting letter' : 'F',
                    'length' : 4
                 },
                 {
                    'category' : 'transportation',
                    'size' : 'bigger',
                    'starting letter' : 'C',
                    'length' : 3
                 },
                 {
                    'category' : 'body part',
                    'size' : 'bigger',
                    'starting letter' : 'A',
                    'length' : 3
                 },
                 {
                    'category' : 'state',
                    'size' : 'bigger',
                    'starting letter' : 'U',
                    'length' : 4
                 },
                 {
                    'category' : 'state',
                    'size' : 'bigger',
                    'starting letter' : 'N',
                    'length' : 7
                 },
                 {
                    'category' : 'transportation',
                    'size' : 'bigger',
                    'starting letter' : 'T',
                    'length' : 5
                 },
                 {
                    'category' : 'body part',
                    'size' : 'smaller',
                    'starting letter' : 'E',
                    'length' : 3
                 },
                 {
                    'category' : 'state',
                    'size' : 'bigger',
                    'starting letter' : 'A',
                    'length' : 7
                 },
                 {
                    'category' : 'transportation',
                    'size' : 'bigger',
                    'starting letter' : 'B',
                    'length' : 4
                 },
                 {
                    'category' : 'transportation',
                    'size' : 'bigger',
                    'starting letter' : 'S',
                    'length' : 8
                 },
                 {
                    'category' : 'body part',
                    'size' : 'smaller',
                    'starting letter' : 'T',
                    'length' : 3
                 }
]

egg = quail.Egg(pres=[next_presented], rec=[next_recalled], features=[next_features])

egg.save('test')

egg = quail.load_egg('test.egg')



egg.analyze('fingerprint')
