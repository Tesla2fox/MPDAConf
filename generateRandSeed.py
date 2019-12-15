import random
conFile = open('benchmark//randSeed.dat','w')
for i in range(50):
    conFile.write(str(random.randint(0,10000))+'\n')
conFile.close()

