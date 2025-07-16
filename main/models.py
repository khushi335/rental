from django.db import models
from django.conf import settings

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('room', 'Room'),
        ('flat', 'Flat'),
        ('apartment', 'Apartment'),
        ('commercial', 'Commercial'),
    ]
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()  # Shows the readable name like "Room"

class Property(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    available_date = models.DateField()
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hot_deal = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')
    is_flagged = models.BooleanField(default=False)
    flagged_reason = models.TextField(blank=True, null=True)
    flagged_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='flagged_properties')

    def __str__(self):
        return self.title

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.PositiveBigIntegerField()
    message=models.TextField()

    def __str__(self):
        return self.name
  
class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.name} on {self.property.title}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')

    def __str__(self):
        return f"{self.user.username} favorited {self.property.title}"

class FindMeRoom(models.Model):
    ROOM_CHOICES = [
        ('single', 'Single Room'),
        ('shared', 'Shared Room'),
        ('flat', 'Flat/Apartment'),
        ('hostel', 'Hostel'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    preferred_location = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_CHOICES)
    price_min = models.PositiveIntegerField()
    price_max = models.PositiveIntegerField()
    message = models.TextField(blank=True, null=True)
    deposit_slip = models.ImageField(upload_to='find_me_room/deposit_slips/')

    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.preferred_location} ({self.room_type})"


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('property', 'user')  # Each user can review a property only once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rated {self.property.title} {self.rating}/5"
    
class ShiftHome(models.Model):
    CATEGORY_CHOICES = [
        ('Room', 'Room'),('Flat', 'Flat'), ('Apartment', 'Apartment'), ('Commercial', 'Commercial')]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    property_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    # Quantities
    beds = models.PositiveIntegerField(default=0)
    cupboards = models.PositiveIntegerField(default=0)
    tvs = models.PositiveIntegerField(default=0)
    dining_tables = models.PositiveIntegerField(default=0)
    tea_tables = models.PositiveIntegerField(default=0)
    kitchen_racks = models.PositiveIntegerField(default=0)
    sofas = models.PositiveIntegerField(default=0)
    chairs = models.PositiveIntegerField(default=0)
    shoe_racks = models.PositiveIntegerField(default=0)
    dressing_tables = models.PositiveIntegerField(default=0)
    table_lamps = models.PositiveIntegerField(default=0)
    gas_cylinders = models.PositiveIntegerField(default=0)
    mattresses = models.PositiveIntegerField(default=0)
    refrigerator = models.PositiveIntegerField(default=0)
    heaters = models.PositiveIntegerField(default=0)
    table_fans = models.PositiveIntegerField(default=0)
    flower_pots = models.PositiveIntegerField(default=0)
    computer_tables = models.PositiveIntegerField(default=0)
    cookware = models.PositiveIntegerField(default=0)
    from_floor = models.PositiveIntegerField(default=0)
    to_floor = models.PositiveIntegerField(default=0)
    WHEN_CHOICES = [('Instant', 'Instant Booking'), ('Later', 'Schedule for Later')]
    when = models.CharField(max_length=10, choices=WHEN_CHOICES)
    schedule_date = models.DateField(blank=True, null=True)
    schedule_time = models.TimeField(blank=True, null=True)
    deposit_slip = models.ImageField(upload_to='deposits/', blank=False, null=False)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ShiftRequest by {self.user.username} from {self.from_location} to {self.to_location}"
    
class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reports')
    reason = models.CharField(max_length=255)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user.username} on {self.property.title}"