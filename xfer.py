import sys
from django.core import serializers

def migrate(model, size=500, start=0):
    count = model.objects.using('mysql').count()
    print "%s objects in model %s" % (count, model)
    for i in range(start, count, size):
        print i,
        sys.stdout.flush()
        original_data = model.objects.using('mysql').all()[i:i+size]
        original_data_json = serializers.serialize("json", original_data)
        new_data = serializers.deserialize("json", original_data_json, 
                                           using='default')
        for n in new_data:
            n.save(using='default')
            
            
import sys
from django.core import serializers

def migrate(model, size=500, start=0):
    count = model.objects.using('mysql').count()
    print "%s objects in model %s" % (count, model)
    for i in range(start, count, size):
        print i,
        sys.stdout.flush()
        original_data = model.objects.using('mysql').all()[i:i+size]
        original_data_json = serializers.serialize("json", original_data)
        new_data = serializers.deserialize("json", original_data_json, 
                                           using='default')
        for n in new_data:
            n.save(using='default')
            
            
            stories_story_pub_date_key	
            UNIQUE (pub_date)
            Drop
            
            tagging_tag_name_key	
            UNIQUE (name)
