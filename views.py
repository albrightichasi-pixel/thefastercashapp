import json
from urllib import request, response
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from investments.models import Investment
from .models import Payment
from .mpesa import stk_push


@login_required
def initiate_payment(request, investment_id):

    investment = get_object_or_404(Investment, id=investment_id, user=request.user)

    phone_number = request.user.phone_number
    amount = investment.amount

    response = stk_push(phone_number, amount)

    payment = Payment.objects.create(
        user=request.user,
        investment=investment,
        phone_number=phone_number,
        amount=amount,
        merchant_request_id=response.get("MerchantRequestID"),
        checkout_request_id=response.get("CheckoutRequestID"),
        status="PENDING"
    )



from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def mpesa_callback(request):

    if request.method == "POST":
        data = json.loads(request.body)

        callback = data.get("Body", {}).get("stkCallback", {})

        checkout_request_id = callback.get("CheckoutRequestID")
        result_code = str(callback.get("ResultCode"))
        result_desc = callback.get("ResultDesc")

        try:
            payment = Payment.objects.get(checkout_request_id=checkout_request_id)

            payment.result_code = result_code
            payment.result_desc = result_desc

            if result_code == "0":
                payment.status = "SUCCESS"
            else:
                payment.status = "FAILED"

            payment.save()

        except Payment.DoesNotExist:
            pass

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

    return JsonResponse({"error": "Invalid request"}, status=400)
