from rest_framework.decorators import api_view
from rest_framework.response import Response
from paymentApp.models import Payment
from paymentApp.paypal_service import capture_paypal_order


@api_view(["POST"])
def capture_payment(request, paypal_order_id):

    try:
        payment = Payment.objects.get(paypal_order_id=paypal_order_id)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    response = capture_paypal_order(paypal_order_id)

    payment.status = "COMPLETED"
    payment.save()

    return Response({
        "message": "Payment captured",
        "paypal_response": response.body
    })
