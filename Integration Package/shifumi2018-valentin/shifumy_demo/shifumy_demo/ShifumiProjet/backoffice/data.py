
from .models import humans
from .models import humansRobot

class Data():


  def get_All_part(self,datatable):
      return datatable.objects.all().values_list('part','round','PlayerOne','PlayerTwo')



  def get_this_part(self,datatable,idpart):
      return datatable.objects.filter(part=idpart).values_list('part','round','PlayerOne','PlayerTwo')









