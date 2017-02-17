#import
import pyrec as pyr

#create pyro object
sub1_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
sub1_recalled=[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]

sub2_presented=[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]
sub2_recalled=[['cat', 'goat', 'bat', 'hat'],['horse', 'zebra', 'zoo', 'animal']]

presented = [sub1_presented, sub2_presented]
recalled = [sub1_recalled, sub2_recalled]

pyro = pyr.Pyro(pres=presented,rec=recalled)

#analysis
analyzed_data = pyr.pfr(pyro, listgroup=[1,1])

#plot
pyr.plot(analyzed_data)
