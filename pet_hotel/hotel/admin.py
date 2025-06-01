import uuid

from django.contrib import admin
from django.utils.html import format_html

from .models import Customer
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "agreement_signed", "show_link")
    actions = ['reset_token']

    def show_link(self, obj):
        if obj.token:
            return format_html(
                '<a href="/hotel/agreement/{}/" target="_blank">링크 열기</a>', obj.token
            )
        return "❌ 없음"
    show_link.short_description = "동의서 링크"

    def reset_token(self, request, queryset):
        for customer in queryset:
            customer.token = uuid.uuid4()
            customer.agreement_signed = False
            customer.save()
        self.message_user(request, f"{queryset.count()}명의 고객에게 새 링크를 발급했습니다.")

