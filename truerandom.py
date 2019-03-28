from urllib2 import urlopen
import json
import numpy as np
import math



class quantrand():
    url = 'https://qrng.anu.edu.au/API/jsonI.php?'
    
    def rand(self,data_type,length=1,size=1):
        length,size = str(length),str(size)
        url_request = self.url+'length='+length+'&type='+data_type
        if data_type=='hex16':
            url_request += '&size='+size
        fetched_rand = json.loads(urlopen(url_request).read().decode('ascii'))
        return fetched_rand['data']
        
    def randbin(self,length=1):
        rand_int = self.rand('uint8',length)
        return [i%2 for i in rand_int]
        
    def randint(self,intmin=0,intmax=65535,length=1):
        rand_int1 = np.array(self.rand('uint16',length))
        rand_int2 = [math.floor(i*float(intmax+1-intmin)/65535+intmin) for i in rand_int1]
        rand_int3 = [int(i) if i<=intmax else intmax for i in rand_int2]
        return rand_int3
        
    def randfloat(self,length=1):
        rand_float = []
        for i in range(length):
            rand_float.append(float("0."+"".join([str(i) for i in self.randint(0,9,16)])))
        return rand_float
        
    def choice(self,sequence):
        return sequence[self.randint(0,len(sequence)-1)[0]]
        
    def sample(self,population,k,remplacement=False):
        sample_pop = []
        for i in range(k):
            choice_pop = self.choice(population)
            sample_pop.append(choice_pop)
            if remplacement==False:
                population.remove(choice_pop)
        return sample_pop
    
    def shuffle(self,sequence):
        shuffled_seq = []
        for i in range(len(sequence)):
            choice_seq = self.choice(sequence)
            shuffled_seq.append(choice_seq)
            sequence.remove(choice_seq)
        return shuffled_seq
