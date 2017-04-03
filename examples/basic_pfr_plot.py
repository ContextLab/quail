#import
import pyrec as pyr

#create pyro object
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['zebra', 'horse', 'zoo']]]
pyro = pyr.Pyro(pres=presented,rec=recalled)

#analysis
analyzed_data = pyr.analyze(pyro, analysis='pfr')

#plot
pyr.plot(analyzed_data)
