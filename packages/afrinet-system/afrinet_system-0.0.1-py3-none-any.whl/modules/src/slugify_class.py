import random

class SlugifyClass:
    def __init__(self,slug=None):
        self.slug = slug

    def generateSlug(self):
        try:
            slug_size = self.getSlugLength()
            prep_slug = self.prepareData()
            serial = str(random.randrange(1000,5000))
            tmp = ""

            for item in range(slug_size):
                if slug_size == 1:
                    tmp  = prep_slug[item] + "-"
                    slug = tmp.lower() + serial
                    return slug
                
                elif slug_size > 1:
                    for item in range(slug_size):
                        tmp +=   prep_slug[item] + "-" 
                        slug = tmp.lower() + serial
                
                return slug
        except:
            print('Slug cannot be generated')


    def getSlugLength(self):
        slug = str(self.slug) 
        prep_slug = self.prepareData()
        slug_size = len(prep_slug)
        return slug_size
    
    def prepareData(self):
        slug = str(self.slug) 
        prep_slug = slug.split()
        return prep_slug

        
# test_slug = SlugifyClass('Hello World')
# print(test_slug.generateSlug())
