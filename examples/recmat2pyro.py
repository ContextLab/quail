#import
import pyrec as pyr

#create pyro object using recmat2pyro
recmat = [[[2, 3, 0, None], [2, 3, 1, 0]]]
pyro = pyr.helpers.recmat2pyro(recmat)

#analysis
analyzed_data = pyr.analyze(pyro, listgroup=[1,1], analysis='spc')

#plot
pyr.plot(analyzed_data)
