from rest_framework import serializers
from .models import Departmentalforcatsedhour

class DepartmentalforcatsedhourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departmentalforcatsedhour
        fields = '__all__'
        many = True
    
    # id = serializers.IntegerField()
    # projectnumber = serializers.CharField(max_length=255)  
    # subdepartmentid = serializers.IntegerField()
    # description = serializers.CharField(max_length=255)  
    # quoteid = serializers.IntegerField()  
    # quantity = serializers.IntegerField()  
    # unit = serializers.CharField(max_length=5) 
    # unitcost = serializers.DecimalField(max_digits=15, decimal_places=2)  
    # costamount = serializers.DecimalField(max_digits=15, decimal_places=2)  
    # currency = serializers.CharField(max_length=3) 
    # priceunit = serializers.CharField(max_length=3) 
    # modifiedby = serializers.CharField(max_length=255)  
    # createddate = serializers.DateTimeField()  
    # updateddate = serializers.DateTimeField()  
    # revisionnumber = serializers.IntegerField()  
    # projectversionid = serializers.IntegerField()  
    # projectdescription = serializers.CharField(max_length=255)  
    # projectdetailid = serializers.IntegerField()
