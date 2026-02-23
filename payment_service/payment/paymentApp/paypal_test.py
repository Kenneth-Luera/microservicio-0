from payment.paymentApp.paypal_service import create_paypal_order

order = create_paypal_order("10.00")

print("Order ID:", order["id"])

for link in order["links"]:
    if link["rel"] == "approve":
        print("Approval URL:", link["href"])