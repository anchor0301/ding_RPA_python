# hotel/views.py
import uuid

from django.views.decorators.csrf import csrf_exempt

import json
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.urls import reverse

from django.template.loader import render_to_string
from .models import Reservation, Dog, Customer
from django.http import HttpResponse

from django.utils.html import format_html
from django.contrib import admin
from django.utils.timezone import make_aware
from datetime import datetime





