#import
import quail

#create egg object
sub1_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
sub1_recalled=[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]

sub2_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
sub2_recalled=[['cat', 'goat', 'bat', 'hat'],['horse', 'zebra', 'zoo', 'animal']]

presented = [sub1_presented, sub2_presented]
recalled = [sub1_recalled, sub2_recalled]

egg = quail.Egg(pres=presented,rec=recalled)

#analysis
analyzed_data = quail.analyze(egg, analysis='spc', listgroup=['average']*2)

#plot
quail.plot(analyzed_data)
