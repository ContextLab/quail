#import
import quail

#create pyro object
presented=[[['cat', 'bat', 'hat', 'goat'],['zoo', 'animal', 'zebra', 'horse']]]
recalled=[[['bat', 'cat', 'goat', 'hat'],['animal', 'horse', 'zoo']]]
egg = quail.Egg(pres=presented,rec=recalled)

#analysis
analyzed_data = quail.analyze(egg, analysis='accuracy')
print(analyzed_data)

#plot
quail.plot(analyzed_data)
