from django.contrib import admin
from .models import Property, Inquiry, Favorite, FindMeRoom, ShiftHome , Review, Category, Report

# Register your models here.

# admin.site.register(Property)
# admin.site.register(Category)
admin.site.register(Inquiry)
admin.site.register(Favorite)
admin.site.register(FindMeRoom)
admin.site.register(ShiftHome)
admin.site.register(Review)
admin.site.register(Report)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_category_display']

    def get_category_display(self, obj):
        return obj.get_name_display()
    get_category_display.short_description = 'Category Name'

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price', 'get_category', 'is_hot_deal', 'is_approved', 'is_flagged', 'flagged_by']
    list_filter = ['is_flagged', 'category']
    actions = ['remove_flagged_properties', 'clear_flags']

    def get_category(self, obj):
        return obj.category.get_name_display() if obj.category else "-"
    get_category.short_description = 'Category'

    def remove_flagged_properties(self, request, queryset):
        flagged = queryset.filter(is_flagged=True)
        count = flagged.count()
        flagged.delete()
        self.message_user(request, f"{count} flagged properties have been removed.")

    remove_flagged_properties.short_description = "Remove flagged fraudulent properties"

    def clear_flags(self, request, queryset):
        flagged = queryset.filter(is_flagged=True)
        count = flagged.update(is_flagged=False, flagged_reason=None, flagged_by=None)
        self.message_user(request, f"Flags cleared on {count} properties.")

    clear_flags.short_description = "Clear flags on selected properties"

class ShiftHomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_location', 'to_location', 'schedule_date', 'schedule_time', 'status', 'created_at')
    list_filter = ('status', 'schedule_date')
    search_fields = ('user__username', 'from_location', 'to_location')

    # Optional: Inline dropdown to change status directly from the list view
    list_editable = ('status',)

    # Optional: Bulk actions
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} request(s) approved.")

    def reject_requests(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} request(s) rejected.")

    approve_requests.short_description = "Mark selected requests as Approved"
    reject_requests.short_description = "Mark selected requests as Rejected"