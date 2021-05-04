#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cron.cron_manager import CronManagerAdaptor

if __name__ == '__main__':
    with CronManagerAdaptor() as cron_manager_adaptor:
        cron_manager_adaptor.start_all()
