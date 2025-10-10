from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1, "HOD"), (2, "Staff"))
    user_type=models.CharField(default=1, choices=user_type_data, max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Customer(models.Model):
    """Customer database"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Customer stats
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sales = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Bidhaas(models.Model):
    id=models.AutoField(primary_key=True)
    jina=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    profile_pic=models.FileField()
    quantity=models.IntegerField(default=0)
    alert_quantity=models.IntegerField(default=0)
    code=models.CharField(max_length=255)
    brand=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    #updated_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Sale(models.Model):
    """Main sales record"""
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile', 'Mobile Transfer'),
        ('bank', 'Bank Transfer'),
        ('credit', 'Credit'),
    ]
    
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.AutoField(primary_key=True)
    sale_number = models.CharField(max_length=50, unique=True)  # e.g., SALE-2025-0001
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    
    # Sale details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True, null=True)
    
    # Staff who made the sale
    sold_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Timestamps
    sale_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering = ['-sale_date']
        
    def __str__(self):
        return f"{self.sale_number} - {self.total_amount} TZS"
    
    def save(self, *args, **kwargs):
        # Auto-generate sale number if not exists
        if not self.sale_number:
            from datetime import datetime
            year = datetime.now().year
            count = Sale.objects.filter(sale_date__year=year).count() + 1
            self.sale_number = f"SALE-{year}-{count:04d}"
        
        # Calculate total
        self.total_amount = self.subtotal - self.discount + self.tax
        
        super().save(*args, **kwargs)

class SaleItem(models.Model):
    """Individual items in a sale"""
    id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    bidhaa = models.ForeignKey('Bidhaas', on_delete=models.PROTECT)
    
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.bidhaa.jina} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        # Calculate subtotal
        self.subtotal = (self.unit_price * self.quantity) - self.discount
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['id']

class SaleReturn(models.Model):
    """Model for sale returns - Add this to models.py"""
    RETURN_REASONS = [
        ('defective', 'Defective Product'),
        ('wrong_item', 'Wrong Item'),
        ('changed_mind', 'Changed Mind'),
        ('expired', 'Expired Product'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    id = models.AutoField(primary_key=True)
    return_number = models.CharField(max_length=50, unique=True)
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='returns')
    
    return_date = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=20, choices=RETURN_REASONS)
    notes = models.TextField(blank=True, null=True)
    
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    def save(self, *args, **kwargs):
        if not self.return_number:
            from datetime import datetime
            year = datetime.now().year
            count = SaleReturn.objects.filter(return_date__year=year).count() + 1
            self.return_number = f"RET-{year}-{count:04d}"
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-return_date']


class ReturnItem(models.Model):
    """Items being returned - Add this to models.py"""
    id = models.AutoField(primary_key=True)
    sale_return = models.ForeignKey(SaleReturn, on_delete=models.CASCADE, related_name='items')
    sale_item = models.ForeignKey(SaleItem, on_delete=models.PROTECT)
    
    quantity_returned = models.PositiveIntegerField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()



class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    
@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,address="")
        

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()

