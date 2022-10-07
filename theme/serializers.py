from rest_framework import serializers
from .models import MembershipCategory, Member,Payment,Fee,Bill


class MembershipCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipCategory
        fields = '__all__'
class feeSerializerObject(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'
class MemberSerializer(serializers.ModelSerializer):
    member_membership_id = MembershipCategorySerializer(read_only=True)
    active_fee_id=feeSerializerObject(read_only=True)
    class Meta:
        model = Member
        fields = '__all__'

class feeSerializer(serializers.ModelSerializer):
    member_id = MemberSerializer(many=False, read_only=True)
    class Meta:
        model = Fee
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    fee_id=feeSerializer(many=False, read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    bill_member_id=MemberSerializer(many=False, read_only=True)
    fee_id=feeSerializer(many=False, read_only=True)
    subscription_id=MembershipCategorySerializer(many=False, read_only=True)
    class Meta:
        model = Bill
        fields = '__all__'