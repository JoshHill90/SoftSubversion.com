import stripe
customer = stripe.Customer.retrieve(
  "cu_1NosoCIf9ppS3CEaZcks0O8d",
  api_key="sk_test_51NjvRqIf9ppS3CEaGkDB5bbYcJVUSPwbvGAYvE4Y2ldsz4CMPcbd6cq2Fhmbw7cnTeIB3BpKTXeqWepXjO48Cyo900wtfsvpDl"
)
print(customer)
