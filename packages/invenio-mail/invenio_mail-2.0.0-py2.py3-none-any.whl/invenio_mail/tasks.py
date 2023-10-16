# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Background tasks for mail module."""

from __future__ import absolute_import, print_function

from celery import shared_task
from flask import current_app
from flask_mail import Message


@shared_task
def send_email(data):
    """Celery task for sending emails.

    .. warning::

       Attachments do not work with Celery tasks since
       :class:`flask_mail.Attachment` is not serializable in ``JSON``
       nor ``msgpack``. Note that a
       `custom serializer <http://docs.celeryproject.org/en/latest/
       userguide/calling.html#serializers>`__
       can be created if attachments are really needed.
    """
    msg = Message()
    msg.__dict__.update(data)
    current_app.extensions["mail"].send(msg)
