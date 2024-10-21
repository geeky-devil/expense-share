# expenses/serializers.py
from rest_framework import serializers
from .models import User, Expense, ExpenseSplit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile']

class ExpenseSplitSerializer(serializers.ModelSerializer):
    
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ExpenseSplit
        fields = ['user', 'amount']

class ExpenseSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    splits = ExpenseSplitSerializer(many=True, read_only=True)
    date = serializers.DateField()
    split_method = serializers.CharField() 
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'date', 'split_method', 'users','splits']
    
    def get_users(self, obj):
        # Return a list of user IDs involved in the expense
        return list(obj.splits.values_list('user', flat=True))
    
class UserExpenseSerializer(serializers.ModelSerializer):
    split = serializers.SerializerMethodField()  # Display the user's specific split
    
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'date', 'split']

    def get_split(self, obj):
        # Get the split specific to the current user
        user_id=self.context.get('user_id')
        request = self.context.get('request')
        if not user_id:
            return []
        
        # Filter the splits for the specific user
        user_splits = ExpenseSplit.objects.filter(expense=obj, user__id=user_id)
        return [{"user": split.user.id, "amount": split.amount} for split in user_splits]