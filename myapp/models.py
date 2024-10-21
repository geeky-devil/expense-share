from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=50)  # 'equal', 'exact', 'percentage'
    users = models.ManyToManyField(User, through='ExpenseSplit')

class ExpenseSplit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='splits')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE,related_name='splits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
