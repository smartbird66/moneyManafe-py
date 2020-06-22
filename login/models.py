from django.db import models


class superman(models.Model):
    familyAccount = models.AutoField(primary_key=True)
    password = models.CharField(max_length=15)
    address = models.CharField(max_length=20, null=True)
    number = models.IntegerField(default=1, null=True)

    class Meta:
        db_table = 'superman'
        verbose_name = '家庭管理员'
        verbose_name_plural = verbose_name


class member(models.Model):
    name = models.CharField(max_length=10)
    # familyAccount = models.IntegerField()
    familyAccount = models.ForeignKey(
        #blank=True,
        #null=True,
        to='superman',
        to_field='familyAccount',
        on_delete=models.DO_NOTHING,
        #related_name='familyAccount'
    )
    innerId = models.SmallIntegerField()
    nickName = models.CharField(max_length=15)
    birthday = models.DateField()
    authority = models.SmallIntegerField(default=1)
    password = models.CharField(max_length=15)
    account = models.IntegerField(primary_key=True)
    addedTime = models.DateTimeField()
    myAccount = models.IntegerField(default=0)

    class Meta:
        db_table = 'member'
        verbose_name = '家庭成员'
        verbose_name_plural = verbose_name


class message(models.Model):
    # familyAccount = models.IntegerField()
    familyAccount = models.ForeignKey(
        to='superman',
        to_field='familyAccount',
        on_delete=models.DO_NOTHING,
    )
    #account = models.IntegerField()
    account = models.ForeignKey(
        to = 'member',
        to_field='account',
        on_delete=models.DO_NOTHING,
    )
    sendTime = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=50, default='无')

    class Meta:
        db_table = 'message'
        verbose_name = '消息'
        verbose_name_plural = verbose_name


class bill(models.Model):
    addTime = models.DateTimeField()
    money = models.IntegerField()
    #familyAccount = models.IntegerField()
    familyAccount = models.ForeignKey(
        to='superman',
        to_field='familyAccount',
        on_delete=models.DO_NOTHING,
    )
    #innerId = models.SmallIntegerField()
    account = models.ForeignKey(
        to='member',
        to_field='account',
        on_delete=models.DO_NOTHING,
        default=1,
    )
    note = models.CharField(max_length=50)
    consumptionType = models.CharField(max_length=10)

    class Meta:
        db_table = 'bill'
        verbose_name = '账单'
        verbose_name_plural = verbose_name


class borrowAndOut(models.Model):
    addTime = models.DateTimeField()
    person = models.CharField(max_length=10)
    #familyAccount = models.IntegerField()
    familyAccount = models.ForeignKey(
        to='superman',
        to_field='familyAccount',
        on_delete=models.DO_NOTHING,
    )
    #innerId = models.SmallIntegerField()
    account = models.ForeignKey(
        to='member',
        to_field='account',
        on_delete=models.DO_NOTHING,
        default=1,
    )
    money = models.IntegerField()
    deathDate = models.DateField()

    class Meta:
        db_table = 'borrowAndOut'
        verbose_name = '借入借出'
        verbose_name_plural = verbose_name


class note(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    #account = models.IntegerField()
    account = models.ForeignKey(
        to='member',
        to_field='account',
        on_delete=models.DO_NOTHING,
        default=1,
    )
    note = models.CharField(max_length=200)

    class Meta:
        db_table = 'note'
        verbose_name = '便签'
        verbose_name_plural = verbose_name


class monthyBill(models.Model):
    billIn = models.IntegerField()
    billOut = models.IntegerField()
    addTime = models.DateTimeField(auto_now_add=True)
    #familyAccount = models.IntegerField()
    familyAccount = models.ForeignKey(
        to='superman',
        to_field='familyAccount',
        on_delete=models.DO_NOTHING,
    )
    #innerId = models.SmallIntegerField()
    account = models.ForeignKey(
        to='member',
        to_field='account',
        on_delete=models.DO_NOTHING,
        default=1,
    )

    class Meta:
        db_table = 'monthyBill'
        verbose_name = '月账单'
        verbose_name_plural = verbose_name


class investment(models.Model):
    addTime = models.DateTimeField()
    InvestmentType = models.CharField(max_length=6)
    principal = models.IntegerField()
    updateTime = models.DateTimeField(auto_now=True)
    earnings = models.IntegerField()
    rate = models.SmallIntegerField()
    #familyAccount = models.IntegerField()
    familyAccount = models.ForeignKey(
        to='superman',
        to_field='familyAccount',
        on_delete=models.DO_NOTHING,
    )
    #innerId = models.SmallIntegerField()
    account = models.ForeignKey(
        to='member',
        to_field='account',
        on_delete=models.DO_NOTHING,
        default=1,
    )

    class Meta:
        db_table = 'investment'
        verbose_name = '投资理财'
        verbose_name_plural = verbose_name

# Create your models here.
