# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from schedule.models.events import Event
from django import forms
import datetime



class Boat(models.Model):
    boat_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False)
    description = models.TextField()
    map_image = models.ImageField(upload_to = 'images/', default = 'images/no-img.jpg')

    
    def __unicode__(self):
        return self.name
    
class Booking(models.Model):
    creator = models.ForeignKey(User, related_name='bookings')
    submitted = models.DateTimeField(default=timezone.now)
    boat = models.ForeignKey(Boat, null=False)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    
    event = models.OneToOneField(Event, related_name='event', default=None)
    readonly_fields =('submitted',)
    

    
    def __unicode__(self):
       return '%s %s' % (self.creator.username, self.boat_id)