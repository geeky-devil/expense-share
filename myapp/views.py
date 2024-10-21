from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from myapp.serializers import ExpenseSerializer, UserExpenseSerializer
from .models import User, Expense, ExpenseSplit
import csv , json
from datetime import date

# Create a user
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        user = User.objects.create(name=name, email=email, mobile=mobile)
        return JsonResponse({"message": "User created successfully", "user_id": user.id})
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Retrieve user details
def get_user_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return JsonResponse({
        'name': user.name,
        'email': user.email,
        'mobile': user.mobile
    })

# Add an expense
def add_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        amount = data.get('amount')
        split_method = data.get('split_method')
        users = data.get('users')
        date_of_expense = data.get('date') or date.today()

        if not users:
            return JsonResponse({"error": "At least one user must be provided."}, status=400)

        # Validate users
        valid_users = User.objects.filter(id__in=users)
        if len(valid_users) != len(users):
            return JsonResponse({"error": "Some users are invalid."}, status=400)
        try:

            with transaction.atomic():
                expense = Expense.objects.create(
                    date=date_of_expense,
                    amount=amount,
                    split_method=split_method,
                )

                # Equal split
                if split_method == 'equal':
                    share_per_user = amount / len(users)
                    for user_id in users:
                        ExpenseSplit.objects.create(
                            user_id=user_id,
                            expense=expense,
                            amount=share_per_user
                        )

                # Exact split
                elif split_method == 'exact':
                    split_amounts = data.get('split_amounts')
                    if not split_amounts or len(split_amounts) != len(users):
                        raise ValueError('Split amounts must be provide for each user')
                    if sum(split_amounts)!=amount:
                        raise ValueError('Splits do not add up to the amount')
                    for user_id, split_amount in zip(users, split_amounts):
                        ExpenseSplit.objects.create(
                            user_id=user_id,
                            expense=expense,
                            amount=split_amount
                        )

                # Percentage split
                elif split_method == 'percentage':
                    split_percentages = data.get('split_percentages')
                    if not split_percentages or sum(split_percentages) != 100:
                        raise ValueError({"error": "Percentages must add up to 100."}, status=400)
                    for user_id, percentage in zip(users, split_percentages):
                        ExpenseSplit.objects.create(
                            user_id=user_id,
                            expense=expense,
                            amount=(amount * percentage / 100)
                        )
                
                return JsonResponse({"message": "Expense added successfully."})
        except Exception as e:
            return JsonResponse({'error':str(e)},status=400)

    return JsonResponse({"error": "Invalid request method."}, status=400)

# Endpoint for user's expenses for a given date
def user_expenses(request, user_id):
    try:
        expenses = Expense.objects.filter(splits__user=user_id)
        serializer = UserExpenseSerializer(expenses, many=True, context={'user_id': user_id})
        return JsonResponse(serializer.data,status=200,safe=False)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

# Endpoint for overall expenses
def overall_expenses(request):
    expenses = Expense.objects.all()
    serialized_data = ExpenseSerializer(expenses, many=True).data
    return JsonResponse({
        "total_expenses": serialized_data,
    })

# Download balance sheet
def download_balance_sheet(request):
    date_filter = request.GET.get('date')

    if date_filter:
        expenses = Expense.objects.filter(date=date_filter)
    else:
        expenses = Expense.objects.all()

    # Generate CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'User', 'Amount'])

    for expense in expenses:
        splits = ExpenseSplit.objects.filter(expense=expense)
        for split in splits:
            writer.writerow([expense.date, split.user.name, split.amount])

    return response
