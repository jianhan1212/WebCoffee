from django.db import models

# Create your models here.
class ProductModel(models.Model):                             #商品資料表
    pname =  models.CharField(max_length=100, default='')     #商品名稱
    pprice = models.IntegerField(default=0)                   #商品價格
    pimages = models.CharField(max_length=100, default='')    #商品照片
    pdescription = models.TextField(blank=True, default='') 
    def __str__(self):
        return self.pname 

class DetailModel(models.Model):                                            #訂單內容
    # dorder = models.ForeignKey('OrdersModel', on_delete=models.CASCADE)     #儲存訂單 OrderModel關聯欄位 on_delete=models.CASCADE 表示移除ordermodel時該訂單所有商品自動移除
    pname = models.CharField(max_length=100, default='')                    #商品名稱
    unitprice = models.IntegerField(default=0)                              #單價
    quantity = models.IntegerField(default=0)                               #數量
    dtotal = models.IntegerField(default=0)                                 #總價
    def __str__(self):
        return self.pname  