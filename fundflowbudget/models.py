from django.db import models

class Transaction(models.Model):
    title = models.CharField(max_length=225)
    amount = models.PositiveIntegerField()
    options=(
        ("expense","expense"),
        ("income","income"),
    )
    type = models.CharField(max_length=225,choices=options, default="expense")
    cat_options =(
        ("fuel","fuel"),
        ("food","food"),
        ("entertainment","entertainment"),
        ("emi","emi"),
        ("bills","bills"),
        ("miscellaneous","miscellaneous")
    )
    category = models.CharField(max_length=225)
    created_date = models.DateTimeField(auto_now_add=True,blank=True)
    user = models.CharField(max_length=225)
    
    def __str__(self):
        return self.title
    
